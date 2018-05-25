# encoding = utf8
import itchat
import time
import xlrd
from itchat.content import *


def print_t(string):
    # 记录日志到文件
    time_s = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
    if show_log:
        f = open('wechat.log','a+')
        print('{0} {1}'.format(time_s, string), file = f)


def get_replay_by_id(index):
    nrows = table_p.nrows
    if (index != 0 and index <= nrows - 1):
        conf = table_p.row_values(index)
        if conf and conf[5] == 1:
            return '@%s@%s' % (conf[1], conf[2])
        else:
            return False


def get_replay_id_by_msg(msg):
    for i in range(0, len(key_words)):
        if msg.find(key_words[i]['word']) != -1:
            return key_words[i]['id']
    return 0


# 如果对方发的是文字，则我们给对方回复以下的东西
@itchat.msg_register([TEXT])
def text_reply(msg):
    index = 0
    try:
        index = int(msg.Text)
    except:
        print_t("输入类型不可转换为int型")
    reply_str = get_replay_by_id(index)
    if reply_str:
        return reply_str
    else:
        index = get_replay_id_by_msg(msg.Text)
        print_t('关键字索引为:' + str(index))
        reply_str = get_replay_by_id(index)
        if reply_str:
            return reply_str


# 处理群消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    if msg['isAt']:
        msg.Text = msg.Text..strip('@')
        index = 0
        try:
            index = int(msg.Text)
        except:
            print_t("输入类型不可转换为int型")
        reply_str = get_replay_by_id(index)
        if reply_str:
            return reply_str
        else:
            index = get_replay_id_by_msg(msg.Text)
            print_t('关键字索引为:' + str(index))
            reply_str = get_replay_by_id(index)
            if reply_str:
                return reply_str


if __name__ == '__main__':
    # 设置参数
    auto_reply = True
    # group_reply = False
    # group_replying = False
    show_log = True
    # 配置表
    workbook = xlrd.open_workbook(u'conf/reply.xls')
    table_p = workbook.sheet_by_name(u'personal')
    # 初始化关键字表
    key_words = []
    ncols = table_p.ncols
    conf_key_word = table_p.col_values(3)
    for i in range(1, len(conf_key_word)):
        tb = conf_key_word[i].split(',')
        for n in range(0, len(tb)):
            dic = {'word': tb[n], 'id': i}
            key_words.insert(0, dic)

itchat.auto_login(hotReload=True)
itchat.run()