#importacion de las librerias que se utilizaran en el codigo
import pandas as pd 
import numpy as np
#importaion de libreria para estandarizar la fecha
from datetime import datetime
#importacion de liberias para la creacion del modelo de recomendacion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#funcion para importar el codigo de datos.py en main.py
def create_df():
    
    #creacion de df por cada archivo suministrado de la informacion de las plataformas"
    movies = pd.read_csv('movies_dataset.csv')
    
    #cambio de  nulos de  revenue, budget por  0.
    movies["revenue"].fillna(0, inplace = True)
    movies["budget"].fillna(0, inplace = True)
   
   #Los valores nulos del campo release date se eliminan para poder realizar la transformacion de el formato de fecha
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

def movies_df():
    #se toma el codigo para poder crear el EDA para el modelo de recomendacion
    movies = pd.read_csv('movies_dataset.csv')
    movies['release_date'] =movies['release_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d') if len(x) > 2 else '')
    movies = movies.drop(movies[movies['release_date'].isna()].index)
    movies['release_year'] = movies['release_date'].str.slice(0,4)
    movies['release_date'] = pd.to_datetime(movies['release_date'],format='%Y-%m-%d')
    movies['release_month'] = movies['release_date'].dt.strftime('%B')
    movies['budget'] = pd.to_numeric(movies['budget'], errors='coerce')
    movies['budget'] = movies['budget'].fillna(0)
    movies['revenue'] = movies['revenue'].fillna(0)
    movies['return'] = movies.apply(lambda x: x['revenue'] / x['budget'] if x['budget'] != 0 else 0, axis=1)
    movies=movies.drop(['video','imdb_id','adult','original_title','vote_count','poster_path','homepage'],axis=1)
    
    #anuevo df para el modelo de recomsndacion escogiendo las columnas que se nesecitan 
    movies_re = movies[[ 'id',  'popularity', 
        'title', 'vote_average',
       'release_year']].copy()
    
    movies_re=movies_re.dropna()
    
    
    return movies_re