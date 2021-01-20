# CCASS_shareholdings

Create Shareholdings object with below parameters
  :param stock_code: int
  :param start_date: datetime.date
  :param end_date: datetime.date

run the function trend_plot
  1) to generate top 10 shareholdings time series plot 'top_10_plot.png'
  2) to generate csv file 'tabular_data.csv' as table with filter in excel

run the function transaction_finder with below parameter
  :param threshold: float > 0 e.g. threshold = 0.01 => 1.0%
  to generate csv file 'transaction_report.csv' which lists out all potential transaction participants for corresponding threshold
