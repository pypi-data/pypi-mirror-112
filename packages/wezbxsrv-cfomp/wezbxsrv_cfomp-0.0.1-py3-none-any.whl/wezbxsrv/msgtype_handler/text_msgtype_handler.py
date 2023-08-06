import re
import time
from typing import overload
from unittest.main import main
import xml.etree.cElementTree as ET
from zabbix_api import ZabbixAPIException
from . import AbstractMsgtypeHandler

class AbstractImpl:
    def __init__(self, handler) -> None:
        self.handler = handler

    def do_run(self):
        return False, ''

class CommentZbxEvent(AbstractImpl):

    def do_run(self):
        match_obj = re.match(r'\s*ack\s+(\d+)\s+(.+)',  self.handler.content, re.I)
        if match_obj:
            eventid = match_obj.group(1)
            comment = match_obj.group(2)
            # self.fromusername
            message = f'{self.handler.fromusername}通过企业微信评论：{comment}'
            try:
                res = self.handler.zbxapi.event.acknowledge(
                    {'eventids': eventid, 'action': 6, 'message': message})
            except ZabbixAPIException as e:
                return True, f'评论失败，{str(e)}'
            return True, '评论成功！'
        
        return super().do_run()


class GetHostInfo(AbstractImpl):
    def do_run(self):
        match_obj = re.match(r'\s*info\s+(.+)', self.handler.content, re.I)
        if match_obj:
            host = match_obj.group(1)
            param = {
                'filter': {
                    'host': [host]
                },
                'selectInventory': ['type', 'type_full', 'alias', 'os', 'os_full', 'os_short', 
                    'serialno_a', 'serialno_b', 'tag', 'macaddress_a', 'macaddress_b', 'location', 
                    'chassis', 'model', 'vendor', 'poc_1_name', 'poc_2_name'],
                # 'selectInventory': 'extend',
                'selectInterfaces': ['type', 'ip', 'port'],
                'selectGroups': ['name'],
                'output': ['hostid', 'host', 'name', ]
            }
            try:
                res = self.handler.zbxapi.host.get(param)
            except ZabbixAPIException as e:
                return True, '查询失败：{0}'.format(str(e))

            return True, '查询结果：{0}'.format(str(res))
        return super().do_run()


class TextMsgtypeHandler(AbstractMsgtypeHandler):

    # ACK_RE = re.compile(r'\s*ack\s+(\d+)\s+(.+)', re.I)
    # INFO_RE = re.compile(r'\s*info\s+(.+)', re.I)

    def __init__(self, xml_tree: ET.Element, zbxapi) -> None:
        self.tousername = None
        self.fromusername = None
        self.createtime = None
        self.msgtype = None
        self.content = None
        self.msgid = None
        self.agentid = None
        super().__init__(xml_tree, zbxapi)

    def parse(self):
        self.tousername = self.xml_tree.find('ToUserName').text
        self.fromusername = self.xml_tree.find('FromUserName').text
        self.createtime = self.xml_tree.find('CreateTime').text
        self.msgtype = self.xml_tree.find('MsgType').text
        self.content = self.xml_tree.find('Content').text
        self.msgid = self.xml_tree.find('MsgId').text
        self.agentid = self.xml_tree.find('AgentID').text

        # if self.tousername != settings.WEWORK_CORPID or self.agentid !=

    def build_rsp(self, content):
        rsp = '<xml>' \
            '<ToUserName><![CDATA[{toUser}]]></ToUserName>' \
            '<FromUserName><![CDATA[{fromUser}]]></FromUserName>' \
            '<CreateTime>{createTime}</CreateTime>' \
            '<MsgType><![CDATA[text]]></MsgType>' \
            '<Content><![CDATA[{content}]]></Content>' \
            '</xml>'
        return rsp.format(toUser=self.fromusername, fromUser=self.tousername, createTime=int(time.time()), content=content)

    def run(self):
        self.parse()
        if self.content.strip().lower() == 'help':
            content =  '''以下为帮助信息：
1，发送“ack+空格+故障ID+空格+回复内容”可确认问题并发送消息给所有跟故障有关的人员, 例: ack 3773316 请XXX立即处理该问题；
2，发送“info+空格+主机名”可获取主机的硬件信息(主机名可在Zabbix中查询)，例：info 网站中间件；
3，发送help获取帮助信息。'''

            return self.build_rsp(content)
        else:
            isdone = False
            for cls in AbstractImpl.__subclasses__():
                impl = cls(self)
                isdone, content = impl.do_run()
                if isdone == True:
                    return self.build_rsp(content)
            
            content = '发送消息格式错误，请发送help获取帮助信息！'
            return self.build_rsp(content)
                    

            

