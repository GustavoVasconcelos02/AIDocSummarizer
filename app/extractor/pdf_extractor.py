import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF (fitz) e aplica pós-processamento para melhorar a formatação."""
    try:
        doc = fitz.open(pdf_path)
        texto_completo = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            texto = page.get_text("text")
            texto = clean_text(texto)  # Limpeza de texto para melhorar a formatação
            texto_completo.append(texto)

        doc.close()
        return "\n\n".join(texto_completo)  # Retorna todas as páginas concatenadas
    except Exception as e:
        print(f"Erro ao extrair texto de {pdf_path}: {e}")
        return None

def clean_text(text):
    """Aplica Regex para formatar os textos extraidos"""
    # Remover quebras de linha isoladas (entre palavras)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Substituir múltiplas novas linhas por uma única nova linha
    text = re.sub(r'\n\s*\n', '\n\n', text)

    # Remover espaços extras
    text = re.sub(r'[ ]+', ' ', text)

    return text
