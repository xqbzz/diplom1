import sys
sys.setrecursionlimit(5000)
from PyQt5.QtWidgets import QApplication
from gui import ImageGeneratorApp
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\Сергей\AppData\Local\Programs\Python\Python313\Lib\site-packages\PyQt5\Qt5\plugins'

def main():
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
