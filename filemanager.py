
import os

Main_Div="/Users/zhuzihao/Desktop/PRO"

class manager(object):
    # http://img1.mm131.com/pic/2625/1.jpg
    def get_getcurrent_div(self,url):
        div = os.path.join(Main_Div, "images")
        list = url.split("/")
        return os.path.join(div,list[-2])

    def get_savepath(self,imgurl,div=None):
        if div==None:
            div=self.get_getcurrent_div(imgurl)
        list = imgurl.split("/")
        path = os.path.join(div,list[-1])
        return path

    def down_finish(self,src):
        if os.path.exists(src):
            os.rename(src,src+"__")
            return
