import os
from twilio.rest import Client
import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key = os.environ.get("OWM_KEY")
auth_token = os.environ.get("AUTH_TOKEN")
account_sid = "ACf21e6506da5233d77a936d156f5890db"
PHONE_NUM = "+17627603600"

newsapi_key = "073f56d1aab84054abd24e5a1a42711d"
STOCK_API_KEY = "YBUXLP9Z47UWWDY8"

stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK ,
    "apikey": STOCK_API_KEY,
}

news_params = {
    "qInTitle": STOCK,
    "searchIn": "title",
    "apiKey": newsapi_key,
}

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.

daily_closings = []
stock_response = requests.get(STOCK_ENDPOINT, params=stock_param)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()]  # List comprehension. Stock_data is a dictionary.
# print(stock_data_list)
for each in stock_data_list:
    daily_closings.append(float(each["4. close"]))

# HINT 2: Work out the value of 5% of yesterday's closing stock price.

yesterday_closing = daily_closings[0]
day_b4_yesterday_closing = daily_closings[1]
# print(yesterday_closing, day_b4_yesterday_closing)

closing_delta = yesterday_closing - day_b4_yesterday_closing
closing_delta = abs(round(closing_delta, 2))
# print(closing_delta)

if yesterday_closing > day_b4_yesterday_closing:
    mkt_direction = "🔺"
else:
    mkt_direction = "🔻"

delta_percent = round(closing_delta / yesterday_closing * 100, 2)
# print(delta_percent)

if delta_percent > 2:
    print(f"{news_params['qInTitle']}{mkt_direction}{delta_percent}%")

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    # HINT 1: Consider using a List Comprehension.

    sr_num = 1
    for each in news_data["articles"][:3]:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"{news_params['qInTitle']}{mkt_direction}{delta_percent}%\n{sr_num}.Headline: {each['title']}\nBrief: {each['description']}\n",
            from_=PHONE_NUM,
            to="+91 81058 06082"
        )
        sr_num += 1
        print(message.status)
