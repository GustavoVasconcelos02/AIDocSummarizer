from app.extractor.pdf_extractor import extract_text_from_pdf
from app.bedrock_api.bedrock_api import process_text
from app.utils.questions import SUMMARY_QUESTIONS
from fastapi import HTTPException
import fitz 
import os
import re

# Função auxiliar para criar um diretório, caso ele ainda não exista
def create_directory(directory_path):
    if not os.path.exists(directory_path):  
        os.makedirs(directory_path)  
        print(f"Diretório criado: {directory_path}")
    else:
        print(f"Diretório já existe: {directory_path}")
        
# Função que salva o texto extraído de um PDF em um arquivo .txt
def save_text_to_file(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)  
        print(f"Texto extraído salvo em: {file_path}")

# Função principal que processa uma pasta de PDFs, extrai os textos e os salva como arquivos de texto
def process_folder(folder_path, output_folder, log_file):
    create_directory(output_folder)  

    arquivos = [arquivo for arquivo in os.listdir(folder_path) if arquivo.endswith(".pdf")]

    # Processa cada arquivo PDF encontrado
    for arquivo in arquivos:
        pdf_path = os.path.join(folder_path, arquivo)
        texto_extraido = extract_text_from_pdf(pdf_path)  

        if texto_extraido:  
            nome_arquivo_saida = os.path.splitext(arquivo)[0] + ".txt"  
            caminho_saida = os.path.join(output_folder, nome_arquivo_saida)
            save_text_to_file(caminho_saida, texto_extraido)  
            print(f"Texto extraído do {pdf_path} e salvo em {caminho_saida}")
        else:
            log_file.write(f"Erro: Não foi possível extrair texto de {pdf_path}\n")
            

# Função responsável por formatar o texto do resumo utilizando Regex para remover quebras de linha e espaços extras
def format_summary(summary_text):
    formatted_text = re.sub(r'\n+', ' ', summary_text)  
    formatted_text = re.sub(r'\s([?.!,])', r'\1', formatted_text)  
    formatted_text = re.sub(r'\s+', ' ', formatted_text)  
    return formatted_text.strip()  

# Função que lê os arquivos .txt de um diretório, processa o texto e retorna uma lista de resumos formatados
def read_and_process_files(directory_path):
    if not os.path.exists(directory_path):  
        raise HTTPException(status_code=404, detail="Diretório não encontrado")
    
    summaries = []
    for file_name in os.listdir(directory_path):  
        if file_name.endswith(".txt"):  
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                summary = process_text(text, SUMMARY_QUESTIONS)  
                formatted_summary = format_summary(summary)  
                summaries.append({"file": file_name, "summary": formatted_summary})  
    return summaries

# Função para processar um dataset completo, dividindo-o em subpastas e processando PDFs individualmente
def process_dataset(dataset_path):
    if not os.path.exists(dataset_path):  
        print(f"A pasta {dataset_path} não existe")
        return

    log_file_path = os.path.join(os.path.dirname(dataset_path), "Corrompidos.txt")  
    output_folder_path = os.path.join(os.path.dirname(dataset_path), "TextosExtraidos")  
    create_directory(output_folder_path)  

    # Abre o arquivo de log para registrar erros
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        subpastas = [subpasta for subpasta in os.listdir(dataset_path) 
                     if os.path.isdir(os.path.join(dataset_path, subpasta))]  

        # Processa cada subpasta individualmente
        for subpasta in subpastas:
            subpasta_path = os.path.join(dataset_path, subpasta)
            subpasta_output_path = os.path.join(output_folder_path, subpasta)
            process_folder(subpasta_path, subpasta_output_path, log_file)  

# Função para extrair texto de um PDF diretamente de um stream de bytes (usado em uploads)
def extract_text_from_pdf_stream(pdf_content):
    try: 
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")  
        text = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return text  
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")  
        return None
