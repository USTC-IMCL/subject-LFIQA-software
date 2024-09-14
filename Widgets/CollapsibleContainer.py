from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QStackedLayout, QSpacerItem, QVBoxLayout
from PySide6 import QtCore, QtWidgets


class KeyPressHandler(QtCore.QObject):
    """Custom key press handler"""
    escapePressed = QtCore.Signal(bool)
    returnPressed = QtCore.Signal(bool)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            event_key = event.key()
            if event_key == QtCore.Qt.Key_Escape:
                self.escapePressed.emit(True)
                return True
            if event_key == QtCore.Qt.Key_Return or event_key == QtCore.Qt.Key_Enter:
                self.returnPressed.emit(True)
                return True

        return QtCore.QObject.eventFilter(self, obj, event)


class EditableLabelWidget(QtWidgets.QFrame):
    """Sample Widget"""
    def __init__(self, parent=None, **kwargs):
        super(EditableLabelWidget, self).__init__(parent)

        # create the editable label
        self.label = EditableLabel(self)
        
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.label,)
        self.setLayout(self.mainLayout)

        self.label.setText("click me to edit")
        self.setWindowTitle("Editable Label")

        # connect our custom signal
        self.label.textChanged.connect(self.labelTextChangedAction)

    def labelTextChangedAction(self, text):
        print("# label updated: \"{0}\"".format(text))


