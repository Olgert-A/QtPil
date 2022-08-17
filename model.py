from PIL import Image, ImageDraw


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


class Model:
    def __init__(self):
        self.folder = ''            # contain path to image files without name. Same to all files
        self.images = {}            # key = name of image with extension, value = pil image object

        self.current_image_name = ''

        self.overlay_image = None

    def add_image(self, path):
        if path:
            name, self.folder = self._divide_path(path)
            image = Image.open(path)
            if image:
                self.images[name] = ImageItem(image, None)

    def load_overlay_image(self, path):
        if path:
            image = Image.open(path)
            if image:
                self.overlay_image = image

    def clear(self):
        for _, item in self.images.items():
            item.image.close()

        self.images.clear()
        self.folder = ''

    def get_image_list(self):
        return self.images.keys()

    def set_current_image(self, name):
        if name and name in self.images.keys():
            self.current_image_name = name

    def set_current_coord(self, x, y):
        if self.current_image_name:
            print('set coord')
            self.images[self.current_image_name].coord = Coord(x, y)

    def get_current_blend(self):
        if self.current_image_name:
            image_item = self.images[self.current_image_name]
            blender = image_item.image.copy()
            if (coord := image_item.coord) and (oi := self.overlay_image):
                x = int(coord.x - oi.width / 2)
                y = int(coord.y - oi.height / 2)
                blender.paste(self.overlay_image, (x, y))

            return blender

    @staticmethod
    def _divide_path(path):
        name = path.split('\\')[-1]
        folder = path.replace(name, '')
        return name, folder
