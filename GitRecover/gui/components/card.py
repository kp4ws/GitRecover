"""
Author: Kent Pawson
card.py provides a styled container for grouped interface widgets.
"""

from PySide6.QtWidgets import QVBoxLayout, QWidget, QLayout, QGroupBox

class Card(QGroupBox):
    def __init__(self, title, items):
        """Initialize a card with grouped items.

        Parameters:
            title: Card title.
            items: Widgets or layouts displayed in the card.
        """
        super().__init__()
        self.setTitle(title)
        self._create_widgets(items)
        self._apply_styles()

    def _create_widgets(self, items):
        """Add widgets and layouts to the card.

        Parameters:
            items: Widgets or layouts to add.
        """
        self.setObjectName("card")
        layout = QVBoxLayout(self)

        for item in items:
            if isinstance(item, QWidget):
                layout.addWidget(item)
            elif isinstance(item, QLayout):
                layout.addLayout(item)
            else:
                print("Unsupported widget type")

    def _apply_styles(self):
        """Apply card-specific styles."""
        self.setStyleSheet("""
        """)