#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm
StreamlitPatcher().jupyter()  # register streamlit with jupyter-compatible wrappers
import pandas as pd
import plotly.express as px
import numpy as np


# In[2]:


# Toggling the season here updates all data below
season = 'Summer'


# In[3]:


athlete_df = pd.read_csv('Olympic_Athlete_Event_Results.csv', usecols=['edition', 'athlete'])
athlete_df[['year', 'season']] = athlete_df['edition'].str.split(' ', expand=True, n=1)

athlete_df['year'] = athlete_df['year'].astype(int)

# Remove "Olympics" from "Summer/Winter Olympics"
athlete_df['season'] = athlete_df['season'].str.split(' ', n=1).str[0]

# rename the column to be uniform with the DataFrame we will merge with later
# not necessary, but helpful to simplify our data
athlete_df = athlete_df.rename(columns={'athlete': 'name'})
athlete_df = athlete_df[athlete_df['season'] == season]

athlete_df.head


# In[5]:


sex_df = pd.read_csv('Olympic_Athlete_Bio.csv', usecols=['name', 'sex', 'country'])
sex_df = sex_df[sex_df['sex'] == 'Female']
sex_df


# In[6]:


df = athlete_df.merge(sex_df, on='name').sort_values('year')
len(df.index)


# In[7]:


appearances = df.groupby(['year', 'country']).size().reset_index(name='country_appearances')
df = df.merge(appearances, on=['year', 'country'])
df


# In[8]:


df.to_csv("women-summer.csv")


# In[9]:


def powspace(start, stop, power, num):
    '''
    start: first endpoint of resulting array
    stop: last endpoint of resulting array
    power: power to use when spacing out points in array
    num: number of points in resulting array
    '''
    start = np.power(start, 1/float(power))
    stop = np.power(stop, 1/float(power))
    return np.power(np.linspace(start, stop, num=num), power)


# In[10]:


colorbar_range = df['country_appearances'].min(), df['country_appearances'].max()

# Pick some thematic color scheme
colors = px.colors.sequential.Redor if season == 'Summer' else px.colors.sequential.OrRd

colormap_vals = powspace(start=0, stop=1, power=3, num=len(colors) - 1)
colormap_vals = [(0, colors[0]), *[(colormap_vals[i], colors[i + 1]) for i in range(len(colormap_vals))]]


# In[12]:


fig = px.choropleth(
    df,
    locations="country",
    locationmode='country names',
    color='country_appearances',
    projection='natural earth',
    animation_frame='year',
   #st.subheader("Data Editor")
    title=f'Women {season} Olympics Participation Through The Ages',
    color_continuous_scale=colormap_vals,
    range_color=colorbar_range)

fig.show() 


# In[13]:


fig.write_html("summer_oly_women.html")


# In[ ]:




