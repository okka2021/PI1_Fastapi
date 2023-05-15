from fastapi import FastAPI
from datos import create_df
from datos import movies_df
import calendar
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI()

#def peliculas_mes(mes): '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se 
# estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente''' 
# return {'mes':mes, 'cantidad':respuesta}
@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str):
    #creacion de diccionario de meses para que el codigo pueda realizar la busqueda en español
    meses = {
        "enero": "January",
        "febrero": "February",
        "marzo": "March",
        "abril": "April",
        "mayo": "May",
        "junio": "June",
        "julio": "July",
        "agosto": "August",
        "septiembre": "September",
        "octubre": "October",
        "noviembre": "November",
        "diciembre": "December"
    }
    if mes.lower() in meses:
        mes_ingles = meses[mes.lower()]
        movies = create_df()
        cont_mes = (movies['release_month'] == mes_ingles).sum()
        return {'mes': mes, 'cantidad': str(cont_mes)}
    else:
        return {'error': 'El mes ingresado no es válido.'}

#def peliculas_dia(dia): '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se 
# estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente''' 
# return {'dia':dia, 'cantidad':respuesta}
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str):
    #creacion de diccionario de dias para que el codigo pueda realizar la busqueda en español
    dias = {
        "lunes": "Monday",
        "martes": "Tuesday",
        "miercoles": "Wednesday",
        "miércoles": "Wednesday",
        "jueves": "Thursday",
        "viernes": "Friday",
        "sábado": "Saturday",
        "sabado": "Saturday",
        "domingo": "Sunday"
    }
    if dia.lower() in dias:
        dia_ingles = dias[dia.lower()]
        movies = create_df()
        movies['dia_semana'] = movies['release_date'].dt.strftime('%A')
        cont_dia = (movies['dia_semana'] == dia_ingles).sum()
        return {'dia': dia, 'cantidad': str(cont_dia)}
    else:
        return {'error': 'El día ingresado no es válido.'}


#def franquicia(franquicia): '''Se ingresa la franquicia, retornando la cantidad de peliculas, 
# ganancia total y promedio''' return {'franquicia':franquicia, 'cantidad':respuesta, 
# 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}

#funcion para desanidadar los datos del dciionario 
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
        'año': anio
    }
    return respuesta

# sistema de recomendacion que utiliza TF-IDF y similitud coseno para encontrar las películas más similares 
    # a una película de referencia y devuelve una lista de títulos de películas recomendadas.
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    movies_re = movies_df()
    #Se utiliza el método TfidfVectorizer para calcular la importancia relativa de los términos en los 
    # títulos de las películas, eliminando las palabras comunes en inglés.
    tfidf = TfidfVectorizer(stop_words='english')
    #Se crea una matriz tfidf_matrix que representa la importancia de los términos en cada película.
    tfidf_matrix = tfidf.fit_transform(movies_re['title'])
    #Se calcula la similitud coseno entre todas las películas utilizando la matriz tfidf_matrix, 
    # obteniendo la matriz cosine_similarities.
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    indice = movies_re[movies_re['title'] == titulo].index[0]
    puntuaciones_similares = list(enumerate(cosine_similarities[indice]))
    puntuaciones_similares = sorted(puntuaciones_similares, key=lambda x: x[1], reverse=True)
    # Obtiene las 5 películas más similares
    puntuaciones_similares = puntuaciones_similares[1:6]  
    
    indices_peliculas = [i[0] for i in puntuaciones_similares]
    
    return {'lista recomendada' : movies_re['title'].iloc[indices_peliculas]}
    
    