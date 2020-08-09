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
        self.setIconSize(QtCore.QSize(24, 24))
        self.setFloatable(False)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.setObjectName('ToolBar')

        self.refreshButton = QtWidgets.QAction(
            QIcon('Resources/folder.svg'),
            'Load directory', self)

        self.cmapButton = QtWidgets.QToolButton(self)
        self.cmapButton.setIcon(QIcon('Resources/color.svg'))
        self.cmapButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.saveButton = QtWidgets.QAction(
            QIcon('Resources/save.svg'),
            'Save curated list', self)
        self.loadButton = QtWidgets.QAction(
            QIcon('Resources/load.svg'),
            'Load curated list', self)

        # Add to toolbar
        self.addAction(self.refreshButton)
        self.separator1 = self.addSeparator()
        self.addWidget(self.cmapButton)
        self.separator2 = self.addSeparator()
        self.addAction(self.saveButton)
        self.addAction(self.loadButton)

        self.cmapButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.loadButton.setEnabled(False)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, studies, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.dict_studies = studies
        self.list_keys = list(studies.keys())

        self.dict_col = {
            0: 'DIRECTORY',
            1: 'TOTAL FILES',
            2: 'SELECTED'
        }

    def rowCount(self, parent=None):
        return len(self.dict_studies.keys())

    def columnCount(self, parent=None):
        return 3  # NOTE Requires changing for each new column

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:

                val_ref = self.list_keys[index.row()]
                if index.column() != 0:
                    key_ref = self.dict_studies[self.list_keys[index.row()]]
                    val_ref = key_ref[self.dict_col[index.column()]]

                if isinstance(val_ref, list):
                    return ', '.join(val_ref)
                else:
                    return str(val_ref)
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.dict_col[col]
        return None

    def update_from_loaded(self, df):
        for idx in range(df.shape[0]):
            try:
                study = df.iloc[idx]['DIRECTORY']
                files = eval(df.iloc[idx]['FILES'])
                self.dict_studies[study]['SELECTED'] = files

            except:  # Using eval() - One, bad practice because Two, anything can happen
                continue


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Instantiate widgets and models
        self.toolBar = ToolBar()
        self.addToolBar(self.toolBar)

        self.dirModel = TableModel(dict())
        self.imageModel = QStandardItemModel()

        self.ui.dockWidget.setTitleBarWidget(QtWidgets.QWidget())

        self.statusBarLabel = QtWidgets.QLabel()
        self.statusBar().addWidget(self.statusBarLabel)

        self.cmapMenu = QtWidgets.QMenu()

        self.in_directory = None

        # Cmap menu
        Config.cmap = 'bone'
        self.create_cmap_menu()

        # Toolbar
        self.toolBar.refreshButton.triggered.connect(self.create_dir_model)
        self.toolBar.saveButton.triggered.connect(self.export_df)
        self.toolBar.loadButton.triggered.connect(self.load_df)

        # Directory list view
        self.ui.dirView.clicked.connect(self.change_image_grid)

        # Image view
        image_size = QtCore.QSize(400, 400)  # Set icon sizing here
        grid_size = QtCore.QSize(450, 450)

        self.ui.imageView.setModel(self.imageModel)
        self.ui.imageView.setViewMode(QtWidgets.QListView.IconMode)
        self.ui.imageView.setIconSize(image_size)
        self.ui.imageView.setGridSize(grid_size)
        self.ui.imageView.clicked.connect(self.image_selected)

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

        self.toolBar.cmapButton.setMenu(self.cmapMenu)

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
        self.in_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Study Directory', os.path.expanduser('~'))

        dict_table = {}
        for root, _, files in os.walk(self.in_directory):
            if not files:
                continue

            dir_name = root.split(os.sep)[-1]
            total_files = len(files)
            selected = pd.NA

            dict_table[dir_name] = {
                'TOTAL FILES': total_files,
                'SELECTED': selected
            }

        self.dirModel = TableModel(dict_table)
        self.ui.dirView.setModel(self.dirModel)
        self.ui.dirView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.update_statusbar()

        self.toolBar.cmapButton.setEnabled(True)
        self.toolBar.saveButton.setEnabled(True)
        self.toolBar.loadButton.setEnabled(True)

    ################################################################

    def change_image_grid(self, index):
        self.imageModel.clear()

        # Get dir path from the index data itself
        directory = self.dirModel.list_keys[index.row()]
        dir_path = os.path.join(
            self.in_directory,
            directory)

        previously_checked = self.dirModel.dict_studies[directory]['SELECTED']

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
            imageItem.setEditable(False)

            imageItem.setCheckable(True)
            if not pd.isnull(previously_checked):
                if filename in previously_checked:
                    imageItem.setCheckState(QtCore.Qt.CheckState.Checked)

            self.imageModel.appendRow(imageItem)

    def image_selected(self, index):
        current_row = self.ui.dirView.currentIndex().row()
        current_dir = self.dirModel.list_keys[current_row]

        images_selected = []

        for row in range(self.imageModel.rowCount()):
            item = self.imageModel.item(row)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                item_text = item.text()
                images_selected.append(item_text)

        if images_selected == []:
            self.dirModel.dict_studies[current_dir]['SELECTED'] = pd.NA
        else:
            self.dirModel.dict_studies[current_dir]['SELECTED'] = images_selected

        # TODO
        # self.dirModel.dataChanged.emit()

    ################################################################

    def export_df(self):
        rows = []
        for directory, values in self.dirModel.dict_studies.items():
            files = values['SELECTED']
            rows.append((directory, files))

        df_studies = pd.DataFrame(rows, columns=['DIRECTORY', 'FILES'])
        df_studies.to_csv(
            os.path.join(os.path.expanduser('~'), 'SelectedFiles.csv'))

    def load_df(self):
        in_csv = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load exported file list', os.path.expanduser('~'))

        try:
            df = pd.read_csv(in_csv[0])
            self.dirModel.update_from_loaded(df)
        except KeyboardInterrupt:
            self.statusBarLabel.setText(
                'No file selected / Error loading saved list')
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
