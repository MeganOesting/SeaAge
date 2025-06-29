import streamlit as st
import pandas as pd
import pdfplumber
import io

st.title("SEA Age Group Championship Parser")

uploaded_pdf = st.file_uploader("Upload the full meet results PDF", type=["pdf"])

if uploaded_pdf:
    all_text = ""
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"

    # Placeholder: parsing logic will go here
    # You'll later break this into: parse_individual_events(), parse_relay_events(), parse_meet_records()
    
    # Stub data for structure preview
    df_individual = pd.DataFrame({"Event": ["100 Free"], "Name": ["Ali"], "Time": ["59.12"]})
    df_relay = pd.DataFrame({"Event": ["4x100 Free"], "Team": ["Malaysia"], "Final Time": ["3:42.67"]})
    df_records = pd.DataFrame({"Event": ["100 Free"], "Record Time": ["58.20"], "Holder": ["Ng, Y.H."], "Country": ["SGP"], "Date": ["12/6/2024"]})

    st.write("### Preview: Individual Events")
    st.dataframe(df_individual)

    st.write("### Preview: Relay Events")
    st.dataframe(df_relay)

    st.write("### Preview: Meet Records")
    st.dataframe(df_records)

    # Create multi-sheet Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_individual.to_excel(writer, index=False, sheet_name='Individual Events')
        df_relay.to_excel(writer, index=False, sheet_name='Relay Events')
        df_records.to_excel(writer, index=False, sheet_name='Meet Records')

    st.download_button("Download 3-Sheet Excel", data=output.getvalue(), file_name="sea_age_parsed.xlsx")

