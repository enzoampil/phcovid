import pandas as pd

def add_edge(s, d, curr_dict):
    """
    Adds edge between s and d in graph curr_dict
    Note: Python uses pass by reference so this 
    function will update curr_dict
    """
    try:
        curr_dict[s].append(d)
    except KeyError:
        curr_dict[s] = []
        curr_dict[s].append(d)

def get_case_graph(df, contact_col, case_no_col):
    """
    Returns a dict which represents a graph modelling cases
    as nodes with edges between direct connections
    """
    case_graph = {}

    for row in df.itertuples():
        current = getattr(row, case_no_col)
        contact_list = getattr(row, contact_col)

        for c in pd.Series(contact_list).unique():
            add_edge(int(current), int(c), case_graph)
            add_edge(int(c), int(current), case_graph)
        
        if(len(contact_list)==0):
            case_graph[int(current)] = []

    for key in case_graph.keys():
        case_graph[key] = list(set(case_graph[key]))

    return case_graph

def get_network(df, contact_col = 'contacts_num', case_no_col = 'case_no_num', as_dict = False):
    """
    Uses Depth First Search on the graph from get_contacts_graph
    and returns a dataframe listing all networks of known cases.
    """
    case_graph = get_case_graph(df, contact_col, case_no_col)
    
    case_cnt = len(df)
    visited = [False for i in range(1,case_cnt+2)]
    visited_pre = [False for i in range(1,case_cnt+2)]
    parent = [-1 for i in range(1,case_cnt+2)]
    
    def dfs (v, g):
        #dfs from node v in graph g
        visited[v] = True
        for node in g[v]:
            if(not visited[node]):
                parent[node] = v
                dfs(node, g)

    network_cnt = 0
    case_network = {}
    #Build data on all networks and cases comprising them
    for i in range(1, case_cnt+1):
        if(not visited[i]):
            network_cnt+=1
            dfs(i, case_graph)
            case_network[network_cnt-1] = []
            
            for j in range(1, case_cnt+1):
                if(not visited_pre[j] and visited[j]):
                    visited_pre[j] = visited[j]
                    case_network[network_cnt-1].append(j)
    
    if as_dict:
        return case_network
    else:
        return pd.DataFrame(case_network)
