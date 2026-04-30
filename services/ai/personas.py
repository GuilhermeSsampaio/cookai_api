from google import genai
from settings.settings import GOOGLE_API_KEY

cookai_client = genai.Client(api_key=GOOGLE_API_KEY)


def make_scrapping_prompt(text: str, font_of_url: str) -> str:
    return (
        "Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:\n\n"
        f"{text}\n\n"
        "Caso nao tenha o tempo de forno indique o recomendado.\n"
        "Use titulos de secao para separar os ingredientes do modo de preparo.\n"
        "O titulo da receita deve ser o primeiro item do resumo e deve usar heading 1.\n"
        f"Abaixo do titulo, coloque a fonte da receita (site) e o link. Use {font_of_url}.\n"
        "Traduza para o portugues."
    )


def make_web_search_prompt(query: str) -> str:
    return (
        "Encontre receitas com base na seguinte especificacao: "
        f"{query}.\n"
        "Busque receitas populares e bem avaliadas na internet.\n"
        "Nao invente receitas.\n"
        "Retorne as receitas no seguinte formato:\n"
        "[\n"
        "  {\n"
        "    \"title\": \"Titulo da receita\",\n"
        "    \"font\": \"Fonte da receita\",\n"
        "    \"link\": \"Link da receita\",\n"
        "    \"content\": \"Resumo com ingredientes, tempo e modo de preparo\"\n"
        "  }\n"
        "]"
    )
