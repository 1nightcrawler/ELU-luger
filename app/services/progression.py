from datetime import datetime, timezone
from ..models import BookProgressStatus
from .assessments import evaluate_test_set_attempt

def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Reveals discoverable books from a node book
def reveal_saved_children(parent_progress):
    now = _utcnow()

    for child in parent_progress.children:
        if child.status == BookProgressStatus.HIDDEN:
            child.status = BookProgressStatus.AVAILABLE
            child.revealed_at = now

# Sets user book progress to complete and reveals books from parent node
def finish_regular_user_book(progress):
    if progress.user_id is None:
        raise ValueError("This progress row does not belong to a regular user.")

    #Prevent new reveals if book is reread
    if progress.status == BookProgressStatus.COMPLETED:
        return

    if progress.status != BookProgressStatus.IN_PROGRESS:
        raise ValueError("Only an in-progress book can be finished")

    progress.status = BookProgressStatus.COMPLETED
    progress.completed_at = _utcnow()
    reveal_saved_children(progress)

def finish_student_book(progress):
    if progress.student_id is None:
        raise ValueError("This progress row does not belong to a student.")

    if progress.status == BookProgressStatus.AWAITING_TEST:
        return

    if progress.status != BookProgressStatus.IN_PROGRESS:
        raise ValueError("Only an in-progress student book can be finished.")

    progress.status = BookProgressStatus.AWAITING_TEST

def finalize_student_test_set(set_attempt, assignment, progress):
    if set_attempt.classroom_assignment_id != assignment.id:
        raise ValueError("Attempt and assignment do not match.")
    if set_attempt.student_id != progress.student_id:
        raise ValueError("Attempt and book progress belong to different students.")
    if assignment.book.id != progress.book_id:
        raise ValueError("The test set is for a different book.")

    if set_attempt.passed is None:
        passed = evaluate_test_set_attempt(set_attempt, assignment)
    else:
        passed = set_attempt.passed

    if passed is None:
        return None

    if passed:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        progress.status = BookProgressStatus.COMPLETED
        progress.completed_at = now

        # Reveal children that were previously saved as hidden.
        for child in progress.children:
            if child.status == BookProgressStatus.HIDDEN:
                child.status = BookProgressStatus.AVAILABLE
                child.revealed_at = now
    else:
        progress.status = BookProgressStatus.RETAKE_REQUIRED

    return passed