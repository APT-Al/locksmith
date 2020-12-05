import sys
from PyQt5 import QtWidgets 
from PyQt5 import uic

from FileExplorerUI import FileExplorer

class Decrpytor(QtWidgets.QMainWindow):
    def __init__(self,uipath):
        super(Decrpytor, self).__init__()
        uic.loadUi(uipath, self)

        self.infoFileButton = self.findChild(QtWidgets.QPushButton, 'infoFileButton') # Find the button
        self.infoFileButton.clicked.connect(self.clickinfoFileButton) # Remember to pass the definition/method, not the return value!

        self.rsaFileButton = self.findChild(QtWidgets.QPushButton, 'rsaFileButton')
        self.rsaFileButton.clicked.connect(self.clickRSAFileButton)

        self.infoFileLocationLabel = self.findChild(QtWidgets.QLabel, "infoFileLocationLabel")
        self.rsaFileLocationLabel = self.findChild(QtWidgets.QLabel, "rsaFileLocationLabel")

        self.show()

    def openFileExplorer(self):
        selected_file = FileExplorer().initUI()
        return selected_file

    def clickinfoFileButton(self):
        self.infoFileLocationLabel.setText(self.openFileExplorer())

    def clickRSAFileButton(self):
        self.rsaFileLocationLabel.setText(self.openFileExplorer())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Decrpytor("dialog.ui")
    app.exec_()