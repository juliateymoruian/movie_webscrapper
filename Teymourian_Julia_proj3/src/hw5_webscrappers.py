#!/usr/bin/env python
# coding: utf-8


import re
import pandas as pd
import requests, bs4
from requests import get
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
from time import sleep
from random import randint
from time import time
import numpy as np
import datetime
import sys
import getopt
import argparse



def metacritic():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    #loop through pages 0 -10 at interval of 2
    pages = [str(i) for i in range(0,10,2)]
    
    #declare lists to stored scraped data
    names = []
    release_dates = []
    ratings= []
    metascores =[]
    userscores = []
    
    #prepare the monitoring loop
    start_time = time()
    requests = 0
    
    for page in pages:
        movies = get('https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page='+ page, headers = headers)
        sleep(randint(8,20))
        requests += 1
        elapsed_time = time() - start_time
        clear_output(wait = True)
        
        if movies.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
            
        if requests > 10:
            warn('Number of requests was greater than expected.')
            break
            
        movie_soup = BeautifulSoup(movies.text, 'html.parser')
        
        for movie in movie_soup.find_all('td', class_ = 'clamp-summary-wrap'):
            name = movie.find('a', class_= 'title').h3.text
            names.append(name)
            
            release_date = movie.find('div', class_='clamp-details').span.text
            release_dates.append(release_date)
            
            try:
                rating = movie.select('div.clamp-details span')[1].text
                ratings.append(rating)
            except Exception as e:
                ratings.append('None')
                
            metascore= movie.select('a.metascore_anchor div')[0].text
            metascores.append(metascore)
            
            userscore = movie.select('a.metascore_anchor div')[2].text
            userscores.append(userscore)
            
        metacritic_df = pd.DataFrame({'Movie': names,'Year': release_dates,'Ratings': ratings,'Metascores': metascores,'Userscores': userscores})
        
        tbr = ['tbd']
        
        #change value type of Userscore and Metascore to float 
        metacritic_df['Userscores'] = metacritic_df['Userscores'].apply(lambda x: np.nan if x in tbr else x)
        metacritic_df = metacritic_df.dropna(axis=0, how='any')
        metacritic_df['Userscores'] = metacritic_df['Userscores'].astype(float)*10 #needs to be mutlipled by 10 for comparesion to user scores
        metacritic_df['Metascores'] = metacritic_df['Metascores'].apply(lambda x: np.nan if x in tbr else x)
        metacritic_df = metacritic_df.dropna(axis=0, how='any')
        metacritic_df['Metascores'] = metacritic_df['Metascores'].astype(float)
        
        metacritic_df[['Metascores','Userscores']].mean()
        metacritic_df[['Metascores','Userscores']].std()
        
        metacritic_df['Comparison'] = metacritic_df['Metascores'] > metacritic_df['Userscores']
        metacritic_df['Difference'] = metacritic_df['Metascores'] - metacritic_df['Userscores']
        metacritic_df.sort_values('Difference',ascending=False)
    
        metacritic_df.to_csv('metacritic_data.csv')
metacritic()


def metacritic_grade(): 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    pages = [str(i) for i in range(0,3,2)] #only 3 pages of the data are scraped
    
    #declare lists to stored scraped data
    names = []
    release_dates = []
    ratings= []
    metascores =[]
    userscores = []
    
    #prepare the monitoring loop
    start_time = time()
    requests = 0
    
    for page in pages:
        movies = get('https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page='+ page, headers = headers)
        sleep(randint(8,20))
        requests += 1
        elapsed_time = time() - start_time
        clear_output(wait = True)
        
        if movies.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))
            
        if requests > 3:
            warn('Number of requests was greater than expected.')
            break
            
        movie_soup = BeautifulSoup(movies.text, 'html.parser')
        
        for movie in movie_soup.find_all('td', class_ = 'clamp-summary-wrap'):
            name = movie.find('a', class_= 'title').h3.text
            names.append(name)
            
            release_date = movie.find('div', class_='clamp-details').span.text
            release_dates.append(release_date)
            
            try:
                rating = movie.select('div.clamp-details span')[1].text
                ratings.append(rating)
            except Exception as e:
                ratings.append('None')
                
            metascore= movie.select('a.metascore_anchor div')[0].text
            metascores.append(metascore)
            
            userscore = movie.select('a.metascore_anchor div')[2].text
            userscores.append(userscore)
            
        metacritic_df = pd.DataFrame({'Movie_names': names,'Release_dates': release_dates,'Ratings': ratings,'Metascores': metascores,'Userscores': userscores})
        metacritic_df.to_csv('metacritic_grader_data.csv')


