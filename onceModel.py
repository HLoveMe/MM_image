
import re
from bs4 import BeautifulSoup as BS
import  os
import  threading
import urllib.request
import filemanager
import time

currentManager =  filemanager.manager()

def _open_image_url(url):
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
    req =  urllib.request.Request(url,headers = head)
    try:
        data = urllib.request.urlopen(req,timeout = 15).read()
        return data
    except Exception:
        print(url,"time out")


class ImageModel(object):
    def __init__(self,html):
        if html==None:
            raise  Exception("bs is none")
        self._bs=BS(html)
        #是否正在下载
        self._isdownload = False
        # 该MM第一张图片
        self.first_url = ""
        #开启的子线程集合
        self.threads = []
        #所有图片url s
        self._urls = []
        # 解析网页
        self._parser_bs()
        #得到该MM应该保持的文件夹
        self._div=currentManager.get_getcurrent_div(self.first_url)

        self._isfinish = os.path.exists(self._div + "__")


        if not os.path.exists(self._div) and not self._isfinish:
            os.makedirs(self._div)

        #是否已经完成



    def _parser_bs(self):
        div = self._bs.find('div',class_='content-pic')

        res = re.search(r'(?<=共)(\d+)(?=页)',str(self._bs.tagStack[-1]))
        if res:
            self._count=int(res.group(1))
        else:
            self._count=1
            raise  Exception("解析出错")
        self.first_url = div.find('a').find('img').attrs['src']

        head, name = os.path.split(self.first_url)
        for i in range(self._count):
             one = head + '/' + str(i + 1) + ".jpg"
             self._urls.append(one)

    # def  next_url(self):
    #     yield self.first_url
    #     head, name = os.path.split(self.first_url)
    #     for i in range(self._count):
    #         one = head + '/' + str(i + 1) + ".jpg"
    #         yield one
    lock = threading.Lock()

    def _download(self):
        if len(self._urls)>=1:
            self.lock.acquire(1)
            url = self._urls.pop(0)
            self._count-=1
            self.lock.release()
            path = currentManager.get_savepath(url)
            if not os.path.exists(path):
                global _open_image_url
                data = _open_image_url(url)
                if  data:
                    with open(path, 'bw') as file:
                        file.write(data)

                self._download()
        else:
            cur = threading.current_thread()
            if cur in self.threads:
                self.threads.remove(cur)

    def download(self):
        self._isdownload=True
        for i in range(5):
            one = threading.Thread(target = self._download)
            self.threads.append(one)
            one.setDaemon(True)
            one.start()
        while (len(self.threads)>=1):
            pass
        currentManager.down_finish(self._div)
        self._isdownload = False
        self.threads.clear()

    def _getBs(self):
        return self._bs

    def _setBs(self, bs):
        self._bs = bs

    bs = property(_getBs, _setBs)

    def _getcount(self):
        return self._count

    #  表示当前种类的图片 有多少页
    page_count = property(fget = _getcount)

    isdownloading = property(fget = lambda self: self._isdownload)

    def _isFinish(self):
        return self._isfinish

    finish = property(fget = _isFinish)


