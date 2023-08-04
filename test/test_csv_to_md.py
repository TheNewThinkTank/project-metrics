import os

from src.csv_to_md import csv_to_md


def test_csv_to_md():
    input_file = "testdata.csv"
    with open(input_file, "w") as f:
        f.write("name,stars\nfitness-tracker,14\nN-body-simulations,5")

    csv_to_md(input_file)

    # Assert that the md file is created
    assert os.path.exists("testdata.md")

    # Assert the contents of the md file
    expected_output = (
        " | name |stars |\n"
        " |--- | --- | \n"
        " | fitness-tracker | 14 | \n"
        " | N-body-simulations | 5 | \n"
    )

    with open("testdata.md", "r") as md:
        actual_output = md.read()

    print(actual_output)
    print(expected_output)

    assert actual_output == expected_output

    # Clean up the test files
    os.remove(input_file)
    os.remove("testdata.md")