def tmdb_scraper():
    df=[]
    for i in range(10):
        url = "https://api.themoviedb.org/3/movie/top_rated?api_key=e55f2333a991d69c2a13199b8e1e4e40&language=en-US&page="
        JSON = requests.get(url+str(i+1)).json()
        result=JSON['results']
        for item in result:
            df.append([item['id'],item['title'], item ['genre_ids'],item['overview'],item['release_date'],item['popularity'],item['vote_average'],item['vote_count'],item['poster_path']])
            tmdb_df=pd.DataFrame(df)
            tmdb_df.columns=['Id','Movie','Genre_Ids','Overview','Year','Popularity','Vote_Average','Vote_Count', 'Poster']
            tmdb_df.to_csv('tmdb_data.csv')


def tmdb_grader():
    df=[]
    for i in range(10):
        url = "https://api.themoviedb.org/3/movie/top_rated?api_key=e55f2333a991d69c2a13199b8e1e4e40&language=en-US&page="
        JSON = requests.get(url+str(i+1)).json()
        result=JSON['results']
        for item in result:
            df.append([item['id'],item['title'], item ['genre_ids'],item['overview'],item['release_date'],item['popularity'],item['vote_average'],item['vote_count'],item['poster_path']])
            tmdb_df=pd.DataFrame(df)
            tmdb_df.columns=['Id','Title','Genre_Ids','Overview','Year','Popularity','Vote_Average','Vote_Count', 'Poster']        
            tmdb_df.head(50).to_csv('tmdb_grader.csv')


