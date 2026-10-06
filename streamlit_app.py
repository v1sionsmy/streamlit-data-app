import streamlit as st
import pandas as pd

st.title("Data App Assignment, due on Oct 6th.")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by month.
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

category = st.selectbox(
    "Category",
    sorted(df["Category"].dropna().unique()),
)

subcategory_options = sorted(
    df.loc[df["Category"] == category, "Sub_Category"].dropna().unique()
)
selected_subcategories = st.multiselect(
    "Sub-categories",
    subcategory_options,
    default=subcategory_options,
)

selected_data = df[
    (df["Category"] == category)
    & (df["Sub_Category"].isin(selected_subcategories))
]

selected_sales_by_month = (
    selected_data.filter(items=["Sales"])
    .groupby(pd.Grouper(freq="M"))
    .sum()
)
st.line_chart(selected_sales_by_month, y="Sales")

total_sales = selected_data["Sales"].sum()
total_profit = selected_data["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0.0

overall_sales = df["Sales"].sum()
overall_profit = df["Profit"].sum()
overall_profit_margin = (overall_profit / overall_sales * 100) if overall_sales else 0.0
margin_delta = profit_margin - overall_profit_margin

sales_column, profit_column, margin_column = st.columns(3)
sales_column.metric("Total sales", f"${total_sales:,.2f}")
profit_column.metric("Total profit", f"${total_profit:,.2f}")
margin_column.metric(
    "Overall profit margin",
    f"{profit_margin:.2f}%",
    delta=f"{margin_delta:+.2f} percentage points",
)
