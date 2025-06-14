from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 600) # Adjusted size for better usability
        self.setMinimumSize(400, 600)  # Increased minimum size for better usability
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # Remove window frame for a cleaner look
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Make the background translucent
        self.settings = QSettings('PC Agent', 'Preferences') # Use a more descriptive organization and application name
        self.dark_mode = self.settings.value('dark_mode', True, type=bool) # Default to dark mode
        self.set_ui()

    def set_ui(self):
        # Set up the UI components here

        central_widget = QWidget() # Create a central widget
        self.setCentralWidget(central_widget) # Set the central widget for the main window
        main_layout = QVBoxLayout() # Create a vertical layout for the main window
        main_layout.setContentsMargins(15, 15, 15, 15) # Set margins for the main layout
        central_widget.setLayout(main_layout) # Set the layout for the central widget


        title_bar = QWidget() # Create a title bar widget
        title_bar.setObjectName("title_bar") # Set an object name for styling
        title_bar_layout = QHBoxLayout() # Create a horizontal layout for the title bar
        title_bar_layout.setContentsMargins(10, 5, 10, 5) # Set margins for the title bar layout

        # Add PC Agent title with robot emoji
        title_label = QLabel("PC Agent 🤖")
        title_label.setObjectName("titleLabel")
        title_bar_layout.addWidget(title_label)


        body = QWidget() # Create a body widget
        body.setObjectName("body") # Set an object name for styling
        body_layout = QVBoxLayout() # Create a vertical layout for the body
        body_layout.setSpacing(0) # Set spacing for the body layout
        