# core/map_data.py

def get_brazil_states_graph():
    """
    Retorna um dicionário de adjacência representando os estados do Brasil e suas fronteiras.
    """
    adjacency = {
        'AC': ['AM', 'RO'],
        'AL': ['BA', 'PE', 'SE'],
        'AP': ['PA'],
        'AM': ['AC', 'RO', 'MT', 'PA', 'RR'],
        'BA': ['AL', 'SE', 'PE', 'PI', 'TO', 'GO', 'MG', 'ES'],
        'CE': ['PI', 'PB', 'PE'],
        'DF': ['GO', 'MG'],
        'ES': ['BA', 'MG', 'RJ'],
        'GO': ['TO', 'BA', 'MG', 'MS', 'MT', 'DF'],
        'MA': ['PA', 'PI', 'TO'],
        'MT': ['AM', 'PA', 'TO', 'GO', 'MS', 'RO'],
        'MS': ['MT', 'GO', 'MG', 'SP', 'PR'],
        'MG': ['BA', 'ES', 'RJ', 'SP', 'MS', 'GO', 'DF'],
        'PA': ['AP', 'RR', 'AM', 'MT', 'TO', 'MA'],
        'PB': ['CE', 'PE', 'RN'],
        'PR': ['MS', 'SP', 'SC'],
        'PE': ['CE', 'PB', 'AL', 'BA', 'PI'],
        'PI': ['MA', 'CE', 'PE', 'BA', 'TO'],
        'RJ': ['ES', 'MG', 'SP'],
        'RN': ['CE', 'PB'],
        'RS': ['SC'],
        'RO': ['AC', 'AM', 'MT'],
        'RR': ['AM', 'PA'],
        'SC': ['PR', 'RS'],
        'SP': ['MG', 'RJ', 'PR', 'MS'],
        'SE': ['AL', 'BA'],
        'TO': ['PA', 'MA', 'PI', 'BA', 'GO', 'MT']
    }
    return adjacency