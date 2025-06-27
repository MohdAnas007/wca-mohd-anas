from urlextract import URLExtract
import matplotlib.pyplot as plt
import emoji
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
extracter = URLExtract()

def fetch_stats(selected_user, df):
    # If specific user is selected, filter the DataFrame
    if selected_user != 'Overall':
        df = df[df['Sender'] == selected_user]

    # Total messages
    num_messages = df.shape[0]

    # Total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Media messages
    media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Links
    links = []
    for message in df['message']:
        links.extend(extracter.find_urls(message))

    return num_messages, len(words), media_messages, len(links)


# // fetch most busy user

def most_busy_user(df):
    x = df['Sender'].value_counts().head()
    df=round((df['Sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'Sender': 'User', 'Count': 'Percent'})

    return x,df


#  creating word cloud

def Word_cloud(selected_user,df):
    if selected_user!='Overall':
       df = df[df['Sender'] == selected_user]


    wc=WordCloud(background_color='white',height=500,width=500,min_font_size=10)
    word=wc.generate(df['message'].str.cat(sep=" "))
    return word

# Most common words

def most_common_words(selected_user,df):
    f = open('/Users/anaszhcet2024/Whatsapp-Chat-Analyser/hinglish Stop_words', 'r')
    stop_words = f.read()

    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]

    temp = df[df['message'] != '<Media omitted>']



    words = []
    for i in temp['message']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# most common emojis

def emojis_used(selected_user,df):
    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]


    Emoji_list=[]
    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                Emoji_list.extend(c)

    return pd.DataFrame(Counter(Emoji_list).most_common(20))


def monthly_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]

    a = df['Date'].dt.month
    df.loc[:, 'month_num'] = a

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    timeline

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]
    b = df['Date'].dt.date
    df.loc[:, 'only_date'] = b
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



def Activity_map(selected_user,df):

    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]

    c = df['Date'].dt.day_name()
    df.loc[:, 'Day_name'] = c
    activity=df['Day_name'].value_counts().reset_index().rename(columns={'count':'Messages'})
    return activity


def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['Sender'] == selected_user]

    return df['month'].value_counts()














