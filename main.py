import requests
from datetime import datetime, timedelta
from twilio.rest import Client

# START OF STOCK VARIABLES AND DATA
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = ""
CURRENT_DAY = datetime.now().strftime("%Y-%m-%d")
PREVIOUS_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
STOCK_API = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&outputsize=full&apikey={API_KEY}'
stock_data = requests.get(STOCK_API).json()
current_day_stock_info = stock_data['Time Series (Daily)'][CURRENT_DAY]
current_day_high = float(current_day_stock_info['2. high'])
current_day_low = float(current_day_stock_info['3. low'])
previous_date_stock_info = stock_data['Time Series (Daily)'][PREVIOUS_DATE]
previous_day_close = float(previous_date_stock_info['4. close'])
percentage_diff = round(float(((current_day_high - previous_day_close) / current_day_high) * 100), 2)

# Texting Variables
account_sid = ''
auth_token = ''
send_to = ''
text_message = ''

# NEWS DATA AND API
API_KEY = ''
NEWS_API = f"https://newsapi.org/v2/everything?q=tesla&from={PREVIOUS_DATE}&sortBy=publishedAt&apiKey={API_KEY}"

up_down = None

if percentage_diff > 0:
    up_down = '🔺'
else:
    up_down = '🔻'

if percentage_diff >= 1:
    tesla_data = requests.get(NEWS_API).json()['articles']
    three_articles = tesla_data[:3]
    formatted_article = [(f'{STOCK}: {up_down}{percentage_diff}% Headline: {article["title"]}. '
                          f'\nBrief: {article["description"]}') for article in three_articles]

    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages.create(
            from_='+18334630475',
            body=article,
            to=send_to
        )
        print(message.status)
