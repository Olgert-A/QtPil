from abc import ABC, abstractmethod
from view.contract import MainViewContract


class MainPresenterContract(ABC):
    @abstractmethod
    def attach_view(self, view: MainViewContract):
        """attach view impl to presenter to use callbacks"""
        pass

    @abstractmethod
    def load_overlay_image(self, path):
        """load blend image using path"""
        pass

    @abstractmethod
    def load_image_list(self, paths):
        """load images to edit using paths"""
        pass

    @abstractmethod
    def set_current_image(self, name):
        """change current editing image to name"""
        pass

    @abstractmethod
    def set_current_coord(self, x, y):
        """change current image coordinates that used to blend image"""
        pass

    @abstractmethod
    def save_all(self, path=''):
        """apply blend to all images and save to new path if set"""
        pass
