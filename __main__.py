import os
import sys
import pandas as pd

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage

from mainWindow import Ui_MainWindow
from image_loading import loader


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.in_directory = '/home/akhil/Temp/'
        self.save_path = '/tmp/BMEImg.png'  # Is temporary

        self.ui.refreshButton.clicked.connect(self.refresh_dirs)

        # Directory list view
        self.dirModel = QStandardItemModel()
        self.ui.dirView.setModel(self.dirModel)
        self.ui.dirView.clicked.connect(self.change_image_grid)

        # Image view
        self.imageModel = QStandardItemModel()
        self.ui.imageView.setModel(self.imageModel)
        self.ui.imageView.setViewMode(QtWidgets.QListView.IconMode)
        image_size = QtCore.QSize(400, 400)  # Set icon sizing here
        self.ui.imageView.setIconSize(image_size)
        self.ui.imageView.setGridSize(QtCore.QSize(450, 450))
        # self.ui.imageView.clicked.connect(self.image_selected)

        # Dataframe that contains state
        self.df_images = pd.DataFrame()


    def refresh_dirs(self):
        self.dirModel.clear()
        for i in os.listdir(self.in_directory):
            if not os.path.isdir(os.path.join(self.in_directory, i)):
                continue

            dirItem = QStandardItem()
            dirItem.setText(i)
            self.dirModel.appendRow(dirItem)

    def change_image_grid(self, index):
        self.imageModel.clear()

        # Get dir path from the index data itself - Avoids having to play with roles
        dir_path = os.path.join(self.in_directory, index.data())

        # Parse arrays within the directory
        image_list = [
            os.path.join(dir_path, i) for i in os.listdir(dir_path)
            if i.endswith('.bmeii')]
        loaded_images = loader(image_list)

        for img_path in loaded_images:
            img_pixmap = QPixmap.fromImage(QImage(img_path))
            filename = os.path.basename(img_path).replace('.png', '')

            imageItem = QStandardItem()
            imageItem.setIcon(img_pixmap)
            imageItem.setText(filename)
            imageItem.setCheckable(True)

            self.imageModel.appendRow(imageItem)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_()) 
