import socket
import threading
from PyQt4 import QtCore
import select


class HttpHelper(QtCore.QThread):

    updated = QtCore.pyqtSignal(str)


__version__ = '0.1.0 Draft 1'
BUFLEN = 8192
VERSION = 'Python Proxy/'+__version__
HTTPVER = 'HTTP/1.1'

form_data = ''
class ConnectionHandler(threading.Thread):

    form_body = ''

    form_header = ''

    form_data = ''

    def __init__(self, connection, address, timeout,callback):
        super(ConnectionHandler, self).__init__()
        self.callback = callback
        self.form_body = ''
        self.form_data = ''
        self.client = connection
        self.client_buffer = ''
        self.client_buffer_byte = b''
        self.timeout = timeout


    def run(self):
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT','DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        self.target.close()

    def get_base_header(self):
        while 1:
            self.client_buffer_byte += self.client.recv(BUFLEN)
            self.client_buffer = self.client_buffer_byte.decode('utf-8',errors='ignore')
            end = self.client_buffer.find('\n')
            if end!=-1:
                break
        # self.callback(self.client_buffer)
        print(self.client_buffer)
        # print ('%s'%self.client_buffer[:end])
        data = (self.client_buffer[:end+1]).split()
        method,tmp1,tmp2 =data
        if method == 'POST':
            self.get_form_body()
        self.client_buffer = self.client_buffer[end+1:]
        return data

    def get_form_body(self):
        post_header = self.client_buffer
        self.callback(post_header)
        print("====wyj===")
        print(post_header)
        print("======wyj===")
        body_index = post_header.find('\r\n\r\n')
        body = post_header[body_index+4:]
        request_header = post_header[:body_index]
        self.form_data = post_header
        self.form_body = body
        self.form_header = request_header

    def method_CONNECT(self):
        self._connect_target(self.path)
        data = HTTPVER+' 200 Connection established\n'+'Proxy-agent: %s\n\n'%VERSION
        self.client.send(data.encode('utf-8'))
        self.client_buffer = ''
        self._read_write()

    def method_others(self):

        self.path = self.path[7:]
        i = self.path.find('/')
        host = self.path[:i]
        path = self.path[i:]
        self._connect_target(host)
        # self.target.send('%s %s %s\n'%(self.method, path, self.protocol)+self.client_buffer)
        self.target.send(self.client_buffer_byte)
        self.client_buffer = ''
        self._read_write()

    def _connect_target(self, host):
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
        self.target = socket.socket(soc_family)
        self.target.settimeout(self.timeout)
        self.target.connect(address)


    def _read_write(self):
        time_out_max = self.timeout/3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for in_ in recv:
                    data = in_.recv(BUFLEN)
                    if in_ is self.client:
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.send(data)
                        count = 0
            if count == time_out_max:
                break

class StartProxy(QtCore.QThread):

    updated = QtCore.pyqtSignal(str)

    def __init__(self):
        super(StartProxy, self).__init__()
        self.Thread = None

    def run(self):
        self.start_server()


    def start_server(self,host='127.0.0.1', port=8083, IPv6=False, timeout=60,handler=ConnectionHandler):
        if IPv6==True:
            soc_type=socket.AF_INET6
        else:
            soc_type=socket.AF_INET
        soc = socket.socket(soc_type)
        soc.bind((host, port))
        print ("Serving on %s:%d."%(host, port))
        soc.listen(5)
        while 1:
            connection, address = soc.accept()
            # my_thread = threading.Thread(target = handler,args = (connection, address,timeout))
            # self.Thread = ConnectionHandler
            # my_thread.setDaemon(True)
            my_thread = handler(connection,address,timeout,self.get_form_data)
            my_thread.setDaemon(True)
            my_thread.start()
            # self.updateUI()

    def get_form_data(self,data):
        # print('on get_form_data',data)
        self.updated.emit(str(data))

    def updateUI(self):
        self.updated.emit(str("UI changed"))
