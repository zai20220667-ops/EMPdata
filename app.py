import streamlit as st
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
st.bar_chart(gender_counts)

st.subheader("Top Job Titles")
st.bar_chart(analyzer.top_jobs())

st.metric("Average Age", f"{analyzer.avg_age():.1f}")
st.metric("Median Age", f"{analyzer.median_age():.0f}")