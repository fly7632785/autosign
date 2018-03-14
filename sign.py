import gzip
import http.cookiejar
import threading
import urllib
import urllib.request
from urllib import parse
import datetime
# from  datetime import time
import time


# python自动签到脚本
# 1、每天早上固定时间签到（可设置固定时间）
# 2、每天晚上固定时间签离（可设置固定时间）
# 3、不设置就是用默认值
# 4、每天循环（定时器，每天执行（周一到周五））
# 5、可装在Android手机上一直保持运行
def getOpener(head):
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        print("未经压缩")
    return data


header = {
    'Connection': 'Keep-Alive',
    'Accept-Language': 'zh-CN',
    'Accept': ' */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://oa.witaction.com:808/oa/login.aspx',
    'Cookie': 'ASP.NET_SessionId=cwvee5uyqtkqhetocmctzdjr',
    'Host': 'ssos.witaction.com:808',
}

url = "http://ssos.witaction.com:808/ssos/ISsoLoginHandler.ashx"
signInUrl = 'http://oa.witaction.com:808/oa/OfficeIndexHandler.ashx?ProcessType=SignInOpt'
signOutUrl = 'http://oa.witaction.com:808/oa/OfficeIndexHandler.ashx?ProcessType=SignOutOpt'
get = {
    'systemId': 'OA',
    'loginType': '1',
    'userName': 'hanjf',
    'password': 'hanjf',
    'redirectUrl': '',
    'jsoncallback': 'myjson119'
}

opener = getOpener(header)


def login():
    postData = urllib.parse.urlencode(get).encode()
    op = opener.open(url, postData)
    data = op.read()
    data = ungzip(data)
    result = data.decode('utf-8')
    unencoded = parse.unquote(result)  # 解码字符串
    # print('登录成功')
    # print(unencoded)

    start = unencoded.index('http')
    end = unencoded.index('\'}}')

    homeurl = unencoded[int(start):int(end)]
    # print(homeurl)

    r = opener.open(homeurl).read()
    rr = ungzip(r).decode('utf-8')


def signIn():
    resultIn = opener.open(signInUrl).read()
    result = ungzip(resultIn).decode('utf-8')
    print(result)


def signOut():
    resultOut = opener.open(signOutUrl).read()
    result = ungzip(resultOut).decode('utf-8')
    print(result)


signInTime = str(input("输入设定的签到时间 默认08:50\n"))
signOutTime = str(input("输入设定的签离时间 默认18:05\n"))
if signInTime == '':
    signInTime = '08:50'
if signOutTime == '':
    signOutTime = '18:05'

print('设定签到时间:' + signInTime)
print('设定签离时间:' + signOutTime)

# 默认间隔一天
interval = 24 * 60 * 60
ONE_DAY = 24 * 60 * 60

thisyear = datetime.datetime.now().year
thismonth = datetime.datetime.now().month
thisday = datetime.datetime.now().day
# 今天的时间 年月日 拼接上 设定的时分 天数默认+1  后面会判断如果减去1天还 大于现在说明设定的时间在今天
nextExeSignInTime = str(thisyear) + '-' + str(thismonth) + '-' + str(thisday + 1) + ' ' + signInTime
# print(nextExeSignInTime)
nextExeSignOutTime = str(thisyear) + '-' + str(thismonth) + '-' + str(thisday + 1) + ' ' + signOutTime
# print(nextExeSignOutTime)
# 获取的是一个元组
signInTargettime = time.strptime(nextExeSignInTime, '%Y-%m-%d %H:%M')
signOutTargettime = time.strptime(nextExeSignOutTime, '%Y-%m-%d %H:%M')

# 判断如果减去1天还 大于现在说明设定的时间在今天
# 使用time.mktime生成时间戳
signInStamp = int(time.mktime(signInTargettime))
if signInStamp - ONE_DAY > time.time():
    signInStamp = signInStamp - ONE_DAY
signOutStamp = int(time.mktime(signOutTargettime))
if signOutStamp - ONE_DAY > time.time():
    signOutStamp = signOutStamp - ONE_DAY

signInTimeDelta = (signInStamp - int(time.time()))
signOutTimeDelta = (signOutStamp - int(time.time()))


def getTime(delta):
    hour = int(delta / (60 * 60))
    minute = int((delta - hour * 60 * 60) / 60)
    second = int(delta - hour * 60 * 60 - minute * 60)
    return str(hour) + '小时' + str(minute) + '分钟' + str(second) + '秒'


print('离下次' + time.strftime('%Y-%m-%d %H:%M', time.localtime(signInStamp)) +
      '签到还有:' + str(signInTimeDelta) + '秒(' + getTime(signInTimeDelta) + ')')

print('离下次' + time.strftime('%Y-%m-%d %H:%M', time.localtime(signOutStamp)) +
      '签离还有:' + str(signOutTimeDelta) + '秒(' + getTime(signOutTimeDelta) + ')')

# test
# signInTimeDelta = 10
# signOutTimeDelta = 10
# interval = 60


def fun_sign_in_timer():
    print(str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))) + ' 签到')  # 打印输出
    # 周末不签
    if datetime.datetime.now().isoweekday() != 6 and 7 != datetime.datetime.now().isoweekday():
        login()
        signIn()
    global signIntimer  # 定义变量
    signIntimer = threading.Timer(interval, fun_sign_in_timer)
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    signIntimer.start()  # 启用定时器


signIntimer = threading.Timer(signInTimeDelta, fun_sign_in_timer)  # 首次启动
signIntimer.start()


def fun_sign_out_timer():
    print(str(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))) + ' 签离')  # 打印输出
    # 周末不签
    if datetime.datetime.now().isoweekday() != 6 and 7 != datetime.datetime.now().isoweekday():
        login()
        signOut()
    global signOuttimer  # 定义变量
    signOuttimer = threading.Timer(interval, fun_sign_out_timer)
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    signOuttimer.start()  # 启用定时器


signOuttimer = threading.Timer(signOutTimeDelta, fun_sign_out_timer)  # 首次启动
signOuttimer.start()
