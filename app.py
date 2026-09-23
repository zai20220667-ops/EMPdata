import streamlit as st
import matplotlib.pyplot as plt
from src.panda import EmployeeLoader, EmployeeAnalysis
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(page_title="Employee Data Dashboard", layout="centered")
st.title("Employee Data Dashboard")

@st.cache_data
def get_data():
    loader = EmployeeLoader(DATA_DIR / "Employee 1000x.csv")
    return loader.load_data()

df = get_data()
analyzer = EmployeeAnalysis(df)

st.subheader("Gender Distribution")
gender_counts = analyzer.count_gender()
fig, ax = plt.subplots()
ax.bar(gender_counts.keys(), gender_counts.values())
ax.set_ylabel("Count")
st.pyplot(fig)

st.subheader("Top Job Titles")
job_counts = analyzer.top_jobs()
fig2, ax2 = plt.subplots()
ax2.bar(job_counts.keys(), job_counts.values())
ax2.set_ylabel("Count")
ax2.tick_params(axis="x", rotation=45)
st.pyplot(fig2)

st.metric("Average Age", f"{analyzer.avg_age():.1f}")
st.metric("Median Age", f"{analyzer.median_age():.0f}")