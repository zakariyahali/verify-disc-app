from fastapi import FastAPI, HTTPException, Request

from app.services.pdf_service_dummy import PdfService
from app.database import database_v1_dict
from app.services.discrepancy_service import compare_dictionaries


app = FastAPI()

@app.get("/")
def read_root():
    return {"Service is up and running"}


@app.get("/status", description="Checks the database content and returns a success or error message.")
def read_db():
    print(f"Database content: Loaded successfully")
    if not database_v1_dict:
        raise HTTPException(status_code=404, detail="Database is empty")
    return {"Service status": "Running",
            "Database status": "DB content is available"}


@app.post("/convert", description="Extracts data from a PDF file and compares it with the data from the database.")
async def convert_pdf(request: Request) -> dict:

    pdf_from_user = await request.json()
    file_path = pdf_from_user.get("file_path")

    pdfs = PdfService(key="TEST_KEY")
    try:
        data_from_user = pdfs.extract(file_path=file_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    company_name = data_from_user.get("Company Name")
    if company_name not in database_v1_dict:
        raise HTTPException(status_code=404, detail="Company not found in database")

    retrieved_data_from_db = database_v1_dict[company_name]
    discrepancies = compare_dictionaries(data_from_user, retrieved_data_from_db)

    return {"discrepancies": discrepancies}