def imdb_scraper():
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    pages = ['0','101','201','301','401','501','601','701','801','901']
    
    titles = []
    years = []
    time = []
    imdb_ratings = []
    votes = []
    us_gross = []
    director = []
    genres = [] 
    description = [] 
    age_ratings = [] 
    actors = []
    meta_score = [] 
    
    for start_itr in pages:
        response = get('https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start='+start_itr+'&ref_=adv_prv',headers = headers)
        soup = BeautifulSoup(response.text,"html.parser")
        movies = soup.find_all('div', class_='lister-item mode-advanced')
        
        
        for stuff in movies:
            #find the name of the film 
            name = stuff.h3.a.text
            titles.append(name)
            
            #finds the year of the film 
            year = stuff.h3.find('span', class_='lister-item-year').text
            years.append(year)
            
            #find the length of the film in minutes
            length = stuff.find('span',class_='runtime').text if stuff.p.find('span', class_='runtime').text else '-'
            time.append(length)
            
            #find the films imdb rating 
            ratings = float(stuff.strong.text)
            imdb_ratings.append(ratings)
            
            #finds the amount of votes the film has 
            voters = stuff.find_all('span',attrs={'name':'nv'})
            vote = voters[0].text
            votes.append(vote)
            
            #finds the gross of the film
            grosses = voters[1].text if len(voters)>1 else '-'
            us_gross.append(grosses)
            
            #finds the directors name
            directorname = stuff.find('p',class_='').a.text
            director.append(directorname)
            
            #finds the genre of the film
            genre = stuff.find('span',class_='genre').text
            genre = genre.strip()
            genres.append(genre)
            
             #fetching metascore
            score = stuff.find('span', class_='metascore').text if stuff.find('span', class_='metascore') else '-'
            meta_score.append(score)
            
            #finds the description of the film 
            movie_description= stuff.find_all('p', class_ = 'text-muted')[1].text
            movie_description = movie_description.strip()
            description.append(movie_description)
            
            #finds the mpaa reating of the film 
            age = stuff.find('span', class_='certificate').text if stuff.p.find('span', class_='certificate') else 'N/A'
            age_ratings.append(age)
            
            #finds the actors in the film 
            actor = ''.join([str(s) for s in stuff.find_all('p','')[2].text.replace('\n','').strip('\n').split('|')[1].split(':')[1:]])
            actors.append(actor)

    
    #Creating a dataframe
    df_imdb = pd.DataFrame({
        'Movie':titles,
        'Year':years,
        'Time':time,
        'IMDB Rating':imdb_ratings,
        'Film Rating':age_ratings,
        'Metascore': meta_score,
        'Votes':votes,
        'US Gross Millions':us_gross,
        'Director':director,
        'Genres':genres,
        'Description':description,
        'Actors': actors,})
    
    
    #Data cleaning to convert various object datatype to int and float
    df_imdb['Year'] = df_imdb['Year'].str.extract('(\d+)').astype(int)
    df_imdb['Time'] = df_imdb['Time'].str.extract('(\d+)').astype(int)
    df_imdb['Votes'] = df_imdb['Votes'].str.replace(',','').astype(int)
    df_imdb['US Gross Millions'] = df_imdb['US Gross Millions'].map(lambda x: x.lstrip('$').rstrip('M')) 
    
    df_imdb.to_csv('imdb_data.csv')

    
    spielberg = df_imdb[df_imdb['Director'] == 'Steven Spielberg']
    hitchcock = df_imdb[df_imdb['Director'] == 'Alfred Hitchcock']
    scorsese = df_imdb[df_imdb['Director'] == 'Martin Scorsese']
    kubrick = df_imdb[df_imdb['Director'] == 'Stanley Kubrick']
    kurosawa = df_imdb[df_imdb['Director'] == 'Akira Kurosawa']
    nolan = df_imdb[df_imdb['Director'] == 'Christopher Nolan']
    tarantino = df_imdb[df_imdb['Director'] == 'Quentin Tarantino']
    
    df_directors = pd.concat([spielberg,hitchcock,scorsese,kubrick,kurosawa,nolan,tarantino])
    df_directors.to_csv('imdb_directors_data.csv')


