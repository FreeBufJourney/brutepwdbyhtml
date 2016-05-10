import re
import traceback
from PyQt4 import QtCore
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import ConnectTimeoutError
from MyWidgets.formHelper import form_url


class AnalysisResponse():

     def __init__(self,valid_urls,weblogic_url_list,tomcat_url_list,invalid_urls,can_deocode_form_urls,cannot_decode_form_urls):
         self.valid_urls = valid_urls
         self.weblogic_url_list = weblogic_url_list
         self.tomcat_url_list = tomcat_url_list
         self.invalid_urls = invalid_urls
         self.can_decoded_forms = can_deocode_form_urls
         self.cannot_decode_form_urls = cannot_decode_form_urls

class QUrlIPAnalysisThread(QtCore.QThread):

    trigger = QtCore.pyqtSignal(AnalysisResponse)

    def __init__(self,urllist):
        super(QUrlIPAnalysisThread, self).__init__()
        self.urls_list = urllist

    def run(self):
        urlAnalysis = UrlAnalysis(self.urls_list)
        valid_urls,invalid_urls = urlAnalysis.get_Valid_Urls()
        #对具备可登录性的网站，进行form表单的分析
        can_decode_forms,cannot_decode_form_urls = self.analyze_form(valid_urls)
        ipanalysis = IpAnalysis(self.urls_list)
        weblogic_url_list,tomcat_url_list = ipanalysis.get_valid_ips()
        self.trigger.emit(AnalysisResponse(valid_urls,weblogic_url_list,tomcat_url_list,invalid_urls,can_decode_forms,cannot_decode_form_urls))

    def analyze_form(self,urls):
        cannot_decoded_forms = []
        cannot_decoded_form_urls = []
        for url in urls:
            try:
                form = form_url(url)
                cannot_decoded_forms.append(form)
            except:
                traceback.print_exc()
                cannot_decoded_form_urls.append(url)
        return cannot_decoded_forms,cannot_decoded_form_urls
class  UrlAnalysis():

    def __init__(self,all_url_list):
        self.url_list,self.ip_list = self.__get_divided_list(all_url_list)

    def get_Valid_Urls(self):
        valid_urls = []
        invalid_urls = []
        #get urls
        for url in self.url_list:
                if self.__validate_url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
        #get ips
        for ip in self.__standardUrl(self.ip_list):
            if self.__validate_url(ip):
                valid_urls.append(ip)
            else:
                invalid_urls.append(ip)
        return valid_urls,invalid_urls

    def get_valid_ips(self):
        ipanalysis = IpAnalysis(self.ip_list)

    def __standardUrl(self,url_list):
        standardized_urls = []
        all_ips = []
        for ip in url_list:
            if re.search('-',ip):
                ips = self.__get_all_ips_by_separator(ip)
                all_ips.extend(ips)
            elif re.search('/',ip):
                ips = self.__get_all_ips_by_slash(ip)
                all_ips.extend(ips)
            else:
                all_ips.append(ip)
        print(str(all_ips))
        for url in all_ips:
            if not url.startswith('http'):
                url = 'http://'+url
            standardized_urls.append(url)
        return standardized_urls

    def __get_all_ips_by_separator(self,ip):
        start,end =[self.__ip2num(x) for x in ip.split('-')]
        return  [self.__num2ip(num) for num in range(start,end+1) if num&0xff]

    def __get_all_ips_by_slash(self,ip):
        x = ip.split('/')
        addr = self.__ip2num(x[0])
        mask  = int(x[1])
        start = addr&(0xffffffff<<(32-mask))
        end = addr|(0xffffffff>>mask)
        return [self.__num2ip(num) for num in range(start,end+1) if num&0xff]

    def __ip2num(self,ip):
        ip = [int(x) for x in ip.split('.')]
        return ip[0]<<24 | ip[1]<<16 | ip[2]<<8 | ip[3]

    def __num2ip(self,num):
        return '%s.%s.%s.%s' % ( (num & 0xff000000)>>24,(num & 0x00ff0000)>>16,(num & 0x0000ff00)>>8,(num & 0x000000ff))

    def __get_divided_list(self,all_url_list):
        url_list = []
        ip_list = []
        for url in all_url_list:
            if url[0].isdigit():
                ip_list.append(url)
            else:
                url_list.append(url)
        return url_list,ip_list


    def __isIp(self,url):
        return url[0].isdigit

    def __validate_url(self,url):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"}
            response = requests.get(url,timeout=3,headers=headers)
        except:
            return False
        html_text = response.text
        html_soup = BeautifulSoup(html_text, "html.parser")
        #check is there form
        forms = html_soup.find('form')
        if not forms:
            return False
        else:
            return True

    def get_deep_url(url):
        url_list = ['ssignin','login.php','','signin']
        for suffix in url_list:
            url = url + '/' +suffix


