#coding=utf8
import os
import traceback

from PyQt4 import QtGui
from PyQt4.QtGui import QTableWidgetItem

from MyWidgets.SimulateHelper import MyLoginThread, QWebLogicThread, QTomcatThread
from MyWidgets.UrlHelper import UrlAnalysis, IpAnalysis, QUrlIPAnalysisThread
from MyWidgets.formHelper import form_url
from MyWidgets.exportHelper import ExportResults
from ui8 import Ui_MainWindow


class MyForm(Ui_MainWindow):

    def __init__(self):
        super(MyForm, self).__init__()
        self.valid_urls_list = []

        self.username_file = 'D:/username.txt'
        self.pwd_file = 'D:/pwdlist.txt'
        self.username_list = []
        self.pwd_list = []
        self.activedthreadleft = 0
        self.setupUi(MainWindow)
        self.can_decoded_forms = None
        self.weblogic_url_list = []
        self.tomcat_url_list = []

    def setupUi(self,MainWindow):
        super(MyForm, self).setupUi(MainWindow)
        self.tableWidget.setSortingEnabled(True)
        self.urlAnalysis.clicked.connect(lambda:self.get_url_list(self.urls.toPlainText()))

        self.usrnamefilebtn.clicked.connect(self.get_UserName_File_Dialog)
        self.pwdfilebtn.clicked.connect(self.get_pwd_file_dialog)

        self.websiteanalysisbtn.clicked.connect(self.start_analysis_login)
        self.export.clicked.connect(self.exportResult)

        self.initUI()

    def initUI(self):
        self.usernamefilepath_label.setText('用户名文件:'+self.username_file)
        self.pwdfilepath_label.setText('密码文件:'+self.pwd_file)

    def get_url_list2(self,urls):
        urls_list = urls.splitlines()
        urlAnalysis = UrlAnalysis(urls_list)
        valid_urls = urlAnalysis.get_Valid_Urls()
        for url in valid_urls:
            print(url)
        self.valid_urls_list = valid_urls
        self.urls.setPlainText('\n'.join(valid_urls))
        ipanalysis = IpAnalysis(urls_list)
        self.weblogic_url_list,self.tomcat_url_list = ipanalysis.get_valid_ips()
        self.urls.appendPlainText('\n'.join(self.weblogic_url_list))
        self.urls.appendPlainText('\n'.join(self.tomcat_url_list))
        self.url_analysis_process_label.setText('分析结束')

    def get_url_list(self,urls):
        self.url_analysis_process_label.setText('')
        urls_list = urls.splitlines()
        urls_list = [url.strip() for url in urls_list if url.strip()!='']
        self.analyasisUrlThread = QUrlIPAnalysisThread(urls_list)
        self.analyasisUrlThread.trigger.connect(self.updateAnalysis_result)
        self.analyasisUrlThread.start()

    def get_UserName_File_Dialog(self):
        name_file = QtGui.QFileDialog.getOpenFileName(None,'用户名文件','C:/')
        if name_file:
            self.username_file = name_file
            self.usernamefilepath_label.setText('用户名文件:'+self.username_file)

    def get_pwd_file_dialog(self):
        pwd_file = QtGui.QFileDialog.getOpenFileName(None,'密码文件','C:/')
        if pwd_file:
            self.pwd_file = pwd_file
            self.pwdfilepath_label.setText('密码文件:'+self.pwd_file)

    def start_analysis_login(self):
        #read the usernamefile and pwdfile
        if self.can_decoded_forms:
            self.__read_file()

        threads = []
        for form in self.can_decoded_forms:
            thread = self.__login_web(form)
            threads.append(thread)

        for ip in self.weblogic_url_list:
            thread = self.__login_weblogic(ip)
            threads.append(thread)

        for ip in self.tomcat_url_list:
            thread = self.__login_tomcat(ip)
            threads.append(thread)

        self.activedthreadleft = len(threads)
        for thread in threads:
            thread.start()

    def __read_file(self):
        usernames = []
        pwds = []
        try:
            with open(self.username_file) as file:
                try:
                    for line in file:
                        usernames.append(line.strip())
                except UnicodeDecodeError:
                    QtGui.QMessageBox.warning(None,'错误','读取密码弱口令文件错误')
                    return
        except:
            traceback.print_exc()
            QtGui.QMessageBox.warning(None,'错误','读取用户名弱口令文件错误')
            return

        try:
            with open(self.pwd_file) as file:
                try:
                    for line in file:
                        pwds.append(line.strip())
                except UnicodeDecodeError:
                    QtGui.QMessageBox.warning(None,'错误','读取密码弱口令文件错误')
                    return
        except:
            traceback.print_exc()
            QtGui.QMessageBox.warning(None,'错误','读取密码弱口令文件错误')
            return
        self.username_list = usernames
        self.pwd_list = pwds

    def __login_web(self,form):
        self.LoginThread = MyLoginThread(self.username_list,self.pwd_list,form)
        self.LoginThread.trigger.connect(self.updateTableWidget)
        self.LoginThread.finished.connect(self.threadleft)
        return self.LoginThread

    def __login_weblogic(self,url):
        self.loginweblogicThread = QWebLogicThread(url=url)
        self.loginweblogicThread.trigger.connect(self.updateTableWidget)
        self.loginweblogicThread.finished.connect(self.threadleft)
        self.loginweblogicThread.start()
        return self.loginweblogicThread

    def __login_tomcat(self,url):
        self.logintomcatThread = QTomcatThread(url=url)
        self.logintomcatThread.trigger.connect(self.updateTableWidget)
        self.logintomcatThread.finished.connect(self.threadleft)
        self.logintomcatThread.start()
        return self.logintomcatThread

    def updateAnalysis_result(self,AnalysisResponse):
        self.valid_urls_list = AnalysisResponse.valid_urls
        self.weblogic_url_list = AnalysisResponse.weblogic_url_list
        self.tomcat_url_list = AnalysisResponse.tomcat_url_list
        self.invalid_urls = AnalysisResponse.invalid_urls
        self.can_decoded_forms = AnalysisResponse.can_decoded_forms
        self.cannot_decode_form_urls = AnalysisResponse.cannot_decode_form_urls
        can_decode_form_urls = [form.url for form in self.can_decoded_forms]
        self.urls.setPlainText('\n'.join(can_decode_form_urls))
        self.urls.appendPlainText('\n'.join(self.weblogic_url_list))
        self.urls.appendPlainText('\n'.join(self.tomcat_url_list))
        if self.invalid_urls:
            self.urls.appendPlainText('\n--------------不能登录的URL-------------------')
            self.urls.appendPlainText('\n'.join(self.invalid_urls))
            self.urls.appendPlainText('-----------------------------------------------')
        if self.cannot_decode_form_urls:
            self.urls.appendPlainText('\n--------------无法解析出form表单的URL-------------------')
            self.urls.appendPlainText('\n'.join(self.cannot_decode_form_urls))
            self.urls.appendPlainText('-----------------------------------------------')
        self.url_analysis_process_label.setText('分析结束')

    def updateTableWidget(self,responseinfo):
        rowPostion = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPostion)
        self.tableWidget.setItem(rowPostion,0,QTableWidgetItem(responseinfo.username))
        self.tableWidget.setItem(rowPostion,1,QTableWidgetItem(responseinfo.password))
        self.tableWidget.setItem(rowPostion,2,QTableWidgetItem(responseinfo.url))

    def threadleft(self):
        self.activedthreadleft -= 1
        print(self.activedthreadleft)
        if self.activedthreadleft == 0:
            QtGui.QMessageBox.warning(None,'Messagebox','执行完毕')

    def exportResult2(self):
        current_path = os.getcwd()
        export_file = current_path+'\\'+'result.txt'
        f = open(export_file,'w')
        row_count = self.tableWidget.rowCount()
        for i in range(0,row_count):
            url = self.tableWidget.item(i,2).text()
            usrname = self.tableWidget.item(i,0).text()
            pwd = self.tableWidget.item(i,1).text()
            f.write(usrname+'       '+pwd+'     '+url+'\n')
        f.close()

    def exportResult(self):
        current_path = os.getcwd()
        export_file = current_path+'\\'+'result.txt'
        f = open(export_file,'w')
        row_count = self.tableWidget.rowCount()
        rs = ExportResults()
        for i in range(0,row_count):
            url = self.tableWidget.item(i,2).text()
            usrname = self.tableWidget.item(i,0).text()
            pwd = self.tableWidget.item(i,1).text()
            rs.add(url,usrname,pwd)
        f.close()
        rs.toString()
        print('执行完毕')

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = MyForm()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())



