from gmail_sending import send
from book_reader import book_reader,filename_clearify
from book_reader.web_browser import get_novel_template
from bs4 import BeautifulSoup
from os.path import dirname, realpath, join

def downloadABook_html(oneurl):
    book = book_reader(oneurl)
    
    booktitle = filename_clearify(book.getBookName())

    local_novel = get_novel_template()
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

if __name__=='__main__': 
    dir_path = dirname(realpath(__file__))
    f = open(join(dir_path,'downloadList.txt'), 'r')
    lines = f.readlines()
    f.close()

    for line in lines:
        if('#' in line[0]):
            continue
        bookname = downloadABook_html(line.strip())
        send_email = send()
        send_email.send('lichiricky@gmail.com', ['lichiricky_4jjvvj@kindle.com','myk406@gmail.com'], bookname, '',join(dir_path,bookname+'.html'))