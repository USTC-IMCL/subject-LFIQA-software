from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QStackedLayout, QSpacerItem, QVBoxLayout, QFrame
from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import Qt, QRect, Property, QPropertyAnimation, QPoint, QEasingCurve
from PySide6.QtGui import QColor, QFontMetrics, QPainterPath, QBrush, QPen, QFont, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QCheckBox


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
        if not self.lineEdit.isVisible():
            return
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

class EditableTexeEdit(QtWidgets.QWidget):
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
        self.lineEdit = QtWidgets.QPlainTextEdit(self)
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
        self.lineEdit.setPlainText(self.label.text())
        self.lineEdit.blockSignals(False)
        self.lineEdit.setFocus(QtCore.Qt.MouseFocusReason)
        self.lineEdit.selectAll()

    def labelUpdatedAction(self):
        """Indicates the widget text has been updated"""
        if not self.lineEdit.isVisible():
            return
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

class Header(QFrame):
    """
    Header class for collapsible group
    """
    clicked = QtCore.Signal()
    def __init__(self, name, content_widget):
        """Header Class Constructor to initialize the object.

        Args:
            name (str): Name for the header
            content_widget (QtWidgets.QWidget): Widget containing child elements
        """
        super(Header, self).__init__()
        self.content = content_widget
        self.collapse_ico = chr(9656)
        self.expand_ico = chr(9663)
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)

        self.header_color="rgba(0,100,200,128)"
        self.icon_font_size = 22

        # Create a stacked layout to hold the background and widget
        stacked = QStackedLayout(self)
        stacked.setStackingMode(QStackedLayout.StackAll)
        # Create a background label with a specific style sheet
        background = QLabel()
        background.setStyleSheet(
            f"QLabel{{ background-color: {self.header_color}; padding-top: -20px; border-radius:2px}}")

        # Create a widget and a layout to hold the icon and label
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Create an icon label and set its text and style sheet
        self.icon = QLabel()
        self.icon.setText(self.expand_ico)
        self.icon.setStyleSheet(
            f"QLabel {{ font-weight: bold; font-size: {self.icon_font_size}px; color: #000000 }}")
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
        self.background=background
        self.collapse()

    def mousePressEvent(self, *args):
        """Handle mouse events, call the function to toggle groups"""
        # Toggle between expand and collapse based on the visibility of the content widget
        self.expand() if not self.content.isVisible() else self.collapse()
        self.clicked.emit()

    def expand(self):
        """Expand the collapsible group"""
        self.content.setVisible(True)
        self.icon.setText(self.expand_ico)  # Set text instead of pixmap

    def collapse(self):
        """Collapse the collapsible group"""
        self.content.setVisible(False)
        self.icon.setText(self.collapse_ico)
    
    def SetColor(self, color):
        '''color : (R, G, B, A)'''
        if len(color) == 4:
            self.header_color=f'rgba({color[0]},{color[1]},{color[2]},{color[3]})'
        if len(color) == 3:
            self.header_color=f'rgba({color[0]},{color[1]},{color[2]},{255})'
        self.background.setStyleSheet(f"{{backgound-color: {self.header_color};}}") 

    
class Container(QFrame):
    """Class for creating a collapsible group similar to how it is implement in Maya

        Examples:
            Simple example of how to add a Container to a QVBoxLayout and attach a QGridLayout

            >>> layout = QtWidgets.QVBoxLayout()
            >>> container = Container("Group")
            >>> layout.addWidget(container)
            >>> content_layout = QtWidgets.QGridLayout(container.contentWidget)
            >>> content_layout.addWidget(QtWidgets.QPushButton("Button"))
    """
    content_clicked=QtCore.Signal()

    def __init__(self, name, color_background=False):
            """Container Class Constructor to initialize the object
    
            Args:
                name (str): Name for the header
                color_background (bool): whether or not to color the background lighter like in maya
            """
            super(Container, self).__init__() # Call the constructor of the parent class
    
            layout = QVBoxLayout(self) # Create a QVBoxLayout instance and pass the current object as the parent
            layout.setContentsMargins(0, 0, 0, 0) # Set the margins of the layout to 0
    
            self._content_widget = QFrame() # Create a QWidget instance and assign it to the instance variable _content_widget
    
            if color_background:
                # If color_background is True, set the stylesheet of _content_widget to have a lighter background color
                self._content_widget.setStyleSheet(".QWidget{background-color: rgb(100,100,100,150); "
                                                   "margin-left: 2px; padding-top: 20px; margin-right: 2px}")
    
            self.header = Header(name, self._content_widget) # Create a Header instance and pass the name and _content_widget as arguments
            header=self.header
            layout.addWidget(header) # Add the header to the layout
            layout.addWidget(self._content_widget) # Add the _content_widget to the layout
            self._content_widget.setStyleSheet(".QFrame{background-color: rgba(0,0,0,30); "
                                               "margin-left: 2px; padding-top: 5px; margin-right: 2px}")
           
            self.collapse = header.collapse 
            self.expand = header.expand 
            self.toggle = header.mousePressEvent 

            self._content_widget.mousePressEvent = self.ContentClicked

    def ContentClicked(self,event):
        if self._content_widget.isVisible() and event.button() == Qt.LeftButton:
            self.content_clicked.emit()

    def SetHeaderColor(self,color):
        self.header.SetColor(color)
    
    @property
    def contentWidget(self):
            """Getter for the content widget
    
            Returns: Content widget
            """
            return self._content_widget
    
