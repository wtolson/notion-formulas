"""Generate a Taskwarrior style [urgency score][1] for a Notion task database.

This can be modified to suit your needs by changing column names, weights, or
by adding/removing score components.

For the lazy, the output of this formula can be found in urgency.txt.

[1]: https://taskwarrior.org/docs/urgency/
"""

from typing import Callable

from notion_formulas import (
    Boolean,
    Date,
    Number,
    String,
    contains,
    date_between,
    empty,
    if_,
    length,
    now,
    prop,
    replace,
    replace_all,
    select,
    to_number,
)

# Forward relationship to "Dependencies" (Task -> Task)
BLOCKING: String = prop("Blocking")

# Created Time
CREATED_AT: Date = prop("Created at")

# Rollup of "Dependencies" Count per group on "Status"
DEPENDENCIES_COMPLETE: String = prop("Dependencies Complete")

# Reverse relationship from "Blocking" (Task -> Task)
DEPENDENCIES: String = prop("Dependencies")

# Date representing the due date of the task
DUE: Date = prop("Due")

# Select with options "High", "Medium", "Low"
PRIORITY: String = prop("Priority")

# String or relationship to "Project" (Task -> Project)
PROJECT: String = prop("Project")

# Date representing the soonest this task can be completed
SCHEDULED: Date = prop("Scheduled")

# Status with options "Not Started" (To-do), "In Progress", "Blocked" (In Progress),
# "Done", and "Archived" (Complete)
STATUS: String = prop("Status")

# Multi-select representing arbitrary tags on the task
TAGS: String = prop("Tags")


def urgency_next() -> Number:
    return if_(contains(TAGS, "next"), 1, 0)


def urgency_overdue() -> Number:
    # Map a range of 21 days to the value 0.2 - 1.0
    days_overdue = date_between(now(), DUE, "days")
    result = ((days_overdue + 14.0) * 0.8 / 21.0) + 0.2
    return select(
        (days_overdue >= 7, 1),
        (days_overdue >= -14, result),
        default=0.2,
    )


def urgency_blocking() -> Number:
    return if_(empty(BLOCKING), 0, 1)


def urgency_high() -> Number:
    return if_(PRIORITY == "High", 1, 0)


def urgency_medium() -> Number:
    return if_(PRIORITY == "Medium", 1, 0)


def urgency_low() -> Number:
    return if_(PRIORITY == "Low", 1, 0)


def urgency_scheduled() -> Number:
    not_scheduled = empty(SCHEDULED)
    scheduled_in_future = SCHEDULED >= now()
    return if_(not_scheduled | scheduled_in_future, 0, 1)


def urgency_started() -> Number:
    return if_(STATUS == "In Progress", 1, 0)


def urgency_age() -> Number:
    age = date_between(now(), CREATED_AT, "days")
    return if_(age > 365, 1, age / 365)


def urgency_tags() -> Number:
    count = length(replace_all(TAGS, "[^,]", "")) + 1
    is_empty = empty(TAGS)
    return select(
        (is_empty, 0),
        (count == 1, 0.8),
        (count == 2, 0.9),
        default=1,
    )


def urgency_project() -> Number:
    return if_(empty(PROJECT), 0, 1)


def dependencies_complete() -> Number:
    return to_number(replace(DEPENDENCIES_COMPLETE, "/[0-9]+$", ""))


def total_dependencies() -> Number:
    return to_number(replace(DEPENDENCIES_COMPLETE, "^[0-9]+/", ""))


def has_uncompleted_dependencies() -> Boolean:
    return dependencies_complete() != total_dependencies()


def urgency_blocked() -> Number:
    return if_((STATUS == "Blocked") | has_uncompleted_dependencies(), 1, 0)


WEIGHTS: list[tuple[float, Callable[[], Number]]] = [
    (15.0, urgency_next),  # "next" tag
    (12.0, urgency_overdue),  # overdue or near due date
    (8.0, urgency_blocking),  # blocking other tasks
    (6.0, urgency_high),  # "High" Priority
    (3.9, urgency_medium),  # "Medium" Priority
    (1.8, urgency_low),  # "Low" Priority
    (5.0, urgency_scheduled),  # scheduled tasks
    (4.0, urgency_started),  # already started tasks
    (2.0, urgency_age),  # coefficient for age
    (1.0, urgency_tags),  # has tags
    (1.0, urgency_project),  # assigned to any project
    (-5.0, urgency_blocked),  # blocked by other tasks
]


def urgency() -> Number:
    return sum(weight * get_urgency() for weight, get_urgency in WEIGHTS)


if __name__ == "__main__":
    print(urgency())
