from typing import Union
from fastapi import FastAPI
from datos import create_df
import calendar
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#def peliculas_mes(mes): '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se 
# estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente''' 
# return {'mes':mes, 'cantidad':respuesta}
@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str):
    movies= create_df()
    cont_mes = (movies['release_month'] == mes).sum()    
    return {'mes': mes,'cantidad':str(cont_mes)}


#def peliculas_dia(dia): '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se 
# estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente''' 
# return {'dia':dia, 'cantidad':respuesta}
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str):
    movies= create_df()
    movies['dia_semana'] = movies['release_date'].dt.strftime('%A')
    cont_dia = (movies['dia_semana'] == dia).sum() 
    return {'dia': dia,'cantidad':str(cont_dia)}


#def franquicia(franquicia): '''Se ingresa la franquicia, retornando la cantidad de peliculas, 
# ganancia total y promedio''' return {'franquicia':franquicia, 'cantidad':respuesta, 
# 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}
def parse_belongs_to_collection(x):
    try:
        return json.loads(x.replace("'",'"'))["name"]
    except:
        return ""
    
@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
    df= create_df()
    df["franquicia"] = df["belongs_to_collection"].apply(parse_belongs_to_collection)
    len(df[df["franquicia"] == franquicia])


    franquicia_df = df[df['franquicia'] == franquicia]
    cantidad = len(franquicia_df)
    ganancia_total = franquicia_df['revenue'].sum()
    ganancia_promedio = franquicia_df['revenue'].mean()
    respuesta = {
        'franquicia': franquicia,
        'cantidad': cantidad,
        'ganancia_total': ganancia_total,
        'ganancia_promedio': ganancia_promedio
    }
    return respuesta




#def peliculas_pais(pais): '''Ingresas el pais, retornando la cantidad de peliculas 
# producidas en el mismo''' return {'pais':pais, 'cantidad':respuesta}
def parse_production_countries(x):
    try:
        return json.loads(x.replace("'",'"'))[0]["name"]
    except:
        return ""
    
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    df= create_df()
    df["country_name"] = df["production_countries"].apply(parse_production_countries)
    cant = len(df[df["country_name"] == pais])
    return {'pais': pais,'cantidad': cant}

#def productoras(productora): '''Ingresas la productora, retornando la ganancia total y la 
# cantidad de peliculas que produjeron''' return {'productora':productora, 'ganancia_total':respuesta, 
# 'cantidad':respuesta}
@app.get("/productoras/{productora}")
def productoras(productora: str):
    df= create_df()
    df["productora"] = df["production_companies"].apply(parse_production_countries)
    productora_df = df[df['productora'] == productora]
    cantidad = len(productora_df)
    ganancia_total = productora_df['revenue'].sum()
    ganancia_promedio = productora_df['revenue'].mean()
    respuesta = {
        'productora': productora,
        'cantidad': cantidad,
        'ganancia_total': ganancia_total,
        'ganancia_promedio': ganancia_promedio
    }
    return respuesta


#def retorno(pelicula): '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno 
# y el año en el que se lanzo''' return {'pelicula':pelicula, 'inversion':respuesta, 
# 'ganacia':respuesta,'retorno':respuesta, 'anio':respuesta}
@app.get("/retorno/{pelicula}")
def retorno(pelicula: str):
    df=create_df()
    pelicula_df = df[df['title'] == pelicula]

    # Obtener los valores de inversión, ganancia, retorno y año de lanzamiento
    inversion = pelicula_df['budget'].iloc[0]
    ganancia = pelicula_df['revenue'].iloc[0]
    retorno = pelicula_df['return'].iloc[0]
    anio = pelicula_df['release_year'].iloc[0]

    respuesta = {
        'pelicula': pelicula,
        'inversion': inversion,
        'ganancia': ganancia,
        'retorno': retorno,
        'anio': anio
    }
    return respuesta

