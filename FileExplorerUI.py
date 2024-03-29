import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class FileExplorer(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"File Explorer", "","All Files (*)", options=options)
        if fileName:
            return fileName

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = FileExplorer()
#     print(ex.initUI())
#     sys.exit(app.exec_())