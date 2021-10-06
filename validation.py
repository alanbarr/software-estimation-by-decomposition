class ValidationFailure(Exception):
    pass


class UniqueIdValidator:
    def __init__(self):
        self.task_ids = []

    def validate(self, task_id):
        if task_id in self.task_ids:
            raise ValidationFailure(f"The task ID {task_id} is not unique")
        self.task_ids.append(task_id)


def validate_data(data):
    id_validator = UniqueIdValidator()
    for task in data["Tasks"]:
        id_validator.validate(task["ID"])
        _ensure_task_estimates_in_range(task)


def _ensure_task_estimates_in_range(task):
    worst = task["WorstCase"]
    best = task["BestCase"]
    likely = task["MostLikely"]
    task_id = task["ID"]

    if likely > worst:
        raise ValidationFailure(
            f"Task ID: {task_id} MostLikely case is greater than WorstCase. {likely} > {worst}"
        )

    if likely < best:
        raise ValidationFailure(
            f"Task ID: {task_id} MostLikely case is less than BestCase. {likely} < {best}"
        )
