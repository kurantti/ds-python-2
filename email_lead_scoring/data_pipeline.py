import pandas as pd
import re
import janitor as jn
import email_lead_scoring as els


def process_leads(leads):
    # time as subsciber
    leads["optin_time"] = pd.to_datetime(leads["optin_time"])
    leads["time_as_subscriber"] = (
        leads["optin_time"].apply(lambda x: pd.to_datetime("today") - x).dt.days
    )

    # email events
    leads["email_sender"] = leads["user_email"].apply(
        lambda x: re.findall(r"@(.*)\.", x)[0]
    )

    return leads


def process_tags(tags):
    tags = tags.assign(count=lambda x: 1)
    tags = (
        tags.pivot_table(index="mailchimp_id", columns="tag", values="count")
        .fillna(0)
        .pipe(func=jn.clean_names)
        .reset_index()
    )
    return tags


def fill_values_with_regexp(df: pd.DataFrame, fill=0, pattern: str = "^tag_"):
    "fill values with 0 if column name matches with regexp"
    for x in df.columns:
        if re.match(pattern=pattern, string=x):
            print(f"replacing {x} with {fill}")
            df[x] = df[x].fillna(value=fill)
    return df


def process_together(leads_prs, tags_prs):
    df = leads_prs.merge(
        tags_prs, how="left", left_on="mailchimp_id", right_on="mailchimp_id"
    )
    return df


def step_other_country(df, txns, above=6):

    df["made_purchase"] = df["user_email"].isin(txns).astype(int)
    sales = els.sales_by_category2(df)
    countries_to_keep = sales.query(f"sales > {above}").index.to_list()
    df["country_code"].fillna("unk", inplace=True)
    df["country_code"] = df["country_code"].apply(
        lambda x: x if x in countries_to_keep else "other"
    )
    return df


def process_features(leads, tags, made_purchase):

    leads_prs = process_leads(leads)
    tags_prs = process_tags(tags)

    df = process_together(leads_prs, tags_prs)
    df = fill_values_with_regexp(df=df)
    df = step_other_country(df=df, txns=made_purchase)

    return df


def read_and_process():
    leads = els.read_data(tbl="Subscribers")
    tags = els.read_data(tbl="Tags")
    made_purchase = els.read_data(tbl="Transactions")["user_email"].unique()
    x = process_features(leads, tags, made_purchase)

    return x
