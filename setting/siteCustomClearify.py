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
