import sys


from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QFileDialog, QListWidget, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PIL import Image
from PIL.ImageQt import ImageQt

from model.contract import ModelContract
from model.impl import ModelImpl


class MainWnd(QMainWindow):
    def __init__(self, model_impl: ModelContract):
        super().__init__()
        self.widgets = {}
        self.model: ModelContract = model_impl
        self.init_window()

    # ============ WINDOW CREATION METHODS ==========
    def init_window(self):
        self.create_widgets()
        self.set_signals()
        self.set_sizes()
        self.place_widgets()

    def create_widgets(self):
        self.widgets['image'] = QLabel()
        self.widgets['overlay_image'] = QLineEdit()
        self.widgets['open_overlay_image'] = QPushButton('Open overlay image...')
        self.widgets['open_images'] = QPushButton('Open images...')
        self.widgets['image_list'] = QListWidget()

    def set_signals(self):
        self.widgets['overlay_image'].setReadOnly(True)
        self.widgets['open_overlay_image'].pressed.connect(self.load_overlay_clicked)
        self.widgets['open_images'].pressed.connect(self.load_images_clicked)
        self.widgets['image_list'].itemSelectionChanged.connect(self.image_selection_changed)

    def set_sizes(self):
        controls_width = 200
        self.setMinimumSize(600, 400)
        self.widgets['image'].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.widgets['overlay_image'].setFixedWidth(controls_width)
        self.widgets['open_overlay_image'].setFixedWidth(controls_width)
        self.widgets['open_images'].setFixedWidth(controls_width)
        self.widgets['image_list'].setFixedWidth(controls_width)

    def place_widgets(self):
        editor = QVBoxLayout()
        editor.addWidget(self.widgets['image'])

        controls = QVBoxLayout()
        controls.addWidget(self.widgets['overlay_image'])
        controls.addWidget(self.widgets['open_overlay_image'])
        controls.addWidget(self.widgets['open_images'])
        controls.addWidget(self.widgets['image_list'])

        main_layout = QHBoxLayout()
        main_layout.addLayout(editor)
        main_layout.addLayout(controls)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ============ EVENTS =========================
    def mousePressEvent(self, e):
        global_click_pos = e.pos()
        image = self.widgets['image']
        image_click_pos = global_click_pos - image.pos()
        self.model.set_current_coord(image_click_pos.x(), image_click_pos.y())
        image = self.model.get_current_blended()
        if image:
            self.show_image(self.to_pixmap(image))

    # ============ SIGNALS ========================
    def load_overlay_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open overlay image", "", "Image Files (*.png *.jpg *.bmp)")

        if path:
            self.model.load_overlay_image(path)
            self.show_overlay_image_path(path)

    def load_images_clicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "Image Files (*.png *.jpg *.bmp)")

        if paths:
            self.model.clear_image_list()
            self.show_image()

            self.model.load_image_list(paths)
            image_list = self.model.get_image_list()
            self.show_image_list(image_list)

    def image_selection_changed(self):
        img_list = self.widgets['image_list']

        if items := img_list.selectedItems():
            image_name = items[0].text()
            self.model.set_current_image(image_name)
            image = self.model.get_current_blended()
            if image:
                self.show_image(self.to_pixmap(image))
        else:
            self.show_image()

    # ============ VIEW UPDATE ========================
    def show_image(self, pixmap: QPixmap = None):
        img: QLabel = self.widgets['image']
        if pixmap:
            img.setPixmap(pixmap)
            img.setFixedSize(pixmap.width(), pixmap.height())
        else:
            img.clear()

    def show_overlay_image_path(self, path):
        self.widgets['overlay_image'].setText(path)

    def show_image_list(self, image_list):
        img_list = self.widgets['image_list']
        img_list.clear()
        img_list.addItems(image_list)
        if img_list.count() > 0:
            img_list.setCurrentRow(0)

    @staticmethod
    def to_pixmap(image: Image) -> QPixmap:
        img1 = ImageQt(image)
        img2 = img1.copy()
        return QPixmap.fromImage(img2)


app = QApplication(sys.argv)

model = ModelImpl()
view = MainWnd(model)
view.show()
sys.exit(app.exec())
