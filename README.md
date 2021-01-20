# CCASS_shareholdings

Create Shareholdings object with below parameters__
  :param stock_code: int__
  :param start_date: datetime.date__
  :param end_date: datetime.date__

run the function trend_plot__
  1) to generate top 10 shareholdings time series plot 'top_10_plot.png'__
  2) to generate csv file 'tabular_data.csv' as table with filter in excel__

run the function transaction_finder with below parameter__
  :param threshold: float > 0 e.g. threshold = 0.01 => 1.0%__
  to generate csv file 'transaction_report.csv' which lists out all potential transaction participants for corresponding threshold
