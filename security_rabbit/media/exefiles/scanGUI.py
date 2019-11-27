#status code 
#200 request success
#403 Forbidden (CSRF token not set) 
#500 internal server error
import requests
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import os
import zipfile

class SecurityRabbitGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()
        self.client=None
        self.uploadURL = 'http://127.0.0.1:8000/uploadjson/'
        self.csrftoken=""

    def initGUI(self):
        self.scanType = "QuickScan"
        self.serverIps = ["127.0.0.1","127.0.0.1"]

        serverLabel = QtWidgets.QLabel('Server')
        directoryLabel = QtWidgets.QLabel('Directories')

        self.serverCombo = QtWidgets.QComboBox()
        self.serverCombo.addItem("Server1")
        self.serverCombo.addItem("Server2")
        self.directoryEdit = QtWidgets.QLineEdit()

        quickScan = QtWidgets.QRadioButton("QuickScan")
        quickScan.scanType = "QuickScan"
        quickScan.setChecked(True)
        quickScan.toggled.connect(self.onClicked)

        normalScan = QtWidgets.QRadioButton("NormalScan")
        normalScan.scanType = "NormalScan"
        normalScan.toggled.connect(self.onClicked)

        deepScan = QtWidgets.QRadioButton("DeepScan")
        deepScan.scanType = "DeepScan"
        deepScan.toggled.connect(self.onClicked)

        progressInfo = QtWidgets.QLabel("adding file to pendingfile...")
        progressBar = QtWidgets.QProgressBar()

        scanBtn = QtWidgets.QPushButton('Start Scan')
        scanBtn.clicked.connect(self.run)

        gridlayout = QtWidgets.QGridLayout()
        gridlayout.addWidget(serverLabel, 1, 0)
        gridlayout.addWidget(self.serverCombo, 1, 1)
        gridlayout.addWidget(directoryLabel, 2, 0)
        gridlayout.addWidget(self.directoryEdit, 2, 1)

        gridlayout.addWidget(quickScan, 3, 0)
        gridlayout.addWidget(normalScan, 3, 1)
        gridlayout.addWidget(deepScan, 3, 2)

        gridlayout.addWidget(progressInfo, 4, 0, 1, 3)
        gridlayout.addWidget(progressBar, 5, 0, 1, 2)
        gridlayout.addWidget(scanBtn, 5, 2)

        self.setLayout(gridlayout)
        self.setWindowTitle('SecurityRabbit')
        self.show()

    def run(self):
        scanType = self.scanType
        self.serverIps[self.serverCombo.currentIndex()]
        self.startSession()
        self.downloadfile('srcore')
        self.startScan()
        self.uploadfile('exeinfo.json')
        self.closeSession()
        self.removeFiles()

    def removeFiles(self):
        removeList = ["srcore.zip","__main__.exe","sigcheck64.exe","userdb_filter.txt"] #,"error.json","exeInfo.xlsx"]
        for removefile in removeList:
            try:
                os.remove(removefile)
            except:
                print("{} already removed".format(removefile))

    def startScan(self):
        self.process = QtCore.QProcess(self)
        zipfile_name = 'srcore.zip'
        z_file = zipfile.ZipFile(zipfile_name)
        zipfile.ZipFile.extract(z_file, '__main__.exe')
        zipfile.ZipFile.extract(z_file, 'sigcheck64.exe')
        zipfile.ZipFile.extract(z_file, 'userdb_filter.txt')

        scanDirectory = self.directoryEdit.text()
        args = [scanDirectory]
        self.process.execute('__main__.exe', args)
        
    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.scanType = radioButton.scanType
    
    def startSession(self):
        self.client = requests.session()
        self.client.get(self.uploadURL)
        self.csrftoken=self.client.cookies['csrftoken']
        #print(r.status_code)
        #print(self.csrftoken)
    
    def uploadfile(self, to_upload):
        with open(to_upload,'rb') as xmlfile:
            self.client.post(
                self.uploadURL,
                files={'docfile':xmlfile},
                data={'csrfmiddlewaretoken':self.csrftoken}
                )
            #print(r2.status_code)
            #print(r2.content)
    
    def downloadfile(self, download_filename):
        r = self.client.get('http://127.0.0.1:8000/downloadzip/'+ download_filename)
        pyfile = open(download_filename+".zip",'wb+')
        pyfile.write(r.content)
        pyfile.close()
    
    def closeSession(self):
        self.client.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    sr = SecurityRabbitGUI()
    app.exec_()
