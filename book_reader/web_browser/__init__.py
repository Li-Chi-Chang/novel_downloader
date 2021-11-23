from msedge.selenium_tools import EdgeOptions, Edge
from os.path import dirname,join,abspath

# adblock path can be found at C:\Users\%username%\AppData\Local\Microsoft\Edge\User Data\Default\Extensions
# edge webdriver please download at https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# replace these paths below

adblock_path = abspath(join(dirname(__file__),'files','adblock','4.39.1_0'))
edge_path = join(dirname(__file__),'files','msedgedriver.exe')

def edge_driver(adb = True, mute = True, popblock = True, headless = False):
    edge_options = EdgeOptions()
    edge_options.use_chromium = True
    
    if headless:
        edge_options.add_argument('headless')
    if adb:
        edge_options.add_argument('load-extension=' + adblock_path)
    if mute:
        edge_options.add_argument('--mute-audio')
    if popblock:
        edge_options.add_experimental_option('excludeSwitches',['disable-popup-blocking'])
    
    browser = Edge(executable_path=edge_path, options=edge_options)
    return browser

def safari_driver():
    from selenium.webdriver import Safari
    browser = Safari()
    return browser

def get_novel_template():
    from bs4 import BeautifulSoup
    return BeautifulSoup('<html><head><title></title></head><body></body></html>','html.parser')