# ListFlow
Projeto de Gerenciamento de Tarefas - ListFlow. Aplicação de terminal para gerenciar tarefas com persistência de dados.

## Descrição

O **ListFlow** é uma ferramenta CLI (Command-Line Interface) para gerenciamento de tarefas e listas. Com ele, você pode adicionar, remover, marcar como concluída, filtrar e organizar tarefas de forma simples e eficiente. Todas as tarefas são armazenadas em um arquivo local JSON, permitindo que você tenha total controle sobre o gerenciamento das suas tarefas de maneira fácil e rápida.

## Funcionalidades

O ListFlow possui as seguintes funcionalidades:

- **Adicionar Tarefa**: Cria novas tarefas com um nome fornecido pelo usuário.
- **Remover Tarefa**: Remove uma tarefa existente com base no número da tarefa listado.
- **Listar Tarefas**: Exibe todas as tarefas, com opções para filtrar por `pendente`, `concluída` ou sem filtro.
- **Marcar/Desmarcar Tarefas como Concluídas**: Permite marcar ou desmarcar tarefas específicas como concluídas.
- **Editar Nome da Tarefa**: Edita o nome de uma tarefa existente.
- **Ordenação**: Ordena as tarefas por:
  - Nome
  - Status (pendente/concluída)
  - Ordem de Entrada (ID)
- **Armazenamento Local**: Todas as tarefas são armazenadas em um arquivo JSON (`tarefas.json`) para fácil persistência de dados.
- **Interface de Menu**: Navegação simples por um menu CLI que oferece várias opções para gerenciar as tarefas.

## Instalação

O projeto não requer dependências adicionais e pode ser executado em um ambiente virtual `venv`. Para configurar o ambiente e executar o projeto, siga os passos abaixo:

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/ListFlow.git
    ```
2. Entre no diretório do projeto:
    ```bash
    cd ListFlow
    ```
3. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate  # Linux/Mac
    ```
    ```bash
    venv\Scripts\activate  # Windows
    ```
4. Execute o script diretamente:
    ```bash
    python listflow.py
    ```

## Uso

Ao iniciar o script `listflow.py`, o menu principal será exibido, permitindo que você escolha entre as opções para gerenciar suas tarefas. As principais opções são:

1. **Listar Tarefas**: Exibe todas as tarefas cadastradas. Pode-se aplicar um filtro para mostrar apenas as `pendentes` ou `concluídas`.
2. **Adicionar Tarefa**: Solicita ao usuário o nome da nova tarefa e a adiciona à lista.
3. **Remover Tarefa**: Remove uma tarefa existente com base em seu número na lista.
4. **Marcar/Desmarcar Tarefa como Concluída**: Permite marcar ou desmarcar tarefas como concluídas.
5. **Editar Tarefa**: Edita o nome de uma tarefa existente com base em seu número na lista.
6. **Ordenar Tarefas**: Ordena a lista de tarefas com base em nome, status ou ordem de entrada.

### Exemplo de Uso

Após iniciar o script, você verá o menu principal:

--- Programa de Gerenciamento de Tarefas ---

1. Listar Tarefas (todas, pendentes ou concluídas)
2. Adicionar Tarefa
3. Remover Tarefa
4. Marcar ou Desmarcar Tarefa como Concluída
5. Editar Tarefa
6. Ordenar Tarefas por Nome
7. Ordenar Tarefas por Status
8. Ordenar Tarefas por Ordem de Entrada
9. Sair


Escolha a opção desejada digitando o número correspondente e siga as instruções fornecidas pelo programa.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias ou correções.

1. Faça um fork do projeto.
2. Crie uma nova branch com a funcionalidade desejada: `git checkout -b minha-nova-feature`.
3. Envie suas alterações: `git commit -m 'Adiciona nova feature'`.
4. Faça um push para a branch: `git push origin minha-nova-feature`.
5. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

- Autor: Rodrigo das Neves Bindewald
- E-mail: [nevesrnb@gmail.com](mailto:nevesrnb@gmail.com)




