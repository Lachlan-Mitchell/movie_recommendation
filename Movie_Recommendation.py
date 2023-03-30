#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


credits_df = pd.read_csv("credits.csv")
movies_df = pd.read_csv("movies.csv")


# In[3]:


credits_df


# In[4]:


movies_df


# Allows us to see all rows and columns!

# In[5]:


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# You can uncomment these to see the whole table


# In[6]:


credits_df


# In[7]:


movies_df


# Combine datasets

# In[8]:


movies_df = movies_df.merge(credits_df, on ='title')


# In[9]:


movies_df.shape #shows columns total and rows total, (23 columns because the title is where we are joining)


# In[10]:


movies_df.head()


# In[11]:


movies_df.info() #gives a breakdown of the table


# In[12]:


movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords','cast','crew']] #Reducing the datset to the topics we will use


# In[13]:


movies_df.head()


# In[14]:


movies_df.info() #Reduced down to the columns we will actually use


# In[15]:


#Checking for missing values 
movies_df.isnull().sum()


# In[16]:


#modififes the dataframe directly,  will remove any rows in the movies_df dataframe that contain missing values (i.e., NaN or null values). dropna() comes from Pandas!
movies_df.dropna(inplace= True) 


# In[17]:


movies_df.duplicated().sum() #checks for duplicates


# In[18]:


movies_df.iloc[0].genres #The iloc(), comes from pandas, selects a specific name and from dataset, this willgive us the genre brekadown of the first movie, in this case genre


# In[19]:


import ast


# In[20]:


def convert(obj):
    L = []
    for item in ast.literal_eval(obj):
        L.append(item["name"])
    return L


# In[21]:


#This eventually worked...
movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)


# In[22]:


movies_df.head()


# In[23]:


# movies_df['keywords'] = movies_df['keywords'].apply(convert)


# In[24]:


movies_df.head()


# In[25]:


def main_cast(obj):
    L=[]
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L


# In[26]:


movies_df['cast'] = movies_df['cast'].apply(main_cast) #Just took the main actor


# In[27]:


movies_df.head()


# In[28]:


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L


# In[29]:


movies_df['crew'] = movies_df['crew'].apply(fetch_director)


# In[30]:


movies_df.head()


# In[31]:


movies_df['overview'][0] #lets us see the full overview of the first movie of the df.


# In[32]:


movies_df['overview'] = movies_df['overview'].apply(lambda x:x.split()) #makes overview an array of words


# In[33]:


movies_df.head()


# In[34]:


#Removes spaces in names, of arrays this will help later on
movies_df['genres'] = movies_df['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['keywords'] = movies_df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['cast'] = movies_df['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['crew'] = movies_df['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[35]:


movies_df.isnull().sum() #cast had null properties


# In[36]:


movies_df.dropna(inplace= True) #When we took the main cast, some movies didnt have a main cast member, we need to remove them now


# In[37]:


movies_df.isnull().sum()


# In[38]:


movies_df.head()


# In[39]:


movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']


# In[40]:


movies_df.head()


# In[41]:


movies_df['tags'][0]


# In[42]:


new_movies_df = movies_df[['movie_id','title','tags']].copy() #making a new dataframe, tags is representative of all the other columns, making a copy because it was throwing warning when i tried to modify tags, letting me know that it was only making changes to the copy and not the original


# In[43]:


new_movies_df.head()


# In[44]:


new_movies_df['tags'] = new_movies_df['tags'].apply(lambda x:' '.join(x))


# In[45]:


new_movies_df.head() #now makes tags a string


# In[46]:


new_movies_df['tags'][0]


# In[47]:


new_movies_df['tags']= new_movies_df['tags'].apply(lambda x:x.lower()) #makes tags all lowercase, will help later


# In[48]:


new_movies_df.head()


# In[49]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words='english') #Stop_words = "english", removes words such as the, and, an, a. from being a feature.


# In[50]:


cv.fit_transform(new_movies_df['tags']).toarray().shape


# In[51]:


vectors = cv.fit_transform(new_movies_df['tags']).toarray()


# In[52]:


vectors[0]


# In[53]:


len(cv.get_feature_names_out()) #


# In[54]:


import nltk #natural language tool kit, text processing lib


# In[55]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[56]:


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[57]:


new_movies_df['tags'] = new_movies_df['tags'].apply(stem)


# In[58]:


from sklearn.metrics.pairwise import cosine_similarity


# In[59]:


cosine_similarity(vectors)


# In[60]:


cosine_similarity(vectors).shape


# In[61]:


similarity = cosine_similarity(vectors)


# In[62]:


similarity[0]


# In[63]:


similarity[0].shape


# In[64]:


sorted(list(enumerate(similarity[0])), reverse= True, key= lambda x:x[1])[1:10]


# In[65]:


def recommend(movie):
    try:
        movie_index = new_movies_df[new_movies_df['title']==movie].index[0]
    except IndexError:
        return "Sorry, the movie title that you requested does not appear to be in my database. Please try another movie!"
    
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key= lambda x:x[1])[1:10]
    
    for i in movies_list:
        print(new_movies_df.iloc[i[0]].title)
        


# In[66]:


recommend('Avatar')


# In[67]:


recommend('Iron Man')


# In[68]:


recommend('Liar Liar')


# In[69]:


recommend('The Avengers')


# In[70]:


recommend('John Wick')


# In[71]:


recommend('The Lion King')


# In[72]:


recommend('The Addams Family')