def imdb_grader():
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    pages = ['0','101','201']
    
    titles = []
    years = []
    time = []
    imdb_ratings = []
    metascores = []
    votes = []
    us_gross = []
    director = []
    genres = [] 
    description = [] 
    age_ratings = [] 
    actors = []
    
    for start_itr in pages:
        response = get('https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start='+start_itr+'&ref_=adv_prv',headers = headers)
        soup = BeautifulSoup(response.text,"html.parser")
        movies = soup.find_all('div', class_='lister-item mode-advanced')
        
        for container in movies:
            #find the name of the film 
            name = container.h3.a.text
            titles.append(name)
            
            #finds the year of the film 
            year = container.h3.find('span', class_='lister-item-year').text
            years.append(year)
            
            #find the length of the film in minutes
            length = container.find('span',class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
            time.append(length)
            
            #find the films imdb rating 
            ratings = float(container.strong.text)
            imdb_ratings.append(ratings)
            
            #finds the amount of votes the film has 
            voters = container.find_all('span',attrs={'name':'nv'})
            vote = voters[0].text
            votes.append(vote)
            
            #finds the gross of the film
            grosses = voters[1].text if len(voters)>1 else '-'
            us_gross.append(grosses)
            
            #finds the directors name
            directorname = container.find('p',class_='').a.text
            director.append(directorname)
            
            #finds the genre of the film
            genre = container.find('span',class_='genre').text
            genre = genre.strip()
            genres.append(genre)
            
            #finds the description of the film 
            movie_description=container.find_all('p', class_ = 'text-muted')[1].text
            movie_description = movie_description.strip()
            description.append(movie_description)
            
            #finds the mpaa reating of the film 
            age = container.find('span', class_='certificate').text if container.p.find('span', class_='certificate') else 'N/A'
            age_ratings.append(age)
            
            #finds the actors in the film 
            actor = ''.join([str(s) for s in container.find_all('p','')[2].text.replace('\n','').strip('\n').split('|')[1].split(':')[1:]])
            actors.append(actor)


    #Creating a dataframe
    movie =({
        'Movie':titles,
        'Year':years,
        'Time':time,
        'IMDB Rating':imdb_ratings,
        'Film Rating':age_ratings,
        'Votes':votes,
        'US Gross Millions':us_gross,
        'Director':director,
        'Genres':genres,
        'Description':description,
        'Actors': actors})
    
    df_imdb = pd.DataFrame.from_dict(movie, orient = 'index')
    df_imdb = df_imdb.transpose() #making sure the arrays in the data frame are equal 
    
    df_imdb.to_csv('imdb_grader.csv')



def main():
  # Create the argument parser
    parser = argparse.ArgumentParser(description="This is parser for the main code for my project")
    parser.add_argument("--source",
                        choices=["remote", "local"],
                        required=True,
                        type=str,
                        help="Choose to retrieve the data locally (stored on disk) or remotely (run scrapers/ API crawlers on your device).")
    parser.add_argument("--grade",
                        required=False,
                        type=str,
                        help="Choose how many web scraper/ API calls to make. Takes an integer input.")
    
    args = parser.parse_args()
    source = args.source
    
    if args.grade is not None:
        calls = args.grade
        try:
            print("The --grade parameter will only scrape a small amount of data from each source")
            print("\n\n Retrieving Some IMDB Movies........")
            imdb_grader()
            print("\n\n--------------- Some IMDb Movies Retrieved ---------------")
        
            print("\n\n Retrieving Some Metacritic Movies........")
            metacritic_grade() 
            print("\n\n--------------- Some Metacritic Retrived ---------------")
        
            print("\n\n Retrieving Some Movies from TMDB........")
            tmdb_grader()
            print("\n\n--------------- Some Movie from TMDB Retrieved ---------------")
        except: 
            print('Grade flag parameter is not working.')
        
    elif source == "remote":
        try:
            print("\n\n Retrieving Top 1000 IMDB Movies........")
            imdb = imdb_scraper()
            print("\n\n--------------- Top 1000 IMDb Movies Retrieved ---------------")
            print("\n\n Retrieving Top 400 Movies from Metacritic........")
            metacritics = metacritic()
            print("\n\n--------------- Top 400 Movies from Metacritic Retrived ---------------")
            print("\n\n Retrieving Top 200 Movies from TMDB........")
            tmdb = tmdb_scraper()
            print("\n\n--------------- Top 200 Movies from TMDB Retrieved ---------------")
        except:
            print('Remote parameter is not working.')

    elif source == 'local':
        try:
            file_reader1 = pd.read_csv('imdb_data.csv')
            print("File read success: imdb_data.csv")
        except:
            print ("Exception Statement: imdb_data.csv does not exist. Try the --remote parameter")
        try:
            file_reader1 = pd.read_csv('metacritic_data.csv')
            print("File read success: metacritic_data.csv")
        except FileNotFoundError:
            print ("Exception Statement: metacritic_data.csv does not exist. Try the --remote parameter")
        try:
            file_reader1 = pd.read_csv('tmdb_data.csv')
            print("File read success: tmdb_data.csv")
        except FileNotFoundError:
            print ("Exception Statement: tmdb_data.csv does not exist. Try the --remote parameter")

if __name__ == '__main__':
    main()

