#!/usr/bin/env python
# coding: utf-8

# ### Using stock twits API

# In[31]:


# create these from the 
client_key = '929ad641389be415'
redirect_url = 'https://sphaeric.ai'


# ### Create url

# In[33]:


auth_url = 'https://api.stocktwits.com/api/2/oauth/authorize?client_id={}&response_type=token&redirect_uri={}&scope=read,watch_lists,publish_messages,publish_watch_lists,follow_users,follow_stocks'.format(client_key, redirect_url)


# In[35]:


# print url
auth_url


# Paste the auth_url into a web browser. After redirecting to your webpage, copy the access_token which is returned in the web broswer URL. Save the access token. 

# In[36]:


# identify access token
access_token = 'a9fdc62bc09b74f449af4bf89b08f2f2c4d9dc2a'


# In[37]:


print('complete...')


# In[ ]:





# ### End
