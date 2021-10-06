import pytest
from validation import ValidationFailure, validate_data


@pytest.fixture
def project_data():
    project_data = {"Tasks": []}
    project_data["Tasks"].append(
        {"BestCase": 2, "MostLikely": 3, "WorstCase": 5, "ID": "Task1"}
    )
    project_data["Tasks"].append(
        {"BestCase": 2, "MostLikely": 3, "WorstCase": 5, "ID": "Task2"}
    )
    return project_data


def test_valid_project_data_will_not_raise(project_data):

    validate_data(project_data)


def test_unique_id_validator_will_raise_for_non_unique_id(project_data):

    project_data["Tasks"][0]["ID"] = "duplicate"
    project_data["Tasks"][1]["ID"] = project_data["Tasks"][0]["ID"] = "duplicate"

    with pytest.raises(ValidationFailure, match=r".*duplicate.*unique"):
        validate_data(project_data)


def test_ensure_tasks_in_range_will_raise_when_best_case_estimate_greater_than_most_likely(
    project_data,
):

    project_data["Tasks"][0]["MostLikely"] = 1

    with pytest.raises(ValidationFailure, match=r"1 < 2"):
        validate_data(project_data)


def test_ensure_tasks_in_range_will_raise_when_worst_case_estimate_less_than_most_likely(
    project_data,
):

    project_data["Tasks"][0]["MostLikely"] = 7

    with pytest.raises(ValidationFailure, match=r"7 > 5"):
        validate_data(project_data)
