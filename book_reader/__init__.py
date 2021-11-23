import requests, re
from bs4 import BeautifulSoup
from urllib import parse
from pandas import read_csv
from .web_browser import safari_driver as webdriver # change if needed
from os.path import dirname, realpath, join

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

def filename_clearify(string, with_space=True):
    signs = ['?','“','”','/','\\','<','>','*','|',':','&', '+','\'','.','!','"','#',]
    for sign in signs:
        string = string.replace(sign,'')
    if not with_space:
        string = string.replace(' ','')
    return string

class book_reader():
    def __init__(self, link):
        self.url = link
        # site config
        self.siteConfig = self.getSiteConfig()
        # object info
        self.web = self.getDriver()
        # chapter info
        self.soup = self.getSoup()
    
    def getSiteConfig(self):
        dir_path = dirname(realpath(__file__))
        configfile = read_csv(join(dir_path, 'siteconfig.csv'),dtype=str,na_filter=False)
        
        web_config = 0
        for idx, line in configfile.iterrows():
            if(line['website'] in self.url):
                web_config = idx
                break
            elif(line['website'] == 'Null'):
                web_config = idx
                break
        
        callback = lambda x:x
        if configfile['callback'][web_config] == 'True':
            pass

        config = {
            'encoding': configfile['encode'][web_config],
            'bookTitle': configfile['bookTitle'][web_config],
            'chapterTitle': configfile['chapterTitle'][web_config],
            'chapterText': configfile['chapterText'][web_config],
            'next': configfile['next'][web_config],
            'callback': callback,
            'webDriverNeed': configfile['webDriver'][web_config]
        }
        return config

    def getDriver(self):
        if self.siteConfig['webDriverNeed'] == 'True':
            return webdriver()
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49'}
            return requests.session(headers=headers)

    def getSoup(self):
        if self.siteConfig['webDriverNeed'] == 'True':
            self.web.get(self.url)
            html = self.web.page_source
        else:
            html = self.web.get(self.url)
            if self.siteConfig['encoding'] != 'Null':
                html.encoding == self.siteConfig['encoding']
        soup = BeautifulSoup(html,'html.parser')
        return soup

    def findIt(self, pattern):
        if pattern == 'Null':
            return None
        
        finditId = self.soup.find(id=pattern)
        finditClass_div = self.soup.find('div', class_=pattern)
        finditClass_a = self.soup.find('a', class_=pattern)

        if finditId is not None:
            return finditId
        elif finditClass_div is not None:
            return finditClass_div
        elif finditClass_a is not None:
            return finditClass_a

    def getContent(self):
        chapterTextFromConfig = self.findIt(self.siteConfig['chapterText'])
        if chapterTextFromConfig is not None:
            return clearify(chapterTextFromConfig)
        else:
            for s in self.soup.select('script'):
                s.extract()
            return clearify(self.soup)
    
    def getBookName(self):
        bookTitleFromConfig = self.findIt(self.siteConfig['bookTitle'])
        if bookTitleFromConfig is not None:
            return clearify(bookTitleFromConfig)
        else:
            return clearify(self.soup.title)
    
    def getChapterTitle(self):
        chapterTitleFromConfig = self.findIt(self.siteConfig['chapterTitle'])
        if chapterTitleFromConfig is not None:
            return clearify(chapterTitleFromConfig)
        else:
            return clearify(self.soup.title)
    
    def haveNextPage(self):
        haveNext = False
        nexturl = ''
        try:
            possibleObjFromConfig = self.findIt(self.siteConfig['next'])
            pattern = re.compile('下[一|壹]{0,1}[頁|章|页|篇]')
            possibleObjA = self.soup.find('a', text=pattern)
            if possibleObjFromConfig is not None:
                partialurl = possibleObjFromConfig['href']
                nexturl = parse.urljoin(self.url,partialurl)
                haveNext = True
                
            elif possibleObjA is not None:
                partialurl = possibleObjA['href']
                nexturl = parse.urljoin(self.url,partialurl)
                haveNext = True
            else:
                print('not found a next without error')
        except:
            print('not found a next with error')
        
        if 'javascript:void(0);' in nexturl:
            print('reach legally final point')
            haveNext = False
            nexturl = ''
        return {'url':nexturl, 'haveNext':haveNext}
    
    def getNextPage(self):
        haveNext = self.haveNextPage()
        if haveNext['haveNext']:
            self.url = haveNext['url']
            self.soup = self.getSoup()
        else:
            print('No next')
        return
    
    def closePage(self):
        if self.siteConfig['webDriverNeed'] == 'True':
            self.web.close()
        else:
            self.web.config['keep_alive'] == False
        return

if __name__=='__main__':
    url = ''
    html = ''
    book = book_reader(url)
    bookName = book.getBookName()
    
    while True:
        chapTitle = book.getChapterTitle()
        chapText = book.getContent()

        haveNextUrl = book.haveNext()
        if haveNextUrl['haveNext']:
            book = book.getNext()
        else:
            break
    print('done')