
from PyQt6.QtWidgets import (
    QWidget,
    QSplitter,
    QListView,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QAbstractItemView
)

from components.filter_classes import *


class FilterPanel(QWidget):
    """
    panel where user can select images to filter
    """
    def __init__(self):
        super().__init__()
        # setup configuration
        self.setMinimumWidth(FILTER_PANEL_WIDTH)

        # create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel('Filter Panel')
        label.setStyleSheet(TITLE_LABEL_STYLE)
        layout.addWidget(label)

        self.filters_selector = FiltersSelector()
        layout.addWidget(self.filters_selector)

        self.setLayout(layout)


class FiltersSelector(QListWidget):
    """
    list widget that holds all the filters
    """
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        self.filters = []

        # adds all the filters to self
        for filter_class in [Scan, Rotate, Flip, Crop, Sharpen, Blur, Smooth, Emboss, Greyscale]:
            # create filter item
            new_filter = filter_class()

            # add filter item
            list_item = QListWidgetItem()
            list_item.setSizeHint(new_filter.sizeHint())
            self.addItem(list_item)
            self.setItemWidget(list_item, new_filter)
            self.filters.append(new_filter)
