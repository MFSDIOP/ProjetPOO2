import pandas as pandas
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import folium
import csv
from collections import deque
import pandas as pd

print("--------------------------Projet2 POO2----------------------")
print("----------------Projet2 Partie1-----------------")
print("Lecture du fichier de transport par pandas")
df = pandas.read_csv(r"transport-nodes.csv")
print(df)
print("------------------------------------------------------")

print("Lecture du fichier de relationships par pandas")
df2 = pandas.read_csv(r"transport-relationships.csv")
print(df2)
print("------------------------------------------------------")

print("Lecture des colonnes src et dst du fichier relationships")
df1 = df2[['src', 'dst']]
print(df1)
print("------------------------------------------------------")

print("Lecture du colonne src du fichier de relationships")
src = df2[['src']]
print(src)
print("------------------------------------------------------")

print("Lecture du colonne dst du fichier de relationships")
dst = df2[['dst']]
print(dst)
print("------------------------------------------------------")

print("Dessin du graphe")
G = nx.Graph()
G = nx.from_pandas_edgelist(df1, 'src', 'dst')
nx.draw(G, with_labels=True, node_color='yellow', node_size=500)
plt.show()

print("Les noeuds du graphe")
print("--------------------")
print(dict(G.nodes.data()))
print("------------------------------------------------------")


def ajouterAttribut(myGraphe, dfnode, nameAttr, Index):
    i = 0;
    while i < 12:
        ajoutDict = {dfnode[Index][i]: {nameAttr: dfnode[nameAttr][i]}}
        i = i + 1
        nx.set_node_attributes(myGraphe, ajoutDict)


print("Ajout des attributs")
ajouterAttribut(G, df, 'latitude', 'id')
ajouterAttribut(G, df, 'longitude', 'id')
ajouterAttribut(G, df, 'population', 'id')

print(dict(G.nodes.data()))
print("------------------------------------------------------")

print("Lecture des colonnes id , latitude, longitude")
df3 = df[['id', 'latitude', 'longitude']]
print(df3)
print("------------------------------------------------------")

for i in G.nodes:
    centre = df[(df['id'] == i)]['latitude'].values[0], df[(df['id'] == i)]['longitude'].values[0]
    basemap = folium.Map(location=centre, zoom_start=12)
    basemap.save('index.html')


def marker(G):
    for i in G.nodes:
        centre = df[(df['id'] == i)]['latitude'].values[0], df[(df['id'] == i)]['longitude'].values[0]
        folium.Marker(
            location=centre, zoom_start=5
        ).add_to(basemap)
        basemap.save('index2.html')


print("Coordonnées voisins")


def construirePointsImage(myGraphe):
    points = []
    for i in myGraphe.nodes:
        for m in myGraphe.neighbors(i):
            points = [df[(df['id'] == i)]['latitude'].values[0], df[(df['id'] == i)]['longitude'].values[0]], [
                df[(df['id'] == m)]['latitude'].values[0], df[(df['id'] == m)]['longitude'].values[0]]
            print(list(points))


construirePointsImage(G)

print("------------------------------------------------------")

print("----------------Projet2 Partie2-----------------")


class Noeud:
    def __init__(self, name):
        self.name = name
        self.attributs = {}
        self.listeNomVois = []

    def setAttributs(self, key, values):
        self.attributs[key] = values

    def getName(self):
        return self.name

    def equal(self, noeud):
        if self.name == noeud.name:
            print("les deux noeuds sont égaux")
        else:
            print("Les deux noeuds ne sont pas égaux")


class Graph:
    def __init__(self):
        self.noeuds = []
        self.arc = {}

    def creerNoeuds(self):
        mydict = {}
        mylist = []
        with open('transport-nodes.csv', mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}
            listOfKeys = dict_from_csv.keys()
            listOfKeys = list(listOfKeys)
        print(listOfKeys)

    def creerArc(self):
        with open('transport-relationships.csv', mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {rows[0]: rows[1] for rows in reader}
            print(dict_from_csv)


G = Graph()
print('---------Créer des noeuds---------')
G.creerNoeuds()

print('-----------Créer des arcs------------')
G.creerArc()

print('------------Projet 2 Partie 3----------')


class Pile:
    def __init__(self):
        self.elements = []

    def push(self, noeud):
        self.elements.append(noeud)

    def contains_noeud(self, name):
        search = name in self.elements
        print(search)

    def empty(self):
        if (self.elements == []):
            print("false")
        else:
            print("true")

    def remove(self):
        if (self.elements == []):
            print("La Pile est vide")
        else:
            del self.elements[len(self.elements) - 1]


p = Pile()
p.push("Timera")
p.push("Awa")
p.push("Babacar")
p.push("Dieynaba")
p.push("Bamba")
p.push("Sam")
print(p.elements)
p.remove()
p.remove()
print(p.elements)
p.contains_noeud("Bamba")


class File(Pile):

    def __init__(self):
        super().__init__()

    def remove(self):
        if (self.elements == []):
            print("La file est vide")
        else:
            del self.elements[0]


f = File()
f.push("Tim")
f.push("Bebou")
f.push("Diaz")
print(f.elements)
f.remove()
print(f.elements)

print('------------Projet 2 Partie 4----------')


def find_paths_bfs(graph, start, end):
    queue = deque()
    queue.append((start, [start]))

    while queue:
        node, path = queue.popleft()
        adjacent_nodes = [n for n in graph[node] if n not in path]
        for adjacent_node in adjacent_nodes:
            if adjacent_node == end:
                yield path + [adjacent_node]
            else:
                queue.append((adjacent_node, path + [adjacent_node]))
