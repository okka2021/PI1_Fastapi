#importacion de las librerias que se utilizaran en el codigo
import pandas as pd 
import numpy as np
from datetime import datetime
# Establecer el idioma local en español
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

def create_df():
    
    #creacion de df por cada archivo suministrado de la informacion de las plataformas"
    movies = pd.read_csv('movies_dataset.csv')
    
    #cambio de  nulos de  revenue, budget por  0.
    movies["revenue"].fillna(0, inplace = True)
    movies["budget"].fillna(0, inplace = True)
   
   #Los valores nulos del campo release date deben eliminarse para poder realizar la transformacion de el formato de fecha
    movies.dropna(subset=['release_date'], inplace=True)
   
   #estandarizacion de fecha al formato AAAA-mm-dd
    movies['release_date'] =movies['release_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d') if len(x) > 2 else '')
    #se eliminan los valores nulos despues de la transformacion de formato de fecha
    movies = movies.drop(movies[movies['release_date'].isna()].index)
   
   #crear la columna release_year donde extraerán el año de la fecha de estreno.
    movies['release_year'] = movies['release_date'].str.slice(0,4)
    #convertir la columna 'release_year'en formato fecha
    movies['release_date'] = pd.to_datetime(movies['release_date'],format='%Y-%m-%d')
    #crear la columna 'release_month'para tener acceso solo al mes 
    movies['release_month'] = movies['release_date'].dt.strftime('%B')
    #crear la columna 'release_day'para tener acceso solo al dia 
   
    
   #convertir los valores a tipo numerico y sino que se establezca como 'NaN'
    movies['budget'] = pd.to_numeric(movies['budget'], errors='coerce')
    #rempazo de los NaN por 0
    movies['budget'] = movies['budget'].fillna(0)
    movies['revenue'] = movies['revenue'].fillna(0)
    #Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, 
    # dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, 
    # deberá tomar el valor 0.
    movies['return'] = movies.apply(lambda x: x['revenue'] / x['budget'] if x['budget'] != 0 else 0, axis=1)
   
   #eliminación de columnas que no constituyen informacion relevante para las querys
    movies=movies.drop(['video','imdb_id','adult','original_title','vote_count','poster_path','homepage'],axis=1)
   
   
   
   
   
   
   
    
    return movies