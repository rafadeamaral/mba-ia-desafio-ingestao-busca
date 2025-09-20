import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

for k in ("OPENAI_API_KEY","DATABASE_URL","PG_VECTOR_COLLECTION_NAME","OPENAI_EMBEDDING_MODEL"):
    if not os.getenv(k):
        raise RuntimeError(f"A variável de ambiente {k} não está definida")
        
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
    
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    def get_context(query):
        results = store.similarity_search_with_score(query, k=10)
        docs = [doc for doc, _ in results]
        return "\n".join(doc.page_content for doc in docs)

    prepare = RunnableLambda(lambda question: {"contexto": get_context(question), "pergunta": question})
    
    return prepare | prompt | llm | StrOutputParser()