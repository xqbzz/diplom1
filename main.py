import sys
import os
import platform
from PyQt5.QtWidgets import QApplication
from gui import ImageGeneratorApp

def setup_qt_plugin_path():
    """Настройка пути к Qt плагинам в зависимости от ОС"""
    current_os = platform.system()

    if current_os == "Windows":
        import PyQt5
        pyqt_path = os.path.dirname(PyQt5.__file__)  # ← исправлено здесь
        possible_plugin_paths = [
            os.path.join(pyqt_path, "Qt5", "plugins"),
            os.path.join(pyqt_path, "Qt", "plugins"),
        ]

        for path in possible_plugin_paths:
            dll_path = os.path.join(path, "platforms", "qwindows.dll")
            if os.path.exists(dll_path):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = path
                print(f"✅ Windows: путь к плагинам установлен → {path}")
                return

        print("❌ Windows: не найден файл qwindows.dll. Убедись, что PyQt5 установлен корректно.")
        sys.exit(1)
    else:
        print(f"✅ {current_os}: настройка Qt плагинов не требуется.")  # ← вывод текущей ОС

def main():
    setup_qt_plugin_path()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
