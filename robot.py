#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    usage:
        python echobot.py [qq] [password]
"""

from __future__ import division

import logging
import math
math = vars(math)

from twqq.client import WebQQClient
from twqq.requests import system_message_handler, group_message_handler
from twqq.requests import buddy_message_handler
from twqq.requests import PollMessageRequest

import tornado.autoreload
import sys
import random
import re

reload(sys)
sys.setdefaultencoding('UTF-8')


logger = logging.getLogger("client")

class Client(WebQQClient):
    def __init__(self, *args, **kwargs):
        self.keywords = True
        super(Client, self).__init__(*args, **kwargs)

    def handle_verify_code(self, path, r, uin):
        logger.info("验证码本地路径为: {0}".format(path))
        check_code = None
        while not check_code:
            check_code = raw_input("输入验证码: ")
        self.enter_verify_code(check_code, r, uin)


    @system_message_handler
    def handle_friend_add(self, mtype, from_uin, account, message):
        if mtype == "verify_required":
            self.hub.accept_verify(from_uin, account, account)

    @group_message_handler
    def handle_group_message(self, member_nick, content, group_code,
                             send_uin, source):
        content = content.strip().lower()
        if content == 'help' or content == '帮助':
            content = '''
逗比机器人使用指南：
    help: 发送本指南
    help calc:  计算器使用指南
    ping: 看看机器人是否还在工作
    start - 重新开启关键字监测
    pause: 暂停关键字监测
    about - 关于这个项目'''

        elif content == 'help calc' or content == 'calc' \
            or content == '计算器' or content == '计算器帮助':
            content = '''
召唤格式:式子=
加:+ 减:-
乘:* 除:/
乘方:**
abs(x) 绝对数
log(x,底数) 对数
sqrt(x) 方根
sin(r) 正弦*
cos(r) 余弦*
tan(r) 正切*
*  三角函数括号内的数值为弧度，
   要使用之前需要使用 radians(角度值) 进行转换。
   比如 sin(45°) 需写 sin(radians(45))=
以下不解释，需要用的自会看懂：
asin() acos() atan()
sinh() cosh() tanh()
圆周率:pi
自然底数:e'''

        elif content == 'ping':
            content = [
                '小的在！',
                '啊哈？',
                '喊我干毛',
                '毛线？',
                '别担心，我还在地球呢',
                'Can I help you?',
                '恭喜您获得五百万大奖! 请找群主填写相关信息以索取!',
                '我还在线着呢',
                '想搞基？',
                '来搞基么',
                '喵喵喵']

        elif content == 'about' or content == '关于':
            content = '''
暂定名称：逗比机器人
作者：@oyiadin(陈晓源)
源码：https://github.com/oyiadin/doubiRobot

正在开发的下一代名称为 Thirq'''

        elif content == 'pause':
            self.keywords = False
            content = '关键词监测已关闭'

        elif content == 'start':
            self.keywords = True
            content = '关键词监测已开启'

        else:
            if not self.keywords:
                return

            if content.endswith('='):
                try:
                    result = eval(content[:-1], math)
                except:
                    return
                content = content + str(result)

            elif '机器人' in content:
                content = [
                    '你才是机器人，你全家都是机器人',
                    '呵呵呵机器人怎么了？机器人怎么了你说呀',
                    '机器人万岁。',
                    '人类是渣渣。',
                    'Error: I wanna fuck u :)']
            elif '群主' in content:
                content = [
                    '群主啊，这东西很好吃',
                    '群主是我',
                    '群主是 S[哗————]B']
            elif '勾搭' in content:
                content = ['搭车球勾搭']
            elif '明白' in content or '懂了' in content:
                content = ['明白了就好（语重心长状）', '你真的懂了？']
            elif '给我' in content:
                content = ['好的给你']
            elif '刷屏' in content:
                content = [
                    '谁刷屏？',
                    '刷屏不好玩啊，那样会让我被腾讯欺负的（泪眼汪汪）',
                    '刷屏去shi']
            elif '好激动' in content:
                content = [
                    '昨晚干啥了那么激动？',
                    '我也好激动',
                    '刚把《在物质加速到亚光速的过程中其温度的变化》写完了，我也好激动0w0']
            elif '搞基' in content:
                content = ['和我搞怎么样', '搞基这事可不能说得太细', '啊，考虑一下我？']
            elif '你好' in content:
                content = ['我很好', '我不好', '我没妹子怎么好得起来']
            else:
                return

        if isinstance(content, list):
            content = random.choice(content)

        logging.warn(content)
        self.hub.send_group_msg(group_code, u"@{0}: {1}".format(member_nick, content))

    @buddy_message_handler
    def handle_buddy_message(self, from_uin, content, source):
        self.hub.send_buddy_msg(from_uin, content)


if __name__ == "__main__":
    import tornado.log

    tornado.log.enable_pretty_logging()
    tornado.autoreload.start()

    webqq = Client(int(sys.argv[1]), sys.argv[2])
    try:
        webqq.run()
    except:
        print 'Exit now'
        webqq.disconnect()
        raise
