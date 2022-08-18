import sys

from PyQt6.QtWidgets import QApplication

from model.impl import ModelImpl
from presenter.impl import MainPresenterImpl
from view.impl import MainViewImpl

app = QApplication(sys.argv)

model = ModelImpl()
presenter = MainPresenterImpl(model)
view = MainViewImpl(presenter)
view.show()
sys.exit(app.exec())
