import sys
from os.path import normpath

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QFileDialog, QListWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PIL import Image
from PIL.ImageQt import ImageQt

from model import Model


class MainWnd(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.widgets = {}
        self.model: Model = model
        self.init_window()

    def load_images_clicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "Image Files (*.png *.jpg *.bmp)")

        self.model.clear()
        (img_list := self.widgets['image_list']).clear()
        for path in paths:
            self.model.add(normpath(path))
        img_list.addItems(self.model.get_image_list())

    def image_selection_changed(self):
        img_list = self.widgets['image_list']

        if items := img_list.selectedItems():
            image_name = items[0].text()
            image = self.model.get_image(image_name)
            if image:
                self.set_image(self.to_pixmap(image))

    def init_window(self):
        img = self.widgets['image'] = QLabel()
        open_images = self.widgets['open_images'] = QPushButton('Open images...')
        img_list = self.widgets['image_list'] = QListWidget()

        open_images.pressed.connect(self.load_images_clicked)
        img_list.itemSelectionChanged.connect(self.image_selection_changed)

        self.setMinimumSize(600, 400)
        controls_width = 200
        img.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        open_images.setFixedWidth(controls_width)
        img_list.setFixedWidth(controls_width)

        editor = QVBoxLayout()
        editor.addWidget(img)

        controls = QVBoxLayout()
        controls.addWidget(open_images)
        controls.addWidget(img_list)

        main_layout = QHBoxLayout()
        main_layout.addLayout(editor)
        main_layout.addLayout(controls)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
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
