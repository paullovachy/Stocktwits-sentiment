#!/usr/bin/env python
# coding: utf-8

# ### Load libs

# In[1]:


import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

n = 200
pd.set_option('display.max_rows', n)
pd.set_option('display.max_columns', n)


# In[2]:


today = str(datetime.now())[0:10]


# ### Set credentials and project

# In[3]:


# access token
access_token = 'xxxxxxxxxxx'


# In[4]:


# type of stocks
stocks_name = 'Tech'


# In[5]:


# set tickers
tickers = ['AAPL', 'MSFT', 'GOOG']


# ### Create functions

# In[6]:


def get_info(ticker, access_token):
    
    print('getting messages for {}...'.format(ticker))
    
    
    """
    Function to parse stocktwits json formatted data into df
    """
    
    # make request
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    company_url = 'https://api.stocktwits.com/api/2/streams/symbol/{}.json'.format(ticker)
    response = requests.get(company_url, headers = header).json()
    
    # get messages
    messages = response['messages'] if 'messages' in response else ''
    
    # parse messages
    holder = []
    for message in messages:

        user = message['user'] if 'user' in message else ''
        likes = message['likes'] if 'likes' in message else ''
        entities = message['entities'] if 'entities' in message else ''
        
        message_dict = {}
        message_dict['id'] = message['id'] if 'id' in message else ''
        message_dict['body'] = message['body'] if 'body' in message else ''
        message_dict['created_at'] = message['created_at'] if 'created_at' in message else ''
        message_dict['user_id'] = user['id'] if 'id' in user else ''
        message_dict['join_date'] = user['join_date'] if 'join_date' in user else ''
        message_dict['followers'] = user['followers'] if 'followers' in user else ''
        message_dict['following'] = user['following'] if 'following' in user else ''
        message_dict['likes'] = likes['total'] if 'total' in likes else ''
        try:
            message_dict['sentiment'] = entities['sentiment']['basic'] if 'basic' in entities['sentiment'] and 'sentiment' in entities else ''  
        except:
            message_dict['sentiment'] = ''
        
        holder.append(message_dict)
        
    # return df
    columns = ['id', 'body', 'sentiment', 'created_at', 'user_id', 'join_date', 'followers', 'following', 'likes']
    df = pd.DataFrame(holder, columns = columns)
    
    print('complete!')
    
    return df


# In[7]:


analyser = SentimentIntensityAnalyzer()
def get_vader_sent(text):
    
    """
    Get vader sentiment from text.
    """
    
    text = str(text)
    responses = analyser.polarity_scores(text)
    sent = responses['compound']
    
    return sent


# In[8]:


def vader_df(row, column):
    
    """
    Apply vader to df.
    """
    
    text = str(row[column])
    
    sent = get_vader_sent(text)
    
    return sent


# ### Apply functions on stocks data

# In[9]:


master_df = pd.DataFrame()

for ticker in tickers:
    
    df = get_info(ticker, access_token)
    
    master_df = master_df.append(df).reset_index(drop = True)
    
    print('------------------------------------')
    
    


# In[10]:


# apply sentiment to df
master_df['sentiment_score'] = master_df.apply(vader_df, args = ('body', ), axis = 1)


# In[11]:


master_df


# ### Export results

# In[12]:


# set export
folder = 'data/'
file = '{} messages {}.xlsx'.format(stocks_name, today)
path = folder + file
path


# In[13]:


# export
master_df.to_excel(path, encoding='utf8', index = False)


# In[14]:


print('complete...')


# In[ ]:





# ### End 
