from flask import current_app
from ..models import QuestionResponseStatus, TestAttemptStatus
from datetime import datetime, timezone

# Calculates if students test attempt has passed or not
def passed_test_set(total_awarded: float, total_possible: float, assignment) -> bool:
    if total_possible <= 0:
        return False

    threshold = assignment.unlock_threshold_percent
    if threshold is None:
        threshold = current_app.config["STUDENT_PASS_PERCENT_DEFAULT"]

    return 100 * total_awarded / total_possible >= threshold

# Checks that every test in a set is completed, totals points and checks if passed test set in an attempt
def evaluate_test_set_attempt(set_attempt, assignment):
    required_test_ids = {test.id for test in assignment.test_set.tests}
    completed_attempts = [
        attempt
        for attempt in set_attempt.test_attempts
        if attempt.status == TestAttemptStatus.COMPLETED
    ]
    completed_test_ids = {attempt.test_id for attempt in completed_attempts}

    #Doesnt evaluate if any test in set is incomplete.
    if completed_test_ids != required_test_ids:
        return None

    # User responses to questions in an attempt
    responses = [
        response
        for attempt in completed_attempts
        for response in attempt.responses
    ]

    # If any question response needs teacher review, doesn't evaluate attempt.
    if any(r.status == QuestionResponseStatus.NEEDS_REVIEW for r in responses):
        return None

    #Points possible for a test
    total_possible = sum(
        question.points_possible
        for test in assignment.test_set.tests
        for question in test.questions
    )

    #Points awarded for each response
    total_awarded = sum(response.points_awarded or 0 for response in responses)

    set_attempt.total_possible = total_possible
    set_attempt.total_awarded = total_awarded

    #Evaluates if test set was passed
    set_attempt.passed = passed_test_set(
        total_awarded,
        total_possible,
        assignment
    )
    set_attempt.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)

    return set_attempt.passed
