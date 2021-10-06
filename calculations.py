import math
import scipy.stats as stats
import numpy as np


def _get_number_standard_deviations(data):
    min_prob = 0.1
    max_prob = 0.99999
    key = "ProbabilityEstimatesInRange"
    project = data["Project"]
    if project[key] > max_prob or project[key] < min_prob:
        print(
            f"{key} was outside of range, {project[key]}. Allowed values are between {min_prob} and {max_prob}"
        )
        raise Exception(f"{key} was outside of range. {project[key]}")

    div = round(2 * stats.norm.ppf(0.5 + (project[key] / 2)), 2)
    return div


def _calculate_individual_sd_and_variance(task, standard_deviation_divisor):
    task["IndividualSD"] = (
        task["WorstCase"] - task["BestCase"]
    ) / standard_deviation_divisor
    task["IndividualSD"] = round(task["IndividualSD"], 3)
    task["Variance"] = task["IndividualSD"] ** 2
    task["Variance"] = round(task["Variance"], 3)


def _calculate_expected_pert(task):
    temp = task["BestCase"] + task["WorstCase"] + task["MostLikely"] * 4
    temp = temp / 6
    temp = round(temp, 2)
    task["Expected"] = temp


def _calculate_mag_rel_error(task):
    if not task.get("Actual", None):
        return

    task["MagnitudeRelativeError"] = abs(task["Actual"] - task["Expected"])


def perform_task_calculations(data):
    data["TaskCount"] = 0
    data["VarianceTotal"] = 0
    data["BestCaseTotal"] = 0
    data["WorstCaseTotal"] = 0
    data["ExpectedTotal"] = 0
    for task in data["Tasks"]:
        _calculate_expected_pert(task)
        _calculate_individual_sd_and_variance(
            task, _get_number_standard_deviations(data)
        )
        _calculate_mag_rel_error(task)
        data["TaskCount"] += 1
        data["VarianceTotal"] += task["Variance"]
        data["BestCaseTotal"] += task["BestCase"]
        data["WorstCaseTotal"] += task["WorstCase"]
        data["ExpectedTotal"] += task["Expected"]
    data["StandardDeviation"] = round(math.sqrt(data["VarianceTotal"]), 2)


def calculate_predictions(data, confidences=None):

    if confidences is None:
        confidences = np.arange(0.1, 1.0, 0.05)

    data["predictions"] = {}
    for percent_confidence in confidences:
        multiplier = round(2 * stats.norm.ppf(percent_confidence), 2) / 2
        estimate = data["ExpectedTotal"] + data["StandardDeviation"] * multiplier
        estimate = round(estimate, 2)
        percent_confidence = int(percent_confidence * 100)
        data["predictions"][str(percent_confidence)] = estimate
