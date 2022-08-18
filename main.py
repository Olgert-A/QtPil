import sys
from os.path import normpath

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QFileDialog, QListWidget, QLineEdit
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
        image = self.model.get_current_blend()
        if image:
            self.set_pixmap(self.to_pixmap(image))

    # ============ SIGNALS ========================
    def load_overlay_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open overlay image", "", "Image Files (*.png *.jpg *.bmp)")

        if path:
            self.model.load_overlay_image(path)
            self.widgets['overlay_image'].setText(path)

    def load_images_clicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "Image Files (*.png *.jpg *.bmp)")

        self.model.clear()
        self.set_pixmap(QPixmap(None))
        img_list = self.widgets['image_list']
        img_list.clear()
        for path in paths:
            self.model.add_image(normpath(path))
        img_list.addItems(self.model.get_image_list())

    def image_selection_changed(self):
        img_list = self.widgets['image_list']

        if items := img_list.selectedItems():
            image_name = items[0].text()
            self.model.set_current_image(image_name)
            image = self.model.get_current_blend()
            if image:
                self.set_pixmap(self.to_pixmap(image))
        else:
            self.set_pixmap()

    # ============ VIEW UPDATE ========================

    def set_pixmap(self, pixmap: QPixmap = None):
        img: QLabel = self.widgets['image']
        if pixmap:
            img.setPixmap(pixmap)
            img.setFixedSize(pixmap.width(), pixmap.height())
        else:
            img.clear()

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
