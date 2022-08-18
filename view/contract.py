from abc import ABC, abstractmethod
from PyQt6.QtGui import QPixmap


class MainViewContract(ABC):
    @abstractmethod
    def show_image(self, pixmap: QPixmap = None):
        """show pixmap image if pixmap else clear view"""
        pass

    @abstractmethod
    def show_overlay_image_path(self, path):
        """show path of loaded overlay image"""
        pass

    @abstractmethod
    def show_image_list(self, image_list):
        """show loaded images to edit"""
        pass
