import pandas as pd

def analyze_medical_equipment(file_path, output_file_path):
    equipment_codes = {
        "КТ": [135190, 282030],
        "ММГ": [113950, 209400, 191110],
        "РГ": [113880, 208940, 191220, 173270, 191330, 173200, 114050, 209270],
        "ФГ": [114400]
    }

    data = pd.read_excel(file_path)

    filtered_data = data[data['Дата вывода из эксплуатации'].isna()]

    organizations = filtered_data['Краткое наименование МО'].unique()

    results = []

    for org in organizations:
        org_data = filtered_data[filtered_data['Краткое наименование МО'] == org]
        counts = {key: 0 for key in equipment_codes}

        for category, codes in equipment_codes.items():
            for code in codes:
                code_str = str(code)
                counts[category] += org_data[org_data['Тип медицинского изделия'].str.contains(code_str, na=False)].shape[0]

        results.append({"Медицинская организация": org, **counts})

    results_df = pd.DataFrame(results)
    results_df.to_excel(output_file_path, index=False)

file_path = '/Users/andru_shaa/Downloads/Отчет_о_наполняемости_блока_Медицинское_оборудование_БЕЗ_СПИСАННОГО.xlsx'
output_file_path = '/Users/andru_shaa/Downloads/И11_оборудование.xlsx'
analyze_medical_equipment(file_path, output_file_path)