import pandas as pd
import numpy as np


def sales_by_category(
    df: pd.DataFrame, category="country_code", sort_by=["sales", "ratio_of_total_sales"]
) -> pd.DataFrame:
    """return sales ratios by category"""
    if type(sort_by) == list:
        sort_by = sort_by[0]

    sales_ratios = (
        df.groupby(category)
        .agg(dict(made_purchase=["sum", lambda x: sum(x) / len(x)]))
        .set_axis(["sales", "sales_ratio_per_country"], axis=1)
        .assign(ratio_of_total_sales=lambda x: x["sales"] / sum(x["sales"]))
        .sort_values(sort_by, ascending=False)
        .assign(cumulative_sum=lambda x: x["ratio_of_total_sales"].cumsum())
    )

    return sales_ratios


def numeric_analysis(
    df: pd.DataFrame, col="tag_count", quantiles=[0.10, 0.5, 0.9]
) -> pd.DataFrame:
    """return numeric analysis with quantiles, quantiles default to 10%, 50%, 90%"""

    if type(col) is list:
        feature_list = [
            "made_purchase",
            *col,
        ]  # this will unpack the list and add the elements to the list
    else:
        feature_list = ["made_purchase", col]  # this will add the element to the list

    print(feature_list)
    df2 = df[feature_list].groupby("made_purchase").quantile(q=quantiles)

    return df2
