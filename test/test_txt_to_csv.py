import os

import pandas as pd

from src.txt_to_csv import txt_to_csv


# def setup():
#     # create sample txt file
#     with open("testdata.txt", "w") as wf:
#         wf.write(
#         """
#         name stars
#         fitness-tracker	14
#         N-body-simulations 5
#         nutrition-planner 4
#         """
#         )


def test_txt_to_csv():
    # expected = """
    # name,stars
    # fitness-tracker,14
    # N-body-simulations,5
    # nutrition-planner,4
    # """
    # assert txt_to_csv("testdata.txt") == expected

    input_file = "testdata.txt"
    with open(input_file, "w") as f:
        f.write("name\tstars\nfitness-tracker\t14\nN-body-simulations\t5")

    txt_to_csv(input_file)

    # Assert that the CSV file is created
    assert os.path.exists("testdata.csv")

    # Assert the contents of the CSV file
    expected_df = pd.DataFrame(
        {"name": ["fitness-tracker", "N-body-simulations"], "stars": [14, 5]}
    )
    actual_df = pd.read_csv("testdata.csv")
    pd.testing.assert_frame_equal(expected_df, actual_df)

    # Clean up the test files
    os.remove(input_file)
    os.remove("testdata.csv")


# def tear_down():
#     # delete sample txt file
#     os.remove("testdata.txt")
