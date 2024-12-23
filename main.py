import sys
from PyQt5.QtWidgets import QApplication
from gui import ImageGeneratorApp

def main():
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
