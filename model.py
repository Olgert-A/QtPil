from PIL import Image


class Model:
    folder = ''            # contain path to image files without name. Same to all files
    data = {}              # key = name of image with extension, value = pil image object

    def add(self, path):
        if path:
            name, self.folder = self._divide_path(path)
            image = Image.open(path)
            if image:
                self.data[name] = image

    def clear(self):
        for _, img in self.data.items():
            img.close()

        self.data.clear()
        self.folder = ''

    @staticmethod
    def _divide_path(path):
        name = path.split('\\')[-1]
        folder = path.replace(name, '')
        return name, folder
