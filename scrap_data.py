
import requests
import datetime

from bs4 import BeautifulSoup

class WebCrawler:

    REQUEST_URL = 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx'

    HEADERS = {
        'authority': 'www.hkexnews.hk',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.hkexnews.hk',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.hkexnews.hk/sdw/search/searchsdw.aspx',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        #'cookie': 'WT_FPC=id=104.84.150.76-2472912240.30861935:lv=1610876319661:ss=1610875985728; TSfff9c5ca027=086f2721efab20001fd534604d2e9805470d23b9cfe45ea9c78ea59e46fa6b96385efff16f5493c708ad703bde113000ea123ad9b82262cd751f2b02e9d111ee71a2bde58f8064d28888143c825e78608b4c30f3ee191bab731305ae23e007ae; TS6b4c3a62027=08754bc291ab2000a60f46ce8f9c32efc0bf8bcbe2445c23c780f6448fb60a354e548db2dfe10c4d08eee1a0091130009cea1c7ac00d814aca3bbba39867dae8066e9e3219e9def09259a79344a1a36aaa385f6947522e606c5999633b939545; TS6b4c3a62027=08754bc291ab20000ecde6c4bf6366221cd06636ca820b3e1295617a873c6b11a95cb028d9bb60ec084e2f050a113000186ce1ea29200156c23119743bb3c9761943dc9b3c90f270af3a1541210def0d0037f278a4aef0c39d6379b338558879'
    }

    def __init__(self,stock_code,search_date):
        '''

        :param stock_code: int
        :param search_date: datetime.date
        '''
        self.stock_code = stock_code
        self.search_date = search_date
        self.PAYLOAD  = '__EVENTTARGET=btnSearch&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTIwNTMyMzMwMThkZLiCLeQCG%2FlBVJcNezUV%2FJ0rsyMr&__VIEWSTATEGENERATOR=A7B2BBE2&today={}&sortBy=shareholding&sortDirection=desc&' \
                                 'alertMsg=&txtShareholdingDate={}%2F{}%2F{}&txtStockCode={}&txtStockName=&txtParticipantID=&txtParticipantName=&txtSelPartID='.format(datetime.date.today().strftime('%Y%M%d'),self.search_date.year,str(self.search_date.month).zfill(2),str(self.search_date.day).zfill(2),str(self.stock_code).zfill(5))

    def send_request(self):

        self.response = requests.request("POST", WebCrawler.REQUEST_URL, headers=WebCrawler.HEADERS, data=self.PAYLOAD)

    def parse_table(self):
        soup = BeautifulSoup(self.response.content, 'html.parser')
        table = soup.find("table", attrs={"class": "table table-scroll table-sort table-mobile-list"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        data = []
        for r in rows:
            cols = r.find_all('td')
            cols = [x.text.strip() for x in cols]
            data.append([x for x in cols if x])

        self.data_dict = {}
        self.data_dict['shareholdings'] = {}
        self.data_dict['shareholdings_pct'] = {}
        for d in data:
            if len(d[0].split('\n')) > 1:
                id = (d[0].split('\n')[-1], d[1].split('\n')[-1])
            else:
                id = (None, d[1].split('\n')[-1])
            self.data_dict['shareholdings'][id] = float(d[3].split('\n')[-1].replace(',', ''))
            self.data_dict['shareholdings_pct'][id] = float(d[4].split('\n')[-1].replace('%', ''))

    def run(self):
        self.send_request()
        self.parse_table()
