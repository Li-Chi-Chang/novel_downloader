from book_reader import book_reader

url = 'https://www.sto.cx/book-203933-145.html'
aBook = book_reader(url)

print(aBook.getBookName())
print(aBook.getChapterTitle())
print(aBook.getContent())
print(aBook.haveNext())
print(aBook.getNext())
print(aBook.getBookName())
print(aBook.getChapterTitle())
print(aBook.getContent())
print(aBook.haveNext())
aBook.closePage()