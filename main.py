import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt, QImage


class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        label = QLabel()
        image = Image.open('.\\3.bmp')
        img1 = ImageQt(image)
        img2 = img1.copy()
        pix = QPixmap.fromImage(img2)
        label.setPixmap(pix)
        self.setCentralWidget(label)


app = QApplication(sys.argv)
view = MainWnd()
view.show()
sys.exit(app.exec())
