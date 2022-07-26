from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from constants import *
from image_filtering.image_processing import *


class FilterListItem(QWidget):
    """
    class that provides an icon, name, checkbox, title, and layout to items in the filter list
    """
    def __init__(self):
        super().__init__()

        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)

        self.activate = QCheckBox()
        name_layout.addWidget(self.activate)

        self.icon = QLabel()
        name_layout.addWidget(self.icon)

        self.title = QLabel()
        name_layout.addWidget(self.title)
        self.title.setStyleSheet("padding-right: 15px;")

        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.description = QLabel()

        widget = QWidget()
        widget.setObjectName('filter-item-information')
        widget.setLayout(name_layout)
        widget.setMinimumWidth(140)
        widget.setStyleSheet(FILTER_ITEM_STYLE)

        layout = QHBoxLayout()
        layout.addWidget(widget, 0)
        layout.addLayout(self.content_layout, 0)
        layout.addWidget(self.description, 1)
        self.setLayout(layout)

    def set_title(self, title: str):
        """
        setter method that sets the title
        :param title: a str to be set as the title
        :return: nothing
        """
        self.title.setText(title)

    def set_icon(self, pixmap: QPixmap):
        """
        setter method that sets the icon
        :param pixmap: a QPixmap to be set as the icon
        :return: nothing
        """
        pixmap = pixmap.scaledToHeight(40)
        self.icon.setPixmap(pixmap)

    def set_description(self, text: str):
        """
        a setter method that sets the description
        :param text: a str to be set as the description
        :return: nothing
        """
        self.description.setText(text)


class Scan(FilterListItem):
    """
    puts images through a "scan" filter
    has a slider which controls the threshold where the item is scanned
    """
    def __init__(self):
        super().__init__()
        self.set_title('Scan')

        icon = QPixmap(SCAN_IMG)
        self.set_icon(icon)

        slider_label = QLabel()
        slider_label.setText('Threshold:')
        self.content_layout.addWidget(slider_label)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(200)
        self.content_layout.addWidget(self.slider)

    def apply_to_image(self, img: Image.Image):
        return filter_scan(img, self.slider.value())


class Rotate(FilterListItem):
    """
    rotates images by a certain angle
    has two buttons that set the rotation angle to left or right
    has an input where the user can manually select the angle
    """
    def __init__(self):
        super().__init__()
        self.set_title('Rotate')

        icon = QPixmap(ROTATE_IMG)
        self.set_icon(icon)

        # 90 degrees buttons
        button_layout = QVBoxLayout()
        rotate_left = QPushButton('90 Degrees Left')
        rotate_left.clicked.connect(self.set_rotate_left)
        button_layout.addWidget(rotate_left)

        rotate_right = QPushButton('90 Degrees Right')
        rotate_right.clicked.connect(self.set_rotate_right)
        button_layout.addWidget(rotate_right)

        self.content_layout.addLayout(button_layout, 1)

        # angle selector
        angle_selector_layout = QHBoxLayout()
        angle_selector_layout.setContentsMargins(0, 0, 0, 0)

        angle_selector_label = QLabel()
        angle_selector_label.setText('Angle:')
        angle_selector_layout.addWidget(angle_selector_label, 0)

        self.angle_selector = QDoubleSpinBox()
        self.angle_selector.setMinimum(-360)
        self.angle_selector.setMaximum(360)
        self.angle_selector.setSingleStep(10)
        angle_selector_layout.addWidget(self.angle_selector, 0)

        self.content_layout.addLayout(angle_selector_layout)

    def apply_to_image(self, img: Image.Image):
        return rotate(img, self.angle_selector.value())

    def set_rotate_left(self):
        self.angle_selector.setValue(90)

    def set_rotate_right(self):
        self.angle_selector.setValue(-90)


class Flip(FilterListItem):
    """
    flips images vertically or horizontally
    has two buttons which control vertical/horizontal
    """
    def __init__(self):
        super().__init__()
        self.set_title('Flip')

        icon = QPixmap(FLIP_HOR_IMG)
        self.set_icon(icon)

        self.flip_horizontal = QPushButton()
        self.flip_horizontal.setCheckable(True)
        self.flip_horizontal.setChecked(True)
        self.flip_horizontal.setEnabled(False)
        self.flip_horizontal.setIcon(QIcon(FLIP_HOR_IMG))
        self.flip_horizontal.setText('Flip Horizontal')
        self.flip_horizontal.clicked.connect(self.horizontal_selected)
        self.content_layout.addWidget(self.flip_horizontal)

        self.flip_vertical = QPushButton()
        self.flip_vertical.setCheckable(True)
        self.flip_vertical.setIcon(QIcon(FLIP_VER_IMG))
        self.flip_vertical.setText('Flip Vertical')
        self.flip_vertical.clicked.connect(self.vertical_selected)
        self.content_layout.addWidget(self.flip_vertical)

    def apply_to_image(self, img: Image.Image):
        if self.flip_horizontal.isChecked():
            return flip(img, True)
        else:
            return flip(img, False)

    def vertical_selected(self):
        self.flip_horizontal.setChecked(False)
        self.flip_horizontal.setEnabled(True)
        self.flip_vertical.setEnabled(False)

    def horizontal_selected(self):
        self.flip_vertical.setChecked(False)
        self.flip_vertical.setEnabled(True)
        self.flip_horizontal.setEnabled(False)


