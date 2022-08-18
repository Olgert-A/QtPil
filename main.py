import sys

from PyQt6.QtWidgets import QApplication

from model.impl import ModelImpl
from view.impl import MainViewImpl

app = QApplication(sys.argv)

model = ModelImpl()
view = MainViewImpl(model)
view.show()
sys.exit(app.exec())
