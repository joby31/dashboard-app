import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pantry Monthly Dashboard", layout="wide")
st.title("🥫 Pantry Monthly Dashboard")

# ---------------- LOAD DATA ----------------
customers_df = pd.read_excel("data/Daily_New_Old_Customers_Nov_2025.xlsx")
retention_df = pd.read_excel("data/Daily_Customer_Retention_Nov_2025.xlsx")

customers_df["Date"] = pd.to_datetime(customers_df["Date"])
retention_df["Date"] = pd.to_datetime(retention_df["Date"])

# ---------------- FILTER ----------------
st.sidebar.header("🔍 Filters")
month = st.sidebar.selectbox(
    "Select Month",
    customers_df["Date"].dt.month_name().unique()
)

customers = customers_df[customers_df["Date"].dt.month_name() == month]
retention = retention_df[retention_df["Date"].dt.month_name() == month]

# ---------------- OVERVIEW ----------------
st.subheader("1️⃣ Overview")

total_customers = customers["Total Customers"].sum()
new_customers = customers["New Customers"].sum()
old_customers = customers["Old Customers"].sum()
retention_rate = round((old_customers / total_customers) * 100, 2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Total Customers", total_customers)
c2.metric("🆕 New Customers", new_customers)
c3.metric("🔁 Returning Customers", old_customers)
c4.metric("📈 Retention %", f"{retention_rate}%")

# ---------------- DAILY ANALYSIS ----------------
st.subheader("2️⃣ Daily Customer Analysis")

line_chart = px.line(customers, x="Date", y="Total Customers",
                     title="Daily Total Customers")

bar_chart = px.bar(customers, x="Date",
                   y=["New Customers", "Old Customers"],
                   title="Daily New vs Old Customers",
                   barmode="stack")

st.plotly_chart(line_chart, use_container_width=True)
st.plotly_chart(bar_chart, use_container_width=True)

# ---------------- RETENTION LINE ----------------
st.subheader("📈 Daily Retention Rate")

retention_chart = px.line(
    retention,
    x="Date",
    y="Retention %",
    markers=True,
    title="Retention Rate Trend"
)

st.plotly_chart(retention_chart, use_container_width=True)

# ---------------- PIE CHART ----------------
st.subheader("🧩 New vs Old Customers")

pie_df = pd.DataFrame({
    "Customer Type": ["New Customers", "Returning Customers"],
    "Count": [new_customers, old_customers]
})

pie_chart = px.pie(
    pie_df,
    names="Customer Type",
    values="Count",
    title="Customer Distribution"
)

st.plotly_chart(pie_chart, use_container_width=True)

# ---------------- MONTHLY SUMMARY ----------------
st.subheader("3️⃣ Monthly Customer Summary")

avg_customers = round(total_customers / len(customers), 2)

st.write(f"• **Total Visits:** {total_customers}")
st.write(f"• **Average Customers per Day:** {avg_customers}")
st.write(f"• **Repeat Customers:** {old_customers}")
st.write(f"• **One-time Customers:** {new_customers}")

# ---------------- WEEKLY COMPARISON ----------------
st.subheader("8️⃣ Weekly Comparison")

customers["Week"] = customers["Date"].dt.isocalendar().week
weekly = customers.groupby("Week")["Total Customers"].sum().reset_index()

weekly_chart = px.bar(weekly, x="Week", y="Total Customers",
                      title="Weekly Customer Count")

st.plotly_chart(weekly_chart, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("9️⃣ Insights & Action Items")

st.markdown("""
- 📈 Retention improved towards month end  
- 🔁 Repeat customers increased steadily  
- ⚠️ Early days show low retention  
- 🎯 Suggest weekday loyalty offers  
""")

st.success("Dashboard loaded successfully ✅")