class Crop(FilterListItem):
    """
    applies crop filter to the images
    has 4 separate inputs for each side of the image
    opposite sides cannot be set to add up to more than 100%
    """
    def __init__(self):
        super().__init__()
        self.set_title('Crop')

        icon = QPixmap(CROP_IMG)
        self.set_icon(icon)

        col_1 = QVBoxLayout()
        col_2 = QVBoxLayout()

        left_input = QHBoxLayout()
        left_input_label = QLabel()
        left_input_label.setText('Left %:')
        left_input.addWidget(left_input_label)
        self.left_spinbox = QDoubleSpinBox()
        self.left_spinbox.setMinimum(0)
        self.left_spinbox.setMaximum(100)
        self.left_spinbox.setSingleStep(5)
        self.left_spinbox.valueChanged.connect(self.left_changed)
        left_input.addWidget(self.left_spinbox)
        col_1.addLayout(left_input)

        top_input = QHBoxLayout()
        top_input_label = QLabel()
        top_input_label.setText('Top %:')
        top_input.addWidget(top_input_label)
        self.top_spinbox = QDoubleSpinBox()
        self.top_spinbox.setMinimum(0)
        self.top_spinbox.setMaximum(100)
        self.top_spinbox.setSingleStep(5)
        self.top_spinbox.valueChanged.connect(self.top_changed)
        top_input.addWidget(self.top_spinbox)
        col_1.addLayout(top_input)

        right_input = QHBoxLayout()
        right_input_label = QLabel()
        right_input_label.setText('Right %:')
        right_input.addWidget(right_input_label)
        self.right_spinbox = QDoubleSpinBox()
        self.right_spinbox.setMinimum(0)
        self.right_spinbox.setMaximum(100)
        self.right_spinbox.setSingleStep(5)
        self.right_spinbox.valueChanged.connect(self.right_changed)
        right_input.addWidget(self.right_spinbox)
        col_2.addLayout(right_input)

        bottom_input = QHBoxLayout()
        bottom_input_label = QLabel()
        bottom_input_label.setText('Bottom %:')
        bottom_input.addWidget(bottom_input_label)
        self.bottom_spinbox = QDoubleSpinBox()
        self.bottom_spinbox.setMinimum(0)
        self.bottom_spinbox.setMaximum(100)
        self.bottom_spinbox.setSingleStep(5)
        self.bottom_spinbox.valueChanged.connect(self.bottom_changed)
        bottom_input.addWidget(self.bottom_spinbox)
        col_2.addLayout(bottom_input)

        self.content_layout.addLayout(col_1)
        self.content_layout.addLayout(col_2)

    def apply_to_image(self, img: Image.Image):
        return crop(
            img,
            self.left_spinbox.value(),
            self.top_spinbox.value(),
            self.right_spinbox.value(),
            self.bottom_spinbox.value()
        )

    def right_changed(self):
        self.left_spinbox.setMaximum(100 - self.right_spinbox.value())

    def left_changed(self):
        self.right_spinbox.setMaximum(100 - self.left_spinbox.value())

    def top_changed(self):
        self.bottom_spinbox.setMaximum(100 - self.bottom_spinbox.value())

    def bottom_changed(self):
        self.top_spinbox.setMaximum(100 - self.top_spinbox.value())


class Sharpen(FilterListItem):
    """
    applies a "sharpen" filter to images
    no inputs
    """
    def __init__(self):
        super().__init__()
        self.set_title('Sharpen')

        icon = QPixmap(SHARPEN_IMG)
        self.set_icon(icon)

    def apply_to_image(self, img: Image.Image):
        return sharpen(img)


class Blur(FilterListItem):
    """
    applies a "blur" filter to images
    has a slider which controls the blur intensity
    """
    def __init__(self):
        super().__init__()
        self.set_title('Blur')

        slider_label = QLabel()
        slider_label.setText('Intensity:')
        self.content_layout.addWidget(slider_label)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(7)
        self.slider.setSingleStep(1)
        self.content_layout.addWidget(self.slider)

        icon = QPixmap(BLUR_IMG)
        self.set_icon(icon)

    def apply_to_image(self, img: Image.Image):
        return blur(img, self.slider.value())


class Smooth(FilterListItem):
    """
    applies a "smooth" filter to images
    has a slider which controls intensity
    """
    def __init__(self):
        super().__init__()
        self.set_title('Smooth')

        slider_label = QLabel()
        slider_label.setText('Intensity:')
        self.content_layout.addWidget(slider_label)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(5)
        self.slider.setSingleStep(1)
        self.content_layout.addWidget(self.slider)

        icon = QPixmap(SMOOTH_IMG)
        self.set_icon(icon)

    def apply_to_image(self, img: Image.Image):
        return smooth(img, self.slider.value())


class Emboss(FilterListItem):
    """
    applies an "emboss" filter to images
    no inputs
    """
    def __init__(self):
        super().__init__()
        self.set_title('Emboss')

        icon = QPixmap(EMBOSS_IMG)
        self.set_icon(icon)

    def apply_to_image(self, img: Image.Image):
        return emboss(img)


class Greyscale(FilterListItem):
    """
    turns images into greyscale
    no inputs
    """
    def __init__(self):
        super().__init__()
        self.set_title('Greyscale')

        icon = QPixmap(GREYSCALE_IMG)
        self.set_icon(icon)

    def apply_to_image(self, img: Image.Image):
        return greyscale(img)

