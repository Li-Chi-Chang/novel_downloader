from gmail_sending import send
from web_browser import safari_driver, edge_driver, get_novel_template

from os.path import realpath,dirname,join
from binascii import unhexlify
import re, time
from bs4 import BeautifulSoup
from urllib import parse

webenv = 'safari'

def filename_clearify(string, with_space=True):
    signs = ['?','“','”','/','\\','<','>','*','|',':','&', '+','\'','.','!','"','#',]
    for sign in signs:
        string = string.replace(sign,'')
    if not with_space:
        string = string.replace(' ','')
    return string

def clearify(soup, callback = lambda x: x):
    funcsoup = soup
    for br in funcsoup.find_all('br'):
        br.replace_with('\n')
    originalText = funcsoup.text.strip()
    originalText = callback(originalText)
    originalText = re.sub('。','。\n',originalText)
    originalText = re.sub('\n{1,}','\n',originalText)
    originalText = re.sub('\t{1,}',' ',originalText)
    originalText = re.sub('[ ]{1,}',' ',originalText)
    originalText = re.sub('[　]{1,}',' ',originalText)
    originalText = re.sub(r'\x00', '', originalText)
    originalText = re.sub('[ ]{1,}',' ',originalText)
    originalText = re.sub('[ |\n]{2,}','\n',originalText)
    return originalText

def get_driver(webenv):
    if (webenv == 'safari'):
        return safari_driver()
    elif(webenv == 'edge'):
        return edge_driver()

def getnext(soup, currenturl):
    hasNext = True
    try:
        pattern = re.compile('下[一|壹]{0,1}[頁|章|页|篇]')
        partialurl = soup.find('a', text=pattern)['href']
        currenturl = parse.urljoin(currenturl,partialurl)
    except:
        hasNext = False
        print('not found a next')
    return {"url":currenturl, "hasNext":hasNext}

def downloadABook(oneurl):
    web = get_driver(webenv)
    web.get(oneurl)
    html = web.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    booktitle = filename_clearify(clearify(soup.title))

    local_novel = get_novel_template()
    local_novel.head.title.string = booktitle

    while(True):
        chapter = local_novel.new_tag('div',loading='lazy')
        chaptertext = BeautifulSoup(clearify(soup).replace('\n','<br/>\n'),'html.parser')
        print(chaptertext.text[:100])
        chapter.insert(0,chaptertext)
        local_novel.body.append(chapter)

        next = getnext(soup, oneurl)
        hasNext = next['hasNext']
        if not hasNext:
            break
        else:
            nextpage = next['url']
            web.get(nextpage)
            html = web.page_source
            soup = BeautifulSoup(html,'html.parser')
    print('done')

    with open(booktitle+'.html','w',encoding='utf-16') as f:
        f.write(str(local_novel))

    web.close()
    return booktitle

if __name__=='__main__': 
    dir_path = dirname(realpath(__file__))
    f = open(join(dir_path,'downloadList.txt'), 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if('#' in line[0]):
            continue
        bookname = downloadABook(line.strip())
        send_email = send()
        send_email.send('lichiricky@gmail.com', ['lichiricky_4jjvvj@kindle.com','myk406@gmail.com'], bookname, '',join(dir_path,bookname+'.html'))