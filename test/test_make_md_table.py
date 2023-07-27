
from make_md_table import table


def test_table_with_strings():
    data = [
        {'Name': 'Alice', 'Age': '30', 'Hobbies': 'Reading'},
        {'Name': 'Bob', 'Age': '25', 'Hobbies': 'Gardening'},
        {'Name': 'Charlie', 'Age': '35', 'Hobbies': 'Playing Guitar'},
    ]

    expected_output = (
        "| Name    | Age | Hobbies        |\n"
        "|---------|-----|----------------|\n"
        "| Alice   | 30  | Reading        |\n"
        "| Bob     | 25  | Gardening      |\n"
        "| Charlie | 35  | Playing Guitar |\n"
    )

    assert table(data) == expected_output


def test_table_with_lists():
    data = [
        {'Name': 'Alice', 'Age': 30, 'Hobbies': ['Reading', 'Painting']},
        {'Name': 'Bob', 'Age': 25, 'Hobbies': ['Gardening']},
        {'Name': 'Charlie', 'Age': 35, 'Hobbies': ['Playing Guitar', 'Swimming', 'Cooking']},
    ]

    expected_output = (
        "| Name    | Age | Hobbies                         |\n"
        "|---------|-----|---------------------------------|\n"
        "| Alice   | 30  | Reading, Painting               |\n"
        "| Bob     | 25  | Gardening                       |\n"
        "| Charlie | 35  | Playing Guitar, Swimming, Cooking|\n"
    )

    assert table(data) == expected_output
