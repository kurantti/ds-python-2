# BUSINESS SCIENCE UNIVERSITY
# COURSE: DS4B 201-P PYTHON MACHINE LEARNING
# MODULE 1: BUSINESS UNDERSTANDING
# ----

# LIBRARIES ----

# BUSINESS SCIENCE PROBLEM FRAMEWORK ----

# View Business as a Machine ----


# Business Units: 
#   - Marketing Department
#   - Responsible for sales emails  
# Project Objectives:
#   - Target Subscribers Likely To Purchase
#   - Nurture Subscribers to take actions that are known to increase probability of purchase
# Define Machine:
#   - Marketing sends out email blasts to everyone
#   - Generates Sales
#   - Also ticks some members off
#   - Members unsubscribe, this reduces email growth and profitability
# Collect Outcomes:
#   - Revenue has slowed, Email growth has slowed

# Understand the Drivers ----

#   - Key Insights:
#     - Company has Large Email List: 100,000 
#     - Email list is growing at 6,000/month less 2500 unsub for total of 3500
#     - High unsubscribe rates: 500 people per sales email
#   - Revenue:
#     - Company sales cycle is generating about $250,000 per month
#     - Average Customer Lifetime Value: Estimate $2000/customer
#   - Costs: 
#     - Marketing sends 5 Sales Emails Per Month
#     - 5% of lost customers likely to convert if nutured TODO: think life


# COLLECT OUTCOMES ----

import pandas as pd
import numpy as np
import janitor as jn
import plotly.express as px



email_list_size_1 = 1e5
email_list_size_1
## unsub count
unsub_count_1 = 5e2
unsub_rate_1 = unsub_count_1 / email_list_size_1

emails_per_month_1 = 5
conversion_1 = 0.05  # customers that can be made loyal if contacted
lost_customer = email_list_size_1 * unsub_rate_1 * emails_per_month_1 * conversion_1
lost_customer  # lost customer for 5 emails per month
customer_value = 2e3
lost_revenue = lost_customer * customer_value

# No-growth scenario $3M cost
lost_revenue_per_year = lost_revenue * 12  # there is large cost involved

# 2.5% growth scenario:
#   amount = principle * ((1+rate)**time)
((1 + 0.035) ** 11) * email_list_size_1  # in 12 months

# If reduce unsubscribe rate by 30%


# COST CALCULATION FUNCTIONS ----
period_series = pd.Series(np.arange(0, 12), name="period")
# Function: Calculate Monthly Unsubscriber Cost Table ----
df = period_series.to_frame()
# no growth
df["email_no_growth"] = np.repeat(email_list_size_1, 12)  # this is email list size during 12 month period
df["lost_customers_no_growth"] = df[
                                     "email_no_growth"] * unsub_rate_1 * emails_per_month_1 * conversion_1  # per month 500 customers are leaving from the list
df["cost_no_grown"] = df["lost_customers_no_growth"] * customer_value  # value of customers that are lost

# with growth
df["emails_with_growth"] = df["email_no_growth"] * ((1 + 0.035) ** df["period"])
df
viz = px.line(df, ["emails_with_growth", "email_no_growth"]).add_hline(y=0)
viz.show(renderer='plotly_mimetype+notebook')

df_test = pd.DataFrame(np.random.randn(100, 4), columns='A B C D'.split())
print(df_test.head())
fig = px.line(df_test)
df.columns
df['lost_customers_with_growth'] = df['emails_with_growth'] * unsub_rate_1 * emails_per_month_1 * conversion_1
df

# cost no growth
df['cost_with_growth'] = df['lost_customers_with_growth'] * customer_value
df
px.line(df, y=['cost_no_grown', 'cost_with_growth'])

# compare cost
df[["cost_no_grown", 'cost_with_growth']].sum()
df[['cost_no_grown']].sum() * .3
df[['cost_with_growth']].sum() * .3
df


# Function: Summarize Cost ----
def create_cost_tbl(
        email_list_size=1e5,
        email_list_growth_rate=0.035,
        sales_emails=5,
        unsub_rate=0.005,
        conversion_rate=0.05,
        customer_value=2000,
        periods = 12
):
    return None

# ARE OBJECTIVES BEING MET?
# - We can see a large cost due to unsubscription
# - However, some attributes may vary causing costs to change


# SYNTHESIZE OUTCOMES (COST SIMULATION) ----
# - Make a cartesian product of inputs that can vary
# - Use list comprehension to perform simulation
# - Visualize results

# Cartesian Product (Expand Grid)


# Function


# VISUALIZE COSTS


# Function: Plot Simulated Unsubscriber Costs


# ARE OBJECTIVES BEING MET?
# - Even with simulation, we see high costs
# - What if we could reduce by 30% through better targeting?


# - What if we could reduce unsubscribe rate from 0.5% to 0.17% (marketing average)?
# - Source: https://www.campaignmonitor.com/resources/knowledge-base/what-is-a-good-unsubscribe-rate/


# HYPOTHESIZE DRIVERS

# - What causes a customer to convert of drop off?
# - If we know what makes them likely to convert, we can target the ones that are unlikely to nurture them (instead of sending sales emails)
# - Meet with Marketing Team
# - Notice increases in sales after webinars (called Learning Labs)
# - Next: Begin Data Collection and Understanding

