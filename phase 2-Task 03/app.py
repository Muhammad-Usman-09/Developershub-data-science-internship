import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Dell\OneDrive - Higher Education Commission\Desktop\internship\Task # 08\Sample - Superstore.csv", encoding='latin1')
    return df

df = load_data()

st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")
st.title("📊 Global Superstore Dashboard")

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]

st.subheader("Key Performance Indicators (KPIs)")

col1, col2, col3 = st.columns(3)

with col1:
    total_sales = filtered_df["Sales"].sum()
    st.metric("💰 Total Sales", f"${total_sales:,.0f}")

with col2:
    total_profit = filtered_df["Profit"].sum()
    st.metric("📈 Total Profit", f"${total_profit:,.0f}")

with col3:
    avg_discount = filtered_df["Discount"].mean()
    st.metric("🏷️ Avg. Discount", f"{avg_discount:.2%}")

st.subheader("Visual Analysis")

# Sales by Sub-Category
fig1 = px.bar(
    filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False),
    x=filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).index,
    y=filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).values,
    title="Sales by Sub-Category",
    labels={"x": "Sub-Category", "y": "Sales"}
)
st.plotly_chart(fig1, use_container_width=True)

# Profit by Region
fig2 = px.pie(
    filtered_df,
    names="Region",
    values="Profit",
    title="Profit Share by Region"
)
st.plotly_chart(fig2, use_container_width=True)

# Top 5 Customers by Sales
top_customers = (
    filtered_df.groupby("Customer Name")["Sales"].sum().nlargest(5)
)

fig3 = px.bar(
    top_customers,
    x=top_customers.index,
    y=top_customers.values,
    title="Top 5 Customers by Sales",
    labels={"x": "Customer Name", "y": "Sales"}
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df.head(20))
