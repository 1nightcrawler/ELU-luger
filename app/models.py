from enum import Enum
from . import db

#TODO: implement tables to hold free answer, drag&drop, speaking (future)

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class ClassroomRole(Enum):
    STUDENT = "STUDENT"
    EDUCATOR = "EDUCATOR"

class BookDifficulties(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class QuestionTypes(Enum):
    DEFAULT = 'DEFAULT'
    SOUNDBITE = 'SOUNDBITE'
    FLASHCARD = 'FLASHCARD'

class AnswerTypes(Enum):
    SINGLE_SELECT = 'SINGLE_SELECT'
    MULTI_SELECT = 'MULTI_SELECT'
    DRAG_AND_DROP = 'DRAG_AND_DROP'
    FREE_ANSWER = 'FREE_ANSWER'
    SPEAKING = 'SPEAKING'

class TestSetVisibility(Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"

class TestPlacement(Enum):
    INLINE = "INLINE"
    END_OF_BOOK = "END_OF_BOOK"

class TestAttemptStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"

class QuestionResponseStatus(Enum):
    NOT_ANSWERED = "NOT_ANSWERED"
    ANSWERED = "ANSWERED"
    SKIPPED = "SKIPPED"
    NEEDS_REVIEW = "NEEDS_REVIEW"

question_response_options = db.Table("question_response_options",
    db.Column("response_id", db.Integer, db.ForeignKey("question_responses.id", ondelete="CASCADE"), primary_key=True),
    db.Column("option_id", db.Integer, db.ForeignKey("question_options.id", ondelete="RESTRICT"), primary_key=True)
)

##Many to many intermediary tables
class ClassroomEducator(db.Model):
    __tablename__ = "classroom_educators"
    educator_user_id = db.Column(db.Integer, db.ForeignKey("educators.user_id", ondelete="CASCADE"), primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id", ondelete="CASCADE"), primary_key=True)
    educator = db.relationship("Educator", back_populates="classroom_memberships")
    classroom = db.relationship("Classroom", back_populates="educator_memberships")

##User-related entities

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True, nullable = False)
    role = db.Column(db.Enum(Role))
    password_hash = db.Column(db.String(100), nullable=False)
    user_statistics = db.relationship('UserStatistics', uselist=False, cascade="all, delete-orphan", back_populates='user') #onetoOne
    book_progress = db.relationship('BookProgress', back_populates="user", cascade="all, delete-orphan")
    educator = db.relationship("Educator", uselist=False, cascade="all, delete-orphan", passive_deletes = True, back_populates="user")
    created_test_sets = db.relationship("BookTestSet", back_populates="creator")
    test_attempts = db.relationship("TestAttempt", back_populates="user")

class Student(db.Model):
    __tablename__ = 'students'
    __table_args__ = (
        db.UniqueConstraint("classroom_id", "pin", name="uq_student_classroom_pin"),
        db.CheckConstraint("length(pin) = 4", name="ck_student_pin_length")
    )
    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100))
    pin = db.Column(db.String(4), nullable=False)
    student_statistics = db.relationship("StudentStatistics", uselist=False, cascade="all, delete-orphan", back_populates="student")
    book_progress = db.relationship("BookProgress", back_populates="student", cascade="all, delete-orphan")
    classroom = db.relationship("Classroom", back_populates="students")
    test_attempts = db.relationship("TestAttempt", back_populates="student")

class Educator(db.Model):
    __tablename__ = "educators"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user = db.relationship("User", back_populates="educator")
    classroom_memberships = db.relationship("ClassroomEducator", cascade="all, delete-orphan", passive_deletes=True, back_populates="educator")

class UserStatistics(db.Model):
    __tablename__ = 'users_statistics'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
    total_books_read = db.Column(db.Integer, nullable=False, default=0)
    total_pages_read = db.Column(db.Integer, nullable=False, default=0)
    average_book_difficulty = db.Column(db.Enum(BookDifficulties), nullable=True)
    most_difficult_book_read = db.Column(db.String(100))

    user = db.relationship("User", back_populates="user_statistics") #see 2.

class StudentStatistics(db.Model):
    __tablename__ = 'student_statistics'
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)
    student = db.relationship("Student", back_populates="student_statistics")
    total_books_read = db.Column(db.Integer)
    total_pages_read = db.Column(db.Integer)
    average_book_difficulty = db.Column(db.Enum(BookDifficulties))
    most_difficult_book_read = db.Column(db.String(100)) #see 2.

##Book-related entities
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=True)
    content = db.relationship("BookContent", uselist=False, back_populates="book", cascade="all, delete-orphan", passive_deletes=True) ## content is stored separately from book info
    test_sets = db.relationship("BookTestSet", back_populates="book", passive_deletes="all") ## books have test sets -> test sets have tests in them

class BookProgress(db.Model):
    __tablename__ = 'book_progress'
    __table_args__ = (
        db.CheckConstraint(
            "(user_id IS NOT NULL AND student_id IS NULL) OR "
            "(user_id IS NULL AND student_id IS NOT NULL)",
            name="ck_progress_exactly_one_learner"
        ),
        db.UniqueConstraint("book_id", "user_id", name="uq_progress_book_user"),
        db.UniqueConstraint("book_id", "student_id", name="uq_progress_book_student")
    )
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=True)
    current_page = db.Column(db.Integer, nullable=False, default=0)

    book = db.relationship("Book")
    user = db.relationship("User", back_populates="book_progress")
    student = db.relationship("Student", back_populates="book_progress")

class BookContent(db.Model):
    __tablename__ = 'book_content'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    book = db.relationship("Book", back_populates="content")

