#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import re

#imports the collected data from the CSV format and save the data as different 
df_imdb = pd.read_csv('./data/imdb_data.csv', index_col=0) #IMDB Data Frame
df_directors = pd.read_csv('./data/imdb_directors_data.csv', index_col = 0) #this is from IMDB webscraper but is just a specific subset of data seperated for visualizations
df_metacritic = pd.read_csv('./data/metacritic_data.csv', index_col=0) #Metacritic DataFrame
df_tmdb = pd.read_csv('./data/tmdb_data.csv', index_col=0) #TMDB data frame 

#images used for the visualization portion of the assignment collected through a file path generated and scraped from TMDB
godfather1 = ('./data/1_godfather.jpg') 
godfather2 = ('./data/2_godfather.jpg') 
angrymen = ('./data/3_angrymen.jpg') 
lord = ('./data/4_lordofrings.jpg')
pulpfuction = ('./data/5_pulpfiction.jpg') 
casablanca = ('./data/6_casablanca.jpg') 
rearwindow =('./data/7_rearwindow.jpg')
vertigo = ('./data/8_vertigo.jpg') 
citylights = ('./data/9_citylights.jpg') 


#This read the data in the data frame so the CSV files dont have to be uploaded in visualizations file 
#Read IMDB Data Frame
for data in df_imdb: 
    if df_imdb[data].dtype == 'object': 
        df_imdb[data] = df_imdb[data].fillna('')
    else: 
        df_imdb[data] = df_imdb[data].fillna(0)


#Reads the Metacritic Data Frame and removes NAN values 
for data in df_metacritic:
    if df_metacritic[data].dtype == 'object': 
        df_metacritic[data] = df_metacritic[data].fillna('')
    else: 
        df_metacritic[data] = df_metacritic[data].fillna(0)


#Reads the TMDB Data Frame and remove NaN values 
for data in df_tmdb:
    if df_tmdb[data].dtype == 'object': 
        df_tmdb[data] = df_tmdb[data].fillna('')
    else: 
        df_tmdb[data] = df_tmdb[data].fillna(0)


#Reads the IMDB Directors Data Frame and removes NaN values, this dataframe was collected from the IMDB webscrapper
for data in df_directors: 
    if df_directors[data].dtype == 'object': 
        df_directors[data] = df_directors[data].fillna('')
    else: 
        df_directors[data] = df_directors[data].fillna(0)
        


