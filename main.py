import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt


class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widgets = {}

        self.init_window()

    def image_open_clicked(self):
        self.set_image(self.to_pixmap(Image.open('.\\3.bmp')))

    def init_window(self):
        img = self.widgets['image'] = QLabel()
        btn = self.widgets['load'] = QPushButton('Load next')
        btn.pressed.connect(self.image_open_clicked)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(img)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def set_image(self, image: QPixmap):
        if image:
            self.widgets['image'].setPixmap(image)

    @staticmethod
    def to_pixmap(image: Image) -> QPixmap:
        img1 = ImageQt(image)
        img2 = img1.copy()
        return QPixmap.fromImage(img2)


app = QApplication(sys.argv)
view = MainWnd()
view.show()
sys.exit(app.exec())
