import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLineEdit, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer

class camera_GUI(QWidget):

    def __init__(self):
        '''
        Parameters:
            N/A
        '''
        QWidget.__init__(self)

        self.linking_layout = QVBoxLayout(self)
        self.setLayout(self.linking_layout)
        self._hsv_picker()

    def nothing(x):
        pass

    def _hsv_picker(self):

        self.object_label = QLabel("Object")
        self.object_label.setAlignment(Qt.AlignCenter)
        self.orientation_layout = QGridLayout()

        self.filter_banana_button = QPushButton("Banana")
        self.filter_banana_button.setStyleSheet("background-color:#999900; color:#E8FFE8")
        self.filter_banana_button.clicked.connect(lambda: self.capture("banana")) #connect here

        self.filter_strawberry_button = QPushButton("Strawberry")
        self.filter_strawberry_button.setStyleSheet("background-color:#2A7E43; color:#E8FFE8")
        self.filter_strawberry_button.clicked.connect(lambda: self.capture("strawberry"))

        #Add text boxs and line edit displays to layout
        self.linking_layout.addWidget(self.object_label, 0)

        self.orientation_layout.addWidget(self.filter_strawberry_button, 2, 0)
        self.orientation_layout.addWidget(self.filter_banana_button, 2, 1)
        self.linking_layout.addLayout(self.orientation_layout, 1)
        

    def capture(self, item):
        self.cam = cv2.VideoCapture(0)

        l_b = np.array([0,0,0])
        u_b = np.array([255,255,255])
        self.object_label.setText("Filtering for " + item)
        if item == "banana":
            l_b = np.array([20, 80, 100])
            u_b = np.array([30, 255, 255])
            l_b2 = np.array([20, 80, 100])
            u_b2 = np.array([30, 255, 255])
        elif item == "strawberry":
            l_b = np.array([0, 80, 100])
            u_b = np.array([10, 255, 255])
            l_b2 = np.array([160,100,100])
            u_b2 = np.array([179,255,255])

        while True:
            _, frame = self.cam.read()
            blurred_frame = cv2.GaussianBlur(frame, (9,9), 2)
            hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

            mask1 = cv2.inRange(hsv, l_b, u_b)
            mask2 = cv2.inRange(hsv,l_b2,u_b2)
            
            mask = mask1 | mask2
            res = cv2.bitwise_and(frame, frame, mask=mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            for contour in contours:
                cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
            #print(self.cam.get(cv2.CAP_PROP_FPS))
            cv2.imshow("frame", frame)
            #cv2.imshow("mask", mask)
            #cv2.imshow("res", res)

            key = cv2.waitKey(1)
            if key == 27:
                break

        self.cam.release()
        cv2.destroyAllWindows()
    

if __name__ == "__main__":
    import sys
    app = QApplication([])
    set_pos_gui = camera_GUI()
    set_pos_gui.show()
    sys.exit(app.exec_())