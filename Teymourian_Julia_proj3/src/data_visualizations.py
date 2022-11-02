import matplotlib.pyplot as plt 
import pandas as pd 
from IPython.display import Image
import ipywidgets as widgets
import IPython.display as display
import plotly.express as px
from functools import reduce
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from src.reads_the_data import*

#IMDB SECTION 
#the top 7 most popular diretcors on IMDB 
def imdb_most_popular_directors():
    fig = px.sunburst(df_directors, path = ['Director','Movie'],hover_data=['Movie'])
    fig.show()
    
def imdb_top_actors():
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    dfs = [df_imdb, df_metacritic]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    df_final_userscore = df_final.nlargest(50,["IMDB Rating"])
    fig = px.sunburst(df_final_userscore,path = ["Actor"], hover_data = ['Movie','Genre1'])
    fig.show()

def imdb_actors_top_grossing():
    #df_imdb['US Gross Millions'] = df_imdb['US Gross Millions'].map(lambda x: x.lstrip('$').rstrip('M')) 
    df_imdb['US Gross Millions'] = pd.to_numeric(df_imdb['US Gross Millions'], errors='coerce')
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    fig = px.scatter(df_imdb, x='IMDB Rating', y='US Gross Millions', color = 'Actor', hover_data = ["Movie", "Metascore","Director", "Actor2", "Actor3"])
    fig.show()

#top genres in IMDB's 1000 Films
def imdb_genres():
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb #seperates genre collumn into speperate columns
    df_imdb1 = df_imdb.dropna()#drops none value types 
    text = df_imdb1.Genre1.values #adds text from Genre1 
    text = df_imdb1.Genre2.values #adds text from Genre2
    text = df_imdb1.Genre3.values #adds text from Genre3
    wordcloud = WordCloud(
        width = 2000,
        height = 1000,
        background_color = 'white',
        stopwords = STOPWORDS).generate(str(text))
    fig = plt.figure(
        figsize = (40, 30),
        facecolor = 'k',
        edgecolor = 'k')
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

#top IMDB films distributed by Film Rating 
def imdb_film_rating(): 
    dataframes = df_imdb
    df_imdb['Metascore'] = pd.to_numeric(df_imdb['Metascore'], errors='coerce')
    fig = px.scatter(df_imdb, x='Metascore', y='IMDB Rating', color = 'Film Rating', hover_data = ["Movie","Year"])
    fig.show()
    
#METACRITIC SECTION 

#IMDB Scores compared to Metacritic Scores for IMDB's Top 1000 films 
def metacritic_scores_years():
   # df_imdb['US Gross Millions'] = df_imdb['US Gross Millions'].map(lambda x: x.lstrip('$').rstrip('M')) 
    df_imdb['US Gross Millions'] = pd.to_numeric(df_imdb['US Gross Millions'], errors='coerce')
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    dfs = [df_imdb,df_metacritic]
    df_imdb_metacritic = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    figs = px.scatter(df_imdb_metacritic, x='Year_x', y='US Gross Millions', color = 'Metascores', hover_data = ["Movie", "Userscores", "Director", 'Actor'])
    figs.show()

def metacritic_top_genres():
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    df_imdb1 = df_imdb.dropna()
    dfs = [df_imdb1, df_metacritic]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    df_final_userscore = df_final.nlargest(1000,["Metascores"])
    text = df_final_userscore.Genre1.values
    text = df_final_userscore.Genre2.values
    text = df_final_userscore.Genre3.values
    wordcloud = WordCloud(
        width = 2000,
        height = 1000,
        background_color = 'white',
        stopwords = STOPWORDS).generate(str(text))
    fig = plt.figure(
        figsize = (40, 30),
        facecolor = 'k',
        edgecolor = 'k')
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
    
def metacritic_top_actors():
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    dfs = [df_imdb, df_metacritic]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    df_final_userscore = df_final.nlargest(25,["Metascores"])
    fig = px.sunburst(df_final_userscore,path = ["Actor"], hover_data = ['Movie'])
    fig.show() 
        
def metascore_actors_top_grossing():
    df_imdb['US Gross Millions'] = df_imdb['US Gross Millions'].map(lambda x: x.lstrip('$').rstrip('M')) 
    df_imdb['US Gross Millions'] = pd.to_numeric(df_imdb['US Gross Millions'], errors='coerce')
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    fig = px.scatter(df_imdb, x='Metascore', y='US Gross Millions', color = 'Actor', hover_data = ["Movie", "Metascore", "Actor2", "Actor3"])
    fig.show()
 
