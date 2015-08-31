class ExportResults():

    def __init__(self):
        self.url_list = []
        self.result_list  = []

    def add(self,url,usrname,pwd):
        if url in self.url_list:
            index = self.url_list.index(url)
            result = self.result_list[index]
            result.append(usrname,pwd)
        else:
            self.url_list.append(url)
            result = Result(url)
            result.append(usrname,pwd)
            self.result_list.append(result)

    def toString(self):
        for result in self.result_list:
            url = result.url
            print(url)
            count = len(result.usr_name_list)
            for i in range(count):
                u = result.usr_name_list[i]
                p = result.pwd_list[i]
                print(u,p)

class Result():

    def __init__(self,url):
        self.url = url
        self.usr_name_list = []
        self.pwd_list = []

    def append(self,usrname,pwd):
        self.usr_name_list.append(usrname)
        self.pwd_list.append(pwd)
