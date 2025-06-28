import streamlit as st
import pandas as pd
import pdfplumber
import io

st.title("SEA Age Group Data Viewer")

option = st.radio("Choose data source:", ["Upload Excel", "Upload PDF"])

# --- EXCEL HANDLER ---
if option == "Upload Excel":
    uploaded_excel = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_excel:
        xls = pd.ExcelFile(uploaded_excel)
        sheet = st.selectbox("Select a sheet", xls.sheet_names)
        df = xls.parse(sheet)
        st.write(f"### Preview of '{sheet}'")
        st.dataframe(df)

        # Optional filtering
        st.write("### Filter data")
        col_to_filter = st.selectbox("Choose column to filter", df.columns)
        keyword = st.text_input("Show rows where this column contains:")
        if keyword:
            filtered_df = df[df[col_to_filter].astype(str).str.contains(keyword, case=False, na=False)]
            st.dataframe(filtered_df)

# --- PDF HANDLER ---
elif option == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_pdf:
        all_tables = []
        with pdfplumber.open(uploaded_pdf) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    try:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)
                    except:
                        pass  # skip malformed tables

        if all_tables:
            combined = pd.concat(all_tables, ignore_index=True)
            st.write("### Extracted Table from PDF:")
            st.dataframe(combined)

            # Download as Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                combined.to_excel(writer, index=False, sheet_name='Extracted')
            st.download_button("Download as Excel", data=output.getvalue(), file_name="converted_from_pdf.xlsx")
        else:
            st.warning("No tables were found in the PDF.")
