# -*- coding: utf-8 -*-

import json
import time
import uuid
import hashlib
import base64
from Crypto.Cipher import AES
import hmac
import requests
from Crypto.Util.Padding import pad

class MessageNotify:
    __instance      =   None
    __projectId     =   0
    __key           =   ""
    __notifyUrl     =   "https://open-api.51baocuo.com/message/notify"
    __messages      =   []

    def __init__(self, projectId, key):
        self.__key          =   key
        self.__projectId    =   projectId
        MessageNotify.__instance           =   self

    def __getProjectId(self):
        return self.__projectId

    def __getKey(self):
        return str(self.__key)

    def __getNotifyUrl(self):
        return str(self.__notifyUrl)

    @staticmethod
    def getInstance():
        return MessageNotify.__instance

    def addMessage(self, messageBody):
        self.__messages.append(messageBody.toDict())
        return self

    def push(self):
        messages    =   self.__messages
        if len(messages) <= 0 :
            return ''

        sendData    =   json.dumps(messages)
        self.__messages.clear()
        return self.__notify(sendData)

    def __md5(self, md5String):
        md5 = hashlib.md5()
        md5.update(md5String.encode('utf-8'))
        return  md5.hexdigest()

    def __getNonce(self):
        return self.__md5(str(uuid.uuid4()))

    def __getAesKey(self):
        companyKey  =   self.__getKey()
        maxLen      =   16
        if  len(companyKey) > 16:
            return companyKey[0:maxLen]
        else:
            return companyKey.rjust(maxLen, '0')

    def __aesEncrypt(self, text, key):
        aes         =   AES.new(key.encode('utf-8'), AES.MODE_ECB)
        pad_pkcs7   =   pad(text.encode('utf-8'), AES.block_size)
        encrypt_data =  aes.encrypt(pad_pkcs7)
        return str(base64.b64encode(encrypt_data), encoding='utf-8')

    def __buildSignStr(self, params):
        paramsList      =   sorted(params)
        connects    =   []
        for value in paramsList:
            connects.append(value + "=" + params[value])

        return '&'.join(connects)

    def __hmacSha256(self, data, key):
        signature   =   hmac.new(key.encode('utf-8'), data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        return signature

    def __notify(self, message):
        currUnixTime    =   int(time.time())
        nonce           =   self.__getNonce()
        headers         = {'Content-Type': 'application/json'}
        aesResult       =   self.__aesEncrypt(message, self.__getAesKey())

        if len(aesResult) <= 0:
            return ''

        params                  =   {
            'time'          :   str(currUnixTime),
            'nonce'         :   str(nonce),
            'project_id'    :   str(self.__getProjectId()),
            'messages'      :   aesResult
        }

        signStr                 =   self.__buildSignStr(params)

        params['sign']          =   self.__hmacSha256(signStr, self.__getKey())

        return self.__post(self.__getNotifyUrl(), json.dumps(params), 3, headers)

    def __post(self,url,data,timeout, headers):
        try:
            r   =   requests.post(url, data=data,headers=headers,timeout=timeout)
            return r.text
        except:
            return ''





