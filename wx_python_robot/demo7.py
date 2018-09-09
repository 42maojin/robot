import itchat
from itchat.content import *
import itchat
import json,re,pymysql
import requests

itchat.auto_login(hotReload = True)
#从图灵机器人API接入接口
def tuling(info):
    #appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    appkey = '1788f633656746d5b7c329d4cf52a7a5'
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
        itchat.send_msg('嘤嘤嘤，我是智障机器人Coder，\n很高兴认识你，回复关键字:\n\n 加群:加入创软俱乐部咨询群\n公众号:获取包含超多实用校园服务的创软公众号  \n\n 来吧！走进我们的代码世界~',
                        msg['RecommendInfo']['UserName'])

@itchat.msg_register(NOTE,isFriendChat=True,isGroupChat=True,isMpChat=True)
def wellcome(msg):
    item = get_group_id(u'测试群')
    chatroom = itchat.update_chatroom(item)
    # print(chatroom['MemberList'])
    if '加入了群聊' in msg['Content']:
        itchat.send("@"+chatroom['MemberList'][-1]['NickName']+"\n欢迎新同学！大家关于社团或是学校有什么问题都可以在群上直接问哦！我们会尽力解答的。\n进群都改下备注哦~\n“年级_专业_姓名”\n例如：17_软件技术_谢心如 \n如果想报名我们社团，可以关注创软公众号回复“加入”", item)
        # print(chatroom['MemberList'][-1]['NickName'])

@itchat.msg_register(TEXT, isGroupChat=True,)
def group_text_reply(msg):
    # 针对@你的人才回复，可以设置if msg['isAt']:
    #item = get_group_id(u'18创软咨询群')  # 根据自己的需求设置
    
    item1 = get_group_id(u'宿舍长群')
    #chatroom = itchat.update_chatroom(item)
    #chatroom1=itchat.update_chatroom(item1)
    if item1:
        if '宿舍号' in msg['Content']:
            itchat.send_msg('D1-717齐',item1)
    if msg['isAt']:
        itchat.send(u'%s' % tuling(msg['Text']), msg['FromUserName'])
    # if item:
    #     #print(chatroom['MemberCount'],type(chatroom['MemberCount']))
    #     #print(chatroom['MemberList'])
    #     db = pymysql.connect("localhost", "root", "root", "wx_data")
    #     cursor = db.cursor()
    #     sql_select = "select count from wx;"
    #     cursor.execute(sql_select)
    #     results = cursor.fetchall()
    #     for x in results:
    #         #print(x[0])
    #         if x[0] !=chatroom['MemberCount']:
    #             itchat.send("欢迎新同学！大家关于社团或是学校有什么问题都可以在群上直接问哦！我们会尽力解答的。\n进群都改下备注哦~\n“年级_专业_姓名”\n例如：17_软件技术_谢心如 \n如果想报名我们社团，可以关注创软公众号回复“加入”", item)
    #             try:
    #                 sql = "update wx set count='%d';"%(chatroom['MemberCount'])
    #                 cursor.execute(sql)
    #                 db.commit()
    #                 db.close()
    #                 print('ok')
    #             except:
    #         # 发生错误时回滚
    #                 db.rollback()
    # for friend in chatroom['MemberList']:
    #     friend = itchat.search_friends(userName=friend['UserName'])
    #     # 如果是演示目的，把下面的方法改为 print 即可
    #     print("ok")
    # if msg['ToUserName'] == item:
    #     itchat.send(u'%s' % tuling(msg['Text']), item)


@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'加群':
        # itchat.add_member_into_chatroom(get_group_id(u"测试群"), [{'UserName': msg['FromUserName']}])
        # itchat.send(str(itchat.search_friends(userName=msg['FromUserName'])['NickName']),toUserName='filehelper')
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

