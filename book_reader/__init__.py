from pandas import read_csv
import requests
from os.path import dirname, realpath, join

class page_reader():
    def __init__(self, link):
        self.url = link
        # site config
        self.siteConfig = self.getSiteConfig()
        # chapter info
        self.soup = self.getSoup()
        # object info
        self.web = self.getDriver()
    
    def getSiteConfig(self):
        dir_path = dirname(realpath(__file__))
        configfile = read_csv(join(dir_path, 'siteconfig.csv'),dtype=str,encoding='utf-16',na_filter=False)
        
        web_config = 0
        for idx, line in configfile.iterrows():
            if(line['website'] in self.url):
                web_config = idx
                break
            elif(line['website'] == 'NULL'):
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
            return 
        else:
            return requests.session()
        return

    def getSoup(self):
        if self.siteConfig['webDriverNeed'] == 'True':
            self.web.get(self.url)
        else:
            browser = requests.session()


        if self.siteConfig['encoding'] != 'NULL':
            html.encoding == self.siteConfig['encoding']
        
        return

    def getContent(self):
        return ''
    
    def getBookName(self):
        return ''
    
    def getChapterTitle(self):
        return ''
    
    def haveNext(self):
        return {'url':'', 'hasNext':False}
    
    def getNext(self):
        haveNext = self.haveNext()
        if haveNext['hasNext']:

            pass
        else:
            print('No next')
        return

if __name__=='__main__':
    url = ''
    html = ''
    book = page_reader(url)
    bookName = book.getBookName()
    
    while True:
        chapTitle = book.getChapterTitle()
        chapText = book.getContent()

        haveNextUrl = book.haveNext()
        if haveNextUrl['hasNext']:
            book = book.getNext()
        else:
            break
    print('done')