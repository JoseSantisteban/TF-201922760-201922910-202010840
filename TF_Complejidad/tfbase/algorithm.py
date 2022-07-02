import json
import random as r
import math
import heapq as hq
import pandas as pd
import numpy as np
from collections import defaultdict
def Grafo():
  roads = pd.read_json("LibroCallesTF.json")
  listacalle1, listacalle2 = roads['calle'],roads['interseccion']
  listaintersecciones = list()
  num_registros = len(listacalle1)
  for i in range(num_registros):
    calle1 = str(listacalle1[i])
    calle2 = str(listacalle2[i])
    nombre = calle1+';'+calle2
    nombre_inverso = calle2+';'+calle1
    if nombre not in listaintersecciones and nombre_inverso not in listaintersecciones:
        listaintersecciones.append(nombre)
# Diccionario que traduce de string a int para nodos
  dict_pos_inter = {}
  dict_inter_pos = {}
  for i in range(len(listaintersecciones)):
   listaintersecciones[i] = [listaintersecciones[i], i] # Esto para facilitar el registrode conexiones
   dict_pos_inter[i] = listaintersecciones[i][0] # Esto para traducir luego de hacer el resultado del algoritmo
   dict_inter_pos[listaintersecciones[i][0]] = i  # Esto para traducir luego de hacer el resultado del algoritmo

  conexiones = list() # Lista de conexiones entre intersecciones a traves de calles (bordes o arista que seran parte del grafo)
  num_intersecciones = len(listaintersecciones)
  for i in range(num_intersecciones-1):
    for j in range(i+1,num_intersecciones):
        nombre_i1, nombre_i2 = listaintersecciones[i][0].split(';')
        nombre_j1, nombre_j2 = listaintersecciones[j][0].split(';')
        if nombre_i1 == nombre_j1 or nombre_i1 == nombre_j2:
            nombre_calle = nombre_i1
            distancia  = np.random.randint(100,500)
            congestion  = np.random.randint(0,100)
            conexiones.append([listaintersecciones[i][1],listaintersecciones[j][1],distancia]) 
        elif nombre_i2 == nombre_j1 or nombre_i2 == nombre_j2:
            nombre_calle = nombre_i2
            distancia  = np.random.randint(100,500)
            congestion  = np.random.randint(0,100)
            conexiones.append([listaintersecciones[i][1],listaintersecciones[j][1],distancia])
  conexiones = conexiones[:round(0.10*len(conexiones))]
  n = len(conexiones)

  G = [[] for _ in range(n)]
  for u,v,w in conexiones:
    G[u].append([v,w])
  #A = [[] for _ in range(n)]
  #for u,v,w in conexiones:
   # A[u].append([u,v])
  return G
  
def transformGraph():
  G= Grafo()
  
  #Loc = [[] for _ in range(n)]
  #for u,v,w in conexiones:
   # Loc[u].append([u,w])
  n, m= 120, 60
  Loc= [(i * 100 - r.randint(145, 155), j * 100 - r.randint(145, 155))
          for i in range(1, n + 1) for j in range(1, m + 1)] 
  return G, Loc

def bfs(G, s):
  n= len(G)
  visited= [False]*n
  path= [-1]*n # parent
  queue= [s]
  visited[s]= True

  while queue:
    u= queue.pop(0)
    for v, _ in G[u]:
      if not visited[v]:
        visited[v]= True
        path[v]= u
        queue.append(v)

  return path

def dfs(G, s, t):
  n= len(G)
  path= [-1]*n
  visited= [False]*n

  stack= [s]
  while stack:
    u= stack.pop()
    visited[u]= True
    if u == t:
        break
    for v, _ in G[u]:
      if not visited[v]:
        path[v]= u
        stack.append(v)

  return path
def dijkstra(G, s):
    n= len(G)
    visited= [False]*n
    path= [-1]*n
    cost= [math.inf]*n

    cost[s]= 0
    pqueue= [(0, s)]
    while pqueue:
        g, u= hq.heappop(pqueue)
        if not visited[u]:
            visited[u]= True
            for v, w in G[u]:
                if not visited[v]:
                    f= g + w
                    if f < cost[v]:
                        cost[v]= f
                        path[v]= u
                        hq.heappush(pqueue, (f, v))

    return path, cost

G, Loc= transformGraph()

def graph():
    return json.dumps({"loc": Loc, "g": G})
def paths(s, t):
    G = Grafo()
    bestpath, _= dijkstra(G, s)
    path1= bfs(G, s)
    path2= dfs(G, s, t)

    return json.dumps({"bestpath": bestpath, "path1": path1, "path2": path2})
