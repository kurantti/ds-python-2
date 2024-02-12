import pandas as pd
import sqlalchemy as sql


def read_data(
    db_location="native",
    con: str = "sqlite:///00_database/crm_database.sqlite",
    tbl: str = "Subscribers",
) -> pd.DataFrame:
    """read data from sqlite database, and return dataframe"""

    if db_location == "native":
        pass
    else:
        con = str.replace(con, "///", "///../")

    engine = sql.create_engine(con)

    with engine.connect() as connect:
        df = pd.read_sql(f"select * from {tbl}", con=connect)
        df_infer = df.convert_dtypes()  # automatically infer data types

    connect.close()

    return df_infer


def get_user_events(df: pd.DataFrame) -> pd.DataFrame:
    """count user bought items from tags"""
    e = (
        df.groupby("mailchimp_id")
        .agg(dict(tag="count"))
        .set_axis(["tag_count"], axis=1)
        .reset_index()
    )
    return e


def join_crm_datas(db_loc="native") -> pd.DataFrame:
    """join all crm datas and retrive made_purchase data"""

    df_subscribers = read_data(db_location=db_loc, tbl="Subscribers")
    tags = read_data(db_location=db_loc, tbl="Tags")
    txns = read_data(db_location=db_loc, tbl="Transactions")

    user_events = get_user_events(tags)
    made_purchase = txns["user_email"].unique()

    subscribers_user_events = df_subscribers.merge(
        user_events, on="mailchimp_id", how="left"
    ).fillna(dict(tag_count=0))

    subscribers_user_events["made_purchase"] = (
        subscribers_user_events["user_email"].isin(made_purchase).astype(int)
    )

    return subscribers_user_events


def get_tbl_names(con: str = "sqlite:///00_database/crm_database.sqlite") -> list[str]:
    """get all table names in database"""
    engine = sql.create_engine(con)
    tbl_names = sql.inspect(engine).get_table_names()

    return tbl_names
