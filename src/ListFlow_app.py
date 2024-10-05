import json
import os
import logging
from logging.handlers import RotatingFileHandler

# Configuração do logger com RotatingFileHandler
LOG_FILENAME = 'listflow.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuração do manipulador de logs com rotação
handler = RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=5 * 1024 * 1024,  # Tamanho máximo de 5 MB por arquivo de log
    backupCount=3  # Manter até 3 arquivos de backup
)

# Definir o formato do log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Caminho para o arquivo de armazenamento das tarefas
ARQUIVO_TAREFAS = 'tarefas.json'


# Função para carregar as tarefas a partir de um arquivo JSON
def carregar_tarefas():
    if not os.path.exists(ARQUIVO_TAREFAS):
        logger.warning("Arquivo de tarefas não encontrado. Criando um novo arquivo.")
        return []
    with open(ARQUIVO_TAREFAS, 'r') as arquivo:
        logger.info("Tarefas carregadas com sucesso do arquivo.")
        return json.load(arquivo)


# Função para salvar as tarefas no arquivo JSON
def salvar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, 'w') as arquivo:
        json.dump(tarefas, arquivo, indent=4)
    logger.info(f"{len(tarefas)} tarefas salvas no arquivo {ARQUIVO_TAREFAS}.")


# Função para listar todas as tarefas com opção de filtro e ordenação
def listar_tarefas(tarefas, filtro=None, ordenar_por=None):
    # Aplicar filtro nas tarefas
    if filtro:
        if filtro == 'pendente':
            tarefas = [tarefa for tarefa in tarefas if not tarefa['concluida']]
        elif filtro == 'concluida':
            tarefas = [tarefa for tarefa in tarefas if tarefa['concluida']]
        logger.info(f"Tarefas filtradas por: {filtro}")

    # Ordenar tarefas
    if ordenar_por:
        if ordenar_por == 'nome':
            tarefas.sort(key=lambda tarefa: tarefa['nome'].lower())
        elif ordenar_por == 'status':
            tarefas.sort(key=lambda tarefa: tarefa['concluida'])
        elif ordenar_por == 'entrada':
            tarefas.sort(key=lambda tarefa: tarefa['id'])
        logger.info(f"Tarefas ordenadas por: {ordenar_por}")

    if not tarefas:
        print("Não há tarefas para exibir com o filtro selecionado.")
        logger.warning("Nenhuma tarefa disponível para exibição com o filtro aplicado.")
        return
    
    print("\n--- Lista de Tarefas ---")
    for index, tarefa in enumerate(tarefas):
        status = 'Concluída' if tarefa['concluida'] else 'Pendente'
        print(f"{index + 1}. {tarefa['nome']} - {status}")
    print("------------------------\n")
    logger.info(f"{len(tarefas)} tarefas listadas.")


# Função para adicionar uma nova tarefa
def adicionar_tarefa(tarefas):
    nome_tarefa = input("Digite o nome da nova tarefa: ").strip()
    if not nome_tarefa:
        print("O nome da tarefa não pode ser vazio.")
        logger.warning("Tentativa de adicionar tarefa com nome vazio.")
        return
    
    nova_tarefa = {'id': len(tarefas) + 1, 'nome': nome_tarefa, 'concluida': False}
    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")
    logger.info(f"Tarefa adicionada: {nova_tarefa}")


# Função para remover uma ou mais tarefas existentes ou todas as tarefas
def remover_tarefas(tarefas):
    listar_tarefas(tarefas)
    try:
        print("Para remover várias tarefas, digite os números separados por vírgula (exemplo: 1,2,3).")
        print("Para remover todas as tarefas, digite 'todas'.")
        entrada = input("Digite o número da(s) tarefa(s) que deseja remover: ").strip().lower()

        if entrada == 'todas':
            tarefas.clear()
            salvar_tarefas(tarefas)
            print("Todas as tarefas foram removidas com sucesso!")
            logger.info("Todas as tarefas foram removidas pelo usuário.")
        else:
            indices = entrada.split(',')
            removidas = []
            for indice in sorted(indices, reverse=True):  # Reverter para remover corretamente
                if indice.isdigit():
                    indice = int(indice) - 1
                    if 0 <= indice < len(tarefas):
                        removidas.append(tarefas.pop(indice)['nome'])
                    else:
                        print(f"Número de tarefa inválido: {indice + 1}")
                        logger.warning(f"Tentativa de remover tarefa com índice inválido: {indice + 1}")
                else:
                    print(f"Entrada inválida: {indice}. Por favor, digite números válidos.")
                    logger.error(f"Entrada inválida fornecida para remover tarefas: {indice}")
            
            if removidas:
                salvar_tarefas(tarefas)
                logger.info(f"Tarefas removidas: {', '.join(removidas)}")
                print(f"Tarefas removidas com sucesso: {', '.join(removidas)}")
            else:
                print("Nenhuma tarefa foi removida.")
    except ValueError:
        print("Entrada inválida. Por favor, digite números separados por vírgula ou 'todas'.")
        logger.error("Erro ao tentar remover tarefas: entrada não numérica.")


