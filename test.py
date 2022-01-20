from book_reader import book_reader

url = 'https://www.51shucheng.net/zh-tw/wangluo/douluodalu/21750.html'
aBook = book_reader(url)

print(aBook.getBookName())
print(aBook.getChapterTitle())
print(aBook.getContent())
print(aBook.haveNextPage())
print(aBook.getNextPage())
print(aBook.getBookName())
print(aBook.getChapterTitle())
print(aBook.getContent())
print(aBook.haveNextPage())
aBook.closePage()