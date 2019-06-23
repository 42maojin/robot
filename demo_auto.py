from itchat.content import *
from apscheduler.schedulers.blocking import BlockingScheduler
import itchat,datetime
import json,re
import requests
import urllib.request
from lxml import etree
# itchat.auto_login(hotReload = True)
#从图灵机器人API接入接口
def tuling(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    #appkey = '1788f633656746d5b7c329d4cf52a7a5'
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
        itchat.send_msg('嘤嘤嘤，我是创智的微信机器人Coder，很高兴认识你，\n回复关键字:\n[报名]:加入我们\n[加群] : 加入创智俱乐部咨询群\n[公众号] : 获取包含超多实用校园服务的创智公众号  \n[简介] : 创智俱乐部相关介绍\n\n 来吧！走进我们的代码世界~',msg['RecommendInfo']['UserName'])


@itchat.msg_register(TEXT, isGroupChat=True,)
def group_text_reply(msg):
    # 针对@你的人才回复，可以设置if msg['isAt']:
    #item = get_group_id(u'18创软咨询群')  # 根据自己的需求设置
    
    item02 = get_group_id(u'宿舍长群')
    news_item = get_group_id(u'18创智修仙群')


    #chatroom = itchat.update_chatroom(item)
    #chatroom1=itchat.update_chatroom(item1)
    if item02:
        if '宿舍号+全齐' in msg['Content']:
            itchat.send_msg('D1-717齐',item02)
    if news_item:
        if '创智早报' in msg['Content']:
            the_news = []
            military_url = "http://www.myzaker.com/channel/3"
            technology_url = "http://www.myzaker.com/channel/13"
            zaker = [military_url, technology_url]
            for url in zaker:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=url, headers=headers)
                data = urllib.request.urlopen(req).read().decode('utf-8')
                html = etree.HTML(data)
                military = html.xpath('//*[@id="section"]/div[1]/div/h2/a/text()')[0]  # 军事新闻
                the_news.append(military)
                # print(military)

            movie = "https://www.cnbeta.com/category/movie.htm"
            music = "https://www.cnbeta.com/category/music.htm"
            game = "https://www.cnbeta.com/category/game.htm"
            comic = "https://www.cnbeta.com/category/comic.htm"
            funny = "https://www.cnbeta.com/category/funny.htm"
            news = [movie, music, game, comic, funny]
            for url in news:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=url, headers=headers)
                data = urllib.request.urlopen(req).read().decode('utf-8')
                html = etree.HTML(data).xpath('//*[@class="cnbeta-hot-big-figure"]/a/text()')[0]
                the_news.append(html)
                # print(html)

            thepaper = ["https://www.thepaper.cn/list_27234", "https://www.thepaper.cn/list_25429",
                        "https://www.thepaper.cn/list_25434"]
            for url in thepaper:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=url, headers=headers)
                data = urllib.request.urlopen(req).read().decode('utf-8')
                if len(re.findall(u'<h2>.*?<a href=".*?" id=".*?" target="_blank">(.*?)</a>.*?</h2>', data, re.S)) > 0:
                    d = re.findall(u'<h2>.*?<a href=".*?" id=".*?" target="_blank">(.*?)</a>.*?</h2>', data, re.S)[0]
                    the_news.append(d)
            with open('file.txt', 'w', encoding='utf-8') as f:
                for x in the_news:
                    f.write(x + "\n\n")
            with open('file.txt', 'r', encoding='utf-8') as file:
                a = file.read()
            print("成功+")
            itchat.send_msg("[ "+"创智早报"+" ]\n"+a, news_item)

    if msg['isAt']:
        itchat.send(u'%s'%tuling(msg['Text']), msg['FromUserName'])

@itchat.msg_register([TEXT])
def deal_with_msg(msg):
    text = msg['Content']
    if text == u'加群':
        # itchat.add_member_into_chatroom(get_group_id(u"测试群"), [{'UserName': msg['FromUserName']}])
        # itchat.send(str(itchat.search_friends(userName=msg['FromUserName'])['NickName']),toUserName='filehelper')
        itchat.send_msg(str(itchat.search_friends(userName=msg['FromUserName'])['NickName']), toUserName='filehelper')
        #itchat.send_msg('您的加群信息已收到\n稍后(我也不知道多久)将会拉您进群...', msg['FromUserName'])
        itchat.send_image('timg.gif', msg['FromUserName'])
    elif text == u'公众号':
        itchat.send_msg('#!/usr/bin/python\n#coding:utf-8\n    def ISA():\n        print("慎言善思，学以致用")\nif __name__ == "__main__":\n    ISA()',msg['FromUserName'])
        itchat.send_msg('欢迎关注我们的公众号，\n“创智俱乐部ISA”',msg['FromUserName'])
        itchat.send_image('QR_ISA.jpg', msg['FromUserName'])
    elif text==u'简介':
        itchat.send("创软俱乐部\n(现已更名为“创智俱乐部”)\n深信息第一科技社团\n\n成立时间：2009年\n\n成就：\n    1.社团成员斩获校内外，省国级各项技术奖项。\n    2.历届社员遍布腾讯等各类技术型企业，从事软件开发，产品经理等技术岗位亦有创业成功的师兄，年盈利已达到百万以上。\n    3.社团微信公众号，提供多项校园与学习服务，基本覆盖全校师生。\n\n创软俱乐部以其技术魅力、有力的组织，完善的培训课程以及杰出的成绩吸引了众多有志于 IT 业发展的学子加入其中，谱写属于自己的程序人生...",msg['FromUserName'])
    #elif text==u'报名':
    #    itchat.send("点击https://sxisa.com/join \n填写报名表就行啦~\n\np.s.我们只能线上报名才能参与面试哟，以防错过面试时间，赶紧报名吧！报名截止日期是9.25号23:59分！\n\n面试时间大概是月底哟~",msg['FromUserName'])

    else:
        itchat.send_msg(u'%s' % tuling(msg['Text']), msg['FromUserName'])
def ydgl():
    item03 = get_group_id(u'远大管理有限公司')
    # item03 = get_group_id(u'测试群')
    itchat.send(" 点餐链接：https://jinshuju.net/f/7xoEkX#__NO_LINK_PROXY__ 点餐时间 ： 上午截止10:20   下午截止 16:20 ",item03)
    # itchat.send("我想睡觉",item03)
def yui():
    user = itchat.search_friends(name=u'yui')
    username = user[0]['UserName']
    itchat.send("niho",toUserName=username)
if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, hotReload=True)

    sched = BlockingScheduler()
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    date_now =now_str+" 09:45:00"
    date_now1 =now_str+" 15:45:00"
    print("ok1")
    yui_time="2019-04-11 11:39:59"
    sched.add_job(ydgl, 'date', run_date=date_now)
    sched.add_job(ydgl, 'date', run_date=date_now1)
    # sched.add_job(yui,'date',run_date=yui_time)

    itchat.run()
    #sched.start()
    itchat.run()
