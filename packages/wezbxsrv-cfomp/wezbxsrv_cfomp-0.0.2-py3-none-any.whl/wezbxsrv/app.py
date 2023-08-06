from flask import abort, request, render_template
import xml.etree.cElementTree as ET
from wework_callback.WXBizMsgCrypt3 import WXBizMsgCrypt, FormatException

from wezbxsrv.msgtype_handler import AbstractMsgtypeHandler

from wezbxsrv import create_flask_app, create_zbx_api

app = create_flask_app()
zapi = create_zbx_api(app)
wxcpt = WXBizMsgCrypt(
        app.config['WEWORK_TOKEN'], app.config['WEWORK_ENCODING_AES_KEY'], app.config['WEWORK_CORPID'])


@app.route('/', methods=['GET'])
def basic_get():
    '''
        *企业开启回调模式时，企业号会向验证url发送一个get请求 
        假设点击验证时，企业收到类似请求：
        * GET /cgi-bin/wxpush?msg_signature=5c45ff5e21c57e6ad56bac8758b79b1d9ac89fd3&timestamp=1409659589&nonce=263014780&echostr=P9nAzCzyDtyTWESHep1vC5X9xho%2FqYX3Zpb4yKa9SKld1DsH3Iyt3tP3zNdtp%2B4RPcs8TgAE7OaBO%2BFZXvnaqQ%3D%3D 
        * HTTP/1.1 Host: qy.weixin.qq.com

        接收到该请求时，企业应	1.解析出Get请求的参数，包括消息体签名(msg_signature)，时间戳(timestamp)，随机数字串(nonce)以及企业微信推送过来的随机加密字符串(echostr),
        这一步注意作URL解码。
        2.验证消息体签名的正确性 
        3. 解密出echostr原文，将原文当作Get请求的response，返回给企业微信
        第2，3步可以用企业微信提供的库函数VerifyURL来实现。
   '''

    # wxcpt = WXBizMsgCrypt(
    #     settings.WEWORK_TOKEN, settings.WEWORK_ENCODING_AES_KEY, settings.WEWORK_CORPID)

    ret, sEchoStr = wxcpt.VerifyURL(request.args['msg_signature'], request.args['timestamp'],
                                    request.args['nonce'], request.args['echostr'])

    if ret != 0:
        app.logger.error(f'VerifyURL ret: {ret}')
        abort(404)
    return sEchoStr


# @app.route('/hosts/', methods=['GET'])
# def host_get():
#     host = request.args['host']
#     res = zapi.host.get({'filter': {'host': host},
#                          'selectGroups': 'extend',
#                          'selectInterfaces': 'extend',
#                          'selectInventory': 'extend'})
#     return render_template('host.html', hosts=res)
    


@app.route('/', methods=['POST'])
def basic_post():
    '''
   用户回复消息或者点击事件响应时，企业会收到回调消息，此消息是经过企业微信加密之后的密文以post形式发送给企业，密文格式请参考官方文档
   假设企业收到企业微信的回调消息如下：
   POST /cgi-bin/wxpush? msg_signature=477715d11cdb4164915debcba66cb864d751f3e6&timestamp=1409659813&nonce=1372623149 HTTP/1.1
   Host: qy.weixin.qq.com
   Content-Length: 613
   <xml> <ToUserName><![CDATA[wx5823bf96d3bd56c7]]></ToUserName><Encrypt><![CDATA[RypEvHKD8QQKFhvQ6QleEB4J58tiPdvo+rtK1I9qca6aM/wvqnLSV5zEPeusUiX5L5X/0lWfrf0QADHHhGd3QczcdCUpj911L3vg3W/sYYvuJTs3TUUkSUXxaccAS0qhxchrRYt66wiSpGLYL42aM6A8dTT+6k4aSknmPj48kzJs8qLjvd4Xgpue06DOdnLxAUHzM6+kDZ+HMZfJYuR+LtwGc2hgf5gsijff0ekUNXZiqATP7PF5mZxZ3Izoun1s4zG4LUMnvw2r+KqCKIw+3IQH03v+BCA9nMELNqbSf6tiWSrXJB3LAVGUcallcrw8V2t9EL4EhzJWrQUax5wLVMNS0+rUPA3k22Ncx4XXZS9o0MBH27Bo6BpNelZpS+/uh9KsNlY6bHCmJU9p8g7m3fVKn28H3KDYA5Pl/T8Z1ptDAVe0lXdQ2YoyyH2uyPIGHBZZIs2pDBS8R07+qN+E7Q==]]></Encrypt>
   <AgentID><![CDATA[218]]></AgentID>
   </xml>

   企业收到post请求之后应该 1.解析出url上的参数，包括消息体签名(msg_signature)，时间戳(timestamp)以及随机数字串(nonce)
   2.验证消息体签名的正确性。 3.将post请求的数据进行xml解析，并将<Encrypt>标签的内容进行解密，解密出来的明文即是用户回复消息的明文，明文格式请参考官方文档
   第2，3步可以用企业微信提供的库函数DecryptMsg来实现。
   '''
    # wxcpt = WXBizMsgCrypt(
    #     settings.WEWORK_TOKEN, settings.WEWORK_ENCODING_AES_KEY, settings.WEWORK_CORPID)
    app.logger.debug('Callback request body: ' +
                     request.get_data().decode('utf-8'))

    ret, sMsg = wxcpt.DecryptMsg(request.get_data(
    ), request.args['msg_signature'], request.args['timestamp'], request.args['nonce'])
    if ret != 0:
        app.logger.error(f'DecryptMsg ret: {ret}')
        abort(400)
    app.logger.debug('DecryptMsg is ' + sMsg.decode('utf-8'))

    xml_tree = ET.fromstring(sMsg)

    if xml_tree.find("MsgType") == None:
        app.logger.error('Can not find MsgType element in xml')
        abort(400)
    msgtype = xml_tree.find("MsgType").text

    fromuser = xml_tree.find('FromUserName').text if xml_tree.find(
        'FromUserName') else None

    handler = AbstractMsgtypeHandler.get_handler(xml_tree, zapi)
    rspdata = handler.run()
    app.logger.debug(f'Rspdata is {rspdata}')

    ret, sEncryptMsg = wxcpt.EncryptMsg(
        rspdata, request.args['nonce'], request.args['timestamp'])
    if ret:
        app.logger.error(f'EncryptMsg ret: {ret}')
        abort(500)
    app.logger.debug(f'EncryptMsg is {sEncryptMsg}')

    return sEncryptMsg
