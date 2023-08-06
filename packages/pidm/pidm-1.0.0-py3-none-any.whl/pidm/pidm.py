import requests
import shutil
import threading
from urllib.request import urlopen
import os
import random
import string

class Download:
    def calc_byte_range(self):
        self.trange= self.content_len// self.threads
        tm = -1
        self.byte_range=[]
        for i in range(self.threads):
            a = dict()
            a["Range"] = "bytes=" + str(tm+1) + "-" + str(tm + self.trange)
            tm += self.trange
            self.byte_range.append(a)
        rem=self.content_len%self.threads
        if(rem>0):
            a = dict()
            a["Range"] = "bytes=" + str(tm-self.trange+1) + "-" + str(tm+1 +rem )
            del self.byte_range[-1]
            self.byte_range.append(a)
        else:
            a = dict()
            a["Range"] = "bytes=" + str(tm - self.trange + 1) + "-" + str(tm + 1 + rem)
            del self.byte_range[-1]
            self.byte_range.append(a)

    def download_parts(self,count):
        try:
            with requests.get(self.url, allow_redirects=True, stream=True, headers=self.byte_range[count]) as r:
                with open(self.temp + str(count), 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            #print('Thread: ',count+1,' done!')
        except:
            try:
                #print('Error occured in thread: ',count+1,' retrying!!')
                with requests.get(self.url, allow_redirects=True, stream=True, headers=self.byte_range[count]) as r:
                    with open(self.temp + str(count), 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                #print('Thread: ',count+1,' done!')
            except:
                #print('Error occured in thread: ', count + 1, ' exiting')
                self.err_list.append(count)

    def create_threads(self):
        thread_list=[]
        for i in range(self.threads):
            thread_list.append(threading.Thread(target=self.download_parts, args=(i, )))
        for i in range(self.threads):
            thread_list[i].start()
        for i in range(self.threads):
            thread_list[i].join()

    def join_files(self):
        with open( self.outfile, 'wb') as f:
            for count in range(self.threads):
                with open(self.temp + str(count), 'rb') as r:
                    shutil.copyfileobj(r, f)

    def flush_temp(self):
        for count in range(self.threads):
            try:
                os.remove(self.temp + str(count))
            except:
                pass

    def get_headers(self,outfile):
        try:
            self.response = urlopen(self.url)
            self.response.close()
        except:
            self.response = requests.head(self.url, allow_redirects=True)

        self.content_len = int(self.response.headers['Content-Length'])
        if(len(outfile)==0):
            if(self.response.headers['filename']!=None):
                self.outfile=self.response.headers['filename']
                #print(self.outfile)
            else:
                self.outfile=self.url.split('/')[-1]
        else:
            self.outfile=outfile

    def __init__(self,url,threads=8,outfile="",flush=True):
        try:
            self.url=url
            self.threads=threads
            self.flush=flush
            self.temp="".join(random.choice(string.ascii_lowercase) for x in range(9))
            self.get_headers(outfile)
            self.calc_byte_range()
            self.err_list = []
            self.create_threads()
            if (len(self.err_list) == 0):
                self.join_files()
                if (self.flush):
                    self.flush_temp()
                self.result=True
            else:
                # print(self.err_list)
                if (self.flush):
                    self.flush_temp()
                self.result=False
        except:
            if (self.flush):
                self.flush_temp()
            self.result=False

    def __bool__(self):
        return self.result
