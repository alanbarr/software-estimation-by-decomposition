import pytest
import math
from critical_path import calculate_critical_path
import networkx


def test_will_pick_biggest_of_two_independant_tasks():

    test_data = {
        "Tasks": [
            {
                "ID": 1,
                "Description": "Feature 1",
                "BestCase": 1,
                "MostLikely": 5,
                "WorstCase": 10,
                "Expected": 4,
            },
            {
                "ID": 2,
                "Description": "Feature 2",
                "BestCase": 2,
                "MostLikely": 4,
                "WorstCase": 11,
                "Expected": 3,
            },
        ]
    }

    crit_path = calculate_critical_path(test_data)
    assert crit_path["BestCase"]["nodes"] == [2]
    assert crit_path["BestCase"]["time"] == 2

    assert crit_path["MostLikely"]["nodes"] == [1]
    assert crit_path["MostLikely"]["time"] == 5

    assert crit_path["WorstCase"]["nodes"] == [2]
    assert crit_path["WorstCase"]["time"] == 11

    assert crit_path["Expected"]["nodes"] == [1]
    assert crit_path["Expected"]["time"] == 4


def test_will_pick_tie_in_independant_paths():

    test_data = {
        "Tasks": [
            {
                "ID": 1,
                "Description": "Feature 1",
                "BestCase": 1,
                "MostLikely": 2,
                "WorstCase": 3,
                "Expected": 2,
            },
            {
                "ID": 2,
                "Description": "Feature 2",
                "BestCase": 1,
                "MostLikely": 2,
                "WorstCase": 3,
                "Expected": 2,
            },
        ]
    }

    crit_path = calculate_critical_path(test_data)
    assert len(crit_path["BestCase"]["nodes"]) == 1
    assert len(crit_path["MostLikely"]["nodes"]) == 1
    assert len(crit_path["WorstCase"]["nodes"]) == 1
    assert len(crit_path["Expected"]["nodes"]) == 1

    # TODO do we care about ties?
    assert crit_path["BestCase"]["nodes"][0] in [1, 2]
    assert crit_path["BestCase"]["time"] == 1

    assert crit_path["MostLikely"]["nodes"][0] in [1, 2]
    assert crit_path["MostLikely"]["time"] == 2

    assert crit_path["WorstCase"]["nodes"][0] in [1, 2]
    assert crit_path["WorstCase"]["time"] == 3

    assert crit_path["Expected"]["nodes"][0] in [1, 2]
    assert crit_path["Expected"]["time"] == 2


def test_longest_path_is_chosen_with_two_divergent_paths():

    test_data = {
        "Tasks": [
            {
                "ID": 1,
                "Description": "Feature 1",
                "BestCase": 2,
                "MostLikely": 2,
                "WorstCase": 2,
                "Expected": 2,
            },
            {
                "ID": 2,
                "Description": "Feature 2",
                "BestCase": 3,
                "MostLikely": 2,
                "WorstCase": 3,
                "Expected": 2,
                "DependsOnIDs": [1],
            },
            {
                "ID": 3,
                "Description": "Feature 2",
                "BestCase": 2,
                "MostLikely": 3,
                "WorstCase": 2,
                "Expected": 3,
                "DependsOnIDs": [1],
            },
        ]
    }

    crit_path = calculate_critical_path(test_data)
    assert crit_path["BestCase"]["nodes"] == [1, 2]
    assert crit_path["BestCase"]["time"] == 5

    assert crit_path["MostLikely"]["nodes"] == [1, 3]
    assert crit_path["MostLikely"]["time"] == 5

    assert crit_path["WorstCase"]["nodes"] == [1, 2]
    assert crit_path["WorstCase"]["time"] == 5

    assert crit_path["Expected"]["nodes"] == [1, 3]
    assert crit_path["Expected"]["time"] == 5


def test_loop_will_throw_exception():

    test_data = {
        "Tasks": [
            {
                "ID": 1,
                "Description": "Feature 1",
                "BestCase": 2,
                "MostLikely": 2,
                "WorstCase": 2,
                "Expected": 2,
                "DependsOnIDs": [2],
            },
            {
                "ID": 2,
                "Description": "Feature 2",
                "BestCase": 3,
                "MostLikely": 2,
                "WorstCase": 3,
                "Expected": 2,
                "DependsOnIDs": [1],
            },
        ]
    }

    with pytest.raises(networkx.exception.NetworkXUnfeasible):
        crit_path = calculate_critical_path(test_data)


def test_unknown_dependancy_id_will_throw():
    test_data = {
        "Tasks": [
            {
                "ID": "a_task_id",
                "Description": "Feature 1",
                "BestCase": 2,
                "MostLikely": 2,
                "WorstCase": 2,
                "Expected": 2,
                "DependsOnIDs": ["non_existant_task_id"],
            },
        ]
    }

    with pytest.raises(IndexError) as exception:
        crit_path = calculate_critical_path(test_data)
    msg = str(exception)
    assert "a_task_id" in msg
    assert "non_existant_task_id" in msg
