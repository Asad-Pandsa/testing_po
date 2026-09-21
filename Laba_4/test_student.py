import pytest

from student import get_result


@pytest.mark.parametrize(
    "score, expected",
    [
        (-1, "Некорректный балл"),
        (0, "Незачёт"),
        (49, "Незачёт"),
        (50, "Зачёт"),
        (69, "Зачёт"),
        (70, "Хорошо"),
        (89, "Хорошо"),
        (90, "Отлично"),
        (100, "Отлично"),
        (101, "Некорректный балл"),
    ],
)
def test_score_equivalence_classes_and_boundaries(score, expected):
    assert get_result(score, 100) == expected


@pytest.mark.parametrize(
    "attendance, expected",
    [
        (-1, "Некорректная посещаемость"),
        (0, "Незачёт"),
        (59, "Незачёт"),
        (60, "Зачёт"),
        (69, "Зачёт"),
        (70, "Хорошо"),
        (79, "Хорошо"),
        (80, "Отлично"),
        (100, "Отлично"),
        (101, "Некорректная посещаемость"),
    ],
)
def test_attendance_equivalence_classes_and_boundaries(attendance, expected):
    assert get_result(100, attendance) == expected


@pytest.mark.parametrize("invalid_score", ["90", None, [], {}])
def test_invalid_score_type_raises_type_error(invalid_score):
    with pytest.raises(TypeError):
        get_result(invalid_score, 80)


@pytest.mark.parametrize("invalid_attendance", ["80", None, [], {}])
def test_invalid_attendance_type_raises_type_error(invalid_attendance):
    with pytest.raises(TypeError):
        get_result(90, invalid_attendance)
