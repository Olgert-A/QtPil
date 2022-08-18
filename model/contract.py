from abc import ABC, abstractmethod


class ModelContract(ABC):
    @abstractmethod
    def load_overlay_image(self, path):
        """load blend image to model"""
        pass

    @abstractmethod
    def close_overlay_image(self, path):
        """close overlay image"""
        pass

    @abstractmethod
    def load_image_list(self, image_paths):
        """load editing images to model"""
        pass

    @abstractmethod
    def clear_image_list(self, image_paths):
        """close all opened images and clear list"""
        pass

    @abstractmethod
    def set_current_image(self, image_name):
        """set current editing image to model"""
        pass

    @abstractmethod
    def set_current_coord(self, coord):
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
