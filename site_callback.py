from binascii import unhexlify
import re
import time

def wwwstocx_clearify_callback(text):
    codes = re.findall('%[a-z|A-Z|0-9]{2}%[a-z|A-Z|0-9]{2}%[a-z|A-Z|0-9]{2}', text)
    if(len(codes)>0):
        for code in codes:
            chrsplit = re.split('%',code)
            word = unhexlify(''.join(chrsplit[1:])).decode("utf-8")
            text = text.replace(code,word)
    text = re.sub('.本.作.品.由.*','',text)
    text = re.sub('..本..作..品..由.*','',text)
    text = re.sub('...本...作...品...由.*','',text)
    text = re.sub('.思.兔.*','',text)
    text = re.sub('..思..兔.*','',text)
    text = re.sub('...思...兔.*','',text)
    text = re.sub('....思....兔.*','',text)
    text = re.sub('＊','',text)
    return text

 
def big5quanben5com_clearify_callback(text):
    text = re.sub(' - 全本小說網','',text)
    return text

def wwwuukanshucom_clearify_callback(text):
    text = re.sub('UU看书 www.uukanshu.com','',text)
    text = re.sub('UU看书www.uukanshu.com','',text)
    return text

def aixdzscom_clearify_callback(text):
    text = re.sub('-愛下電子書','',text)
    return text

def shubaownet_clearify_callback(text):
    time.sleep(1)
    return text