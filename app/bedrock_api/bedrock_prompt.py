from app.utils.questions import SUMMARY_QUESTIONS

# Prompt para gerar os resumos parciais
def create_summary_prompt(text, questions=SUMMARY_QUESTIONS):
    questions_text = "\n".join(f"- {q}" for q in questions)
    prompt = f"""
Human: Crie um resumo **detalhado e abrangente** do seguinte texto. O resumo deve ser escrito de forma **fluida e contínua**, apresentando **todos os pontos** com profundidade, para que o usuário final tenha uma compreensão completa e detalhada sobre o conteúdo. Use as questões abaixo como base, mas **não inclua as perguntas no resumo final**. O foco deve ser em oferecer um panorama **geral, coeso e bem estruturado**, com **detalhes suficientes para cobrir todas as nuances e pontos implícitos** do texto. Não resuma excessivamente, forneça **explicações detalhadas e exemplos** sempre que possível.
Texto:
{text}

Questões:
{questions_text}

Assistant:
"""
    return prompt

# Prompt para gerar o resumo final
def generate_final_summary(summaries, questions=SUMMARY_QUESTIONS):
    questions_text = "\n".join(f"- {q}" for q in questions)
    prompt = f"""
Human: Baseado nos resumos parciais fornecidos, crie uma **Sinteze final detalhado e coeso** do diretório de documentos em 4000 palavras. A sinteze deve ser escrita de forma **fluida e contínua**, apresentando **todos os pontos com profundidade** para que o usuário final tenha uma compreensão completa e abrangente sobre o processo. Utilize as questões abaixo como base para **integrar e sintetizar** as informações dos resumos parciais em um único panorama geral. A sitenze deve ser **abrangente, explicativo e conter entre uma e duas páginas** de conteúdo, fornecendo um panorama **detalhado e bem estruturado**. Não resuma excessivamente, forneça **detalhes e exemplos sempre que possível** para garantir que o conteúdo seja rico e completo. OBS: O resumo final deve ser estruturado em parágrados

Resumos Parciais:
{summaries}

Questões:
{questions_text}

Assistant:
"""
    return prompt
