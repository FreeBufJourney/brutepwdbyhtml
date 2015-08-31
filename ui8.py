# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '登录界面4.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.urls = QtGui.QPlainTextEdit(self.groupBox_3)
        self.urls.setObjectName(_fromUtf8("urls"))
        self.verticalLayout_5.addWidget(self.urls)
        self.urlAnalysis = QtGui.QPushButton(self.groupBox_3)
        self.urlAnalysis.setObjectName(_fromUtf8("urlAnalysis"))
        self.verticalLayout_5.addWidget(self.urlAnalysis)
        self.url_analysis_process_label = QtGui.QLabel(self.groupBox_3)
        self.url_analysis_process_label.setText(_fromUtf8(''))
        self.url_analysis_process_label.setObjectName(_fromUtf8('url_analysis_process_label'))
        self.verticalLayout_5.addWidget(self.url_analysis_process_label)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.usrnamefilebtn = QtGui.QPushButton(self.groupBox)
        self.usrnamefilebtn.setObjectName(_fromUtf8("usrnamefilebtn"))
        self.horizontalLayout.addWidget(self.usrnamefilebtn)
        self.pwdfilebtn = QtGui.QPushButton(self.groupBox)
        self.pwdfilebtn.setObjectName(_fromUtf8("pwdfilebtn"))
        self.horizontalLayout.addWidget(self.pwdfilebtn)
        self.websiteanalysisbtn = QtGui.QPushButton(self.groupBox)
        self.websiteanalysisbtn.setObjectName(_fromUtf8("websiteanalysisbtn"))
        self.horizontalLayout.addWidget(self.websiteanalysisbtn)
        self.export = QtGui.QPushButton(self.groupBox)
        self.export.setObjectName(_fromUtf8("export"))
        self.horizontalLayout.addWidget(self.export)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.usernamefilepath_label = QtGui.QLabel(self.centralwidget)
        self.usernamefilepath_label.setObjectName(_fromUtf8("usernamefilepath_label"))
        self.verticalLayout_4.addWidget(self.usernamefilepath_label)
        self.pwdfilepath_label = QtGui.QLabel(self.centralwidget)
        self.pwdfilepath_label.setObjectName(_fromUtf8("pwdfilepath_label"))
        self.verticalLayout_4.addWidget(self.pwdfilepath_label)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        #self.analysisResultTxtEdit = QtGui.QTextEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.analysisResultTxtEdit.sizePolicy().hasHeightForWidth())
        # self.analysisResultTxtEdit.setSizePolicy(sizePolicy)
        # self.analysisResultTxtEdit.setMinimumSize(QtCore.QSize(0, 50))
        # self.analysisResultTxtEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.analysisResultTxtEdit.setBaseSize(QtCore.QSize(0, 10))
        # self.analysisResultTxtEdit.setObjectName(_fromUtf8("analysisResultTxtEdit"))
        # self.verticalLayout_2.addWidget(self.analysisResultTxtEdit)
        self.tableWidget = QtGui.QTableWidget(self.groupBox_2)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "网址", None))
        self.urlAnalysis.setText(_translate("MainWindow", "网址分析", None))
        self.groupBox.setTitle(_translate("MainWindow", "操作", None))
        self.usrnamefilebtn.setText(_translate("MainWindow", "选取用户名文件", None))
        self.pwdfilebtn.setText(_translate("MainWindow", "选取密码文件", None))
        self.websiteanalysisbtn.setText(_translate("MainWindow", "开始分析", None))
        self.export.setText(_translate("MainWindow", "导出结果", None))
        self.usernamefilepath_label.setText(_translate("MainWindow", "用户名文件：", None))
        self.pwdfilepath_label.setText(_translate("MainWindow", "密码文件：", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "网页分析结果", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "用户名", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "密码", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "网址", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

