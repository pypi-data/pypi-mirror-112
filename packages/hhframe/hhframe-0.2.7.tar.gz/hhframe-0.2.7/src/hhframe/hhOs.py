
# -*- codeing = utf-8 -*-
# @File：hhOs.py
# @Ver：1.2.0
# @Author：立树
# @Time：2021/07/04 18:00
# @IDE：PyCharm

"""
更新：
- 新增 hhOpenFile 打开文件功能
"""

import os

# 打开文件（文本类型的文件）
def hhOpenFile(file="",mode="r",encoding="utf-8"):
    # 参数判断
    if file == "":
        print("hhframe.hhOs.hhOpenFile() Error - 请补全参数（file）")
        return ""

    # 路径判断
    if not os.path.exists(file):
        print(f"hhframe.hhOs.hhOpenFile() Error - '{file}'文件路径不存在")
        return ""

    try:
        with open(file,mode,encoding=encoding) as f:
            contt = f.read()
            # print(contt)
            return contt
    except Exception as err:
        print(f"hhframe.hhOs.hhOpenFile() Error - {str(err)}")
        return ""

# 创建文件
def hhCreateFile(path="",mode="w",content="",encoding=None):
    # 参数判断
    if path == "" or content == "":
        print("hhframe.hhOs.hhCreateFile() Error - 请补全参数（path、content）")
        return {"state": False, "msg": "缺少参数"}

    # 路径检测
    if path.find("/")>-1:
        if path[-1]!="/":
            # 匹配内容：
            # - [./][dir/].filename
            # - [./][dir/]filename
            # - [./][dir/]filename.ext
            dir = path[0:path.rfind("/")+1]
            if not os.path.exists(dir):
               os.makedirs(dir)
        else:
            # 匹配内容：
            # - ./
            # - ./dir/
            # - ./dir/dir/
            # - ../dir/
            # - dir/dir/
            print(f"hhframe.hhOs.hhCreateFile() Error - 参数不合法（'{path}'不是有效文件路径）")
            return {"state": False, "msg": f"参数不合法（'{path}'不是有效文件路径）"}
    else:
        # 匹配内容：
        # - .filename
        # - filename
        # - filename.ext
        pass

    try:
        with open(path,mode,encoding=encoding) as f:
            f.write(content)
        return {"state": True, "msg": "保存成功"}
    except IOError as err:
        return {"state": False, "msg": str(err)}

# 删除文件、文件夹
def hhDelete(path=""):
    # 参数判断
    if path == "":
        print("hhframe.hhOs.hhDelete() Error - 请补全参数（path）")
        return {"state": False, "msg": "缺少参数"}

    # 路径判断
    if not os.path.exists(path):
        print(f"hhframe.hhOs.hhDelete() Error - 路径不存在（{path}）")
        return {"state": False, "msg": f"路径不存在（{path}）"}

    # 屏蔽风险操作
    if path=="." or path=="./" or path[0]=="/" or path.find("..")>-1:
        print(f"hhframe.hhOs.hhDelete() Error - 路径无法删除（{path}）")
        return {"state": False, "msg": f"路径无法删除（{path}）"}

    # 删除
    try:
        if os.path.isfile(path):
            # 删除文件
            os.remove(path)
            return {"state": True, "msg": "文件删除成功"}
        else:
            # 删除当前文件夹下的所有文件、子文件夹
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    file = os.path.join(root, name).replace("\\", "/")
                    # print("file - ", file)
                    if os.path.exists(file):
                        os.remove(file)
                for name in dirs:
                    dir = os.path.join(root, name).replace("\\", "/")
                    # print("folder - ", dir)
                    if os.path.exists(dir):
                        os.removedirs(dir)
            # 删除当前文件夹
            os.removedirs(path)
            return {"state": True, "msg": "文件夹删除成功"}
    except IOError as err:
        return {"state": False, "msg": str(err)}
