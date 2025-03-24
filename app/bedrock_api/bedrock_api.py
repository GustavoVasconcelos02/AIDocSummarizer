from app.bedrock_api.bedrock_prompt import create_summary_prompt, generate_final_summary
from app.bedrock_api.bedrock_client import get_bedrock_client
import json

# Configurações da GenAI
def get_completion(prompt, max_tokens_to_sample=2000):
    client = get_bedrock_client()
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens_to_sample,
        "temperature": 0.7, # Aleatoriedade da geração de texto
        "top_k": 1, # Quantas palavras candidatas são consideradas em cada etapa da geração
        "top_p": 0.9 
    })

    response = client.invoke_model(
        body=body, 
        modelId='anthropic.claude-v2', 
        accept='application/json', 
        contentType='application/json')

    response_body = json.loads(response['body'].read())
    completion = response_body.get('completion')

    return completion.replace('\n', ' ').replace("\"", "")

def process_text(text, questions, is_final_summary=False):
    if is_final_summary:
        # Se for um resumo final, usamos generate_final_summary
        prompt = generate_final_summary(text, questions)
    else:
        # Caso contrário, usamos create_summary_prompt
        prompt = create_summary_prompt(text, questions)
    
    # Obtém a resposta da IA com base no prompt
    response_text = get_completion(prompt)

    return response_text
    
