# PDF Text Extractor API

## Visão Geral
Este projeto é uma API desenvolvida em Python usando FastAPI para extrair texto de arquivos PDF e gerar resumos utilizando um modelo de inteligência artificial da AWS Bedrock. O objetivo é processar documentos legais e gerar resumos detalhados com base em perguntas predefinidas.

## Funcionalidades
- **Extração de Texto**: Utiliza a biblioteca PyMuPDF (fitz) para extrair texto de arquivos PDF.
- **Geração de Resumos**: Usa a AWS Bedrock para criar resumos baseados em prompts bem estruturados.
- **Processamento de Diretórios**: Lê múltiplos documentos e gera um resumo final combinando informações de vários arquivos.
- **Endpoints API**: Disponibiliza rotas para upload de PDFs e obtenção de resumos por número do processo.

## Estrutura do Projeto
```
app/
┣ bedrock_api/
┃ ┣ bedrock_prompt.py   # Gera prompts para resumos parciais e finais
┃ ┣ bedrock_client.py   # Configuração do cliente AWS Bedrock
┃ ┣ bedrock_prompt.py
┣ extractor/
┃ ┗ pdf_extractor.py    # Extração de texto de PDFs
┣ routes/
┃ ┗ pdf_routes.py       # Define rotas da API
┣ utils/
┃ ┣ file_utils.py
┃ ┣ questions.py        # Lista de perguntas usadas para gerar resumos
┣ main.py               # Ponto de entrada da API
┣ .env                  # Configurações de credenciais AWS
┣ requirements.txt      # Dependências do projeto
```

## Instalação
### 1. Clonar o repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

### 2. Criar um ambiente virtual e instalar dependências
```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configurar credenciais da AWS
Crie um arquivo `.env` na raiz do projeto e adicione:
```sh
AWS_ACCESS_KEY_ID=<SUA_ACCESS_KEY>
AWS_SECRET_ACCESS_KEY=<SUA_SECRET_KEY>
AWS_SESSION_TOKEN=<SEU_SESSION_TOKEN>
```

## Como Usar
### Executar a API
```sh
uvicorn app.main:app --reload
```
A API estará disponível em: `http://127.0.0.1:8000`

### Endpoints Disponíveis
#### Upload de PDF e Geração de Resumo
- **POST** `/pdf/upload-pdf/`
  - Upload de um arquivo PDF e retorno do resumo gerado.

#### Obter Resumo por Número de Processo
- **GET** `/pdf/generate-summary/?process_number=<NUMERO>`
  - Obtém o resumo final de um conjunto de documentos baseados em um número de processo.

#### Processar um Diretório de PDFs
- **GET** `/pdf/process-dataset/`
  - Processa todos os arquivos PDF de um diretório específico.

## Tecnologias Utilizadas
- **Python 3.9+**
- **FastAPI** (Framework para API REST)
- **PyMuPDF (fitz)** (Extração de texto de PDFs)
- **AWS Bedrock** (Modelo de IA para geração de resumos)
- **Boto3** (Integração com AWS)
- **Uvicorn** (Servidor ASGI para FastAPI)

## Contribuição
Se você deseja contribuir para o projeto:
1. Fork o repositório
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adiciona minha feature'`
4. Envie para o repositório: `git push origin minha-feature`
5. Abra um Pull Request

## Licença
Este projeto está sob a licença MIT.

