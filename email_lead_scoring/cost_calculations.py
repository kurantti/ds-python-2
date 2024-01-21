import pandas as pd
import numpy as np
import plotly.express as px
import pandas_flavor as pf


def cost_tbl(
    email_list_size=1e5,
    email_list_growth_rate=0.035,
    emails_per_month=500,
    unsub_rate=0.005,
    conversion_rate=0.05,
    customer_value=2000,
    periods=12,
) -> pd.DataFrame:
    """creates cost table for email growth analysis

    Args:
        email_list_size (_type_, optional): _description_. Defaults to 1e5.
        email_list_growth_rate (float, optional): _description_. Defaults to 0.035.
        emails_per_month (int, optional): _description_. Defaults to 500.
        unsub_rate (float, optional): _description_. Defaults to 0.005.
        conversion_rate (float, optional): _description_. Defaults to 0.05.
        customer_value (int, optional): _description_. Defaults to 2000.
        periods (int, optional): _description_. Defaults to 12.

    Returns:
        dataframe: generatered tablew
    """

    period_series = pd.Series(np.arange(0, periods), name="period")
    df = period_series.to_frame()

    df["email_no_growth"] = np.repeat(email_list_size, periods)

    df["lost_customers_no_growth"] = (
        df["email_no_growth"] * unsub_rate * emails_per_month * conversion_rate
    )

    df["cost_no_grown"] = (
        df["lost_customers_no_growth"] * customer_value
    )  # value of customers that are lost

    df["emails_with_growth"] = df["email_no_growth"] * (
        (1 + email_list_growth_rate) ** df["period"]
    )

    df["lost_customers_with_growth"] = (
        df["emails_with_growth"] * unsub_rate * emails_per_month * conversion_rate
    )
    df["cost_with_growth"] = df["lost_customers_with_growth"] * customer_value

    return df


@pf.register_dataframe_method
def cost_summary(cost_df: pd.DataFrame) -> pd.DataFrame:
    """inputs from cost table and generates total sum for growth and no growth scenarios

    Args:
        cost_df (pd.DataFrame): a cost table dataframe

    Returns:
        _type_: _description_
    """
    summary_df = (
        cost_df[["cost_no_grown", "cost_with_growth"]].sum().to_frame().transpose()
    )

    return summary_df


def simulate_cost(
    email_growth_rate: list[int] = [0.01, 0.10, 0.11],
    conversion: list[float] = [0.003, 0.006, 0.010],
    **kwargs
) -> pd.DataFrame:
    """generate growth simulation based on parameters

    Args:
        email_growth_rate (list[float], optional): input values to scenarios. Defaults to [0,2,3].
        conversion (list[float], optional): customers that can be made loyal if contacted. Defaults to [0.003, 0.006, 0.010].

    Returns:
        pd.DataFrame: Cartesian product of simulation inputs
    """
    d = {"email_gth_rate": email_growth_rate, "convertion_rate": conversion}

    out = (
        pd.MultiIndex.from_product(d.values(), names=d.keys())
        .to_frame()
        .reset_index(drop=True)
    )

    def temp_func2(x, y):
        cost_df = cost_tbl(email_list_growth_rate=x, conversion_rate=y, **kwargs)

        summary_df = cost_summary(cost_df)
        return summary_df

    summary_list = [
        temp_func2(x, y) for x, y in zip(out["email_gth_rate"], out["convertion_rate"])
    ]

    summary_params = (
        pd.concat(summary_list, axis=0)
        .reset_index()
        .drop("index", axis=1)
        .merge(out, left_index=True, right_index=True)
    )

    return summary_params


@pf.register_dataframe_method
def plot_simulations(res: pd.DataFrame):
    """generates plots

    Args:
        res (pd.DataFrame): simulated costs

    Returns:
        _type_: a plotly plot
    """
    res_ims = res.drop("cost_no_grown", axis=1).pivot(
        index="email_gth_rate", columns="convertion_rate", values="cost_with_growth"
    )

    fig = px.imshow(res_ims, origin="lower", aspect="auto", title="Cost simulation")

    return fig
