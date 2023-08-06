from typing import Tuple, List, Bool

import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query

from .evaluate import get_actual_predicted_special

app = FastAPI()


class ISBN13(str):
    """13-digit International Serial Book Number."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, isbn: str) -> str:
        """Validate ISBN-13s."""
        if not isinstance(isbn, str):
            raise ValueError(f"Expected str, not {type(isbn)}")
        if len(isbn) != 13 or not re.match(r"978\d{10}", isbn):
            raise ValueError(f"Invalid ISBN-13: {isbn}")
        return isbn


@app.get("/{isbn}")
def run_inference(input_isbn: ISBN13, start_date: Query(dt.date), end_date: Query(dt.date)) -> Tuple[List, pd.DataFrame, Bool]:
    """
    http://localhost:1234/978...?start_date=2021-01-01&end_date=2021-04-04
    Takes as input the ISBN that received promo activity and the start and end dates of that activity, and returns
    a list of the comp titles used, a dataframe of actual versus predicted sales, and a Boolean whether the increase 
    in sales was caused by the activity
    """
    return comp_titles,df_actual_predicted,causation_check = get_actual_predicted_special(
        input_isbn,
        start_date,
        end_date
    )