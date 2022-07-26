import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QSplitter,
    QMenuBar,
    QMenu,
    QPushButton,
    QVBoxLayout
)
from PyQt6.QtGui import QAction, QIcon, QPixmap

from constants import *

from components.side_panel import SidePanel
from components.image_viewer import ImageViewer
from components.filter_panel import FilterPanel


def exit_app():
    """
    quits the app
    :return: Nothing
    """
    app.quit()


def except_hook(cls, exception, traceback):
    """
    used to make sure that tracebacks work
    """
    sys.__excepthook__(cls, exception, traceback)


class MainWindow(QMainWindow):
    """
    main window that holds the entire app
    """
    def __init__(self):
        super().__init__()
        # setup configuration
        self.setStyleSheet(STYLESHEET)
        self.setMinimumSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Mass Image Editor')
        window_icon = QIcon(
            QPixmap(WINDOW_ICON_IMG)
        )
        self.setWindowIcon(window_icon)

        # create main windows
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.side_panel = SidePanel()
        self.side_panel.menu.itemSelectionChanged.connect(self.photo_selected)
        self.image_viewer = ImageViewer()
        self.filter_panel = FilterPanel()

        # holds folder selector and image viewer
        splitter = QSplitter()
        splitter.addWidget(self.side_panel)
        splitter.addWidget(self.image_viewer)
        splitter.addWidget(self.filter_panel)
        splitter.setSizes([SIDE_PANEL_WIDTH,
                           SCREEN_WIDTH - SIDE_PANEL_WIDTH - FILTER_PANEL_WIDTH,
                           FILTER_PANEL_WIDTH])
        splitter.setMinimumHeight(TOP_PANEL_MIN_HEIGHT)

        # panel that holds the preview button
        bottom_panel = QHBoxLayout()
        preview_button = QPushButton("Update Image Previews")
        preview_button.clicked.connect(self.update_images)
        preview_button.setFixedHeight(50)
        bottom_panel.addWidget(preview_button)

        # add everything to outer layout
        layout.addWidget(splitter)
        layout.addLayout(bottom_panel)

        # set layout
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create menu bar
        self.action_save = QAction('Save Copies', self)
        self.action_save.triggered.connect(self.save_all)
        self.action_open = QAction('Open', self)
        self.action_open.triggered.connect(self.side_panel.select_dir)
        self.action_quit = QAction('Quit', self)
        self.action_quit.triggered.connect(exit_app)

        self.menubar = QMenuBar(self)
        self.menu_file = QMenu('File', self.menubar)

        MainWindow.setMenuBar(self, self.menubar)

        # add actions to menubar
        self.menubar.addAction(self.menu_file.menuAction())

        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_quit)

    def photo_selected(self):
        """
        updates the image viewer tabs to match the selection in the side panel
        :return: nothing
        """
        # selection is a list of strings with the selected items in the menu
        selection = self.side_panel.menu.selectedItems()
        selection = list(map(lambda n: n.text(), selection))
        self.image_viewer.update_tabs(selection, self.side_panel.selected_dir)

    def update_images(self):
        """
        updates all images in the image viewer to the current selected filters
        :return: nothing
        """
        modified_images = self.image_viewer.opened_images.copy()
        for key in modified_images:
            img = modified_images[key]
            modified_images[key] = self.apply_all_filters(img)
        self.image_viewer.set_multiple_images(modified_images)

    def apply_all_filters(self, img):
        """
        applies all selected filters to an image
        :param img: the image to apply the filters to
        :return: the modified image
        """
        for image_filter in self.filter_panel.filters_selector.filters:
            if image_filter.activate.isChecked():
                img = image_filter.apply_to_image(img)
        return img

    def save_all(self):
        """
        creates a new folder called "output" then
        filters all the selected images and then saves them as their filename
        uses png for the created images
        :return: nothing
        """
        # creates a new folder
        path_to_folder = self.side_panel.selected_dir + '/output'
        if not os.path.exists(path_to_folder):
            os.makedirs(path_to_folder)
        else:
            ending_num = 1
            while os.path.exists(path_to_folder + str(ending_num)):
                ending_num += 1
            path_to_folder = path_to_folder + str(ending_num)
            os.makedirs(path_to_folder)

        # saves all images into that folder
        modified_images = self.image_viewer.opened_images.copy()
        for key in modified_images:
            img = modified_images[key]
            img = self.apply_all_filters(img)
            filename = key[:key.index('.')]
            path = path_to_folder + '/' + filename + '.png'
            img.save(path)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)

    window = MainWindow()

    # default to maximized screen
    window.showMaximized()

    app.exec()
