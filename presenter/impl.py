from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap

from model.contract import ModelContract
from presenter.contract import MainPresenterContract
from view.contract import MainViewContract


class MainPresenterImpl(MainPresenterContract):
    model: ModelContract
    view: MainViewContract

    def __init__(self, model: ModelContract):
        self.model = model

    def attach_view(self, view: MainViewContract):
        self.view = view

    def load_overlay_image(self, path):
        if path:
            self.model.load_overlay_image(path)
            self.view.show_overlay_image_path(path)

    def load_image_list(self, paths):
        if paths:
            self.model.clear_image_list()
            self.model.load_image_list(paths)
            #self.view.show_image()
            self.view.show_image_list(self.model.get_image_list())

    def set_current_image(self, name):
        self.model.set_current_image(name)
        if blended := self.model.get_current_blended():
            self.view.show_image(self._to_pixmap(blended))

    def set_current_coord(self, x, y):
        self.model.set_current_coord(x, y)
        if blended := self.model.get_current_blended():
            self.view.show_image(self._to_pixmap(blended))

    def save_all(self, path=''):
        pass

    @staticmethod
    def _to_pixmap(image: Image) -> QPixmap:
        img1 = ImageQt(image)
        img2 = img1.copy()
        return QPixmap.fromImage(img2)
