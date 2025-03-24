from fastapi import FastAPI, Request
from app.routes.pdf_routes import router as pdf_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="PDF Text Extractor API")

# Inclui as rotas de PDF
app.include_router(pdf_router)

# Monta o diretório 'static' para servir arquivos estáticos
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")

# Configura o diretório para templates
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Para iniciar o servidor: uvicorn app.main:app --reload