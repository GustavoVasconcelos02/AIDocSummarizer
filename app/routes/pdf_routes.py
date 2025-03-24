from app.utils.file_utils import process_dataset, extract_text_from_pdf_stream, format_summary, read_and_process_files
from fastapi import APIRouter, HTTPException, File, UploadFile, Query
from app.bedrock_api.bedrock_api import process_text
from app.utils.questions import SUMMARY_QUESTIONS
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
import os

router = APIRouter(prefix="/pdf", tags=["PDF Extraction"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "data", "input_pdfs")
TEXTS_DIR = os.path.join(BASE_DIR, "data", "TextosExtraidos")

# Rota para processamento de dataset (opcional, depende do seu uso)
@router.get("/process-dataset/")
async def process_pdf_dataset():
    try:
        process_dataset(DATASET_DIR)
        return {"message": "Processamento de dataset concluído com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o dataset: {str(e)}")

# Rota GET para obter resumo por número do processo
@router.get("/generate-summary/")
async def get_summary_by_process_number(process_number: str = Query(..., description="Número do processo")):
    try:
        directory_path = os.path.join(TEXTS_DIR, process_number)

        summaries = read_and_process_files(directory_path)
        
        final_summary = process_text(" ".join([s['summary'] for s in summaries]), SUMMARY_QUESTIONS, is_final_summary=True)
        formatted_summary = format_summary(final_summary)
        
        # Salvar o resumo final em um arquivo temporário
        with NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(formatted_summary.encode('utf-8'))
            temp_file_path = temp_file.name
        
        return FileResponse(path=temp_file_path, filename="resumo_final.txt", media_type='text/plain')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o número do processo: {str(e)}")
    
# Rota POST para upload de PDF e geração de resumo
@router.post("/upload-pdf/")
async def upload_pdf_and_generate_summary(file: UploadFile = File(...)):
    try:
        pdf_content = await file.read()
        pdf_text = extract_text_from_pdf_stream(pdf_content)
        summary = process_text(pdf_text, SUMMARY_QUESTIONS)
        formatted_summary = format_summary(summary)
        
        # Salvar o resumo em um arquivo temporário
        with NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(formatted_summary.encode('utf-8'))
            temp_file_path = temp_file.name
        
        return FileResponse(path=temp_file_path, filename="resumo_de_arquivo_unico.txt", media_type='text/plain')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o PDF: {str(e)}")

