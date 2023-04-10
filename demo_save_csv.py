import bs4 as bs
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import csv

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    key = input('Please enter the term : ') #'Hotels'
    lokasi = input('Please enter location too : ') #'London'
    datas = []
    for hal in range(1,3):
        url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords={}&location={}&scrambleSeed=1553628242&pageNum='.format(key, lokasi)+str(hal)
        page = Page(url)
        
        soup = bs.BeautifulSoup(page.html, 'html.parser')
        js_test = soup.find_all('div', class_='businessCapsule--mainRow')
        for it in js_test:
            name =it.find('h2', 'businessCapsule--name text-h2').text
            try : alamat = ''.join(it.find('span', {'itemprop':"address"}).text.replace('We serve', '').replace('|', ' ').strip().split('\n'))
            except: alamat = ""
            try : web = it.find('a', {'rel': 'nofollow noopener'})['href'].replace('http://', '').replace('www.', '').replace('https://', '').split('/')[0]
            except : web = ''
            try : telp = it.find('span', 'business--telephoneNumber').text
            except : telp = ''
            image = it.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
            if 'http' not in image:
                image = 'https://www.yell.com{}'.format(image)
            
            datas.append([name, alamat, web, telp, image])

    head = ['Name', 'Address', 'Website', 'Phone Number', 'Image URL']
    writer = csv.writer(open('results/{}_{}.csv'.format(key, lokasi), 'w', newline=''))
    writer.writerow(head)
    for d in datas:
        writer.writerow(d)
            


if __name__ == '__main__': main()