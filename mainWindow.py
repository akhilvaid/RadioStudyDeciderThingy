# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1695, 747)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.imageView = QListView(self.centralwidget)
        self.imageView.setObjectName(u"imageView")

        self.gridLayout.addWidget(self.imageView, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout_2 = QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.outDirEdit = QLineEdit(self.dockWidgetContents)
        self.outDirEdit.setObjectName(u"outDirEdit")

        self.horizontalLayout.addWidget(self.outDirEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.inDirEdit = QLineEdit(self.dockWidgetContents)
        self.inDirEdit.setObjectName(u"inDirEdit")

        self.horizontalLayout_2.addWidget(self.inDirEdit)

        self.refreshButton = QPushButton(self.dockWidgetContents)
        self.refreshButton.setObjectName(u"refreshButton")

        self.horizontalLayout_2.addWidget(self.refreshButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.dirView = QListView(self.dockWidgetContents)
        self.dirView.setObjectName(u"dirView")

        self.verticalLayout.addWidget(self.dirView)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"RadioPicker", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Config", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"OutputDir", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"InputDir", None))
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
    # retranslateUi

