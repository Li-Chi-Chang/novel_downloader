from gmail_sending import send
from novel_downloader import onlineBook

from os.path import realpath,dirname,join
from bs4 import BeautifulSoup
from time import sleep
from random import randrange

def get_html_template():
    return BeautifulSoup('<html><head><title></title></head><body></body></html>','html.parser')

def downloadABook_HTML(starturl,endurl):
    thisbook = onlineBook(starturl,endurl)
    booktitle = thisbook.title

    local_novel = get_html_template()
    local_novel.head.title.string = booktitle

    while(True):
        sleep(2 + randrange(300)/100)
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
        
        if(thisbook.goToNextPage()):
            continue
        else:
            break

    with open(booktitle+'.html','w',encoding='utf-16') as f:
        f.write(str(local_novel))

    thisbook.close()
    return booktitle

def downloadAndPushToAmazon(starturl,endurl):
    bookname = downloadABook_HTML(starturl,endurl)
    send_email = send()
    # lichiricky_4jjvvj@kindle.com
    send_email.send('lichiricky@gmail.com', ['lichiricky@gmail.com'], bookname, '',join(dir_path,bookname+'.html'))


if __name__=="__main__": 
    f = open("downloadList.txt", "r")
    dir_path = dirname(realpath(__file__))

    for line in f:
        if('#' in line[0]):
            continue
        starturl = line.strip().split(' ')[0]
        endurl = line.strip().split(' ')[1]
        # downloadABook_HTML(starturl,endurl)
        downloadAndPushToAmazon(starturl,endurl)
    f.close()
