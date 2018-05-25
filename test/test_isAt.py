# encoding = utf8
import itchat
from itchat.content import *


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        outer = msg.Text
        print(outer.strip('D'))
        itchat.send(outer.strip('D'),msg['FromUserName'])


itchat.auto_login(hotReload=True)
itchat.run()