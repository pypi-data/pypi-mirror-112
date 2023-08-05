
# -*- codeing = utf-8 -*-
# @File：hhUrl.py
# @Ver：1.1.0
# @Author：立树
# @Time：2021/07/04 05:23
# @IDE：PyCharm

"""
更新：
- 优化 hhDownload 新增了 headers 参数
"""

import re
import urllib.request,urllib.error,urllib.parse
from .hhOs import hhCreateFile

# 下载文件
def hhDownload(url="",savefile="",headers={}):
    # 参数判断
    if url == "":
        print("hhframe.hhUrl.hhDownload() Error - 请补全参数（url）")
        return {"state":False,"msg":"参数错误"}

    # 保存的文件
    if savefile=="":
        url2 = re.sub("http[s]?://","",url)
        if url2.find("/")>-1 and url2[-1]!="/":
            savefile = url2[url2.rfind("/")+1:len(url2)]
        else:
            savefile = "tempfile"

    # 请求数据
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"}
    header.update(headers)
    request = urllib.request.Request(
        url = urllib.request.quote(url,safe=";/?:@&=+$,",encoding="utf-8"),
        method = "GET",
        headers = header
    )
    # 返回数据
    hhRet = {
        "state": None,
        "url": url,
        "savefile": savefile,
        "code": -1,
        "msg": ""
    }
    # 发起请求
    try:
        response = urllib.request.urlopen(request,timeout=60)
        hhCreateFile(savefile,"wb",response.read())
        hhRet["state"] = True
        hhRet["code"] = 200
        hhRet["msg"] = "下载成功"
    except (urllib.error.URLError,IOError) as err:
        hhRet["state"] = False
        if hasattr(err,"code"):
            hhRet["code"] = err.code
        if hasattr(err,"reason"):
            hhRet["msg"] = err.reason
    finally:
        print(" hhframe.hhUrl.hhDownload() ".center(100,"="))
        print("url".ljust(10),hhRet["url"])
        print("savefile".ljust(10),hhRet["savefile"])
        print("result".ljust(10),hhRet["code"],hhRet["msg"])
        print("="*100)
        return hhRet

# url 解析
def hhParse(url=""):
    # 解析结果
    hhRet = {
        "url": url,
        "domain": "",
        "host": "",
        "ip": "",
        "protocol": "",
        "path": "",
        "file": "",
        "filename": "",
        "ext": "",
        "query": "",
        "hash": ""
    }
    # 参数判断
    if url == "":
        return hhRet
    # 协议
    if url.find("://"):
        protocal = url[0:url.find("://")+3]
        hhRet["protocol"] = protocal
        url = url.replace(protocal, "")
    # 主机
    ret = re.findall("^(([a-z\d]([a-z\d-]{0,57}[a-z\d])?.)+(com|net|cn|org|me|xyz|top|tech|gov|edu|ink|int|pub|mil|biz|info|mobi|name|tv))",url)
    host = ret[0][0] if len(ret) else ""
    hhRet["host"] = host
    url = url.replace(host, "")
    # IP
    ret = re.findall("^(((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3})",url)
    ip = ret[0][0] if len(ret) else ""
    hhRet["ip"] = ip
    url = url.replace(ip, "")
    # 端口
    ret = re.findall("^:(\d+)",url)
    port = ret[0] if len(ret) else ""
    hhRet["port"] = port
    url = url.replace(f":{port}", "")
    # 域名
    hhRet["host"] = hhRet["ip"] if not hhRet["host"] else hhRet["host"]
    hhRet["domain"] = hhRet["protocol"]+hhRet["host"]+(f":{hhRet['port']}" if hhRet["port"] else "")
    # 锚点
    if url.find("#") > -1:
        hash = url[url.find("#"):len(url)]
        hhRet["hash"] = hash.replace("#", "")
        url = url.replace(hash, "")
    # 查询字符串
    if url.find("?") > -1:
        query = url[url.find("?"):len(url)]
        hhRet["query"] = query.replace("?", "")
        url = url.replace(query, "")
    # 文件
    if url.find(".")>-1:
        file = url[url.rfind("/")+1:len(url)]
        hhRet["file"] = file
        hhRet["path"] = url.replace(hhRet["file"],"")
        hhRet["filename"] = file[0:file.rfind(".")]
        hhRet["ext"] = file.replace(hhRet["filename"]+".","")
    else:
        hhRet["path"] = url

    return hhRet
