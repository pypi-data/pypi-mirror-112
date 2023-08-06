from sys import stdout
from time import sleep

def print(*w,t=None,end="\n",sep=" "):
    def replace(strname,*w):
        for x in w:
            strname=strname.replace(x[0],x[1])
        return strname
    str_all=""
    for x in w:
        if w.index(x)==len(w)-1:
            str_all+=str(x)
        else:
            str_all+=str(x)+sep
    str_all=replace(str_all,
                ("\\黑","\033[30m"),
                ("\\clear","\033[2J\033[00H"),
                ("\\under","\033[4m"),
                ("\\nounder","\033[24m"),
                ("\\anti","\033[7m"),
                ("\\noanti","\033[27m"),
                ("\\hide","\033[25l"),
                ("\\show","\033[25h"),
                ("\\红","\033[31m"),
                ("\\绿","\033[32m"),
                ("\\黄","\033[33m"),
                ("\\蓝","\033[34m"),
                ("\\紫","\033[35m"),
                ("\\青","\033[36m"),
                ("\\白","\033[37m" ),
                ("\\l红", "\033[91m"),
                ("\\l绿", "\033[92m"),
                ("\\l黄", "\033[93m"),
                ("\\l蓝", "\033[94m"),
                ("\\l紫", "\033[95m"),
                ("\\l青", "\033[96m"),
                ("\\l白", "\033[97m"),
                ("\\bl红","\033[101m"),
                ("\\bl绿","\033[102m"),
                ("\\bl黄","\033[103m"),
                ("\\bl蓝","\033[104m"),
                ("\\bl紫","\033[105m"),
                ("\\bl青","\033[106m"),
                ("\\bl白","\033[107m"),
                ("\\bl黑","\033[100m"),
                ("\\b红", "\033[41m"),
                ("\\b绿", "\033[42m"),
                ("\\b黄", "\033[43m"),
                ("\\b蓝", "\033[44m"),
                ("\\b紫", "\033[45m"),
                ("\\b青", "\033[46m"),
                ("\\b白", "\033[47m"),
                ("\\b黑", "\033[40m"),
                ("\\","\033[0m"),
                ("//","\\"),)
    if t==None:
        stdout.write(str_all)
        stdout.flush()
    else:
        for y in str_all:
            stdout.write(y)
            stdout.flush()
            sleep(t)
    stdout.write(end)

if __name__ == "__main__":
    from time import sleep
    print("\\l黄这个被重新定义过的print函数能干许多事情\n\n",t=0.05)
    print("\\l蓝1.字体变色\\",t=0.05)
    print("这个版本的字体变色被我化简到了随便都能背下来的程度",t=0.05)
    print("下面附上表格",t=0.05)
    for x in "红、白、绿、蓝、黄、青、紫".split("、"):
        for y in ":字本身,b:字背景,l:亮色,bl:背景亮色".split(","):
            z=y.split(":")
            print("“\\"+z[0]+x+"////"+z[0]+x+"\\”"+z[1]+"\\",end=" ")
            sleep(0.1)
        print("")
    print("////=取消所有变色还原成原来的")
    print("\n")
    print("\\l蓝2.字体变化\\",t=0.05)

    for x in "under:显示下划线,anti:反色（将背景颜色与字体颜色互换）".split(","):
        y=x.split(":")
        print("\\"+y[0]+y[0]+y[1]+"\\",end=" ")
        print("\\no"+y[0]+"no"+y[0]+"取消"+y[1]+"\\\n")
    print("\n")
    print("\\l蓝3.清屏\\",t=0.05)
    print("清屏代码：////clear",t=0.05)
    print("\\白有兴趣自己试这里就不体现了")
    print("\n")
    print("\\l蓝4.一些参数的含义\\",t=0.05)
    print("""(1)print("nice",t=0.1)
    t这个参数是用来逐字输出的
    t=0.1的意思就是每个字停留0.1秒
    默认为不逐字输出

    (2)print("nice",end="。")
    end这个参数的意思是“结尾”
    默认为“////n”(换行)
    print("nice",end="。")将会输出“nice。”
    若后面还有一个print如
    print("nice",end="!")
    print(".?")
    会输出“nice。.?”（不换行）

    (3)print("n","ce",sep="i")
    sep这个参数是用来控制,间的空格的
    print("n","ce",sep="i")将会输出“nice”
    sep默认为“\\b白 \\”(一个空格)
    这也就是为什么正常时
    print(1,2)将会输出“1 2”了而不是“12”
    """,t=0.03)
