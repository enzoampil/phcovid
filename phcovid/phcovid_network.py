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

        if len(contact_list) == 0:
            case_graph[int(current)] = []

    for key in case_graph.keys():
        case_graph[key] = list(set(case_graph[key]))

    return case_graph


def get_case_network(df, contact_col="contacts_num", case_no_col="case_no_num"):
    """
    Uses Depth First Search on the graph from get_contacts_graph
    and returns a dataframe listing all networks of known cases.
    """
    case_graph = get_case_graph(df, contact_col, case_no_col)

    case_cnt = len(df)
    visited = [False for i in range(1, max(case_graph.keys()) + 2)]
    visited_pre = [False for i in range(1, max(case_graph.keys()) + 2)]
    parent = [-1 for i in range(1, max(case_graph.keys()) + 2)]

    def dfs(v, g):
        visited[v] = True

        for node in g[v]:
            if not visited[node]:
                parent[node] = v
                dfs(node, g)

    network_cnt = 0
    case_network = {}
    # Build data on all networks and cases comprising them
    for i in case_graph.keys():
        if not visited[i]:
            network_cnt += 1
            dfs(i, case_graph)
            case_network[network_cnt - 1] = []

            for j in case_graph.keys():
                if not visited_pre[j] and visited[j]:
                    visited_pre[j] = visited[j]
                    case_network[network_cnt - 1].append(j)

    df_case_network = pd.DataFrame(
        [i for i in case_network.items()], columns=["network_no", "network_cases"]
    )
    df_case_network["network_num_cases"] = df_case_network["network_cases"].apply(
        lambda x: len(x)
    )
    return df_case_network
