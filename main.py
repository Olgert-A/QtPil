import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt

from model import Model


class MainWnd(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.widgets = {}
        self.model: Model = model
        self.init_window()

    def image_open_clicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "Image Files (*.png *.jpg *.bmp)")

        self.model.clear()
        for path in paths:
            self.model.add(path)

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

model = Model()
view = MainWnd(model)
view.show()
sys.exit(app.exec())
