import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "price",
    "sqft",
    "bedrooms",
    "bathrooms",
    "location",
    "year_built",
    "condition",
}


def validate_data(input_file: str) -> None:
    path = Path(input_file)
    if not path.is_file():
        raise FileNotFoundError(f"Data file does not exist: {input_file}")

    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")
    if data.empty:
        raise ValueError("The dataset is empty")
    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required columns contain missing values")

    numeric_columns = ["price", "sqft", "bedrooms", "bathrooms", "year_built"]
    if not data[numeric_columns].apply(lambda column: pd.api.types.is_numeric_dtype(column)).all():
        raise ValueError("Numeric columns contain non-numeric values")
    if not data[numeric_columns].apply(lambda column: column.map(pd.api.types.is_number).all()).all():
        raise ValueError("Numeric columns contain invalid values")
    if (data[numeric_columns] < 0).any().any():
        raise ValueError("Numeric columns contain negative values")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate the cleaned house dataset")
    parser.add_argument("--input", required=True, help="Path to the CSV file")
    args = parser.parse_args()
    validate_data(args.input)
    print(f"Data contract passed: {args.input}")
