
import time
import random

import pandas as pd
import matplotlib.pyplot as plt

import scrap_data

class Shareholdings:

    def __init__(self, stock_code, start_date, end_date):
        '''

        :param stock_code: int
        :param start_date: datetime.date
        :param end_date: datetime.date
        '''
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date

    def scrap_all(self):
        self.full_dict = {}
        self.full_pct_dict = {}
        for d in pd.date_range(self.start_date,self.end_date):
            w = scrap_data.WebCrawler(self.stock_code,d.date())
            w.run()
            self.full_dict[d.date()] = w.data_dict['shareholdings']
            self.full_pct_dict[d.date()] = w.data_dict['shareholdings_pct']
            time.sleep(3.0 + random.random() * 1.5)
        self.sh_dict = {}
        self.sh_pct_dict = {}
        for (d,dd) in self.full_dict.items():
            for (id,sh) in dd.items():
                if id not in self.sh_dict.keys():
                    self.sh_dict[id] = {}
                self.sh_dict[id][d] = sh
        for (d,dd) in self.full_pct_dict.items():
            for (id,sh) in dd.items():
                if id not in self.sh_dict.keys():
                    self.sh_dict[id] = {}
                if id not in self.sh_pct_dict.keys():
                    self.sh_pct_dict[id] = {}
                self.sh_pct_dict[id][d] = sh

    def trend_plot(self):
        self.get_top_10()
        self.plot_top_10()
        self.display_tabular_data()

    def get_top_10(self):

        last_dict = self.full_dict[self.end_date]
        ls = last_dict.items()
        ls.sort(key=lambda x: x[1], reverse=True)
        kls = ls[:10]
        self.top10 = [x[0] for x in kls]

    def plot_top_10(self):

        top10_dict = {k: v for (k, v) in self.sh_dict.items() if k in self.top10}
        df = pd.DataFrame(top10_dict)
        df.plot(legend=True,figsize=(15,10))
        plt.legend(bbox_to_anchor=(1.0, 0.5))
        plt.show()
        plt.savefig('top_10_plot.png')

    def display_tabular_data(self):
        '''

        :return: generate csv file to be viewed in excel as table with filter
        '''
        pd.DataFrame(self.sh_dict).to_csv('tabular_data.csv')

    def transaction_finder(self,threshold):
        '''
        :param threshold: float > 0 e.g. threshold = 0.01 => 1.0%

        generate csv file which lists out all potential transaction participants for corresponding threshold
        '''
        t = threshold * 100.0
        transaction_dict = {}
        ddf = pd.DataFrame(self.sh_pct_dict)
        df_pct_change = ddf.diff()
        df_pct_change = df_pct_change.iloc[1:, :]
        for (d,r) in df_pct_change.iterrows():
            transaction_dict[d] = [x for x in list(r.items()) if
             isinstance(x[1], float) and abs(x[1]) > t]

        with open('transaction_report.csv', 'w') as f:
            f.write('stock code:{}\n'.format(self.stock_code))
            f.write('threshold:{}%\n'.format(t))
            f.write('start date:{}\n'.format(self.start_date))
            f.write('end date:{}\n\n'.format(self.end_date))
            f.write('date,name,shareholdings_pct_change\n')
            for (d, ls) in transaction_dict.items():
                for (id, pc) in ls:
                    f.write('{},{},{}%\n'.format(d, id[1].replace(',',''), round(pc, 3)))






