# Desafio 1 de Web Services RESTful com Flask e MySQL

## Objetivo
Neste desafio, você desenvolverá um sistema completo de vendas online, abrangendo clientes, produtos, estoque, carrinhos de compras e pedidos. Implementando RESTful Web Services com Flask e MySql, seu objetivo é construir uma API RESTful robusta, aplicando os princípios do Nível 2 do Modelo de Maturidade de Richardson.

## Requisitos do Sistema

### Estrutura do Projeto
Mantenha uma estrutura de projeto limpa e organizada, dividida em:
- Código (incluindo `app.py` e módulos Python adicionais).
- Coleção Postman (`postman_collection.json`).
- Documentação da API (recomendada).

### Modelagem Relacional
Desenvolva um esquema de banco de dados relacional no PostgreSQL com as seguintes entidades e atributos:

#### Tabelas
- **tbl_clientes**: `id` (auto incremento), `nome`, `email` (único), `cpf` (único), `senha`.
- **tbl_produtos**: `id` (auto incremento), `nome`, `descricao`, `preco`, `qtd_em_estoque`, `fornecedor_id`, `custo_no_fornecedor`.
- **tbl_fornecedores**: `id` (auto incremento), `nome`, `email` (único), `cnpj` (único).
- **tbl_carrinho**: `id` (auto incremento), `produto_id`, `quantidade`.
- **tbl_pedido**: `id` (auto incremento), `cliente_id`, `carrinho_id`, `data_hora`, `status` (`pendente`, `aprovado`, `cancelado`, `entregue`).

### Implementação da API RESTful

#### Endpoints e Verbos HTTP

- **Clientes**
  - `GET /clientes`: Lista todos os clientes.
  - `POST /clientes`: Cria um novo cliente.
  - `GET /clientes/{cliente_id}`: Detalhes do cliente.
  - `PUT /clientes/{cliente_id}`: Atualiza cliente.
  - `DELETE /clientes/{cliente_id}`: Exclui cliente.

- **Produtos**
  - `GET /produtos`: Lista todos os produtos.
  - `POST /produtos`: Cria novo produto.
  - `GET /produtos/{produto_id}`: Detalhes do produto.
  - `PUT /produtos/{produto_id}`: Atualiza produto.
  - `DELETE /produtos/{produto_id}`: Exclui produto.

- **Carrinho**
  - `POST /carrinhos`: Adiciona item ao carrinho.
  - `PUT /carrinhos/{carrinho_id}`: Atualiza item no carrinho.
  - `DELETE /carrinhos/{carrinho_id}`: Remove item do carrinho.
  - `GET /carrinhos`: Lista todos os carrinhos.
  - `GET /carrinhos/{carrinho_id}`: Lista um carrinho específico.
  - `GET /carrinhos/cliente/{cliente_id}`: Lista todos os carrinhos de um cliente específico.

- **Pedidos**
  - `GET /pedidos`: Lista todos os pedidos do cliente.
  - `POST /pedidos`: Cria novo pedido.
  - `GET /pedidos/{pedido_id}`: Detalhes do pedido.
  - `GET /pedidos/cliente/{cliente_id}`: Lista pedidos do cliente.

- **Pense e crie o restante das especificações de rota dos recursos não listado acima**


#### Relacionamentos e Restrições:

- Um cliente pode ter vários pedidos.
- Um carinho pode ter vários produtos e um produto pode estar em vários carrinhos. 
- Um pedido tem um cliente e um carrinho (relacionamento com Carrinho).


#### Códigos de Status HTTP

Use os códigos de status HTTP corretamente para indicar o resultado de cada operação (200, 201, 400, 404, 500).

#### Validação de Campos

Valide campos obrigatórios e opcionais, fornecendo feedback claro ao usuário.

#### Atualizações Parciais

Permita atualizações parciais de recursos nos endpoints apropriados.

### Deploy

Realize o deploy de sua API no Render ou outra plataforma de nuvem.

#### Filtros e Ordenação

Implemente filtros e ordenação nos endpoints de listagem.

#### Imagens para Produtos (totalmente opcional)

Adicione suporte a imagens nos produtos. [Não cai na prova]

#### Sistema de Notificações (totalmente opcional)

Crie notificações por email para pedidos. Dica: Pesquise "enviar email gmail flask". [Não cai na prova]

## Tutoriais e Recursos

Aqui estão alguns recursos que podem ajudá-lo a completar este desafio:

## Fonte de Informação

### Notion da dicplina: 
- https://slender-ceder-1da.notion.site/a09548d285554638af41c2ad3989b79f?v=c25df69714e94eb1aca7df10cebb9ec7&pvs=4


### Ajuda com Flask

- Intro: https://www.tutorialspoint.com/flask/flask_application.htm

- Recebendo JSON via requisição: https://stackabuse.com/how-to-get-and-parse-http-post-body-in-flask-json-and-form-data/

- Variáveis na URL (urls dinâmicas): https://www.geeksforgeeks.org/generating-dynamic-urls-in-flask/

- Query Parameters: https://stackabuse.com/get-request-query-parameters-with-flask/

- Documentação oficial: https://flask.palletsprojects.com/en/3.0.x/

### Ajuda com Postman

- Intro: https://learning.postman.com/docs/getting-started/first-steps/sending-the-first-request/

- Importando uma collection: https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data/


## Conclusão

Este desafio é uma oportunidade excelente para aprimorar suas habilidades de desenvolvimento de Web Services RESTful com tecnologias modernas. Esperamos que você encontre este projeto não apenas educativo, mas também agradável. Boa sorte!

## Observações

- Adapte o desafio conforme necessário, focando no aprendizado e na aplicação de boas práticas.
- Priorize a clareza e a segurança em sua implementação.
- Use este desafio como uma chance para explorar novas ferramentas e técnicas.
