import streamlit as st
import pandas as pd
from io import BytesIO

def analyze_medical_equipment(uploaded_file, header_index):
    equipment_codes = {
        "КТ": [135190, 282030],
        "ММГ": [113950, 209400, 191110],
        "РГ": [113880, 208940, 191220, 173270, 191330, 173200, 114050, 209270],
        "ФГ": [114400]
    }
    
    # Читаем Excel-файл с выбранной строкой заголовка
    data = pd.read_excel(uploaded_file, header=header_index)
    
    filtered_data = data[data['Дата вывода из эксплуатации'].isna()]
    organizations = filtered_data['Краткое наименование МО'].unique()
    results = []
    
    for org in organizations:
        org_data = filtered_data[filtered_data['Краткое наименование МО'] == org]
        counts = {key: 0 for key in equipment_codes}
        
        for category, codes in equipment_codes.items():
            for code in codes:
                code_str = str(code)
                counts[category] += org_data[
                    org_data['Тип медицинского изделия'].astype(str).str.contains(code_str, na=False)
                ].shape[0]
                
        results.append({"Медицинская организация": org, **counts})
        
    results_df = pd.DataFrame(results)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, index=False)
    output.seek(0)
    return output

st.title("Анализ медицинского оборудования")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx"])

if uploaded_file is not None:
    header_option = st.radio("Выберите строку, содержащую заголовки", options=["Первая строка", "Шестая строка"])
    header_index = 0 if header_option == "Первая строка" else 5
    
    processed_file = analyze_medical_equipment(uploaded_file, header_index)
    
    st.download_button(
        label="Скачать обработанный файл",
        data=processed_file,
        file_name="И11_оборудование.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
