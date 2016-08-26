# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup as BS
import os
import  re
import sys
from onceModel import ImageModel
import filemanager

main_url = "http://www.mm131.com/xinggan/"


page_count=0
current_url=main_url

def request_url(url=main_url,code=True):
    """
    :param url:q请求的网络地址
    :param code: 是否对请求数据进行解码
    :return: code:False return urlResponse
             code:true  return(conternt,code)
    """
    head={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
    request = urllib.request.Request(url,headers = head)
    response=urllib.request.urlopen(request)
    if not code :
        return  response.read()
    else:
        result = response.read()
        try:
            res = result.decode('utf-8')
            return (res,'utf-8')
        except Exception as e:
            try:
                res = result.decode('gbk')
                return (res,"gbk")
            except Exception as e:
                raise  Exception("啥子编码格式")
 #得到一级界面上的所有图片源
def get_this_source(bs):
    global page_count
    if page_count<=0:
        res = bs.find_all('a',class_="page-en")[-1].attrs['href']
        page = re.search(r'(\d+)(?=\.html)', res)
        page_count=int(page.group(1))
    a = bs.find_all("dl", class_ = "list-left public-box")
    list = []
    for i in a[-1].children:
        if i.name == "dd":
            aaa = i.find('a')
            if aaa:
                list.append(aaa.attrs['href'])
    return  list[0:-1]

# 修改当前主页面
def revise_next_url():
    global  current_url
    if current_url==main_url:
        current_url=main_url+"list_6_2.html"
    else:
        res = re.search(r'(?<=list_6_)(\d+)',current_url)
        if res:
            start,end =res.span()
            currenPage = int(res.group(1))
            result = currenPage+1
            if result > page_count:
                current_url=None
            else:
                start= current_url[:start]
                end = current_url[end:]
                a =  start+str(result)+end
                current_url=a


if __name__=="__main__":
    args = sys.argv
    if len(args)>=2:
        DIV=args[1]
        if os.path.exists(DIV):
            filemanager.Main_Div=DIV
        else:
            raise Exception("输入的保存文件路径不存在")
    while (current_url):
        result,code = request_url(current_url)
        group=BS(result)
        list = get_this_source(group)
        print(current_url)
        print (list)
        for i in range(len(list)):
            one_url = list[i]
            html,code = request_url(one_url)
            img = ImageModel(html)
            if not img.finish:
                img.download()
            print("完成",one_url)
        revise_next_url()
        print(current_url)
