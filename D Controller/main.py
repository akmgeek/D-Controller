from PyQt5.QtWidgets import QApplication
from dcontroller.window import mainWin


if __name__ == "__main__":
    import sys
    import qdarktheme
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarktheme.load_stylesheet("dark")) 
    MainWindow = mainWin()
    MainWindow.show()
    sys.exit(app.exec_())