# -*- coding: utf-8 -*-

import time
import json

class MessageBody:
    __title         =   ""
    __type          =   1
    __line          =   ""
    __file          =   ""
    __time          =   0
    __message       =   ""
    __requestUrl    =   ""
    __requestBody   =   ""
    __customData    =   ""
    __userAgent     =   ""
    __clientIp      =   ""
    __requestId     =   ""

    def getTitle(self):
        return str(self.__title)

    def setTitle(self, title):
        self.__title    =   title

    def getType(self):
        return str(self.__type)

    def setType(self, _type):
        self.__type =   _type

    def getLine(self):
        return str(self.__line)

    def setLine(self, line):
        self.__line =   line

    def getFile(self):
        return str(self.__file)

    def setFile(self,file):
        self.__file =   file

    def getTime(self):
        myTime    =   self.__time
        if myTime <= 0 :
            myTime =    time.time()

        return str(myTime)

    def setTime(self, _time):
        self.__time =   _time

    def getMessage(self):
        return str(self.__message)

    def setMessage(self, message):
        self.__message  =   message

    def getRequestUrl(self):
        return str(self.__requestUrl)

    def setRequestUrl(self, requestUrl):
        self.__requestUrl   =   requestUrl

    def getRequestBody(self):
        return str(self.__requestBody)

    def setRequestBody(self, requestBody):
        self.__requestBody  =   requestBody

    def getCustomData(self):
        return str(self.__customData)

    def setCustomData(self, customData):
        self.__customData   =   customData

    def getUserAgent(self):
        return str(self.__userAgent)

    def setUserAgent(self, userAgent):
        self.__userAgent    =   userAgent

    def getClientIp(self):
        return str(self.__clientIp)

    def setClientIp(self,clientIp):
        self.__clientIp =   clientIp

    def getRequestId(self):
        return str(self.__requestId)

    def setRequestId(self,requestId):
        self.__requestId    =   requestId

    def toDict(self):
        return {
            'type'          :   self.getType(),
            'title'         :   self.getTitle(),
            'file'          :   self.getFile(),
            'line'          :   self.getLine(),
            'message'       :   self.getMessage(),
            'request_url'   :   self.getRequestUrl(),
            'request_body'  :   self.getRequestBody(),
            'time'          :   self.getTime(),
            'user_agent'    :   self.getUserAgent(),
            'client_ip'     :   self.getClientIp(),
            'request_id'    :   self.getRequestId(),
            'custom_data'   :   self.getCustomData()
        }

    def toSting(self):
        return  json.dumps(self.toDict())


