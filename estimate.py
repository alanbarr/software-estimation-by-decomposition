#! /usr/bin/env python3

import argparse
import yaml
import tabulate
from calculations import perform_task_calculations, calculate_predictions
from validation import validate_data
import critical_path


def _print_tasks(data):
    units = f'\n({data["Project"]["Units"]})'
    headers = [
        "ID",
        "BestCase" + units,
        "MostLikely" + units,
        "WorstCase" + units,
        "Expected (PERT)" + units,
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
        "Best Case Total" + units,
        "Worst Case Total" + units,
        "Most Likely Case Total" + units,
        "Expected (PERT) Total" + units,
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
    return parser.parse_args()


def process_project_data(data, confidence_percentages=None):
    validate_data(data)
    perform_task_calculations(data)
    calculate_predictions(data, confidence_percentages)


if __name__ == "__main__":
    data = None

    args = _parse_arguments()

    with open(args.input_yaml, "r") as f:
        data = yaml.load(f.read(), yaml.SafeLoader)

    process_project_data(data)

    _print_tasks(data)
    _print_summary(data)
    _print_prediction(data)

    graph_builder.graphing(data)
