import os

import pandas as pd

from src.util.txt_to_csv import txt_to_csv


def test_txt_to_csv():
    input_file = "testdata.txt"
    with open(input_file, "w") as f:
        f.write("name\tstars\nfitness-tracker\t14\nN-body-simulations\t5")

    txt_to_csv(input_file, sep="\t")

    # Assert that the CSV file is created
    assert os.path.exists("testdata.csv")

    # Assert the contents of the CSV file
    expected_df = pd.DataFrame(
        {"name": ["fitness-tracker", "N-body-simulations"], "stars": [14, 5]}
    )
    actual_df = pd.read_csv("testdata.csv")

    print(expected_df)
    print(actual_df)

    pd.testing.assert_frame_equal(expected_df, actual_df)

    # Clean up the test files
    os.remove(input_file)
    os.remove("testdata.csv")