class IpAnalysis():

    def __init__(self,all_url_list):
        self.ip_list,self.url_list = self.__get_ip_list(all_url_list)


    def __get_ip_list(self,all_url_list):
        iplist =  [url for url in all_url_list if url[0].isdigit()]
        all_ips = []
        for ip in iplist:
            if re.search('-',ip):
                ips = self.__get_all_ips_by_separator(ip)
                all_ips.extend(ips)
            elif re.search('/',ip):
                ips = self.__get_all_ips_by_slash(ip)
                all_ips.extend(ips)
            else:
                all_ips.append(ip)
        standard_all_ips =  ['http://'+url for url in all_ips if url[0].isdigit()]
        urllist = [urlparse(url).scheme+'://'+urlparse(url).netloc for url in all_url_list if not url[0].isdigit()]
        return standard_all_ips,urllist

    def __get_all_ips_by_separator(self,ip):
        start,end =[self.__ip2num(x) for x in ip.split('-')]
        return  [self.__num2ip(num) for num in range(start,end+1) if num&0xff]

    def __get_all_ips_by_slash(self,ip):
        x = ip.split('/')
        addr = self.__ip2num(x[0])
        mask  = int(x[1])
        start = addr&(0xffffffff<<(32-mask))
        end = addr|(0xffffffff>>mask)
        return [self.__num2ip(num) for num in range(start,end+1) if num&0xff]

    def __ip2num(self,ip):
        ip = [int(x) for x in ip.split('.')]
        return ip[0]<<24 | ip[1]<<16 | ip[2]<<8 | ip[3]

    def __num2ip(self,num):
        return '%s.%s.%s.%s' % ( (num & 0xff000000)>>24,(num & 0x00ff0000)>>16,(num & 0x0000ff00)>>8,(num & 0x000000ff))

    def get_valid_ips(self):
        weblogic_url_list = self.__get_weblogic_urls()
        tomcat_url_list = self.__get_tomcat_ips()
        return weblogic_url_list,tomcat_url_list

    def __get_weblogic_urls(self):
        weblogic_url = '/console/login/LoginForm.jsp'
        ip_list = []
        ip_set = set()
        all_list = self.ip_list+self.url_list
        for ip in all_list:
            #test port 80
            try:
                url = ip + weblogic_url
                response = requests.get(url,timeout=3)
                if response.status_code == 200:
                    # ip_list.append(url)
                    ip_set.add(url)
            except (ConnectTimeoutError,requests.exceptions.ConnectionError):
                pass
            #test port 8080
            try:
                url = ip+':8080'+weblogic_url
                response = requests.get(url,timeout=3)
                if response.status_code == 200:
                    # ip_list.append(url)
                    ip_set.add(url)
            except :
                pass
            #test port 7001
            try:
                url = ip+':7001'+weblogic_url
                response = requests.get(url,timeout=3)
                if response.status_code == 200:
                    # ip_list.append(url)
                    ip_set.add(url)
            except :
                pass
        ip_list = list(ip_set)
        return ip_list

    def __get_tomcat_ips(self):
        tomcat_manager_url = '/manager/html'
        ip_list = []
        ip_set = set()
        all_list = self.ip_list+self.url_list
        for ip in all_list:
            #test port 80
            try:
                url = ip+tomcat_manager_url
                response = requests.get(url,timeout=3)
                if response.status_code == 401:
                    # ip_lsit.append(url)
                    ip_set.add(url)
            except (ConnectTimeoutError ,requests.exceptions.ConnectionError):
                pass
            #test port 8080
            try:
                url = ip+':8080'+tomcat_manager_url
                response = requests.get(url,timeout=3)
                if response.status_code ==401:
                    # ip_lsit.append(url)
                    ip_set.add(url)
            except:
                pass
        ip_list = list(ip_set)
        return ip_list

    def __standardUrl(self,url_list):
        standardized_urls = []
        for url in url_list:
            if not url.startwith('http'):
                url = 'http://'+url
            standardized_urls.append(url)
        return standardized_urls

if __name__ == '__main__':
    url = 'http://www.towords.com/login.jsp'
    url2 = 'http://210.42.121.241/'
    url3 = 'http://open.freebuf.com/oversea/445.html'
    # myclass = UrlAnalysis([url,url2,url3])
    mylist = ['192.168.48.1','192.168.15,123','158.125.258.56','http://www.baidu.com']
    mylist2  = ['http://'+url for url in mylist if url[0].isdigit()]
    mylist3 = [urlparse(url).scheme+'://'+urlparse(url).netloc for url in mylist if not url[0].isdigit()]
    print(str(mylist2))
    print(mylist3)