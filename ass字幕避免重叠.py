"""
最近在同步视频弹幕的时候发现，用Bilibili-Evolved导出的弹幕居然坐标重叠了!!
多么不可思议，于是就写了这样一个程序，把弹幕文件坐标去重啦！
就是顶部和底部固定的弹幕还没设计好去重，有大佬帮帮忙吗？
到时候把参考的弹幕文件发你帮忙改一下代码呗，嘻嘻
作者：萧垣
制作完成时间：2020.9.30
适用弹幕文件：格式为.ass且为Bilibili-Evolved导出（目前已知），不知道其他的适不适用
转载请联系作者：QQ2330153227
"""
def get_info():
    global filename, filepath, n
    is_dirct = input("文件是否处于同一目录下(y/n)：")
    is_dirct = is_dirct.lower()
    if is_dirct == "y":
        filepath = input("请输入文件名称：")
    
    elif is_dirct == "n":
        while True:
            filepath = input("请输入文件路径，用'/'作为路径分隔符：")
            if "/" not in filepath and ".ass" not in filepath:
                print("不符合输入规范，请重新输入")
                continue
            else:
                break

    else:
        print("不符合输入规范，请重新输入，y代表在同一目录下，n代表不在同一目录下")
        get_info()
    
    while True:
        n = input("请输入弹幕层数：")
        if n.isdigit():
            n = int(n)
            if n >= 1:
                break
            else:
                print("请输入大于等于一的整数")
                continue
        else:
            print("请输入大于等于一的整数")
            continue
    filename = filepath.split("/")[-1]


def get_connect(filepath):
    global connect
    with open(filepath, "r+", encoding="utf-8") as f:
        connect = f.readlines()
        c = []
        for s in connect:
            s = s.strip()
            c.append(s)
        connect = c
        

def process(connect, per=55):
    global subs
    subs = connect[:]
    where_event = subs.index("[Events]")
    floor_move = 1
    floor_pos = 1
    for i in range(where_event, len(subs)):
        connects = subs[i]
        if 'move' in connects:
            where_move = connects.find("move")
            before_move = connects[:where_move]
            move_pos_list = connects[where_move:].split(",")
            move_pos_list[1] = str(int(move_pos_list[1]) + per*(floor_move - 1))
            move_pos_list[3] = str(int(move_pos_list[3]) + per*(floor_move - 1))
            movement = ','.join(move_pos_list)
            connects_new = before_move + movement
            if floor_move % n == 0:
                floor_move = 0
            floor_move += 1
        
        elif 'pos' in connects:
            pass                # 暂时还没想好怎么改坐标，嘻嘻
        else:
            connects_new = connects
        subs[i] = connects_new
        print("已完成：{}/{}".format(i - where_event + 1, len(subs) - where_event))

def output(subs):
    with open("set_{}.ass".format(filename), 'w', encoding='utf-8') as f:
        for sub in subs:
            f.write(sub+'\n')

def main():
    get_info()
    get_connect(filepath)
    process(connect)
    output(subs)

try:
    main()
except Exception as error:
    import datetime
    import traceback
    traceback.print_exc(file=open('error.log', 'w'))
    print("""@_@，出错啦！请在当前目录下找到error.log文件
        联系邮箱2330153227@qq.com获取帮助""")
