#==============================================
#=== Created by Magister Héctor Andres Mora ===
#=== GitHub: https://github.com/magohector ====
#==============================================
import matplotlib.pyplot as plt
import networkx as nx
#Método para obtener el producto vectorial de dos vectores
#retorna una matriz
def comVec(vec1, vec2):
    mat=[]
    for i in vec1:        
        for j in vec2:
            mat.append([i,j])            
    return mat
#Método para obtener el el producto vectorial de un vector
#y una matriz, retorna una matriz con una columna adicional
#el numéro de filas sera len(mat)*len(vec)
def comMat(mat, vec):    
    lst=[]
    for i in vec:             
        for row in mat:
            r=[]  
            for item in row: 
                r.append(item)
            r.append(i)
            lst.append(r)
    return lst
#Método para obtener todos los cruces de las filas de la matriz
#retorna una matriz con len(mat) columnas, el n�mero de filas
#viene determinado por el product(len(mat[i]))
def combinar(mat):
    m=comVec(mat[0],mat[1])
    for i in range(2,len(mat)):
        m=comMat(m,mat[i])
    return m
#Método para encontrar una matriz triangular con las distancias
#dadas por los cruces en una matriz de doble entrada
def MatrizTriangularDeMetricas(synsets, metric="path_similarity"):
    n=len(synsets)
    mat=[]
    for i,ssi in enumerate(synsets[0:n-1]):  
        row=[]
        for j,ssj in  enumerate(synsets[i+1:n]):
            d=None
            if(metric=='path_similarity'):
                d=ssi.path_similarity(ssj)
            elif(metric=='lowest_common_hypernyms'):
                d=ssi.lowest_common_hypernyms(ssj)
            elif(metric=="wup_similarity"):
                d=ssi.wup_similarity(ssj)
            if d!=None:
                row.append(d)
            else:
                row.append(0)
        mat.append(row)
    return mat

#Método para obtener una matriz de los grupos de synsets            
def getGroups(words, df):
    mat=[]
    for word in words:
        row=[]
        for d in df[df['key']==word]["synset"]:
            row.append(d)
        mat.append(row)
    return mat
#Método para sumar los elementos de una matriz
def sumaMat(mat):
    s=0
    for r in mat:
        s+=sum(r)
    return s
#https://rstopup.com/se-puede-obtener-jerarquica-graficos-de-networkx-con-python-3.html
def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):    
    if pos is None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
    if len(children)!=0:
        dx = width/len(children) 
        nextx = xcenter - width/2 - dx/2
    for child in children:
        nextx += dx
        pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
        vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,parent = root)
    return pos
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
#Método para pintar un tesauro
def pintarTesauro(tesauro):
    plt.figure(figsize=(10,5))
    my_graph = nx.Graph() 
    my_graph.add_edges_from(tesauro) 
    pos = hierarchy_pos(my_graph,'entity')  
    nx.draw(my_graph, pos=pos, with_labels=True, font_weight='bold', node_size=500)
    plt.show()

# Se aporta a la biblioteca con el siguiente método.
# Metodo para graficar el grafo
def graph_science(graph):
    plt.figure(figsize=(16,16))
    G=nx.Graph(graph)
    pos = nx.spring_layout(G)
    nx.draw(G,pos=pos ,with_labels=True, font_weight='bold', node_size=2000)
    for p in pos:  # raise text positions
        pos[p][1] += 500
    nx.draw_networkx_labels(G, pos)
    plt.show()
    
