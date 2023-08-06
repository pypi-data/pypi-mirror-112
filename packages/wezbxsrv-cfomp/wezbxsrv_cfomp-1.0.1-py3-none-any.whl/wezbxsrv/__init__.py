
import os
from flask import Flask
from zabbix_api import ZabbixAPI
from wework_callback.WXBizMsgCrypt3 import WXBizMsgCrypt

class DefaultConfig:
    WEWORK_TOKEN = os.environ.get('WEWORK_TOKEN')
    WEWORK_ENCODING_AES_KEY = os.environ.get('WEWORK_ENCODING_AES_KEY')
    WEWORK_CORPID = os.environ.get('WEWORK_CORPID')
    WEWORK_AGENTID = os.environ.get('WEWORK_AGENTID')
    WEWORK_SECRET =  os.environ.get('WEWORK_SECRET')

    ZABBIX_USERNAME = os.environ.get('ZABBIX_USERNAME')
    ZABBIX_PASSWORD = os.environ.get('ZABBIX_PASSWORD')
    ZABBIX_URL = os.environ.get('ZABBIX_URL')

def create_flask_app():
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)
    app.config.from_envvar("PROJECT_SETTING", silent=True)
    # app.config.from_envvar("PROJECT_SETTING")
    return app

# app = create_flask_app()

def create_zbx_api(app):
    zapi = ZabbixAPI(server=app.config['ZABBIX_URL'])
    zapi.login(user=app.config['ZABBIX_USERNAME'], password=app.config['ZABBIX_PASSWORD'])
    return zapi

# zapi = create_zbx_api()

# wxcpt = WXBizMsgCrypt(
#         app.config['WEWORK_TOKEN'], app.config['WEWORK_ENCODING_AES_KEY'], app.config['WEWORK_CORPID'])
