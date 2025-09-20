# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de busca semântica que permite fazer perguntas sobre o conteúdo de um arquivo PDF usando LangChain, PostgreSQL com pgVector e OpenAI.

## Como executar a solução

### 1. Configurar ambiente virtual Python

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure sua chave da OpenAI:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Subir o banco de dados PostgreSQL

```bash
docker compose up -d
```

### 5. Executar ingestão do PDF

```bash
python3 src/ingest.py
```

### 6. Iniciar o chat

```bash
python3 src/chat.py
```

## Como usar

Após executar `python src/chat.py`, você verá a interface do chat:

```
==================================================
Digite 'sair' ou 'quit' para encerrar o chat.
Faça sua pergunta:
==================================================

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?

Buscando informações...

RESPOSTA: O faturamento da SuperTechIABrazil é R$ 10.000.000,00.
```

### Exemplos de uso:

**Pergunta sobre conteúdo do PDF:**
```
PERGUNTA: Qual o faturamento da empresa?
RESPOSTA: [Resposta baseada no conteúdo do PDF]
```

**Pergunta fora do contexto:**
```
PERGUNTA: Qual é a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## Arquitetura

- **ingest.py**: Script para processar o PDF e armazenar embeddings no banco
- **search.py**: Função para criar a chain de busca semântica e LLM  
- **chat.py**: Interface CLI para interagir com o usuário

## Tecnologias utilizadas

- **Python** + **LangChain**: Framework principal
- **PostgreSQL** + **pgVector**: Banco de dados vetorial
- **OpenAI**: Embeddings (text-embedding-3-small) e LLM (gpt-5-nano)
- **Docker**: Para execução do banco de dados

## Configuração

### Variáveis de ambiente (.env):
- `OPENAI_API_KEY`: Sua chave da OpenAI
- `OPENAI_EMBEDDING_MODEL`: Modelo de embeddings (text-embedding-3-small)
- `DATABASE_URL`: URL do PostgreSQL
- `PG_VECTOR_COLLECTION_NAME`: Nome da coleção no banco
- `PDF_PATH`: Caminho para o arquivo PDF

### Parâmetros de ingestão:
- **Chunk size**: 1000 caracteres
- **Chunk overlap**: 150 caracteres

## Comandos para parar

Para parar o banco de dados:
```bash
docker compose down
```

Para limpar volumes (apagar dados):
```bash
docker compose down -v
```