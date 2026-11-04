# core/graph_coloring.py
import networkx as nx

def validate_coloring(graph, coloring):
    """
    Verifica se a coloração é válida: 
    Nenhum par de vértices adjacentes pode ter a mesma cor.
    """
    for u, v in graph.edges():
        if coloring.get(u) == coloring.get(v):
            return False, f"Conflito encontrado entre {u} e {v} (mesma cor)"
    return True, "Coloração Válida (Sem conflitos)"

def welsh_powell_coloring(graph):
    """
    Algoritmo de Welsh-Powell:
    1. Ordena os vértices por grau decrescente.
    2. Atribui a menor cor disponível sequencialmente.
    """
    sorted_nodes = sorted(graph.nodes(), key=lambda x: graph.degree(x), reverse=True)
    coloring = {}
    
    for node in sorted_nodes:
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(node) if neighbor in coloring}
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color
        
    return coloring

def dsatur_coloring(graph):
    """
    Algoritmo DSATUR (Degree of Saturation):
    Heurística avançada que prioriza vértices com maior saturação de cores vizinhas.
    """
    coloring = {}
    saturation = {node: 0 for node in graph.nodes()}
    degrees = {node: graph.degree(node) for node in graph.nodes()}
    uncolored = set(graph.nodes())
    
    while uncolored:
        node = max(uncolored, key=lambda n: (saturation[n], degrees[n]))
        neighbor_colors = {coloring[neigh] for neigh in graph.neighbors(node) if neigh in coloring}
        
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color
        uncolored.remove(node)
        
        for neigh in graph.neighbors(node):
            if neigh in uncolored:
                distinct_colors = {coloring[v] for v in graph.neighbors(neigh) if v in coloring}
                saturation[neigh] = len(distinct_colors)
                
    return coloring