import re, os, sys
from csv import DictReader
from dotenv import load_dotenv

# put web_browser in root (same with folder: novel_downloader)!!!!!!!!
from web_browser import edge_driver

load_dotenv()
if(os.getenv('siteCustomClearifyFolder') == None):
	sys.path.append('setting')
else:
	sys.path.append(os.getenv('siteCustomClearifyFolder'))

if(os.getenv('siteSettingFile') == None):
	siteSettingFile = 'setting/novelSitesSetting.csv'
else:
	siteSettingFile = os.getenv('siteSettingFile')

import siteCustomClearify

def filename_clearify(astring, with_space=True):
	signs = ['?','“','”','/','\\','<','>','*','|',':','&', '+','\'','.','!','"','#',]
	for sign in signs:
		astring = astring.replace(sign,'')
	if not with_space:
		astring = astring.replace(' ','')
	return astring

def content_clearify(originalText, callback = lambda x: x):
	originalText = callback(originalText)
	originalText = re.sub('\n{1,}','\n',originalText)
	originalText = re.sub('\t{1,}',' ',originalText)
	originalText = re.sub('[ ]{1,}',' ',originalText)
	originalText = re.sub('[　]{1,}',' ',originalText)
	originalText = re.sub(r'\x00', '', originalText)
	originalText = re.sub('[ ]{1,}',' ',originalText)
	originalText = re.sub('[ |\n]{2,}','\n',originalText)
	return originalText

class onlineBook:
	def __init__(self,starturl,endurl) -> None:
		self.currenturl = starturl
		self.endurl = endurl
		self.webdriver = edge_driver()
		self.webdriver.get(starturl)
		self.SiteConfig = False

		with open(siteSettingFile, 'r', encoding='utf-8-sig') as file:
			reader = DictReader(file)
			for row in reader:
				if row['URL'] in starturl and row['URL'] in self.endurl:
					self.siteName = row['URL']
					self.TitleCSSSelector = row['TitleCSSSelector']
					self.ContentCSSSelector = row['ContentCSSSelector']
					self.ChapterCSSSelector = row['ChapterCSSSelector']
					self.NextPageButtonCSSSelector = row['NextPageButtonCSSSelector']
					self.needCustomClearify = row['needCustomClearify']
					self.SiteConfig = True
					break

		self.title = self.__getTitle()

	def __getTitle(self):
		title = ''
		if self.SiteConfig == True:
			title = self.webdriver.find_element_by_css_selector(self.TitleCSSSelector).get_attribute('innerText')
		else:
			title = self.webdriver.title
		return filename_clearify(title)

	def getChapter(self):
		chapter = ''
		if self.SiteConfig == True:
			chapter = self.webdriver.find_element_by_css_selector(self.ChapterCSSSelector).text
			if(self.needCustomClearify == 'Y'):
				return content_clearify(chapter,getattr(siteCustomClearify,self.siteName.replace('.','')+'_clearify_callback'))
		else:
			chapter = self.webdriver.title
		return content_clearify(chapter)

	def getContent(self):
		content = ''
		if self.SiteConfig == True:
			content = self.webdriver.find_element_by_css_selector(self.ContentCSSSelector).text
			if(self.needCustomClearify == 'Y'):
				return content_clearify(content,getattr(siteCustomClearify,self.siteName.replace('.','')+'_clearify_callback'))
		else:
			content = self.webdriver.webdriver.find_element_by_xpath('/html/body').text
		return content_clearify(content)

	def goToNextPage(self):
		if(self.currenturl == self.endurl): return False
		if self.SiteConfig == True:
			try:
				self.webdriver.find_element_by_css_selector(self.NextPageButtonCSSSelector).click()
				self.currenturl = self.webdriver.current_url
			except:
				print('no button found')
				return False
		else:
			try:
				self.webdriver.find_element_by_xpath('//a[starts-with(text(),"下一")]').click()
				self.currenturl = self.webdriver.current_url
			except:
				print('no button found')
				return False
		return True

	def close(self):
		self.webdriver.quit()