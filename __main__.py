import os
import sys
import pandas as pd

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage, QIcon

from mainWindow import Ui_MainWindow
from image_loading import loader
from config import Config


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.setMovable(False)
        self.setIconSize(QtCore.QSize(22, 22))
        self.setFloatable(False)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setObjectName('ToolBar')

        self.refreshButton = QtWidgets.QAction(
            QIcon.fromTheme('fileopen'),
            'Load directory', self)

        self.cmapButton = QtWidgets.QToolButton(self)
        self.cmapButton.setIcon(QIcon.fromTheme('colormanagement'))
        self.cmapButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.prevButton = QtWidgets.QAction(
            QIcon.fromTheme('previous'),
            'Previous', self)

        self.nextButton = QtWidgets.QAction(
            QIcon.fromTheme('next'),
            'Next', self)

        self.saveButton = QtWidgets.QAction(
            QIcon.fromTheme('filesave'),
            'Save', self)

        # Add to toolbar
        self.addAction(self.refreshButton)
        self.separator1 = self.addSeparator()
        self.addWidget(self.cmapButton)
        self.separator2 = self.addSeparator()
        self.addAction(self.prevButton)
        self.addAction(self.nextButton)
        self.separator3 = self.addSeparator()
        self.addAction(self.saveButton)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.in_directory = '/home/akhil/Temp/'

        # Instantiate widgets and models
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar)

        self.dirModel = QStandardItemModel()
        self.imageModel = QStandardItemModel()

        self.ui.dockWidget.setTitleBarWidget(QtWidgets.QWidget())

        self.statusBarLabel = QtWidgets.QLabel()
        self.statusBar().addWidget(self.statusBarLabel)

        self.cmapMenu = QtWidgets.QMenu()

        # Cmap menu
        Config.cmap = 'bone'
        self.create_cmap_menu()

        # Toolbar
        self.toolbar.refreshButton.triggered.connect(self.create_dir_model)

        # Directory list view
        self.ui.dirView.setModel(self.dirModel)
        self.ui.dirView.clicked.connect(self.change_image_grid)

        # Image view
        image_size = QtCore.QSize(400, 400)  # Set icon sizing here
        grid_size = QtCore.QSize(450, 450)

        self.ui.imageView.setModel(self.imageModel)
        self.ui.imageView.setViewMode(QtWidgets.QListView.IconMode)
        self.ui.imageView.setIconSize(image_size)
        self.ui.imageView.setGridSize(grid_size)
        # self.ui.imageView.clicked.connect(self.image_selected)

        # Dataframe to save to
        self.df_images = pd.DataFrame()

        # Final touches
        self.update_statusbar()

    ################################################################

    def create_cmap_menu(self):
        self.cmapMenu.clear()
        for cmap_type, cmaps in Config.cmaps.items():
            thisMenu = QtWidgets.QMenu(cmap_type)
            self.cmapMenu.addMenu(thisMenu)

            for cmap in cmaps:
                thisAction = QtWidgets.QAction(cmap, self.cmapMenu)
                thisAction.triggered.connect(self.update_cmap)
                thisMenu.addAction(thisAction)

        self.toolbar.cmapButton.setMenu(self.cmapMenu)

    def update_cmap(self, args):
        Config.cmap = self.sender().text()
        self.change_image_grid(self.ui.dirView.currentIndex())
        self.update_statusbar()

    ################################################################

    def update_statusbar(self):
        self.statusBarLabel.setText(
            f'Colormap: {Config.cmap} | Directories loaded: {self.dirModel.rowCount()}')

    ################################################################

    def create_dir_model(self):
        self.dirModel.clear()
        for i in os.listdir(self.in_directory):
            if not os.path.isdir(os.path.join(self.in_directory, i)):
                continue

            dirItem = QStandardItem()
            dirItem2 = QStandardItem()
            dirItem.appendColumn([dirItem2])
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
