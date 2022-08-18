from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QFileDialog, QListWidget, QLineEdit, QSlider
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from view.contract import MainViewContract
from presenter.contract import MainPresenterContract


class MainViewMeta(type(QMainWindow), type(MainViewContract)):
    # solve metaclass conflict with PyQt
    pass


class ImageSize:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class MainViewImpl(QMainWindow, MainViewContract, metaclass=MainViewMeta):
    def __init__(self, presenter: MainPresenterContract):
        super().__init__()
        self.widgets = {}
        self.image_size = ImageSize(0, 0)
        self.presenter = presenter
        self.presenter.attach_view(self)
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
        w = self.widgets['overlay_resize'] = QSlider(Qt.Orientation.Horizontal)
        self.widgets['open_images'] = QPushButton('Open images...')
        self.widgets['image_list'] = QListWidget()

    def set_signals(self):
        self.widgets['overlay_image'].setReadOnly(True)
        self.widgets['open_overlay_image'].pressed.connect(self.load_overlay_clicked)
        self.widgets['overlay_resize'].valueChanged.connect(self.overlay_resize_change)
        self.widgets['open_images'].pressed.connect(self.load_images_clicked)
        self.widgets['image_list'].itemSelectionChanged.connect(self.image_selection_changed)

    def set_sizes(self):
        controls_width = 200
        self.setMinimumSize(600, 400)
        self.widgets['image'].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.widgets['overlay_image'].setFixedWidth(controls_width)
        self.widgets['open_overlay_image'].setFixedWidth(controls_width)
        self.widgets['overlay_resize'].setFixedWidth(controls_width)
        self.widgets['overlay_resize'].setMaximum(100)
        self.widgets['overlay_resize'].setMinimum(1)
        self.widgets['overlay_resize'].setValue(100)
        self.widgets['open_images'].setFixedWidth(controls_width)
        self.widgets['image_list'].setFixedWidth(controls_width)

    def place_widgets(self):
        editor = QVBoxLayout()
        editor.addWidget(self.widgets['image'])

        controls = QVBoxLayout()
        controls.addWidget(self.widgets['overlay_image'])
        controls.addWidget(self.widgets['open_overlay_image'])
        controls.addWidget(self.widgets['overlay_resize'])
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
        w: QLabel = self.widgets['image']
        widget_click_pos = global_click_pos - w.pos()
        width_delta = (w.size().width() - self.image_size.width) / 2
        height_delta = (w.size().height() - self.image_size.height) / 2
        x = int(widget_click_pos.x() - width_delta)
        y = int(widget_click_pos.y() - height_delta)

        if 0 <= x <= self.image_size.width and 0 <= y <= self.image_size.height:
            self.presenter.set_current_coord(x, y)

    # ============ SIGNALS ========================
    def load_overlay_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open overlay image", "", "Image Files (*.png *.jpg *.bmp)")
        self.presenter.load_overlay_image(path)

    def overlay_resize_change(self, value):
        self.presenter.resize_overlay_image(value)

    def load_images_clicked(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open image", "", "Image Files (*.png *.jpg *.bmp)")
        self.presenter.load_image_list(paths)

    def image_selection_changed(self):
        if items := self.widgets['image_list'].selectedItems():
            self.presenter.set_current_image(items[0].text())
        else:
            self.show_image()

    # ============ VIEW CONTRACT ========================
    def show_image(self, pixmap: QPixmap = None):
        img: QLabel = self.widgets['image']
        if pixmap:
            self.image_size = ImageSize(pixmap.width(), pixmap.height())
            img.setPixmap(pixmap)
        else:
            self.image_size = ImageSize(0, 0)
            img.clear()

    def show_overlay_image_path(self, path):
        self.widgets['overlay_image'].setText(path)

    def show_image_list(self, image_list):
        img_list = self.widgets['image_list']
        img_list.clear()
        img_list.addItems(image_list)
        if img_list.count() > 0:
            img_list.setCurrentRow(0)
