#! /usr/bin/env python3

import argparse
import yaml
import tabulate
from calculations import perform_task_calculations, calculate_predictions
from validation import validate_data
import critical_path

_HEADING_BC = "Best Case"
_HEADING_ML = "Most Likely Case"
_HEADING_WC = "Worst Case"
_HEADING_EC = "Expected (PERT) Case"


def _print_tasks(data):
    units = f'\n({data["Project"]["Units"]})'
    headers = [
        "ID",
        _HEADING_BC + units,
        _HEADING_ML + units,
        _HEADING_WC + units,
        _HEADING_EC + units,
        "Variance",
    ]

    rows = []

    for task in data["Tasks"]:
        rows.append(
            [
                task["ID"],
                task["BestCase"],
                task["MostLikely"],
                task["WorstCase"],
                task["Expected"],
                f'{task["Variance"]:.5f}',
            ]
        )

    print(
        tabulate.tabulate(
            rows, headers=headers, floatfmt=[""] + ["0.2f"] * 4 + ["0.3f"]
        )
    )
    print()


def _print_summary(data):
    units = f'\n ({data["Project"]["Units"]})'
    headers = [
        "Task Count",
        _HEADING_BC + " Total" + units,
        _HEADING_WC + " Total" + units,
        _HEADING_ML + " Total" + units,
        _HEADING_EC + " Total" + units,
        "Standard Deviation",
    ]
    rows = [
        [
            data["TaskCount"],
            data["BestCaseTotal"],
            data["WorstCaseTotal"],
            data["MostLikelyTotal"],
            data["ExpectedTotal"],
            data["StandardDeviation"],
        ]
    ]

    print(tabulate.tabulate(rows, headers=headers, floatfmt=[""] + ["0.2f"] * 5))
    print()


def _print_prediction(data):
    units = f' ({data["Project"]["Units"]})'
    headers = ["Percentage Confidence (%)", "Project Estimate" + units]
    rows = []
    for prediction, estimate in data["predictions"].items():
        rows.append([prediction, estimate])

    print(tabulate.tabulate(rows, headers=headers, floatfmt=[""] + [".1f"]))


def _parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate task breakdown summary")
    parser.add_argument("input_yaml", help="Input file")
    parser.add_argument("--graph", help="Filename of the dependancy graph")
    return parser.parse_args()


def process_project_data(data, confidence_percentages=None):
    validate_data(data)
    perform_task_calculations(data)
    calculate_predictions(data, confidence_percentages)


def _make_critical_path_row(critical_paths, estimate_lookup, estimate_log ):

    nodes = [str(node) for node in critical_paths[estimate_lookup]["nodes"]]
    nodes = "->".join(nodes)

    row = []
    row.append(estimate_log)
    row.append(critical_paths[estimate_lookup]['time'])
    row.append(nodes)

    return row


def _print_critical_path(critical_paths):
    units = data["Project"]["Units"]

    headers = [
        "Critical Path Type",
        f"Estimate ({units})",
        "Tasks"
    ]

    types_to_tabulate = [
            ("Expected", _HEADING_EC),
            ("BestCase", _HEADING_BC),
            ("WorstCase", _HEADING_WC),
            ("MostLikely", _HEADING_ML),
    ]

    rows = [_make_critical_path_row(critical_paths, t[0], t[1]) for t in types_to_tabulate]

    print("\n")
    print(tabulate.tabulate(rows, headers=headers, floatfmt=[""] + [".1f"]))

def _handle_critical_path(data, output_graph_filename: str):
    crit_paths = critical_path.calculate_critical_path(data, output_graph_filename)

    _print_critical_path(crit_paths)


if __name__ == "__main__":
    data = None

    args = _parse_arguments()

    with open(args.input_yaml, "r") as f:
        data = yaml.load(f.read(), yaml.SafeLoader)

    process_project_data(data)

    _print_tasks(data)
    _print_summary(data)
    _print_prediction(data)

    _handle_critical_path(data, args.graph)
