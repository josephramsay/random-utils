'''
UI for alpha merge
Created on 19/06/2020
@author: jramsay

Script to convert RGBA to RGB preserving alpha transparency by allocating nodata to 0 or 255
if the full black/white colours are unoccupied. If not a single colour gradient shift is used 
to clear the upper 255x3 colour for nodata

usage: python alphaMerge [-h|--help] src <source path> [dst <destination path>]
-h/--help : Print out this help message
src <source path> : The path to the source imagery
dst <destination path> : The path where converted imagery is written (same as src if omitted, with _ prefix)

'''
import sys
import os
from alphaMerge import Control 

from PyQt5.QtWidgets import QDialog,QWidget,QMessageBox,QApplication,QGridLayout,QGroupBox,QFileSystemModel,QTreeView,QPushButton,QLabel

home_directory = os.path.expanduser('~')

class PathPicker(QDialog):

    def __init__(self, parent=None):
        super(PathPicker, self).__init__(parent)
        self.resize(700, 600)
        
        infoLabel = QLabel("Select and run alpha processing")

        self.inSelection = None
        self.outSelection = None

        self.model = {'in':QFileSystemModel(),'out':QFileSystemModel()}
        self.model['in'].setRootPath(home_directory)
        self.model['out'].setRootPath(home_directory)

        self.createInPathGB()
        self.createOutPathGB()
        self.createPathOK()
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(infoLabel,  0, 0)
        mainLayout.addWidget(self.pathInGB, 1, 0)
        mainLayout.addWidget(self.pathOutGB, 2, 0)
        mainLayout.addWidget(self.pathOK, 3, 0)
        self.setLayout(mainLayout)
 
    def createInPathGB(self):
        self.pathInGB = QGroupBox("Input Path Selection")

        #self.inpath.model = QDirModel()
        view = QTreeView()
        view.setModel(self.model['in'])
        view.setRootIndex(self.model['in'].index(home_directory))
        view.clicked.connect(self.onInTreeClick)

        layout = QGridLayout()
        layout.addWidget(view, 0, 0)

        self.pathInGB.setLayout(layout)    
        
    def createOutPathGB(self):
        self.pathOutGB = QGroupBox("Output Path Selection")

        view = QTreeView()
        view.setModel(self.model['out'])
        view.setRootIndex(self.model['out'].index(home_directory))
        view.clicked.connect(self.onOutTreeClick)

        layout = QGridLayout()
        layout.addWidget(view, 0, 0)

        self.pathOutGB.setLayout(layout)

    def createPathOK(self):
        self.pathOK = QGroupBox()

        okPushButton = QPushButton("OK")
        okPushButton.setDefault(True)

        cancelPushButton = QPushButton("Cancel")
        #cancelPushButton.setFlat(True)
        cancelPushButton.setDefault(True)

        cancelPushButton.clicked.connect(self.onCancelClick)
        okPushButton.clicked.connect(self.onOkClick)

        layout = QGridLayout()
        layout.addWidget(okPushButton,0,0)
        layout.addWidget(cancelPushButton,0,1)
        self.pathOK.setLayout(layout)

    def onCancelClick(self):
        self.close()#sys.exit(1)
        
    def onOkClick(self,index):
        if self.inSelection:
            c = Control()
            c.process(self.inSelection,self.outSelection)
        else:
            alert = QMessageBox()
            alert.setWindowTitle('Nothing Selected')
            alert.setIcon(QMessageBox.Warning)
            alert.setText('No Input directory selected')
            alert.exec_()

    def onOutTreeClick(self,index):
        self.outSelection = self.model['out'].filePath(index)

    def onInTreeClick(self,index):
        self.inSelection = self.model['in'].filePath(index)


if __name__ == '__main__':
    app = QApplication([])
    pp = PathPicker()
    pp.show() 
    sys.exit(app.exec_())