import sys
import logging
from PyQt6.QtWidgets import QApplication
from .window import MainWindow

logging.basicConfig(filename='agent.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
# Initialize logging to capture debug information

def main():
    app = QApplication(sys.argv) # Create the application instance
    # app.setQuitOnLastWindowClosed(False)  # Prevent app from quitting when window is closed
    window = MainWindow() # Initialize the main window
    window.show()  # Just show normally, no maximize
    sys.exit(app.exec()) # Start the application event loop

if __name__ == "__main__":
    main()
