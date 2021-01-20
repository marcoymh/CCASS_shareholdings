# CCASS_shareholdings

## Step 1
Create Shareholdings object with below parameters\
  &nbsp;&nbsp;:param stock_code: int\
  &nbsp;&nbsp;:param start_date: datetime.date\
  &nbsp;&nbsp;:param end_date: datetime.date

## Step 2
run the function trend_plot\
  1) to generate top 10 shareholdings time series plot 'top_10_plot.png'
  2) to generate csv file 'tabular_data.csv' as table with filter in excel

## Step 3
run the function transaction_finder with below parameter\
  &nbsp;&nbsp;:param threshold: float > 0 e.g. threshold = 0.01 => 1.0%\
  &nbsp;&nbsp;to generate csv file 'transaction_report.csv' which lists out all potential transaction participants for corresponding threshold
