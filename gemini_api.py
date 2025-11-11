import google.generativeai as genai

# Substitua pela sua API key do Gemini
API_KEY = "SUA_API_KEY_AQUI"

genai.configure(api_key=API_KEY)

def gerar_feedback(pergunta, resposta):
    prompt = f"""
    Você é um recrutador profissional. Avalie a resposta de um candidato para a pergunta abaixo.
    Pergunta: {pergunta}
    Resposta: {resposta}

    Forneça um feedback construtivo e uma nota de 0 a 10.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Erro ao gerar feedback automático: {e}]"
