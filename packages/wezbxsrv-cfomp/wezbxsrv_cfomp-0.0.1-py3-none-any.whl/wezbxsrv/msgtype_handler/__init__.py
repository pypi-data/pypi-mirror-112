# https://open.work.weixin.qq.com/api/doc/90000/90135/90237

import importlib
import xml.etree.cElementTree as ET
# from zabbix_api import ZabbixAPI

class AbstractMsgtypeHandler:
    def __init__(self, xml_tree:ET.Element, zbxapi) -> None:
        self.xml_tree = xml_tree
        self.zbxapi = zbxapi
        self.rspdata = None

    def parse(self):
        pass

    def run(self):
        pass

    @classmethod
    def get_handler(cls, xml_tree:ET.Element, zbxapi):
        msgtype = xml_tree.find("MsgType").text
        modulename = '{0}_msgtype_handler'.format(msgtype)
        module = importlib.import_module(f'wezbxsrv.msgtype_handler.{modulename}')
        # module = importlib.import_module('.', modulename)
        clsname = f'{msgtype.capitalize()}MsgtypeHandler'
        module_cls = getattr(module, clsname)
        return module_cls(xml_tree=xml_tree, zbxapi=zbxapi)



