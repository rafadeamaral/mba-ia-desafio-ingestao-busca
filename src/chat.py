from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("="*50)
    print("Digite 'sair' ou 'quit' para encerrar o chat.")
    print("Faça sua pergunta:")
    print("="*50)
    
    while True:
        print()

        pergunta = input("PERGUNTA: ").strip()

        print()
        
        if pergunta.lower() in ['sair', 'quit', 'exit', 'q']:
            print("Chat encerrado. Até logo!")
            break
        
        if not pergunta:
            print("Por favor, digite uma pergunta válida.")
            continue
        
        print("Buscando informações...")
        
        resposta = chain.invoke(pergunta)
        
        print()
        print(f"RESPOSTA: {resposta}")
        print()
        print("-"*50)

if __name__ == "__main__":
    main()