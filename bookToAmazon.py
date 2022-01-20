from gmail_sending import send
from book_reader import book_reader,filename_clearify
from book_reader.web_browser import get_html_template
from mongo_IO import thisdirNovel, getRoot
from bs4 import BeautifulSoup
from os.path import dirname, realpath, join
from subprocess import Popen, PIPE

def downloadABook_html(oneurl):
    book = book_reader(oneurl)
    
    booktitle = filename_clearify(book.getBookName())

    local_novel = get_html_template()
    local_novel.head.title.string = booktitle

    while(True):
        chapter = local_novel.new_tag('div',loading='lazy')
        chaptertext = BeautifulSoup(book.getContent().replace('\n','<br/>\n'),'html.parser')
        print(chaptertext.text[:100])
        chapter.insert(0,chaptertext)
        local_novel.body.append(chapter)

        next = book.haveNextPage()
        haveNext = next['haveNext']
        if not haveNext:
            break
        else:
            book.getNextPage()
    print('done')

    with open(booktitle+'.html','w',encoding='utf-16') as f:
        f.write(str(local_novel))

    book.closePage()
    return booktitle

def downloadABook_epub(oneurl):
    book = book_reader(oneurl)
    booktitle = filename_clearify(book.getBookName())
    
    f = open(booktitle, 'w')
    f.write('% ' + booktitle + '\n')
    f.write('% unknown\n\n')

    while(True):
        chapter = book.getChapterTitle()
        chaptertext = book.getContent()

        f.write('# ' + chapter.replace('\n','') + '\n\n')
        f.write(chaptertext.replace('\n','\n\n') + '\n\n')
        print(chaptertext[:100])
        
        next = book.haveNextPage()
        haveNext = next['haveNext']
        if not haveNext:
            break
        else:
            book.getNextPage()
    print('done')
    
    process = Popen('pandoc "'+booktitle+'" -o "' + booktitle + '.epub"', shell=True, stdout=PIPE)
    process.wait()
    f.close()
    book.closePage()
    return booktitle

def downloadABook_ForMyServer(oneurl,dbdirID):
    book = book_reader(oneurl)
    dbio = thisdirNovel(dbdirID)

    booktitle = filename_clearify(book.getBookName())
    dbio.insertANovel(booktitle)

    while(True):
        chapter = book.getChapterTitle()
        chaptertext = book.getContent()
        dbio.insertAChapter(chapter,chaptertext.replace('\n','<br/>\n'))
        print(chaptertext[:100])
        
        next = book.haveNextPage()
        haveNext = next['haveNext']
        if not haveNext:
            break
        else:
            book.getNextPage()
    print('done')
    
    book.closePage()
    dbio.close()
    return booktitle

def downloadAndSendToAmazon(oneurl, sender, sendeelist):
    bookname = downloadABook_html(oneurl.strip())
    send_email = send()
    send_email.send(sender, sendeelist, bookname, 'as attachment',join(dir_path,bookname+'.html'))

if __name__=='__main__': 
    dir_path = dirname(realpath(__file__))
    f = open(join(dir_path,'downloadList.txt'), 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if('#' in line[0]):
            continue
        # downloadAndSendToAmazon(line.strip(), sender='lichiricky@gmail.com', sendeelist=['lichiricky_4jjvvj@kindle.com','myk406@gmail.com'])

        # booktitle = downloadABook_epub(line.strip())
        # send_email = send()
        # send_email.send('lichiricky@gmail.com', ['lichiricky_4jjvvj@kindle.com','myk406@gmail.com'], booktitle, 'as attachment',join(dir_path,booktitle+'.epub'))

        # root = getRoot()
        downloadABook_ForMyServer(line.strip(),'61e971482ecb06ca7117f4da')