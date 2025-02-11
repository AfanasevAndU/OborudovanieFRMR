from fastapi import FastAPI, File, UploadFile, Form, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO
from urllib.parse import quote

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_medical_equipment(data, header_index):
    equipment_codes = {
        "КТ": [135190, 282030],
        "ММГ": [113950, 209400, 191110],
        "РГ": [113880, 208940, 191220, 173270, 191330, 173200, 114050, 209270],
        "ФГ": [114400]
    }

    try:
        df = pd.read_excel(data, header=header_index)
        print("DataFrame loaded successfully:")
        print(df.head())
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        raise ValueError("Failed to read the uploaded file.")

    required_columns = ["Дата вывода из эксплуатации", "Краткое наименование МО", "Тип медицинского изделия"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Отсутствуют необходимые столбцы: {', '.join(missing_columns)}")

    filtered_data = df[df['Дата вывода из эксплуатации'].isna()]
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
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        results_df.to_excel(writer, index=False)
    output.seek(0)
    return output

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), header_option: str = Form(...)):
    if not file.filename.endswith('.xlsx'):
        return {"error": "Invalid file format. Only .xlsx files are allowed."}, 400

    header_index = 0 if header_option == "Первая строка" else 5

    try:
        processed_file = analyze_medical_equipment(file.file, header_index)
        processed_file.seek(0)  

        filename = "И11_оборудование.xlsx"
        quoted_filename = quote(filename)

        return Response(
            content=processed_file.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"}
        )
    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}, 500
