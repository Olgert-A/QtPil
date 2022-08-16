from PIL import Image


class Model:
    folder = ''            # contain path to image files without name. Same to all files
    images = {}            # key = name of image with extension, value = pil image object

    def add(self, path):
        if path:
            name, self.folder = self._divide_path(path)
            image = Image.open(path)
            if image:
                self.images[name] = image

    def clear(self):
        for _, img in self.images.items():
            img.close()

        self.images.clear()
        self.folder = ''

    def get_image(self, name):
        return self.images.get(name)

    def get_image_list(self):
        return self.images.keys()

    @staticmethod
    def _divide_path(path):
        name = path.split('\\')[-1]
        folder = path.replace(name, '')
        return name, folder
