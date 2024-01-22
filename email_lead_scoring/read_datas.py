import pandas as pd
import numpy as np
import sqlalchemy as sql
import os

os.getcwd()


def read_data(
    con: str = "sqlite:///00_database/crm_database.sqlite", tbl: str = "Subscribers"
) -> pd.DataFrame:
    """read data from sqlite database, and return dataframe"""
    engine = sql.create_engine(con)

    with engine.connect() as connect:
        df = pd.read_sql(f"select * from {tbl}", con=connect)
        df_infer = df.convert_dtypes()  # automatically infer data types

    connect.close()

    return df_infer


def get_user_events(df: pd.DataFrame) -> pd.DataFrame:
    e = (
        df.groupby("mailchimp_id")
        .agg(dict(tag="count"))
        .set_axis(["tag_count"], axis=1)
        .reset_index()
    )
    return e

def made_purchase(df: pd.DataFrame) -> pd.DataFrame:
    emails_purchases = df['user_email'].unique()
subscribers['made_purchase'] = subscribers['user_email'].isin(emails_purchases).astype(int) 


def join_crm_datas() -> pd.DataFrame:
    """join all crm datas"""
    df_subscribers = read_data(tbl="Subscribers")
    tags = read_data(tbl="Tags")
    txns = read_data(tbl="Transactions")

    user_events = get_user_events(tags)
    made_purchase = txns['user_email'].unique()

    subscribers_user_events = df_subscribers.merge(
        user_events, on="mailchimp_id", how="left"
    ).fillna(dict(tag_count=0))

    subscribers_user_events['made_purchase'] = subscribers_user_events['user_email'].isin(made_purchase).astype(int)

    return subscribers_user_events


join_crm_datas().info()