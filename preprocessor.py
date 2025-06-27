import pandas as pd
import re


def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}"
    message = re.split(pattern, data)[1:]  # <- this fixes the length mismatch
    date = re.findall(pattern, data)

    df = pd.DataFrame({'message': message, 'date': date})
    df['Date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M')

    extracted = df['message'].str.extract(r"- (.*?): (.*)")
    extracted = extracted.fillna(" ")
    sender = extracted[0]
    text = extracted[1]

    df['Sender'] = sender
    df['message'] = text
    df['Day_name']= df['Date'].dt.day_name()
    df['month_num']= df['Date'].dt.month
    df['year'] = df['Date'].dt.year
    df['only_date'] = df['Date'].dt.date
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    return df
