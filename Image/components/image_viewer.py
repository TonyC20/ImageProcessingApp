from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from constants import *
from PIL import Image
from PIL.ImageQt import ImageQt

# im = ImageQt(Image.open('notes.png'))
# pixmap = QtGui.QPixmap.fromImage(im)
# label = QtWidgets.QLabel(self)
# label.setPixmap(pixmap)
# label.setFixedSize(500, 500)
# label.move(100, 100)


class ImageViewer(QWidget):
    """
    image viewer that displays the edited images
    """
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(IMAGE_VIEWER_MIN_WIDTH)
        # stores all opened images as PIL images
        self.opened_images = dict()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel('Image Preview')
        label.setStyleSheet(TITLE_LABEL_STYLE)
        layout.addWidget(label)

        self.image_tabs = QTabWidget()
        self.image_tabs.currentChanged.connect(self.scale_current_tab)
        layout.addWidget(self.image_tabs)

        self.setLayout(layout)

    def update_tabs(self, selection, selected_dir):
        """
        updates tabs to only include the files chosen by the user
        :param selection: selection the user chose
        :param selected_dir: directory where the selection items are located
        :return: nothing
        """
        # add tabs that are newly selected
        for item_name in selection:
            newly_selected = True

            for i in range(self.image_tabs.count()):
                if item_name == self.image_tabs.tabText(i):
                    newly_selected = False
                    break

            if newly_selected:
                # if the item was just selected, add to the tabs
                path = selected_dir + '\\' + item_name
                image = Image.open(path)
                self.add_image(image, item_name)
                self.opened_images[item_name] = image

        # remove all the tabs that are not in the current selection
        for i in range(self.image_tabs.count() - 1, -1, -1):
            tab_name = self.image_tabs.tabText(i)
            if tab_name not in selection:
                self.image_tabs.removeTab(i)
                self.opened_images.pop(tab_name)

    def add_image(self, image, tab_name) -> None:
        """
        adds a new tab with an image
        :param image: image to be in the tab
        :param tab_name: name of the tab
        :return: nothing
        """
        # convert image to format usable for pyqt
        image_tab = ImageTab()
        image_tab.set_image(image, self.width(), self.height())
        self.image_tabs.addTab(image_tab, tab_name)

    def set_multiple_images(self, image_dict: dict):
        """
        sets the images of tabs to be images from the image_dict dictionary
        :param image_dict: format is {tab-name: image-to-be-set}
        :return:
        """
        for tab_name in image_dict:
            img = image_dict[tab_name]
            self.set_image(tab_name, img)

    def set_image(self, tab_name, img):
        """
        sets the image of a single tab given the tab name
        :param tab_name: str name of the tab where the image is contained
        :param img: image to be set
        :return: nothing
        """
        for i in range(self.image_tabs.count()):
            if self.image_tabs.tabText(i) == tab_name:
                image_tab = self.image_tabs.widget(i)
                image_tab.set_image(img, self.width(), self.height())
                break

    def resizeEvent(self, event):
        """
        scales the image in the current tab whenever it is resized
        """
        self.scale_current_tab()
        return super().resizeEvent(event)

    def scale_current_tab(self):
        """
        scales the image of the current tab to fit the width and height
        :return: nothing
        """
        current_tab = self.image_tabs.currentWidget()
        if current_tab is not None:
            current_tab.scale_image(self.width(), self.height())


class ImageTab(QWidget):
    """
    tab that can hold an image and resize it. Used with the ImageViewer
    """
    def __init__(self):
        super().__init__()
        # image that the tab is currently showing
        self.img = None

        # create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def set_image(self, img: Image.Image, width: int, height: int):
        """
        sets the image of the tab to the passed in image and scales it to width and
        height while keeping the same aspect ratio
        :param img: the image to be set
        :param width: the width to be scaled to
        :param height: the height to be scaled to
        :return: nothing
        """
        # convert image to usable format
        img = img.convert('RGBA')
        self.img = img
        # pixmap from image
        pixmap = QPixmap.fromImage(ImageQt(img))
        pixmap = pixmap.scaled(
            int(width * IMAGE_VIEW_SCALE),
            int(height * IMAGE_VIEW_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)

    def scale_image(self, width: int, height: int):
        """
        scales the current image to width and height while
        keeping the same aspect ratio
        :param width: the width to be scaled to
        :param height: the height to be scaled to
        :return: nothing
        """
        pixmap = QPixmap.fromImage(ImageQt(self.img))
        pixmap = pixmap.scaled(
            int(width * IMAGE_VIEW_SCALE),
            int(height * IMAGE_VIEW_SCALE),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        self.image_label.setPixmap(pixmap)