import pytest
import math
from estimate import process_project_data


def _get_td(prob_in_range):

    test_data = {
        "Project": {
            "Name": "Individual Estimate Example from Software Estimatiom by Steve McConnell",
            "ProbabilityEstimatesInRange": prob_in_range,
            "Units": "hours",
        },
        "Tasks": [
            {
                "ID": 1,
                "Description": "Feature 1",
                "BestCase": 1.6,
                "MostLikely": 2.0,
                "WorstCase": 3.0,
            },
            {
                "ID": 2,
                "Description": "Feature 2",
                "BestCase": 1.8,
                "MostLikely": 2.5,
                "WorstCase": 4.0,
            },
            {
                "ID": 3,
                "Description": "Feature 3",
                "BestCase": 2.0,
                "MostLikely": 3.0,
                "WorstCase": 4.2,
            },
            {
                "ID": 4,
                "Description": "Feature 4",
                "BestCase": 0.8,
                "MostLikely": 1.2,
                "WorstCase": 1.6,
            },
            {
                "ID": 5,
                "Description": "Feature 5",
                "BestCase": 3.8,
                "MostLikely": 4.5,
                "WorstCase": 5.2,
            },
            {
                "ID": 6,
                "Description": "Feature 6",
                "BestCase": 3.8,
                "MostLikely": 5,
                "WorstCase": 6,
            },
            {
                "ID": 7,
                "Description": "Feature 7",
                "BestCase": 2.2,
                "MostLikely": 2.4,
                "WorstCase": 3.4,
            },
            {
                "ID": 8,
                "Description": "Feature 8",
                "BestCase": 0.8,
                "MostLikely": 1.2,
                "WorstCase": 2.2,
            },
            {
                "ID": 9,
                "Description": "Feature 9",
                "BestCase": 1.6,
                "MostLikely": 2.5,
                "WorstCase": 3.0,
            },
            {
                "ID": 10,
                "Description": "Feature 10",
                "BestCase": 1.6,
                "MostLikely": 4,
                "WorstCase": 6,
            },
        ],
    }
    return test_data


def test_example_from_sw_estimation_99point7_percent_confidence():

    test_data = _get_td(0.997)

    process_project_data(test_data)

    assert math.isclose(test_data["VarianceTotal"], 1.22, rel_tol=0.04)
    assert math.isclose(test_data["StandardDeviation"], 1.1, rel_tol=0.02)

    assert math.isclose(test_data["Tasks"][0]["Variance"], 0.054, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][1]["Variance"], 0.134, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][2]["Variance"], 0.134, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][3]["Variance"], 0.018, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][4]["Variance"], 0.054, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][5]["Variance"], 0.134, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][6]["Variance"], 0.040, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][7]["Variance"], 0.054, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][8]["Variance"], 0.054, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][9]["Variance"], 0.538, rel_tol=0.04)


def test_example_from_sw_estimation_80_percent_confidence():

    test_data = _get_td(0.80)

    confidences_to_calcuate = [
        0.02,
        0.10,
        0.16,
        0.20,
        0.25,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.75,
        0.80,
        0.90,
        0.98,
    ]

    process_project_data(test_data, confidences_to_calcuate)

    assert math.isclose(test_data["VarianceTotal"], 6.48, rel_tol=0.04)
    assert math.isclose(test_data["StandardDeviation"], 2.55, rel_tol=0.02)

    assert math.isclose(test_data["Tasks"][0]["Variance"], 0.290, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][1]["Variance"], 0.716, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][2]["Variance"], 0.716, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][3]["Variance"], 0.095, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][4]["Variance"], 0.290, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][5]["Variance"], 0.716, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][6]["Variance"], 0.213, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][7]["Variance"], 0.290, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][8]["Variance"], 0.290, rel_tol=0.04)
    assert math.isclose(test_data["Tasks"][9]["Variance"], 2.864, rel_tol=0.04)

    assert math.isclose(test_data["predictions"]["2"], 23.5, rel_tol=0.010)
    assert math.isclose(test_data["predictions"]["10"], 25.4, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["16"], 26.1, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["30"], 27.3, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["50"], 28.6, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["70"], 30.0, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["90"], 31.8, rel_tol=0.005)
    assert math.isclose(test_data["predictions"]["98"], 33.7, rel_tol=0.010)
