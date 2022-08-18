from os.path import normpath
from PIL import Image
from model.contract import ModelContract


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"X: {self.x} Y: {self.y}"


class ImageItem:
    def __init__(self, image: Image, coord):
        self.image = image
        self.coord = coord


class OverlayImage:
    def __init__(self, image: Image):
        self.image = image
        self.transparency = 100


class ModelImpl(ModelContract):
    def __init__(self):
        self.folder = ''            # contain path to image files without name. Same to all files
        self.images = {}            # key = name of image with extension, value = pil image object
        self.current_image_name = ''
        self.overlay = None

    def load_overlay_image(self, path):
        if path:
            image = Image.open(path)
            if image:
                self.overlay = OverlayImage(image)

    def close_overlay_image(self):
        if self.overlay and (image := self.overlay.image):
            image.close()

    def load_image_list(self, paths):
        for path in paths:
            path = normpath(path)
            name, self.folder = self._divide_path(path)
            image = Image.open(path)
            if image:
                self.images[name] = ImageItem(image, None)

    def get_image_list(self, only_names=True):
        return [name if only_names else self.folder+name
                for name in self.images.keys()]

    def clear_image_list(self):
        for _, item in self.images.items():
            item.image.close()

        self.images.clear()
        self.folder = ''

    def set_current_image(self, name):
        if name and name in self.images.keys():
            self.current_image_name = name

    def set_current_coord(self, x, y):
        if self.current_image_name:
            self.images[self.current_image_name].coord = Coord(x, y)

    def get_current_blended(self):
        if self.current_image_name:
            return self._blend_image(self.current_image_name)

    def save_all(self, path=''):
        pass

    def _blend_image(self, name):
        if name in self.images.keys():
            image_item = self.images[name]
            blender = image_item.image.copy()
            if (coord := image_item.coord) and (overlay := self.overlay):
                x = int(coord.x - overlay.image.width / 2)
                y = int(coord.y - overlay.image.height / 2)
                blender.paste(overlay.image, (x, y), overlay.image.convert('RGBA'))
            return blender

    @staticmethod
    def _divide_path(path):
        name = path.split('\\')[-1]
        folder = path.replace(name, '')
        return name, folder
