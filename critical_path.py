import matplotlib.pyplot as plt
import networkx as nx


def _draw_it(graph, filename):
    pos = nx.spring_layout(
        graph, seed=7
    )  # positions for all nodes - seed for reproducibility

    A = nx.nx_agraph.to_agraph(graph)
    print(type(A))
    print(A)
    A.layout("dot")
    A.draw(filename)


def _calculate_critical_path(graph, cost_label):
    return nx.dag_longest_path(graph, weight=cost_label, default_weight=0)


def _calculate_critical_paths(graph):

    critical_paths = {
        "Expected": _calculate_critical_path(graph, "WeightExpected"),
        "BestCase": _calculate_critical_path(graph, "WeightBestCase"),
        "WorstCase": _calculate_critical_path(graph, "WeightWorstCase"),
        "MostLikely": _calculate_critical_path(graph, "WeightMostLikelyCase"),
    }

    for list_of_nodes in critical_paths.values():
        try:
            list_of_nodes.remove("START")
        except ValueError:
            continue

        try:
            list_of_nodes.remove("END")
        except ValueError:
            continue

    return critical_paths


def _build_critical_paths(graph):
    pass


def _build_graph(data):
    graph = nx.DiGraph()

    est_type = "Expected"

    for task in data["Tasks"]:

        task_id = task["ID"]
        graph.add_edge(task_id, "END")

        weights = {
            "WeightBestCase": task["BestCase"],
            "WeightMostLikelyCase": task["MostLikely"],
            "WeightWorstCase": task["WorstCase"],
            "WeightExpected": task["Expected"],
        }

        try:
            if task["DependsOnIDs"]:
                for dep in task["DependsOnIDs"]:
                    graph.add_edge(dep, task_id, label=task[est_type], **weights)

        except KeyError:
            # Nothing depends on it, so tie it to start
            graph.add_edge("START", task_id, label=task[est_type], **weights)
            continue

    for task in data["Tasks"]:

        task_id = task["ID"]

        # If this task is pointing to another, remove the END node
        if graph.out_degree(task_id) > 1:
            graph.remove_edge(task_id, "END")

    return graph

    _draw_it(graph)
    print("Best Case Critical Path")
    print(nx.dag_longest_path(graph, weight="WeightBestCase", default_weight=0))

    print("Expected Case Critical Path")
    print(nx.dag_longest_path(graph, weight="WeightExpected", default_weight=0))

    print("Worst Case Critical Path")
    print(nx.dag_longest_path(graph, weight="WeightWorstCase", default_weight=0))


def calculate_critical_path(data, output_file_name=None):

    graph = _build_graph(data)

    if output_file_name:
        _draw_it(graph, output_file_name)

    return _calculate_critical_paths(graph)