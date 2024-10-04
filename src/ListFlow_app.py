import json
import os

# Caminho para o arquivo de armazenamento das tarefas
ARQUIVO_TAREFAS = 'tarefas.json'


# Função para carregar as tarefas a partir de um arquivo JSON
def carregar_tarefas():
    if not os.path.exists(ARQUIVO_TAREFAS):
        return []
    with open(ARQUIVO_TAREFAS, 'r') as arquivo:
        return json.load(arquivo)


# Função para salvar as tarefas no arquivo JSON
def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, 'w') as arquivo:
        json.dump(tarefas, arquivo, indent=4)


# Função para listar todas as tarefas com opção de filtro e ordenação
def listar_tarefas(tarefas, filtro=None, ordenar_por=None):
    # Aplicar filtro nas tarefas
    if filtro:
        if filtro == 'pendente':
            tarefas = [tarefa for tarefa in tarefas if not tarefa['concluida']]
        elif filtro == 'concluida':
            tarefas = [tarefa for tarefa in tarefas if tarefa['concluida']]
    
    # Ordenar tarefas
    if ordenar_por:
        if ordenar_por == 'nome':
            tarefas.sort(key=lambda tarefa: tarefa['nome'].lower())
        elif ordenar_por == 'status':
            tarefas.sort(key=lambda tarefa: tarefa['concluida'])
        elif ordenar_por == 'entrada':
            tarefas.sort(key=lambda tarefa: tarefa['id'])

    # Verifica se há tarefas após a filtragem
    if not tarefas:
        print("Não há tarefas para exibir com o filtro selecionado.")
        return
    
    print("\n--- Lista de Tarefas ---")
    for index, tarefa in enumerate(tarefas):
        status = 'Concluída' if tarefa['concluida'] else 'Pendente'
        print(f"{index + 1}. {tarefa['nome']} - {status}") # (ID: {tarefa['id']}
    print("------------------------\n")


# Função para adicionar uma nova tarefa
def adicionar_tarefa(tarefas):
    nome_tarefa = input("Digite o nome da nova tarefa: ").strip()
    if not nome_tarefa:
        print("O nome da tarefa não pode ser vazio.")
        return
    
    # Definir um novo ID para a tarefa com base na quantidade de tarefas existentes
    nova_tarefa = {'id': len(tarefas) + 1, 'nome': nome_tarefa, 'concluida': False}
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")


# Função para remover uma tarefa existente
def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    try:
        indice = int(input("Digite o número da tarefa que deseja remover: ")) - 1
        if 0 <= indice < len(tarefas):
            tarefa_removida = tarefas.pop(indice)
            salvar_tarefas(tarefas)
            print(f"Tarefa '{tarefa_removida['nome']}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")


# Função para marcar ou desmarcar uma ou mais tarefas como concluídas
def marcar_tarefa_concluida(tarefas):
    listar_tarefas(tarefas)
    try:
        # Perguntar ao usuário se deseja marcar ou desmarcar tarefas
        acao = input("Deseja 'marcar' ou 'desmarcar' as tarefas como concluídas? ").strip().lower()
        if acao not in ['marcar', 'desmarcar']:
            print("Opção inválida. Escolha 'marcar' ou 'desmarcar'.")
            return

        # Instruções para o usuário
        print("Para marcar/desmarcar várias tarefas, digite os números separados por vírgula (ex: 1,2,3).")
        print("Para marcar/desmarcar todas as tarefas, digite 'todas'.")
        
        # Receber a entrada do usuário
        entrada = input("Digite o número da(s) tarefa(s) que deseja alterar: ").strip().lower()
        
        if entrada == 'todas':
            # Marcar ou desmarcar todas as tarefas com base na escolha
            for tarefa in tarefas:
                tarefa['concluida'] = (acao == 'marcar')
            salvar_tarefas(tarefas)
            if acao == 'marcar':
                print("Todas as tarefas foram marcadas como concluídas!")
            else:
                print("Todas as tarefas foram desmarcadas como concluídas!")
        else:
            # Marcar/desmarcar as tarefas selecionadas com base nos números fornecidos
            indices = entrada.split(',')
            alteradas = []
            for indice in indices:
                if indice.isdigit():
                    indice = int(indice) - 1  # Ajuste para índice base 0
                    if 0 <= indice < len(tarefas):
                        tarefas[indice]['concluida'] = (acao == 'marcar')
                        alteradas.append(tarefas[indice]['nome'])
                    else:
                        print(f"Número de tarefa inválido: {indice + 1}")
                else:
                    print(f"Entrada inválida: {indice}. Por favor, digite números válidos ou 'todas'.")
            
            # Salvar somente se houver tarefas válidas para alterar o status
            if alteradas:
                salvar_tarefas(tarefas)
                print(f"Tarefas {acao}das como concluídas: {', '.join(alteradas)}")
            else:
                print(f"Nenhuma tarefa foi {acao}da como concluída.")

    except ValueError:
        print("Entrada inválida. Por favor, digite números separados por vírgula ou 'todas'.")


# Função para editar o nome de uma tarefa existente
def editar_tarefa(tarefas):
    listar_tarefas(tarefas)
    try:
        indice = int(input("Digite o número da tarefa que deseja editar: ")) - 1
        if 0 <= indice < len(tarefas):
            novo_nome = input(f"Digite o novo nome para a tarefa '{tarefas[indice]['nome']}': ").strip()
            if novo_nome:
                tarefas[indice]['nome'] = novo_nome
                salvar_tarefas(tarefas)
                print(f"Tarefa '{novo_nome}' editada com sucesso!")
            else:
                print("O nome da tarefa não pode ser vazio.")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")


# Função principal que executa o loop do menu
def menu():
    tarefas = carregar_tarefas()
    while True:
        print("\n--- Programa de Gerenciamento de Tarefas ---")
        print("1. Listar Tarefas (todas, pendentes ou concluídas)")
        print("2. Adicionar Tarefa")
        print("3. Remover Tarefa")
        print("4. Marcar ou Desmarcar Tarefa como Concluída")
        print("5. Editar Tarefa")
        print("6. Ordenar Tarefas por Nome")
        print("7. Ordenar Tarefas por Status")
        print("8. Ordenar Tarefas por Ordem de Entrada")
        print("9. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            # Tratamento do filtro para listar tarefas
            while True:
                filtro = input("Deseja aplicar um filtro? (todas, pendente, concluida): ").strip().lower()
                if filtro in ['todas', 'pendente', 'concluida']:
                    listar_tarefas(tarefas, filtro if filtro != 'todas' else None)
                    break
                else:
                    print("Opção inválida. Por favor, escolha entre: todas, pendente ou concluida.")
        elif opcao == '2':
            adicionar_tarefa(tarefas)
        elif opcao == '3':
            remover_tarefa(tarefas)
        elif opcao == '4':
            marcar_tarefa_concluida(tarefas)
        elif opcao == '5':
            editar_tarefa(tarefas)
        elif opcao == '6':
            listar_tarefas(tarefas, ordenar_por='nome')
        elif opcao == '7':
            listar_tarefas(tarefas, ordenar_por='status')
        elif opcao == '8':
            listar_tarefas(tarefas, ordenar_por='entrada')
        elif opcao == '9':
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida do menu.")


# Executar o programa
if __name__ == '__main__':
    menu()
