# About

Software estimation is _hard_.
However, techniques exist which try to produce more accurate estimates.
The weighty tome:
"Software Estimation: Demystifying the Black Art by Steve McConnell" discusses
various approaches to producing software estimates.

This script aims to assist in estimation using feature decomposition, and
performs the calculations as described in Chapter 9 and Chapter 10 of Software
Estimation, namely:

- the PERT weighted average / Expected Case estimates for individual features
- the percentage confidence effort for the project from individual feature
  estimates

# Getting Setup

    python3 venv -m venv
    source venv/bin/activate
    pip3 install -r requirements.txt

    python3 -m pytest


# Running the Script

    ./estimate.py example.yaml

# The YAML File

The input to this script should be provided in the form of a YAML file, with
its format described below. For an example see the file `example.yaml`.

The **Project** section consists of:

- Name: The name of the project
- Units: The time units of the individual estimates. Currently only used as a
  reminder. Expected to be one of: "hours", days", "weeks".
- ProbabilityEstimatesInRange: Used to scale how the percentage confidence
  estimates maps to the standard deviation calculated from individual estimates.
  The higher the certainty that a task's actual estimate falls between its
  BestCase and WorstCase estimate the closer this should be to 1.0.

The **Tasks** section is an array of the individual tasks required to complete
the project. Each task requires:

- ID: A unique identifer for the task.
- Description: An optional, detailed description for the task.
- BestCase: The best case estimate for the task.
- WorstCase: The worst case estimate for the task.
- MostLikely: The outcome deemed most likely for the task.


