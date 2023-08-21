# import pandas as pd
from src.util.make_md_table import table_from_nested  # , table

# def test_table_with_strings():
#     data = [
#         {'Name': 'Alice', 'Age': '30', 'Hobbies': 'Reading'},
#         {'Name': 'Bob', 'Age': '25', 'Hobbies': 'Gardening'},
#         {'Name': 'Charlie', 'Age': '35', 'Hobbies': 'Playing Guitar'},
#     ]

#     expected_output = (
#         "| Name    | Age | Hobbies        |\n"
#         "|---------|-----|----------------|\n"
#         "| Alice   | 30  | Reading        |\n"
#         "| Bob     | 25  | Gardening      |\n"
#         "| Charlie | 35  | Playing Guitar |\n"
#     )

#     assert table(data) == expected_output


def test_table_from_nested_with_single_project():
    data = [{"Python": ["project1"]}]
    df = table_from_nested(data, debug=True)

    assert df.shape == (1, 1)
    assert df.iloc[0, 0] == "project1"


def test_table_from_nested_with_multiple_projects():
    data = [
        {
            "Python": ["project1", "project2"],
            "JavaScript": ["js_project1", "js_project2", "js_project3"],
            "Java": ["java_project1"],
        }
    ]

    df = table_from_nested(data, debug=True)

    assert df.shape == (3, 3)
    assert df.iloc[0, 0] == "project1"
    assert df.iloc[0, 1] == "js_project1"
    assert df.iloc[0, 2] == "java_project1"
    assert df.iloc[1, 0] == "project2"
    assert df.iloc[1, 1] == "js_project2"
    assert df.iloc[1, 2] == ""
    assert df.iloc[2, 0] == ""
    assert df.iloc[2, 1] == "js_project3"
    assert df.iloc[2, 2] == ""


def test_table_from_nested_with_empty_data():
    data = []
    df = table_from_nested(data, debug=True)
    assert df.shape == (0, 0)


# def test_table_from_nested_with_lists():
#     data = [
#         {'Name': 'Alice', 'Age': 30, 'Hobbies': ['Reading', 'Painting']},
#         {'Name': 'Bob', 'Age': 25, 'Hobbies': ['Gardening']},
#         {'Name': 'Charlie', 'Age': 35, 'Hobbies': ['Playing Guitar', 'Swimming', 'Cooking']},
#     ]

#     expected_output = (
#         "| Name    | Age | Hobbies                         |\n"
#         "|---------|-----|---------------------------------|\n"
#         "| Alice   | 30  | Reading, Painting               |\n"
#         "| Bob     | 25  | Gardening                       |\n"
#         "| Charlie | 35  | Playing Guitar, Swimming, Cooking|\n"
#     )

#     assert table_from_nested(data) == expected_output
