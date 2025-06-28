import streamlit as st
import pandas as pd

st.title("SEA Age Group Championship Data Explorer")

# Upload the Excel file
uploaded_file = st.file_uploader("Upload your SEA Age spreadsheet", type=["xlsx"])

if uploaded_file is not None:
    # Load all sheet names
    xls = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("Choose a worksheet", xls.sheet_names)

    # Read selected sheet
    df = xls.parse(sheet_name)

    st.write(f"### Preview of '{sheet_name}'")
    st.dataframe(df)

    # Optional: simple filtering
    st.write("### Filter data")
    filter_col = st.selectbox("Select column to filter", df.columns)
    filter_val = st.text_input(f"Show rows where '{filter_col}' contains:")

    if filter_val:
        filtered_df = df[df[filter_col].astype(str).str.contains(filter_val, case=False, na=False)]
        st.dataframe(filtered_df)