from gmail_sending import send
from web_browser import edge_driver

from os.path import realpath,dirname,join
from binascii import unhexlify
import re, time

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
    time.sleep(1)
    return text

def downloadABook(oneurl):
    web = edge_driver()
    web.get(oneurl)
    booktitle = web.title
    with open(booktitle+'.html','w',encoding='utf-16') as f:
        f.write('<!DOCTYPE html><html><head><title>' + booktitle + '</title></head>')
        f.write('<body>')
        while(True):
            bookcontent = web.find_element_by_id('BookContent').text
            bookcontent = wwwstocx_clearify_callback(bookcontent)
            f.write('<div loading="lazy">')
            f.write(bookcontent.replace('。','。<br/>\n'))
            f.write('</div>\n')
            nextpage = web.find_element_by_link_text('下壹頁').get_attribute('href')
            if nextpage is None:
                f.write('</body>\n</html>\n')
                break
            else:
                web.get(nextpage)
        print('done')
    web.close()
    return booktitle

if __name__=="__main__": 
    f = open("downloadList.txt", "r")
    dir_path = dirname(realpath(__file__))

    for line in f:
        if('#' in line[0]):
            continue
        bookname = downloadABook(line.strip())
        send_email = send()
        send_email.send('lichiricky@gmail.com', ['lichiricky_4jjvvj@kindle.com','myk406@gmail.com'], bookname, '',join(dir_path,bookname+'.html'))
    f.close()
