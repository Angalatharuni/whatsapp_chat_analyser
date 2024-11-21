#writing functions here
from collections import Counter
import emoji
import nltk
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords



# Ensure the stopwords are downloaded
nltk.download('stopwords')

# Get the list of stopwords for English
stop_words = set(stopwords.words('english'))

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    #number of messages
    num_messages=df.shape[0]

    #number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    #number of media messages
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    #number of links
    extractor=URLExtract()
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # x=df['user'].value_counts() all users freq
    x = df['users'].value_counts().head()
    df=(round(df['users'].value_counts()/df.shape[0]*100,2)).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def remove_stop_words(message):
    words = [word for word in message.lower().split() if word not in stop_words]
    return ' '.join(words)

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # remove group notifications and media omitted messages
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]

    # remove group notif and media ommited

    temp=df[df['users']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)