from abc import ABC, abstractmethod


class ModelContract(ABC):
    @abstractmethod
    def load_overlay_image(self, path):
        """load blend image to model"""
        pass

    @abstractmethod
    def resize_overlay_image(self, percent):
        """set resize percent to overlay image"""
        pass

    @abstractmethod
    def close_overlay_image(self):
        """close overlay image"""
        pass

    @abstractmethod
    def load_image_list(self, paths):
        """load editing images to model"""
        pass

    @abstractmethod
    def get_image_list(self, only_names=True):
        """get list of opened images names if only_names = True else get list of full image paths"""
        pass

    @abstractmethod
    def clear_image_list(self):
        """close all opened images and clear list"""
        pass

    @abstractmethod
    def set_current_image(self, name):
        """set current editing image to model"""
        pass

    @abstractmethod
    def set_current_coord(self, x, y):
        """set new overlay coordinates to current image"""
        pass

    @abstractmethod
    def get_current_blended(self):
        """get current blended image"""
        pass

    @abstractmethod
    def save_all(self, path=''):
        """save current image states to file with same names and (optional) new path"""
        pass
