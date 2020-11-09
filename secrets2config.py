# -*- coding: utf-8 -*-
# 用Secrets生成配置文件config.json

import json, os, re
from collections import OrderedDict

ADVCONFIG: str = os.environ.get('ADVCONFIG', None)

if ADVCONFIG:
    with open('./config/config.json','w',encoding='utf-8') as fp:
        fp.write(ADVCONFIG)


BILICONFIG: str = os.environ.get('BILICONFIG', None)
PUSH_MESSAGE: str = os.environ.get('PUSH_MESSAGE', None)

if BILICONFIG or PUSH_MESSAGE:

    with open('./config/config.json','r',encoding='utf-8') as fp:
        configData: dict = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', fp.read()), object_pairs_hook=OrderedDict)

    if BILICONFIG:
        SESSDATA, bili_jct, DedeUserID = False, False, False
        users = []
        cookieDatas = {}
        for x in BILICONFIG.split("\n"):
            if re.match("[a-z 0-9]{8}%2C[0-9]{10}%2C[a-z 0-9]{5}\*[a-z 0-9]{2}", x):
                cookieDatas["SESSDATA"] = x
                SESSDATA = True
            elif re.match("[a-z 0-9]{31}", x):
                cookieDatas["bili_jct"] = x
                bili_jct = True
            elif re.match("^[0-9]*$", x):
                cookieDatas["DedeUserID"] = x
                DedeUserID = True
            if SESSDATA and bili_jct and DedeUserID:
                users.append({"cookieDatas": cookieDatas.copy(), "tasks": {}})
                SESSDATA, bili_jct, DedeUserID = False, False, False
        configData["users"] = users

    elif not ADVCONFIG:
        print("secrets(BILICONFIG)和secrets(ADVCONFIG)至少填写一个")
        exit(-1)

    if PUSH_MESSAGE:
        for x in PUSH_MESSAGE.split("\n"):
            if x.startswith("SCU"):
                configData["SCKEY"] = x
            elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", x):
                configData["email"] = x

    with open('./config/config.json','w',encoding='utf-8') as fp:
        json.dump(configData, fp, ensure_ascii=False)

