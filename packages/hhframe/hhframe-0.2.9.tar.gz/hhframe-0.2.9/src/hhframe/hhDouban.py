
# -*- codeing = utf-8 -*-
# @File：hhDouban.py
# @Ver：1.5.2
# @Author：立树
# @Time：2021/07/07 02:02
# @IDE：PyCharm

"""
更新：
- 优化 getMovieDetail 调整演员数据格式
"""

import re
import execjs
from .hhAjax import hhGet
from bs4 import BeautifulSoup

class hhDouban(object):

    def __init__(self):
        pass

    # 豆瓣搜索
    def search(self,opt={}):
        # 配置
        hhOpt = {
            "search": "",
            "decrypt": ""
        }
        hhOpt.update(opt)

        # 参数判断
        if hhOpt["search"]=="" or hhOpt["decrypt"]=="":
            print("hhframe.hhDouban.search() Error - 请补全参数（search、decrypt）")
            return {}

        try:
            # 发起请求
            page = hhGet(f"https://search.douban.com/movie/subject_search?search_text={hhOpt['search']}&cat=1002")

            # 获取加密数据
            encrypt = re.search('window.__DATA__ = "([^"]+)"',page).group(1)
            # print(encrypt)

            # 提取解密 js
            with open(hhOpt["decrypt"], "r", encoding="UTF-8", errors="ignore") as f:
                decrypt_js = f.read()
                # print(decrypt_js)

            # 解密数据
            ctx = execjs.compile(decrypt_js)
            ret = ctx.call("decrypt",encrypt)
            return ret["payload"]
        except Exception as err:
            print(f"hhframe.hhDouban.search() Error - {err}")
            return {}

    # 豆瓣明星列表抓取
    def getStarList(self,name=""):
        # 参数判断
        if name == "":
            print("hhframe.hhDouban.getStarList() Error - 请补全参数（name）")
            return []

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/celebrities/search?search_text={name}&cat=1002")
            html = BeautifulSoup(page,"html.parser")
            list = html.select("div.article .result")
            stars = []
            for item in list:
                star = {
                    "name": item.select(".content h3 a")[0].text,
                    "poster": item.select(".pic img")[0].attrs["src"],
                    "url": item.select(".content h3 a")[0].attrs["href"]
                }
                infos = item.select(".content > ul li")
                star["jobs"] = infos[0].text.strip().split(" / ")
                star["id"] = re.findall("\d+",star["url"])[0]
                if len(infos) == 3:
                    dates = infos[1].text.strip().split(" 至 ")
                    birth = dates[0]
                    death = dates[1] if len(dates) == 2 else ""
                    works = infos[2].text.replace("作品:", "").strip().split(" / ")
                    star["birth"] = birth
                    star["death"] = death
                    star["works"] = works
                if len(infos) == 2:
                    works = infos[1].text.replace("作品:", "").strip().split(" / ")
                    star["works"] = works
                stars.append(star)

            return stars
        except Exception as err:
            print(f"hhframe.hhDouban.getStarList() Error - {err}")
            return []

    # 豆瓣明星详情抓取
    def getStarDetail(self,id=""):
        # 参数判断
        if id == "":
            print("hhframe.hhDouban.getStarDetail() Error - 请补全参数（id）")
            return {}

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/celebrity/{id}/")

            # 调试
            # import os
            # from src.hhframe import hhUrl,hhOs
            # file = "./demo_douban_star_detail.html"
            # if not os.path.exists(file):
            #     hhUrl.hhDownload(f"https://movie.douban.com/celebrity/{id}/",file)
            # page = hhOs.hhOpenFile(file,"r")

            html = BeautifulSoup(page,"html.parser")

            star = {
                "id": id,
                "poster": html.select("#headline .pic img")[0].attrs["src"]
            }
            names = html.select("#content > h1")[0].text
            name = html.select("#headline .pic img")[0].attrs["title"]
            alias = names.replace(name,"").strip()
            star["name"] = name
            star["alias"] = alias

            info = html.select("#headline .info li")
            for item in info:
                label = item.select("span")[0].text
                # print(label)
                # print(item)
                if label=="星座":
                    star["constellation"] = item.text.replace("星座:","").strip()
                if label=="出生日期":
                    dates = re.findall("((\d+)年(\d+)月(\d+)日)", item.text)
                    birth, bY, bM, bD = dates[0]
                    star["birth"] = f"{bY}-{bM}-{bD}"
                if label=="生卒日期":
                    dates = re.findall("((\d+)年(\d+)月(\d+)日)", item.text)
                    birth, bY, bM, bD = dates[0]
                    death, dY, dM, dD = dates[1]
                    star["birth"] = f"{bY}-{bM}-{bD}"
                    star["death"] = f"{dY}-{dM}-{dD}"
                if label=="出生地":
                    star["area"] = item.text.replace("出生地:","").strip()
                if label=="职业":
                    star["jobs"] = item.text.replace("职业:","").strip().split(" / ")
                if label=="更多中文名":
                    star["chinese_names"] = item.text.replace("更多中文名:","").strip().split(" / ")
                if label=="更多外文名":
                    star["other_names"] = item.text.replace("更多外文名:","").strip().split(" / ")
                if label=="imdb编号":
                    star["imdb"] = item.select("a")[0].text
                    star["imdb_url"] = item.select("a")[0].attrs["href"]
                if label=="家庭成员":
                    star["family"] = item.text.replace("家庭成员:","").strip().split(" / ")

            # 简介
            if len(html.select("#intro .all")):
                star["descp"] = html.select("#intro .all")[0].text.replace("\u3000","").replace("\r","<br>").strip()
            else:
                star["descp"] = html.select("#intro .bd")[0].text.replace("\u3000","").replace("\r","<br>").strip()

            return star
        except Exception as err:
            print(f"hhframe.hhDouban.getStarDetail() Error - {err}")
            return {}

    # 豆瓣明星详情抓取
    def getStarPhotoList(self,id="",page=1,sort="like"):
        # sort
        # - like 喜欢
        # - size 尺寸
        # - time 时间

        # 参数判断
        if id == "":
            print("hhframe.hhDouban.getStarPhoto() Error - 请补全参数（id）")
            return {}

        try:
            # 发起请求
            contt = hhGet(f"https://movie.douban.com/celebrity/{id}/photos/?type=C&start={(int(page)-1)*30}&sortby={sort}&size=a&subtype=a")

            # 调试
            # import os
            # from src.hhframe import hhUrl,hhOs
            # file = "./demo_douban_star_photo_list.html"
            # if not os.path.exists(file):
            #     hhUrl.hhDownload(f"https://movie.douban.com/celebrity/{id}/photos/?type=C&start={page-1}&sortby={sort}&size=a&subtype=a",file)
            # contt = hhOs.hhOpenFile(file,"r")

            html = BeautifulSoup(contt,"html.parser")

            star = {
                "id": id,
                "name": html.select("#content h1")[0].text.replace("的图片",""),
                "sum": 0,
                "page": page,
                "size": 30,
                "pics": [],
                "items": []
            }

            list = html.select(".article .poster-col3 li")
            for item in list:
                url = item.select(".cover a")[0].attrs["href"]
                img = item.select(".cover img")[0].attrs["src"]
                size = item.select(".prop")[0].text.strip()
                reply = item.select(".name a")[0].text if len(item.select(".name a")) else ""
                title = item.select(".name")[0].text.replace(reply, "").strip()
                star["items"].append({
                    "url": url,
                    "img": img,
                    "width": int(size.split("x")[0]),
                    "height": int(size.split("x")[1]),
                    "title": title
                })
                star["pics"].append(img)

            # 图片总数
            if len(html.select(".paginator")):
                star["sum"] = int(re.findall("(\d+)",html.select(".paginator .count")[0].text)[0])
            else:
                star["sum"] = len(list)

            return star
        except Exception as err:
            print(f"hhframe.hhDouban.getStarPhoto() Error - {err}")
            return {}

    # 豆瓣明星图片详情抓取
    # http://www.3qphp.com/python/pybase/4278.html
    def getStarPhotoDetail(self,star_id="",pic_id="",cookie=""):

        # 参数判断
        if star_id == "" or pic_id == "":
            print("hhframe.hhDouban.getStarPhotoDetail() Error - 请补全参数（star_id、pic_id）")
            return {}

        try:
            # 发起请求
            # Cookie 临时获取：
            # - 登陆豆瓣
            # - 随便打开一个图片详情（比如：https://movie.douban.com/celebrity/1013782/photo/1888623099/）
            # - F12 - Network - All - 选择第一个请求（1888623099/）- Headers - Request Headers - Cookie
            page = hhGet(
                url=f"https://movie.douban.com/celebrity/{star_id}/photo/{pic_id}/",
                headers={"Cookie":cookie}
            )

            # 调试
            # import os
            # from src.hhframe import hhUrl,hhOs
            # file = "./demo_douban_star_photo_detail.html"
            # if not os.path.exists(file):
            #     hhUrl.hhDownload(
            #         url="https://movie.douban.com/celebrity/{star_id}/photo/{pic_id}/",
            #         file=file,
            #         headers={"Cookie":cookie}
            #     )
            # page = hhOs.hhOpenFile(file,"r")

            html = BeautifulSoup(page,"html.parser")

            name = html.select("#content h1")[0].text.replace("的图片","")
            size1 = html.select("#content .poster-info .pl")[0].text.replace("原图尺寸：","")
            width = size1.split("x")[0]
            height = size1.split("x")[1]
            size2 = html.select("#content .poster-info .pl")[1].text.replace("文件大小：","")
            url = html.select("#content .photo-zoom")[0].attrs["href"]

            return {
                "star_id": star_id,
                "pic_id": pic_id,
                "name": name,
                "url": url,
                "width": width,
                "height": height,
                "size": size2
            }
        except Exception as err:
            print(f"hhframe.hhDouban.getStarPhotoDetail() Error - {err}")
            return {}

    # 豆瓣电影详情抓取
    def getMovieDetail(self,id=""):
        # 参数判断
        if id == "":
            print("hhframe.hhDouban.getMovieDetail() Error - 请补全参数（id）")
            return {}

        # 返回的数据
        movie = {"id": id}

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/subject/{id}/")

            # 调试
            # import os
            # from src.hhframe import hhUrl,hhOs
            # file = "./demo_douban_movie_detail.html"
            # if not os.path.exists(file):
            #     hhUrl.hhDownload(f"https://movie.douban.com/subject/{id}/",file)
            # page = hhOs.hhOpenFile(file,"r")

            html = BeautifulSoup(page,"html.parser")

            names = html.select("#content > h1 > span")[0].text
            name = html.select("#mainpic > a > img")[0].attrs["alt"]
            alias = names.replace(name,"").strip()
            movie["name"] = name
            movie["alias"] = alias

            movie["poster"] = html.select("#mainpic > a > img")[0].attrs["src"]
            movie["score"] = html.select("#interest_sectl .rating_num")[0].text
            movie["rating_num"] = html.select("#interest_sectl .rating_people span")[0].text

            # movie["director"] = "、".join(list(map(lambda item:item.text,html.select("#info > span:nth-child(1) a"))))
            # movie["writer"] = "、".join(list(map(lambda item:item.text,html.select("#info > span:nth-child(3) a"))))
            # movie["type"] = "、".join(list(map(lambda item:item.text,html.select("#info > span[property='v:genre']"))))

            for item in html.select("#info")[0].text.strip().split("\n"):
                # print(item)
                if "导演" in item:
                    movie["director"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "编剧" in item:
                    movie["writer"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "主演" in item:
                    movie["actor"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "类型" in item:
                    movie["type"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "官方网站" in item:
                    movie["type"] = item.split(": ")[1]
                    continue
                if "制片国家/地区" in item:
                    movie["area"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "语言" in item:
                    movie["language"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "上映日期" in item:
                    movie["release_time"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "片长" in item:
                    movie["duration"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "又名" in item:
                    movie["alias2"] = item.split(": ")[1].replace(" / ","、")
                    continue
                if "IMDb" in item:
                    movie["imdb"] = item.split(": ")[1]
                    continue

            # 简介
            if len(html.select(".related-info .all")):
                movie["descp"] = html.select(".related-info .all")[0].text
            else:
                movie["descp"] = html.select("#link-report > span")[0].text

            movie["descp"] = movie["descp"].replace("\u3000","").replace("\r","<br>").strip()
            movie["descp"] = movie["descp"].replace("\n","<br>")
            movie["descp"] = re.sub("\s","",movie["descp"])

        except Exception as err:
            print(f"hhframe.hhDouban.getMovieDetail() Error - {err}")
            return {}

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/subject/{id}/celebrities")

            # 调试
            # import os
            # from src.hhframe import hhUrl,hhOs
            # file = "./demo_douban_movie_actors.html"
            # if not os.path.exists(file):
            #     hhUrl.hhDownload(f"https://movie.douban.com/subject/{id}/celebrities",file)
            # page = hhOs.hhOpenFile(file,"r")

            html = BeautifulSoup(page,"html.parser")

            actors = []
            for actor in html.select("#celebrities .list-wrapper:nth-child(2) li"):
                actors.append({
                    "name": actor.select(".info .name a.name")[0].text,
                    "role": "".join(re.findall("\([饰|配] (.*)\)", actor.select(".info .role")[0].text))
                })
            movie["actor2"] = actors

            return movie
        except Exception as err:
            print(f"hhframe.hhDouban.getMovieDetail() Error - {err}")
            return {}