#IMDB AND METACRITIC
#IMDB Scores compared to Metacritic Scores for IMDB's Top 1000 films 
def metacritics_userscores():
    df = df_metacritic
    g = px.scatter(df, x="Metascores", y="Userscores", color = 'Difference', hover_data = ['Movie'])
    return g

#FINAL 35 Films featured in the three databases 
def final_genres():
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    df_imdb1 = df_imdb.dropna()
    dfs = [df_imdb1, df_metacritic, df_tmdb]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    text = df_final.Genre1.values
    text = df_final.Genre2.values
    text = df_final.Genre3.values
    wordcloud = WordCloud(
        width = 2000,
        height = 1000,
        background_color = 'white',
        stopwords = STOPWORDS).generate(str(text))
    fig = plt.figure(
        figsize = (40, 30),
        facecolor = 'k',
        edgecolor = 'k')
    plt.imshow(wordcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show() 
 

#out of the 35 films common amongst all the data bases, these were the top 5 rated accoridng to IMDB users 
def imdb_rating_top5(): 
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    dfs = [df_imdb, df_tmdb, df_metacritic] #the databases
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs) #merging the data to one database 
    df_final_userscore = df_final.nlargest(5,["IMDB Rating"]) 
    fig = px.sunburst(df_final_userscore,path = ["US Gross Millions", "Year_x","Genres","Actor","Director", "Movie"], hover_data = ['Movie'])
    
    img1 = open('./data/1_godfather.jpg', 'rb').read()
    img2 = open('./data/2_godfather.jpg', 'rb').read()
    img3 = open('./data/3_angrymen.jpg', 'rb').read()
    img4 = open('./data/4_lordofrings.jpg', 'rb').read()
    img5 = open('./data/5_pulpfiction.jpg', 'rb').read()
    
    widget1 = widgets.Image(value=img1, format='jpg', width=150, height=200)
    widget2 = widgets.Image(value=img2, format='jpg', width=150, height=200)
    widget3 = widgets.Image(value=img3, format='jpg', width=150, height=200)
    widget4 = widgets.Image(value=img4, format='jpg', width=150, height=200)
    widget5 = widgets.Image(value=img5, format='jpg', width=150, height=200)
    #makes the images go side by side 
    sidebyside = widgets.HBox([widget1, widget2, widget3, widget4, widget5])
    display.display(sidebyside)
    fig.show()        

def metacritic_rating_top5():
    df_imdb[['Actor','Actor2','Actor3', 'Actor4']] = df_imdb.Actors.str.split(',\s+', expand=True); df_imdb
    df_imdb[['Genre1','Genre2','Genre3']] = df_imdb.Genres.str.split(',\s+', expand=True); df_imdb
    dfs = [df_imdb, df_tmdb, df_metacritic]
    df_final = reduce(lambda left,right: pd.merge(left,right,on='Movie'), dfs)
    df_final_userscore = df_final.nlargest(5,["Metascores"])
    fig = px.sunburst(df_final_userscore,path = ["US Gross Millions", "Year_x","Genres","Actor", "Director", "Movie"], hover_data = ['Movie'])
    
    imges1 = open('./data/1_godfather.jpg', 'rb').read()
    imges2 = open('./data/6_casablanca.jpg', 'rb').read()
    imges3 = open('./data/7_rearwindow.jpg', 'rb').read()
    imges4 = open('./data/8_vertigo.jpg', 'rb').read()
    imges5 = open('./data/9_citylights.jpg', 'rb').read()
    
    wi1 = widgets.Image(value=imges1, format='jpg', width=150, height=200)
    wi2 = widgets.Image(value=imges2, format='jpg', width=150, height=200)
    wi3 = widgets.Image(value=imges3, format='jpg', width=150, height=200)
    wi4 = widgets.Image(value=imges4, format='jpg', width=150, height=200)
    wi5 = widgets.Image(value=imges5, format='jpg', width=150, height=200)
    #makes the images go side by side 
    sidebyside = widgets.HBox([wi1, wi2, wi3, wi4, wi5])
    display.display(sidebyside)
    fig.show()