class BookTestSet(db.Model):
    __tablename__ = 'book_test_sets'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    creator_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    visibility = db.Column(db.Enum(TestSetVisibility), nullable=False, default=TestSetVisibility.PRIVATE)
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    book = db.relationship("Book", back_populates="test_sets")
    creator = db.relationship("User", back_populates="created_test_sets")
    tests = db.relationship("BookTest", back_populates="test_set", cascade="all, delete-orphan", passive_deletes=True, order_by="BookTest.position")
    
class BookTest(db.Model):
    __tablename__ = 'book_tests'
    __table_args__ = (
        db.CheckConstraint(
            "(placement = 'INLINE' AND start_char_index IS NOT NULL "
            "AND start_char_index >= 0) OR "
            "(placement = 'END_OF_BOOK' AND start_char_index IS NULL)",
            name="ck_test_placement_matches_anchor"
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    test_set_id = db.Column(db.Integer, db.ForeignKey("book_test_sets.id", ondelete="CASCADE"), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0) ##in what order tests appear in editor
    placement= db.Column(db.Enum(TestPlacement), nullable=False, default=TestPlacement.INLINE) ##test type, on a certain line or at the end of the book 
    start_char_index = db.Column(db.Integer, nullable=True) ##at what char does inline test start
    test_set = db.relationship("BookTestSet", back_populates="tests")
    questions = db.relationship("BookTestQuestion", back_populates="book_test", cascade="all, delete-orphan", passive_deletes=True, order_by="BookTestQuestion.position")

class BookTestQuestion(db.Model):
    __tablename__ = 'book_test_questions'
    id = db.Column(db.Integer, primary_key=True)
    book_test_id = db.Column(db.Integer, db.ForeignKey("book_tests.id", ondelete="CASCADE"), nullable=False)
    position = db.Column(db.Integer, nullable=False, default = 0)
    first_question_type = db.Column(db.Enum(QuestionTypes), nullable=False, default=QuestionTypes.DEFAULT)
    soundbite_audio_url = db.Column(db.String(150), nullable=True)
    main_question = db.Column(db.String(100), nullable=False)
    secondary_question = db.Column(db.String(100), nullable=True) ##only can be used if soundbite is also used and provides additional info
    question_answer_type = db.Column(db.Enum(AnswerTypes), nullable = False)

    options = db.relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan", order_by="QuestionOption.position")
    book_test = db.relationship("BookTest", back_populates="questions")

class QuestionOption(db.Model):
    __tablename__ = "question_options"
    __table_args__ = (
        db.UniqueConstraint("question_id", "position", name="uq_question_option_position"),
        db.CheckConstraint("position >= 0", name="ck_option_position_nonnegative")
    )

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("book_test_questions.id", ondelete="CASCADE"), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)
    question = db.relationship('BookTestQuestion', back_populates="options")

class TestAttempt(db.Model):
    __tablename__ = "test_attempts"
    __table_args__ = (
        db.CheckConstraint(
            "(user_id IS NOT NULL AND student_id IS NULL) OR "
            "(user_id IS NULL AND student_id IS NOT NULL)",
            name="ck_attempt_exactly_one_learner",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey("book_tests.id", ondelete="RESTRICT"), nullable=False)
    # Set this when the test was taken through a classroom assignment.
    classroom_assignment_id = db.Column(db.Integer, db.ForeignKey("classroom_book_assignments.id", ondelete="SET NULL"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="RESTRICT"), nullable=True)

    status = db.Column(db.Enum(TestAttemptStatus), nullable=False, default=TestAttemptStatus.IN_PROGRESS)

    started_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True)

    test = db.relationship("BookTest")
    user = db.relationship("User", back_populates="test_attempts")
    student = db.relationship("Student", back_populates="test_attempts")
    responses = db.relationship("QuestionResponse", back_populates="attempt", cascade="all, delete-orphan", order_by="QuestionResponse.question_id")

class QuestionResponse(db.Model):
    __tablename__ = "question_responses"
    __table_args__ = (
        db.UniqueConstraint("attempt_id", "question_id", name="uq_attempt_question_response"),
    )

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("test_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("book_test_questions.id", ondelete="RESTRICT"), nullable=False)

    status = db.Column(db.Enum(QuestionResponseStatus), nullable=False, default=QuestionResponseStatus.NOT_ANSWERED)
    free_text_answer = db.Column(db.Text, nullable=True)
    audio_url = db.Column(db.String(500), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)  # null when not yet graded
    points_awarded = db.Column(db.Float, nullable=True)
    answered_at = db.Column(db.DateTime, nullable=True)

    selected_options = db.relationship("QuestionOption", secondary=question_response_options)
    attempt = db.relationship("TestAttempt", back_populates="responses")
    question = db.relationship("BookTestQuestion")

#Classroom-related entities
class Classroom(db.Model):
    __tablename__ = 'classrooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    classroom_code = db.Column(db.String(16), unique = True)
    students = db.relationship("Student", back_populates="classroom", cascade = "all, delete-orphan")
    educator_memberships = db.relationship("ClassroomEducator", back_populates="classroom", cascade="all, delete-orphan", passive_deletes=True)
    book_assignments = db.relationship("ClassroomBookAssignment", back_populates="classroom", cascade="all, delete-orphan", passive_deletes=True)

##teacher can set test sets for the classroom 
class ClassroomBookAssignment(db.Model):
    __tablename__ = "classroom_book_assignments"

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    test_set_id = db.Column(db.Integer, db.ForeignKey("book_test_sets.id", ondelete="RESTRICT"), nullable=False)
    assigned_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    classroom = db.relationship("Classroom", back_populates="book_assignments")
    test_set = db.relationship("BookTestSet")
    assigned_by = db.relationship("User")

    @property
    def book(self):
        return self.test_set.book


