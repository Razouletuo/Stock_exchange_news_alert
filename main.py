import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = "292CYLIGB3MX0LVB"
news_api_key = "eb40f3731bcb46d49beba2f0a1429a6e"
ACCOUNT_SID = "AC417c36e521a4caa6bd2831b1eea6e759"
AUTH_TOKEN ="7319d7fc6f680c100e0ab48aa79f17d4"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : stock_api_key,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
print(yesterday_closing)
# - Get the day before yesterday's closing stock price
dayBefore_data = data_list[1]
dayBefore_close = dayBefore_data["4. close"]
print("day before closing: ", dayBefore_close)
# - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing) - float(dayBefore_close))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
#- Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_perc = round((difference / float(yesterday_closing))) * 100
print(diff_perc,"%")
# - If TODO4 percentage is greater than 5 then print("Get News").

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(diff_perc) < 5:
    news_params = {
        "apikey" : "eb40f3731bcb46d49beba2f0a1429a6e",
        "qInTitle" : COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
# - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_perc}%\nHeadline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]
#- Send each article as a separate message via Twilio.
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
#Optional : Format the message like this:
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_= "+17752541810",
            to="+919774745431",
        )

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

