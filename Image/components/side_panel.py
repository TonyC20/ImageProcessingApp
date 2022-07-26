from constants import *
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QLabel
)
from PyQt6.QtGui import QPixmap, QIcon
import os


# file formats supported by pillow library
SUPPORTED_FORMATS = (
    '.blp',
    '.bmp',
    '.dds',
    '.dib',
    '.eps',
    '.icns',
    '.ico',
    '.im',
    '.jpeg',
    '.jfif',
    '.msp',
    '.pcx',
    '.png',
    'jpg',
    '.ppm',
    '.sgi',
    '.spider',
    '.tga',
    '.tiff',
    '.webp',
    '.xbm',
    '.cur',
    '.dcx',
    '.fits',
    '.fli',
    '.flc',
    '.fpx',
    '.ftex',
    '.gbr',
    '.gd',
    '.imt',
    '.iptc',
    '.naa',
    '.mcidas',
    '.mic',
    '.mpo',
    '.pcd',
    '.pixar',
    '.psd',
    '.wal',
    '.wmf',
    '.xpm'
)


def get_images_dir(path: str) -> list:
    """
    gets all image names from the passed in path
    """
    files = os.listdir(path)
    images = []
    for file in files:
        # uses SUPPORTED_FORMATS from constants.py
        if file.endswith(SUPPORTED_FORMATS):
            images.append(file)
    return images


class SidePanel(QWidget):
    """
    side panel for selecting a folder + files
    """
    def __init__(self):
        super().__init__()

        # create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel('File Selector')
        label.setStyleSheet(TITLE_LABEL_STYLE)
        layout.addWidget(label)

        # create file selector
        self.menu = QListWidget()
        self.menu.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.menu)
        self.selected_dir = DEFAULT_FOLDER
        self.update_menu()

        # button for selecting new folder
        self.select_button = QPushButton('Select Folder')
        self.select_button.clicked.connect(self.select_dir)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def select_dir(self):
        """
        opens a window where the user can select a new folder
        :return: nothing
        """
        new_dir = QFileDialog.getExistingDirectory(self, 'Select Folder', self.selected_dir)
        if len(new_dir) > 0:
            self.selected_dir = new_dir
            self.update_menu()

    def update_menu(self):
        """
        updates the menu with the files in the current selected directory
        only shows files ending in one of the `SUPPORTED_FORMATS`
        :return: nothing
        """
        if len(self.selected_dir) > 0:
            self.menu.clear()
            files = get_images_dir(self.selected_dir)
            for file in files:
                item = QListWidgetItem()
                item.setText(file)

                # add icon
                pixmap = QPixmap(self.selected_dir + '\\' + file)
                icon = QIcon(pixmap)
                item.setIcon(icon)

                self.menu.addItem(item)