class EditableLabel(QtWidgets.QWidget):
    """Editable label"""
    textChanged = QtCore.Signal(str)
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent)

        self.is_editable = kwargs.get("editable", True)
        self.keyPressHandler = KeyPressHandler(self)

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName("mainLayout")
        
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.mainLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.mainLayout.addWidget(self.lineEdit)
        # hide the line edit initially
        self.lineEdit.setHidden(True)

        # setup signals
        self.create_signals()

    def create_signals(self):
        self.lineEdit.installEventFilter(self.keyPressHandler)
        self.label.mousePressEvent = self.labelPressedEvent

        # give the lineEdit both a `returnPressed` and `escapedPressed` action
        self.keyPressHandler.escapePressed.connect(self.escapePressedAction)
        self.keyPressHandler.returnPressed.connect(self.returnPressedAction)

    def text(self):
        """Standard QLabel text getter"""
        return self.label.text()

    def setText(self, text):
        """Standard QLabel text setter"""
        self.label.blockSignals(True)
        self.label.setText(text)
        self.label.blockSignals(False)

    def labelPressedEvent(self, event):
        """Set editable if the left mouse button is clicked"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.setLabelEditableAction()

    def setLabelEditableAction(self):
        """Action to make the widget editable"""
        if not self.is_editable:
            return

        self.label.setHidden(True)
        self.label.blockSignals(True)
        self.lineEdit.setHidden(False)
        self.lineEdit.setText(self.label.text())
        self.lineEdit.blockSignals(False)
        self.lineEdit.setFocus(QtCore.Qt.MouseFocusReason)
        self.lineEdit.selectAll()

    def labelUpdatedAction(self):
        """Indicates the widget text has been updated"""
        text_to_update = self.lineEdit.text()

        if text_to_update != self.label.text():
            self.label.setText(text_to_update)
            self.textChanged.emit(text_to_update)

        self.label.setHidden(False)
        self.lineEdit.setHidden(True)
        self.lineEdit.blockSignals(True)
        self.label.blockSignals(False)

    def returnPressedAction(self):
        """Return/enter event handler"""
        self.labelUpdatedAction()

    def escapePressedAction(self):
        """Escape event handler"""
        self.label.setHidden(False)
        self.lineEdit.setHidden(True)
        self.lineEdit.blockSignals(True)
        self.label.blockSignals(False)

class Header(QWidget):
    """
    Header class for collapsible group
    """
    def __init__(self, name, content_widget):
        """Header Class Constructor to initialize the object.

        Args:
            name (str): Name for the header
            content_widget (QtWidgets.QWidget): Widget containing child elements
        """
        super(Header, self).__init__()
        self.content = content_widget
        self.expand_ico = ">"   
        self.collapse_ico = "v"  
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)

        # Create a stacked layout to hold the background and widget
        stacked = QStackedLayout(self)
        stacked.setStackingMode(QStackedLayout.StackAll)
        # Create a background label with a specific style sheet
        background = QLabel()
        background.setStyleSheet(
            "QLabel{ background-color: rgb(93, 93, 93); padding-top: -20px; border-radius:2px}")

        # Create a widget and a layout to hold the icon and label
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Create an icon label and set its text and style sheet
        self.icon = QLabel()
        self.icon.setText(self.expand_ico)
        self.icon.setStyleSheet(
            "QLabel { font-weight: bold; font-size: 20px; color: #000000 }")
        layout.addWidget(self.icon)

        # Add the icon and the label to the layout and set margins
        layout.addWidget(self.icon)
        layout.addWidget(self.icon)
        layout.setContentsMargins(11, 0, 11, 0)

        # Create a font and a label for the header name
        font = QFont()
        font.setBold(True)
        label = QLabel(name)
        label.setStyleSheet("QLabel { margin-top: 5px; }")
        label.setFont(font)

        # Add the label to the layout and add a spacer for expanding
        layout.addWidget(label)
        layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Add the widget and the background to the stacked layout
        stacked.addWidget(widget)
        stacked.addWidget(background)
        # Set the minimum height of the background based on the layout height
        background.setMinimumHeight(layout.sizeHint().height() * 1.5)

    def mousePressEvent(self, *args):
        """Handle mouse events, call the function to toggle groups"""
        # Toggle between expand and collapse based on the visibility of the content widget
        self.expand() if not self.content.isVisible() else self.collapse()

    def expand(self):
        """Expand the collapsible group"""
        self.content.setVisible(True)
        self.icon.setText(self.collapse_ico)  # Set text instead of pixmap

    def collapse(self):
        """Collapse the collapsible group"""
        self.content.setVisible(False)
        self.icon.setText(self.expand_ico)


class Container(QWidget):
    """Class for creating a collapsible group similar to how it is implement in Maya

        Examples:
            Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout

            >>> layout = QtWidgets.QVBoxLayout()
            >>> container = Container("Group")
            >>> layout.addWidget(container)
            >>> content_layout = QtWidgets.QGridLayout(container.contentWidget)
            >>> content_layout.addWidget(QtWidgets.QPushButton("Button"))
    """

    def __init__(self, name, color_background=False):
            """Container Class Constructor to initialize the object
    
            Args:
                name (str): Name for the header
                color_background (bool): whether or not to color the background lighter like in maya
            """
            super(Container, self).__init__() # Call the constructor of the parent class
    
            layout = QVBoxLayout(self) # Create a QVBoxLayout instance and pass the current object as the parent
            layout.setContentsMargins(0, 0, 0, 0) # Set the margins of the layout to 0
    
            self._content_widget = QWidget() # Create a QWidget instance and assign it to the instance variable _content_widget
    
            if color_background:
                # If color_background is True, set the stylesheet of _content_widget to have a lighter background color
                self._content_widget.setStyleSheet(".QWidget{background-color: rgb(73, 73, 73); "
                                                   "margin-left: 2px; padding-top: 20px; margin-right: 2px}")
    
            header = Header(name, self._content_widget) # Create a Header instance and pass the name and _content_widget as arguments
            layout.addWidget(header) # Add the header to the layout
            layout.addWidget(self._content_widget) # Add the _content_widget to the layout
    
           
            self.collapse = header.collapse 
            self.expand = header.expand 
            self.toggle = header.mousePressEvent 
    
    @property
    def contentWidget(self):
            """Getter for the content widget
    
            Returns: Content widget
            """
            return self._content_widget

if __name__ == "__main__":
     pass