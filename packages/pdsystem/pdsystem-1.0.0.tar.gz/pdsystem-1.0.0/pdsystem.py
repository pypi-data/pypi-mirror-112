from colorama import init
from time import sleep as dd
from sys import exit as n
def pdios():
    import platform
    print('判断系统中\n','-'*20)
    dd(1)
    if (platform.system()=='Windows'):
        print('欢迎Windows系统用户')
        init(autoreset=True)
    elif (platform.system()=='Linux'):
        print('欢迎Linux系统用户')
        init(autoreset=False)
    elif (platform.system()=='Unix'):
        print('欢迎Unix用户')
        init(autoreset=False)
    elif (platform.system()=='Darwin'):
        print('欢迎Max os用户,以下显示可能出现异常')
        init(autoreset=False)
    else:
        print('其他')
        print('无法判断系统,请更换设备重试,否则将回影响您的视觉感受并出现乱码情况')
        print('你现在可以选择1.退出\n2.我能忍受，开始\n3.输入其他字符退出')
        choose_exit=input('请选择')
        if choose_exit=='1':
            n('goodbye')
        elif choose_exit=='2':
            pass
        else:
            n('goodbye')