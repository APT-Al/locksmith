import sys
import os
from random import randint
from PyQt5 import QtWidgets 
from PyQt5 import uic

from FileExplorerUI import FileExplorer

class Decrpytor(QtWidgets.QMainWindow):
    def __init__(self,uipath):
        super(Decrpytor, self).__init__()
        uic.loadUi(uipath, self)

        # BUTTONS
        self.infoFileButton = self.findChild(QtWidgets.QPushButton, 'infoFileButton') # Find the button
        self.infoFileButton.clicked.connect(self.clickinfoFileButton) # Remember to pass the definition/method, not the return value!

        self.rsaFileButton = self.findChild(QtWidgets.QPushButton, 'rsaFileButton')
        self.rsaFileButton.clicked.connect(self.clickRSAFileButton)

        self.savemylifeButton = self.findChild(QtWidgets.QPushButton, 'savemylifeButton')
        self.savemylifeButton.clicked.connect(self.clickSavemylifeButton)
        self.savemylifeButton.setEnabled(True)

        # LABELS
        self.infoFileLocationLabel = self.findChild(QtWidgets.QLabel, "infoFileLocationLabel")
        self.flaginfo = False
        self.rsaFileLocationLabel = self.findChild(QtWidgets.QLabel, "rsaFileLocationLabel")
        self.flagrsa = False

        # PROGRESS BAR
        self.progressBar = self.findChild(QtWidgets.QProgressBar, "progressBar")
        #self.progressBar.setValue(randint(0,100))

        # LIST WIDGET
        self.decryptedFilesListWidget = self.findChild(QtWidgets.QListWidget,"decryptedFilesList")

        # SCROLL AREA
        self.scrollBar = self.findChild(QtWidgets.QScrollArea,"fileListScroolArea")

        self.show()

    def openFileExplorer(self):
        _selected_file = FileExplorer().initUI()
        return _selected_file

    def clickinfoFileButton(self):
        _selected_file = self.openFileExplorer()
        if _selected_file:
            self.infoFileLocationLabel.setText(_selected_file)
            self.flaginfo = True
        self.enableSavemylifeButton()
        
    def clickRSAFileButton(self):
        _selected_file = self.openFileExplorer()
        if _selected_file:
            self.rsaFileLocationLabel.setText(_selected_file)
            self.flagrsa = True
        self.enableSavemylifeButton()

    def enableSavemylifeButton(self):
        if self.flaginfo and self.flagrsa:
            self.savemylifeButton.setEnabled(True)

    def clickSavemylifeButton(self):
        for i in range(50):
            self.decryptedFilesListWidget.addItem(str(randint(0,100)))

def resourcePath(filename, folders = ""):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, folders, filename)

if __name__ == "__main__":
    GUI_path = resourcePath("mainScreen.ui")
    app = QtWidgets.QApplication(sys.argv)
    window = Decrpytor(GUI_path)
    app.exec_()