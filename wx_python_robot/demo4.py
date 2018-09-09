import itchat
from itchat.content import *
import json,re
import requests
itchat.auto_login(hotReload = True)
#从图灵机器人API接入接口
def tuling(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    # appkey = '1788f633656746d5b7c329d4cf52a7a5'
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(appkey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer

# 获得群聊id
def get_group_id(group_name):
    group_list = itchat.search_chatrooms(name=group_name)
    return group_list[0]['UserName']

# 自动通过加好友
add_friend_compile = re.compile(r'.*?')
@itchat.msg_register(itchat.content.FRIENDS)
def deal_with_friend(msg):
    if add_friend_compile.search(msg['Content']) is not None:
        itchat.add_friend(**msg['Text'])  # 自动将新好友的消息录入，不需要重载通讯录
        itchat.send_msg('嘤嘤嘤，我是智障机器人Coder，\n很高兴认识你，回复关键字:\n\n 加群，公众号 \n\n 走进我们的代码世界！',
                        msg['RecommendInfo']['UserName'])


@itchat.msg_register(TEXT, isGroupChat=True,)
def group_text_reply(msg):
    # 针对@你的人才回复，可以设置if msg['isAt']:
    item = get_group_id(u'测试群')  # 根据自己的需求设置
    if msg['ToUserName'] == item:
        itchat.send(u'%s' % tuling(msg['Text']), item)
    if msg['isAt']:
        itchat.send(u'%s'%tuling(msg['Text']),msg['FromUserName'])

@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'加群':
        # itchat.add_member_into_chatroom(get_group_id(u"测试群"), [{'UserName': msg['FromUserName']}])
        itchat.send(str(itchat.search_friends(userName=msg['FromUserName'])['NickName']),toUserName='filehelper')
        itchat.send_msg(str(itchat.search_friends(userName=msg['FromUserName'])['NickName']), toUserName='filehelper')
        itchat.send_msg('您的加群信息已收到\n稍后(我也不知道多久)将会拉您进群', msg['FromUserName'])
        itchat.send_image('timg.gif', msg['FromUserName'])
    elif text == u'公众号':
        itchat.send_msg('#!/usr/bin/python\n#coding:utf-8\n    def ISA():\n        print("慎言善思，学以致用")\nif __name__ == "__main__":\n    ISA()',msg['FromUserName'])
        itchat.send_msg('欢迎关注我们的公众号，\n“创软俱乐部ISA”',msg['FromUserName'])
        itchat.send_image('QR_ISA.jpg', msg['FromUserName'])
    else:
        itchat.send_msg(u'%s' % tuling(msg['Text']), msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    itchat.run()

