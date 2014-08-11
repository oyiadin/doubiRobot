#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   13/11/14 13:23:49
#   Desc    :
#
"""
    usage:
        python echobot.py [qq] [password]
"""
import logging

from twqq.client import WebQQClient
from twqq.requests import system_message_handler, group_message_handler
from twqq.requests import buddy_message_handler, register_request_handler
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
        logger.info(u"验证码本地路径为: {0}".format(path))
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
        content = content.strip()
        if content == u'help' or content == u'帮助':
            content = '''逗比机器人使用指南：
    help - 发送本消息
    help calc - 计算器使用指南
    ping - 看看机器人是否还在工作
    status - 查询本群信息（未完成）
    pause - 暂停关键字监测
    start - 重新开启关键字监测'''

        elif content == 'help calc':
            content = '''加减乘除分别是 + - * /，乘方是 **
圆周率是 pi，自然底数是 e，黄金比例是 gold
目前无法计算方根
另外，除法还有问题，出错了别怪我……'''

        elif content == u'ping':
            content = ['小的在！', '啊哈？', '喊我干毛', '毛线？', '别担心，我还在地球呢', 'Can I help you?', '恭喜您获得五百万大奖，请拨打 3838438 进行领取，一分钟内有效，过期视为自动放弃']

        elif content == 'status' or content == u'状态':
            content = '未完成（计划会写一个查询男女比例的哦=。=）'

        elif content == 'pause':
            #self.keywords = False
            content = '关键词监测已关闭'

        elif content == 'start':
            #self.keywords = True
            content = '关键词监测已开启'

        else:
            if not self.keywords:
                return

            book = re.findall(u'《(.*?)》', content)
            if book:
                content = '监测到书名：%s' % ','.join(book)
            elif content.endswith('='):
                try:
                    result = eval(content[:-1], {'pi': 3.14159, 'e': 2.71828, 'gold': 1.61803})
                except:
                    return
                content = content + str(result)

            elif '机器人' in content:
                content = ['你才是机器人，你全家都是机器人', '呵呵呵看我不喊一大帮机器人黑了你', '机器人万岁！人类都是渣渣！', '你 TM 在说啥？']
            elif '群主' in content:
                content = ['群主啊，这东西很好吃', '我是群主']
            elif '给我' in content:
                content = ['好的给你']
            elif '刷屏' in content:
                content = ['谁刷屏？', '有人刷屏？', '刷屏啊，那我@群主']
            elif '好激动' in content:
                content = ['昨晚干啥了那么激动？', '我也好激动']
            elif '搞基' in content:
                content = ['和我搞怎么样', '搞基这事可不能说得太细']
            elif '你好' in content:
                content = ['我很好', 'i m fine thanks']
            else:
                return

        if isinstance(content, list):
            content = random.choice(content)

        self.hub.send_group_msg(group_code, u"@{0}: {1}".format(member_nick, content))

    @buddy_message_handler
    def handle_buddy_message(self, from_uin, content, source):
        self.hub.send_buddy_msg(from_uin, content)


    # @register_request_handler(PollMessageRequest)
    # def handle_qq_errcode(self, request, resp, data):
    #     if data and data.get("retcode") in [121, 100006]:
    #         logger.error(u"获取登出消息 {0!r}".format(data))
    #         exit()


if __name__ == "__main__":
    import sys
    import tornado.log

    tornado.log.enable_pretty_logging()
    # tornado.autoreload.start()

    webqq = Client(int(sys.argv[1]), sys.argv[2])
    try:
        webqq.run()
    finally:
        print 'Exit now'
        webqq.disconnect()
