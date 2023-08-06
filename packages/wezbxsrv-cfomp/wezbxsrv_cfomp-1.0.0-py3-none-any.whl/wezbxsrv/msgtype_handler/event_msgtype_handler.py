import time
from . import AbstractMsgtypeHandler

class EventMsgtypeHandler(AbstractMsgtypeHandler):
    def __init__(self, xml_tree, zbxapi) -> None:
        super().__init__(xml_tree, zbxapi)
        self.tousername = None
        self.fromusername = None
        self.createtime = None
        self.msgtype = None
        self.event = None
        self.eventkey = None
        self.taskid = None
        self.agentid = None

    def parse(self):
        self.tousername = self.xml_tree.find('ToUserName').text
        self.fromusername = self.xml_tree.find('FromUserName').text
        self.createtime = self.xml_tree.find('CreateTime').text
        self.msgtype = self.xml_tree.find('MsgType').text
        self.event = self.xml_tree.find('Event').text
        self.eventkey = self.xml_tree.find('EventKey').text
        self.taskid = self.xml_tree.find('TaskId').text
        self.agentid = self.xml_tree.find('AgentId').text

    def build_rsp(self, content):
        rsp = '<xml>' \
            '<ToUserName><![CDATA[{toUser}]]></ToUserName>' \
            '<FromUserName><![CDATA[{fromUser}]]></FromUserName>' \
            '<CreateTime>{createTime}</CreateTime>' \
            '<MsgType><![CDATA[text]]></MsgType>' \
            '<Content><![CDATA[{content}]]></Content>' \
            '</xml>'
        return rsp.format(toUser=self.fromusername, fromUser=self.tousername,
                          createTime=int(time.time()), content=content)

    def run(self):
        self.parse()
 
        zbx_eventid = self.taskid.split('_')[-1]
        if self.eventkey.lower() == 'ack':
            message = '用户{0}通过企业微信确认问题ID{1}'.format(
                self.fromusername, zbx_eventid)
            self.zbxapi.event.acknowledge(
                eventids=zbx_eventid, action='6', message=message)
            return self.build_rsp('确认问题成功')
        elif self.eventkey.lower() == 'close':
            message = '用户{0}通过企业微信关闭问题ID{1}'.format(
                self.fromusername, zbx_eventid)
            self.zbxapi.event.acknowledge(
                eventids=zbx_eventid, action='1', message=message)
            return self.build_rsp('关闭问题成功')

        return self.build_rsp('内部错误，无法找到{0}事件类型处理类'.format(self.eventkey))


# class AbstractZbxEventImpl:
#     def __init__(self, handler) -> None:
#         self.handler = handler

#     @staticmethod
#     def target_eventkey(cls):
#         pass

#     def do_run(self) -> str:
#         pass


# class AckZbxEventImpl(AbstractZbxEventImpl):

#     @staticmethod
#     def target_eventkey(cls):
#         return 'ack'

#     def do_run(self) -> str:
#         zbx_eventid = self.handler.taskid
#         message = '用户{0}通过企业微信确认问题ID{1}'.format(
#             self.handler.fromusername, zbx_eventid)
#         self.zbxapi.event.acknowledge(
#             eventids=zbx_eventid, action='6', message=message)
#         return '确认问题成功'


# class CloseZbxEventImpl(AbstractZbxEventImpl):

#     @staticmethod
#     def target_eventkey(cls):
#         return 'close'

#     def do_run(self) -> str:
#         zbx_eventid = self.handler.taskid
#         message = '用户{0}通过企业微信关闭问题ID{1}'.format(
#             self.handler.fromusername, zbx_eventid)
#         self.handler.zbxapi.event.acknowledge(
#             eventids=zbx_eventid, action='1', message=message)
#         return '关闭问题成功'