# Função para marcar ou desmarcar uma ou mais tarefas como concluídas
def marcar_tarefa_concluida(tarefas):
    listar_tarefas(tarefas)
    try:
        acao = input("Deseja 'marcar' ou 'desmarcar' as tarefas como concluídas? ").strip().lower()
        if acao not in ['marcar', 'desmarcar']:
            print("Opção inválida. Escolha 'marcar' ou 'desmarcar'.")
            logger.warning("Ação inválida fornecida para marcar/desmarcar tarefas.")
            return

        print("Para marcar/desmarcar várias tarefas, digite os números separados por vírgula (exemplo: 1,2,3).")
        print("Para marcar/desmarcar todas as tarefas, digite 'todas'.")
        entrada = input("Digite o número da(s) tarefa(s) que deseja alterar: ").strip().lower()
        
        if entrada == 'todas':
            for tarefa in tarefas:
                tarefa['concluida'] = (acao == 'marcar')
            salvar_tarefas(tarefas)
            logger.info(f"Todas as tarefas foram {acao}das como concluídas.")
            print(f"Todas as tarefas foram {acao}das como concluídas!")
        else:
            indices = entrada.split(',')
            alteradas = []
            for indice in indices:
                if indice.isdigit():
                    indice = int(indice) - 1
                    if 0 <= indice < len(tarefas):
                        tarefas[indice]['concluida'] = (acao == 'marcar')
                        alteradas.append(tarefas[indice]['nome'])
                    else:
                        print(f"Número de tarefa inválido: {indice + 1}")
                        logger.warning(f"Tentativa de marcar tarefa com índice inválido: {indice + 1}")
                else:
                    print(f"Entrada inválida: {indice}. Por favor, digite números válidos ou 'todas'.")
                    logger.error(f"Entrada inválida fornecida para marcar/desmarcar tarefas: {indice}")
            
            if alteradas:
                salvar_tarefas(tarefas)
                logger.info(f"Tarefas {acao}das como concluídas: {', '.join(alteradas)}")
                print(f"Tarefas {acao}das como concluídas: {', '.join(alteradas)}")
            else:
                print(f"Nenhuma tarefa foi {acao}da como concluída.")

    except ValueError:
        print("Entrada inválida. Por favor, digite números separados por vírgula ou 'todas'.")
        logger.error("Erro ao tentar marcar/desmarcar tarefas: entrada não numérica.")


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
                logger.info(f"Tarefa editada: {tarefas[indice]}")
            else:
                print("O nome da tarefa não pode ser vazio.")
                logger.warning("Tentativa de editar tarefa com nome vazio.")
        else:
            print("Número de tarefa inválido.")
            logger.warning("Número de tarefa inválido fornecido para edição.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
        logger.error("Erro ao tentar editar tarefa: entrada não numérica.")


# Função principal que executa o loop do menu
def menu():
    tarefas = carregar_tarefas()
    logger.info("Programa iniciado.")
    while True:
        print("\n--- Programa de Gerenciamento de Tarefas ---")
        print("1. Listar Tarefas (todas, pendentes ou concluídas)")
        print("2. Adicionar Tarefa")
        print("3. Remover Tarefa(s)")
        print("4. Marcar ou Desmarcar Tarefa como Concluída")
        print("5. Editar Tarefa")
        print("6. Ordenar Tarefas por Nome")
        print("7. Ordenar Tarefas por Status")
        print("8. Ordenar Tarefas por Ordem de Entrada")
        print("9. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
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
            remover_tarefas(tarefas)
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
            logger.info("Programa encerrado pelo usuário.")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida do menu.")
            logger.warning("Opção inválida fornecida no menu.")

# Executar o programa
if __name__ == '__main__':
    menu()

