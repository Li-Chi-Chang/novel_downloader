from gmail_sending import send
from novel_downloader import onlineBook

from os.path import realpath,dirname,join
from bs4 import BeautifulSoup
from time import sleep
from random import randrange

from dotenv import load_dotenv
import os
load_dotenv()
if(os.getenv('downloadListFile') == None):
    downloadListFile = 'setting/downloadList.txt'
else:
    downloadListFile = os.getenv('downloadListFile')
if(os.getenv('downloadDoneFolder') == None):
    downloadDoneFolder = ''
else:
    downloadDoneFolder = os.getenv('downloadDoneFolder')

if(os.getenv('EmailFrom') == None):
    EmailFrom = 'temp@temp.com'
else:
    EmailFrom = os.getenv('EmailFrom')
if(os.getenv('EmailTo') == None):
    EmailTo = 'temp@temp.com'
else:
    EmailTo = os.getenv('EmailTo')

def get_html_template():
    return BeautifulSoup('<html><head><title></title></head><body></body></html>','html.parser')

def downloadABook_HTML(starturl,endurl):
    thisbook = onlineBook(starturl,endurl)
    booktitle = thisbook.title

    local_novel = get_html_template()
    local_novel.head.title.string = booktitle

    while(True):
        sleep(1 + randrange(200)/100)
        htmlchapter = local_novel.new_tag('h4',loading='lazy')
        htmlcontent = local_novel.new_tag('div',loading='lazy')

        chapter = thisbook.getChapter()
        content = thisbook.getContent()

        htmlchapter.string = chapter
        htmlcontent.append(BeautifulSoup(content.replace('\n','<br>\n'),'html.parser'))

        print(chapter)
        print(content[:100])
        
        local_novel.body.append(htmlchapter)
        local_novel.body.append(htmlcontent)

        with open(join(downloadDoneFolder,booktitle+'.html'),'w',encoding='utf-16') as f:
                f.write(str(local_novel))
        if(thisbook.goToNextPage()):
            
            continue
        else:
            break

    thisbook.close()
    return booktitle

def downloadAndPushToAmazon(starturl,endurl):
    bookname = downloadABook_HTML(starturl,endurl)
    send_email = send()
    dir_path = join(dirname(realpath(__file__)),downloadDoneFolder)
    send_email.send(EmailFrom, [EmailTo], bookname, '',join(dir_path,bookname+'.html'))


if __name__=="__main__": 
    f = open(downloadListFile, "r")
    

    for line in f:
        if('#' in line[0]):
            continue
        starturl = line.strip().split(' ')[0]
        endurl = line.strip().split(' ')[1]
        # downloadABook_HTML(starturl,endurl)
        downloadAndPushToAmazon(starturl,endurl)
    f.close()
