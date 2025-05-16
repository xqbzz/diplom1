import sys
sys.setrecursionlimit(5000)
from PyQt5.QtWidgets import QApplication
from gui import ImageGeneratorApp
import os
import PyQt5

# Получаем папку, где установлен PyQt5
pyqt_path = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(pyqt_path, "Qt5", "plugins")

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

def main():
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
