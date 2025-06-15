from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenu, QPushButton, QTextEdit, QProgressBar, QApplication
from PyQt6.QtCore import Qt, QSettings, QPoint
from PyQt6.QtGui import QAction
import qtawesome as qta

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

        central_widget = QWidget() # Create a central widget
        self.setCentralWidget(central_widget) # Set the central widget for the main window
        main_layout = QVBoxLayout() # Create a vertical layout for the main window
        main_layout.setContentsMargins(15, 15, 15, 15) # Set margins for the main layout
        central_widget.setLayout(main_layout) # Set the layout for the central widget

        self.ui_container = QWidget() # Create a container widget for all the UI elements
        self.ui_container.setObjectName("ui_container") # Set an object name for styling
        ui_container_layout = QVBoxLayout() # Create a vertical layout for the body
        ui_container_layout.setSpacing(0) # Set spacing for the body layout
        self.ui_container.setLayout(ui_container_layout) # Set the layout for the body widget

        main_layout.addWidget(self.ui_container) # Add the container widget to the main layout

# ------------------------Title Bar----------------------------------------------------------

        # Title bar with buttons and menu
        title_bar = QWidget() # Create a title bar widget
        title_bar.setObjectName("title_bar") # Set an object name for styling
        title_bar_layout = QHBoxLayout() # Create a horizontal layout for the title bar
        title_bar_layout.setContentsMargins(10, 5, 10, 5) # Set margins for the title bar layout
        title_bar.setLayout(title_bar_layout) # Set the layout for the title bar widget
        self.ui_container_layout.addWidget(title_bar) # Add the title bar to the ui_container layout

        # Add PC Agent title with robot emoji
        title_label = QLabel("PC Agent 🤖")
        title_label.setObjectName("titleLabel")
        title_bar_layout.addWidget(title_label)

        file_menu = QMenu("File") # Create a file menu
        new_task_action = QAction("New Task", self) # Create a new task action
        new_task_action.setShortcut("Ctrl+N") # Set a shortcut for the new task action
        edit_prompt_action = QAction("Edit System Prompt", self) # Create an edit prompt action
        edit_prompt_action.setShortcut("Ctrl+E") # Set a shortcut for the edit prompt action
        edit_prompt_action.triggered.connect(self.show_prompt_dialog) # Connect the edit prompt action to a method
        quit_action = QAction("Quit", self) # Create a quit action
        quit_action.setShortcut("Ctrl+Q") # Set a shortcut for the quit action
        quit_action.triggered.connect(self.quit_application) # Connect the quit action to a method
        file_menu.addAction(new_task_action) # Add the new task action to the file menu
        file_menu.addAction(edit_prompt_action) # Add the edit prompt action to the file menu
        file_menu.addSeparator() # Add a separator in the file menu
        file_menu.addAction(quit_action) # Add the quit action to the file menu

        file_button = QPushButton("File") # Create a file button
        file_button.setObjectName("menuButton") # Set an object name for styling
        file_button.clicked.connect(lambda: file_menu.exec(file_button.mapToGlobal(QPoint(0, file_button.height())))) # Connect the file button to show the file menu
        title_bar_layout.addWidget(file_button) # Add the file button to the title bar layout
        
        # Add spacer to push remaining items to the right
        title_bar_layout.addStretch()

        # Theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setObjectName("titleBarButton")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.update_theme_button()
        title_bar_layout.addWidget(self.theme_button)

        # Minimize and close buttons
        minimize_button = QPushButton("−")
        minimize_button.setObjectName("titleBarButton")
        minimize_button.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(minimize_button)

        close_button = QPushButton("×")
        close_button.setObjectName("titleBarButton")
        close_button.clicked.connect(self.close)
        title_bar_layout.addWidget(close_button)

# ------------------------Action Log------------------------------------------------------------

        # Action log with modern styling
        self.action_log = QTextEdit()
        self.action_log.setReadOnly(True)
        self.action_log.setStyleSheet("""
            QTextEdit {
                background-color: #262626;
                border: none;
                border-radius: 0;
                color: #ffffff;
                padding: 16px;
                font-family: Inter;
                font-size: 13px;
            }
        """)
        ui_container_layout.addWidget(self.action_log)


    def show_prompt_dialog(self):
        # dialog = SystemPromptDialog(self, self.prompt_manager)
        # dialog.exec()
        pass

    def quit_application(self):
        # Stop any running agent
        self.store.stop_run()
        
        # Clean up voice control
        if hasattr(self, 'voice_controller'):
            self.voice_controller.cleanup()
        
        # Save settings
        self.settings.sync()
        
        # Hide tray icon before quitting
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        # Actually quit the application
        QApplication.quit()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue('dark_mode', self.dark_mode)
        self.update_theme_button()
        self.apply_theme()

    def apply_theme(self):
        # Apply styles based on theme
        colors = {
            'bg': '#1a1a1a' if self.dark_mode else '#ffffff',
            'text': '#ffffff' if self.dark_mode else '#000000',
            'button_bg': '#333333' if self.dark_mode else '#f0f0f0',
            'button_text': '#ffffff' if self.dark_mode else '#000000',
            'button_hover': '#4CAF50' if self.dark_mode else '#e0e0e0',
            'border': '#333333' if self.dark_mode else '#e0e0e0'
        }

        # ui_container style
        ui_container_style = f"""
            QWidget#container {{
                background-color: {colors['bg']};
                border-radius: 12px;
                border: 1px solid {colors['border']};
            }}
        """
        self.ui_container.setStyleSheet(ui_container_style) # Set the style for the ui_container

        self.findChild(QLabel, "titleLabel").setStyleSheet(f"color: {colors['text']}; padding: 5px;") # Set the style for the title label

        # action_log style
        self.action_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: {colors['bg']};
                border: none;
                border-radius: 0;
                color: {colors['text']};
                padding: 16px;
                font-family: Inter;
                font-size: 13px;
            }}
        """)

        # Update input area
        self.input_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {colors['bg']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                color: {colors['text']};
                padding: 12px;
                font-family: Inter;
                font-size: 14px;
                selection-background-color: {colors['button_hover']};
            }}
            QTextEdit:focus {{
                border: 1px solid {colors['button_hover']};
            }}
        """)

        # Update progress bar
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {colors['bg']};
                height: 2px;
                margin: 0;
            }}
            QProgressBar::chunk {{
                background-color: {colors['button_hover']};
            }}
        """)


    def update_theme_button(self):
        if self.dark_mode:
            self.theme_button.setIcon(qta.icon('fa5s.sun', color='white'))
            self.theme_button.setToolTip("Switch to Light Mode")
        else:
            self.theme_button.setIcon(qta.icon('fa5s.moon', color='black'))
            self.theme_button.setToolTip("Switch to Dark Mode")