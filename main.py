import requests
from datetime import timedelta, date
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = "5GUEXU8027S46T1V"
alhpa_url = "https://www.alphavantage.co/query"
NEWS_API_KEY = "47d1581cba8d4559bba639c9632d4657"
news_url = "https://newsapi.org/v2/everything"
account_sid = "AC4a180f059febe490c20d7ae861822b0b"
auth_token = "81867abe67c7e1f27f10a2bf0e6f53c3"

parameters_alpha = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY,
}

yesterday = date.today() - timedelta(days=1)
before_yesterday = date.today() - timedelta(days=2)
response = requests.get(alhpa_url, params=parameters_alpha, verify=False)
response.raise_for_status()
data = response.json()
yesterday_value = float(data['Time Series (Daily)'][f"{yesterday}"]['4. close'])
before_yesterday_value = float(data['Time Series (Daily)'][f"{before_yesterday}"]['4. close'])
percentage = round((1 - before_yesterday_value/yesterday_value) * 100)

up_down = None
if percentage >= 0:
    up_down = "🔺"
else:
    up_down = "invers"

if percentage not in range(-5, 6):
    last_month = date.today() - timedelta(days=25)

    parameters_news = {
        "q": "tesla",
        "from": f"{last_month}",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(news_url, params=parameters_news, verify=False)
    response.raise_for_status()
    data = response.json()
    articles = data["articles"][:3]
    result = [f"{STOCK}: {up_down}{percentage}%\nHeadline: {article['title']}\nBrief: {article['description']}\n" for article in articles]

    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body="".join(result),
            from_="+12058093489",
            to="+",
    )

    print(message.status)
