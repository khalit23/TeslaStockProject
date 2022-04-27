import requests
import os
from twilio.rest import Client

SID = "ACb344da34ea2bb8427164f099282c5192"
AUTH_TOKEN = "6c8915974d573544f0183361b84b13b9"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API_KEY = "11d67d2ad93c49208c5887a494a61437"
STOCK_API_KEY = "QZ9WA99WZ1AZ4QCJ"

news_params = {
    "q": STOCK,
    "apiKey": NEWS_API_KEY
}

stock_params = {
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}


def stock_percentage_change():
    response = requests.get(url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY", params=stock_params)
    data = response.json()
    daily_data = data["Time Series (Daily)"]
    stock_date_list = list(data["Time Series (Daily)"])
    today = stock_date_list[0]
    yesterday = stock_date_list[1]
    today_price = int(float(daily_data[today]["4. close"]))
    yesterday_price = int(float(daily_data[yesterday]["4. close"]))

    percentage_change = ((today_price - yesterday_price) / yesterday_price) * 100

    return percentage_change


def news_info():
    response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)

    data = response.json()
    articles = data["articles"]
    first_three = articles[:4]
    articles_headlines = []

    for n in range(3):
        articles_headlines.append(first_three[n]["title"])

    return articles_headlines


change_in_price = stock_percentage_change()
articles = news_info()

if change_in_price <= -3:
    account_sid = SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"""
        TSLA: 🔻{round(change_in_price, 2)}% 
        THESE ARE THE MOST RECENT HEADLINES:
        Headline 1: {articles[0]}
        Headline 2: {articles[1]}
        Headline 3: {articles[2]}
        """,
        from_='+19034195836',
        to='+447397564228'
    )

    print(message.status)

if change_in_price > 3:
    account_sid = SID
    auth_token = AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"""
            TSLA: 🔺{round(change_in_price, 2)}% 
            THESE ARE THE MOST RECENT HEADLINES:
            Headline 1: {articles[0]}
            Headline 2: {articles[1]}
            Headline 3: {articles[2]}
            """,
        from_='+19034195836',
        to='+447397564228'
    )

    print(message.status)