class QToggle(QCheckBox):
    bg_color = Property(
        QColor, lambda self: self._bg_color,
        lambda self, col: setattr(self, '_bg_color', col))
    circle_color = Property(
        QColor, lambda self: self._circle_color,
        lambda self, col: setattr(self, '_circle_color', col))
    active_color = Property(
        QColor, lambda self: self._active_color,
        lambda self, col: setattr(self, '_active_color', col))
    disabled_color = Property(
        QColor, lambda self: self._disabled_color,
        lambda self, col: setattr(self, '_disabled_color', col))
    text_color = Property(
        QColor, lambda self: self._text_color,
        lambda self, col: setattr(self, '_text_color', col))

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_color, self._circle_color, self._active_color, \
            self._disabled_color, self._text_color = QColor("#0BF"), \
            QColor("#DDD"), QColor('#777'), QColor("#CCC"), QColor("#000")
        self._circle_pos, self._intermediate_bg_color = None, None
        self.setFixedHeight(22)
        self._animation_duration = 500  # milliseconds
        self.stateChanged.connect(self.start_transition)
        self._user_checked = False  # Introduced flag to check user-initiated changes

    circle_pos = Property(
        float, lambda self: self._circle_pos,
        lambda self, pos: (setattr(self, '_circle_pos', pos), self.update()))
    intermediate_bg_color = Property(
        QColor, lambda self: self._intermediate_bg_color,
        lambda self, col: setattr(self, '_intermediate_bg_color', col))

    def setDuration(self, duration: int):
        """
        Set the duration for the animation.
        :param duration: Duration in milliseconds.
        """
        self._animation_duration = duration

    def update_pos_color(self, checked=None):
        #self._circle_pos = self.height() * (1.1 if checked else 0.1)
        self._circle_pos = self.height() * (0.1 if checked else 1.1)
        if self.isChecked():
            self._intermediate_bg_color = self._active_color
        else:
            self._intermediate_bg_color = self._bg_color

    def start_transition(self, state):
        if not self._user_checked:  # Skip animation if change isn't user-initiated
            self.update_pos_color(state)
            return
        for anim in [self.create_animation, self.create_bg_color_animation]:
            animation = anim(state)
            animation.start()
        self._user_checked = False  # Reset the flag after animation starts

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            event.ignore()
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            event.ignore()
    
    def ManualShutDown(self):
        self.setChecked(True)
        self._user_checked = True
        self.start_transition(True)
    
    def ReOpen(self):
        self.setEnabled(True)
        self.setChecked(True)

    def mousePressEvent(self, event):
        self._user_checked = True  # Set flag when user manually clicks the toggle
        super().mousePressEvent(event)

    def create_animation(self, state):
        return self._create_common_animation(
            state, b'circle_pos', self.height() * 1.1, self.height() * 0.1)

    def create_bg_color_animation(self, state):
        return self._create_common_animation(
            state, b'intermediate_bg_color', self._bg_color, self._active_color)

    def _create_common_animation(self, state, prop, start_val, end_val):
        animation = QPropertyAnimation(self, prop, self)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.setDuration(self._animation_duration)
        animation.setStartValue(start_val if state else end_val)
        animation.setEndValue(end_val if state else start_val)
        return animation

    def showEvent(self, event):
        super().showEvent(event)  # Ensure to call the super class's implementation
        self.update_pos_color(self.isChecked())

    def resizeEvent(self, event):
        self.update_pos_color(self.isChecked())

    def sizeHint(self):
        size = super().sizeHint()
        text_width = QFontMetrics(
            self.font()).boundingRect(self.text()).width()
        size.setWidth(int(self.height() * 2 + text_width * 1.075))
        return size

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        circle_color = QColor(
            self.disabled_color if not self.isEnabled() else self.circle_color)
        bg_color = QColor(
            self.disabled_color if not self.isEnabled() else
            self.intermediate_bg_color)
        text_color = QColor(
            self.disabled_color if not self.isEnabled() else self.text_color)

        bordersradius = self.height() / 2
        togglewidth = self.height() * 2
        togglemargin = self.height() * 0.3
        circlesize = self.height() * 0.8

        bg_path = QPainterPath()
        bg_path.addRoundedRect(
            0, 0, togglewidth, self.height(), bordersradius, bordersradius)
        painter.fillPath(bg_path, QBrush(bg_color))

        circle = QPainterPath()
        circle.addEllipse(
            self.circle_pos, self.height() * 0.1, circlesize, circlesize)
        painter.fillPath(circle, QBrush(circle_color))

        painter.setPen(QPen(QColor(text_color)))
        painter.setFont(self.font())
        text_rect = QRect(int(togglewidth + togglemargin), 0, self.width() -
                          int(togglewidth + togglemargin), self.height())
        text_rect.adjust(
            0, (self.height() - painter.fontMetrics().height()) // 2, 0, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft |
                         Qt.AlignmentFlag.AlignVCenter, self.text())
        painter.end()


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()

    checkbox0 = QToggle()
    checkbox0.setFixedHeight(12)
    layout.addWidget(checkbox0)

    checkbox1 = QToggle()
    checkbox1.setText('Checkbox 1 - Disabled')
    checkbox1.setEnabled(False)
    layout.addWidget(checkbox1)

    checkbox2 = QToggle()
    checkbox2.setText('Checkbox 2 - Checked, custom height, animation duration, colors and font')
    checkbox2.setFixedHeight(24)
    checkbox2.setFont(QFont('Segoe Print', 10))
    checkbox2.setStyleSheet("QToggle{"
                            "qproperty-bg_color:#FAA;"
                            "qproperty-circle_color:#DDF;"
                            "qproperty-active_color:#AAF;"
                            "qproperty-disabled_color:#777;"
                            "qproperty-text_color:#A0F;}")
    checkbox2.setDuration(2000)
    checkbox2.setChecked(False)

    checkbox2.clicked.connect(lambda: checkbox1.ReOpen())
    layout.addWidget(checkbox2)

    window.setLayout(layout)
    window.show()
    app.exec()