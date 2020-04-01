import socket
import threading
import time


users = {}#用户字典，也可以连接数据库

def run(ck, ca):
    userName = ck.recv(1024)#接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
    users[userName.decode("utf-8")] = ck#解码并储存用户的信息
    print(users)
    printStr = "" + userName.decode("utf-8") + "连接\n"#在连接显示框中显示是否连接成功
    print(printStr)

    try:
        while True:
            time.sleep(1)
            rData = ck.recv(1024)  # 接受客户端发送的信息以1k作为单位这里接受到的信息为byte类型
            #print(rData)
            dataStr = rData.decode("utf-8")
            infolist = dataStr.split(":")  # 分割字符串从而得到所要发送的用户名和客户端所发送的信息
            users[infolist[0]].send((userName.decode("utf-8") + ": " +
                                     time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n      ' +
                                     infolist[1]).encode("utf"))
            # 要发送信息的客户端向目标客户端发送信息
    except Exception as e:
        print(str(e))

def start():
    ipStr = getIp()#从输入端中获取ip
    portStr = getport()#从输入端中获取端口，注意端口取得时候不能被占用（可以取8080，9876，等）
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6，和相关协议的
    server.bind((ipStr, int(portStr)))#绑定ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    #2:bind()的参数是一个元组的形式
    server.listen(10)#设置监听，和设置连接的最大的数量
    printStr = "服务器启动成功\n"#，是否连接成功
    print(printStr)
    try:
        while True:  # 这里用死循环是因为模拟的服务器要一直运行
            ck, ca = server.accept()  # 接受所连接的客户端的信息
            # 其中ca是ip和端口号组成的元组，ck有关客户端的信息

            t = threading.Thread(target=run, args=(ck, ca))  # 每连接一个客户端就开启一个线程
            # 其中Thread函数中的传入函数的参数也是以元组的形式
            t.start()  # 开启线程
    except Exception as e:
        print(str(e))


def startSever():
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程


def getIp():

    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return ip

def getport(prot=8080):
    return prot

if __name__ == '__main__':
    startSever()