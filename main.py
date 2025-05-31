import sys
import os
import PyQt5

pyqt_path = os.path.dirname(PyQt5.__file__)
possible_plugin_paths = [
    os.path.join(pyqt_path, "Qt5", "plugins"),
    os.path.join(pyqt_path, "Qt", "plugins"),
]

plugin_path = None
for path in possible_plugin_paths:
    if os.path.exists(os.path.join(path, "platforms", "qwindows.dll")):
        plugin_path = path
        break

if plugin_path:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
    print(f"✅ Используем путь к плагинам: {plugin_path}")
else:
    print("❌ Плагин платформы не найден. Убедись, что файл qwindows.dll существует.")
    sys.exit(1)  # Завершаем работу, чтобы не запускать GUI без плагинов

from PyQt5.QtWidgets import QApplication
from gui import ImageGeneratorApp

sys.setrecursionlimit(5000)

def main():
    app = QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
