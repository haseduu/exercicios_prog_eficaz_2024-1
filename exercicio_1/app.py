# initiaç setup ===============================
from flask import Flask, render_template, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

app = Flask(__name__)

def connect_db():
    """Establishes a connection to the database using the provided configuration."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# LANDING PAGE ===================================
@app.route('/')
def landing_page():
    return {"status": "api working"}

# CLIENTES========================================

@app.route('/clientes', methods=["GET"])
def lista_clientes():
    conn = None
    cursor = None
    error = None
    clientes = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_clientes"
            cursor.execute(sql)
            clientes = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"Livros": [{"nome": cliente["nome"], "cpd": cliente["cpf"], "email": cliente["email"], "id": cliente["id"]} for cliente in clientes]}, 200
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    dados = request.json
    campos_obrigatorios = ["nome", "cpf", "email", "senha"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400
    nome = dados['nome']
    cpf = dados['cpf']
    email = dados['email']
    senha = dados['senha']
    conn = None
    cursor = None
    cliente_id = None
    error = None

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_clientes (nome, cpf, email, senha) VALUES (%s, %s, %s, %s)"
            values = (nome,cpf,email,senha)
            cursor.execute(sql, values)
            conn.commit()
            cliente_id = cursor.lastrowid
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"mensagem": f"Cliente de nome {nome} cadastrado com sucesso! o id é {cliente_id}, guarde esse valor para realizar buscas!"}, 201

@app.route('/clientes/<int:idd>', methods=['GET'])
def buscar_cliente(idd):
    conn = None
    cursor = None
    cliente = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_clientes WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            cliente = cursor.fetchone()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not cliente:
        return {"error": "ID especificado não encontrado"}, 404
    return {"nome": cliente['nome'], "email": cliente["email"], "cpf": cliente["cpf"], "seenha": cliente['senha'], "id": cliente["id"]}, 200

@app.route('/clientes/<int:idd>', methods=['PUT'])
def editar_cliente(idd):
    dados = request.json
    campos_obrigatorios = ["nome", "cpf", "email", "senha"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400

    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE tbl_clientes SET nome = %s, email = %s, cpf = %s, senha = %s WHERE id = %s"
            values = (dados['nome'], dados['email'], dados['cpf'], dados["senha"], idd)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado cheque as informações"}, 400
    return {"mensagem": "Cliente editado com sucesso"}, 200

@app.route('/clientes/<int:idd>', methods=['DELETE'])
def deletar_cliente(idd):
    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM tbl_clientes WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado, cheque as informações"}, 400
    return {"mensagem": "Cliente deletado com sucesso"}, 200

# PRODUTOS ============================================

@app.route('/produtos', methods=["GET"])
def lista_produtos():
    conn = None
    cursor = None
    error = None
    produtos = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_produtos"
            cursor.execute(sql)
            produtos = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"produtos": [{"nome": produto["nome"], "descricao": produto["descricao"], "preco": produto["preco"], "qtd_em_estoque": produto['qtd_em_estoque'], "custo_no_fornecedor": produto["custo_no_fornecedor"], "id": produto["id"], "id_fornecedor": produto['fornecedor_id']} for produto in produtos]}, 200


@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    dados = request.json
    campos_obrigatorios = ["nome", "descricao", "preco", "qtd_em_estoque", "fornecedor_id", "custo_no_fornecedor"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400
    nome = dados['nome']
    descricao = dados['descricao']
    preco = dados['preco']
    qtd_em_estoque = dados['qtd_em_estoque']
    fornecedor_id = dados['fornecedor_id']
    custo_no_fornecedor = dados['custo_no_fornecedor']
    conn = None
    cursor = None
    produto_id = None
    error = None

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_produtos (nome, descricao, preco, qtd_em_estoque, fornecedor_id, custo_no_fornecedor) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nome,descricao,preco,qtd_em_estoque,fornecedor_id,custo_no_fornecedor)
            cursor.execute(sql, values)
            conn.commit()
            produto_id = cursor.lastrowid
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"mensagem": f"produto de nome {nome} cadastrado com sucesso! o id é {produto_id}, guarde esse valor para realizar buscas!"}, 201

@app.route('/produtos/<int:idd>', methods=['GET'])
def buscar_produto(idd):
    conn = None
    cursor = None
    produto = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_produtos WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            produto = cursor.fetchone()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not produto:
        return {"error": "ID especificado não encontrado"}, 404
    return {"nome": produto['nome'], "descricao": produto["descricao"], "preco": produto["preco"], "qtd_em_estoque": produto['qtd_em_estoque'], 
            "fornecedor_id": produto['fornecedor_id'], 
            "custo_no_fornecedor": produto["custo_no_fornecedor"],
            "id": produto["id"]}, 200

@app.route('/produtos/<int:idd>', methods=['PUT'])
def editar_produto(idd):
    dados = request.json
    campos_obrigatorios = ["nome", "descricao", "preco", "qtd_em_estoque", "fornecedor_id", "custo_no_fornecedor"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400

    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE tbl_produtos SET nome = %s, descricao = %s, preco = %s, qtd_em_estoque = %s, fornecedor_id = %s, custo_no_fornecedor = %s WHERE id = %s"
            values = (dados['nome'], dados['descricao'], dados['preco'], dados["qtd_em_estoque"], dados["fornecedor_id"], dados['custo_no_fornecedor'], idd)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado cheque as informações"}, 400
    return {"mensagem": "produto editado com sucesso"}, 200

@app.route('/produtos/<int:idd>', methods=['DELETE'])
def deletar_produto(idd):
    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM tbl_produtos WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado, cheque as informações"}, 400
    return {"mensagem": "produto deletado com sucesso"}, 200

# FORNECEDORES ===============================================

@app.route('/fornecedores', methods=["GET"])
def lista_fornecedores():
    conn = None
    cursor = None
    error = None
    fornecedores = []
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_fornecedores"
            cursor.execute(sql)
            fornecedores = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"fornecedores": [{"nome": fornecedor["nome"], "email": fornecedor["email"], "cnpj": fornecedor["cnpj"], "id": fornecedor["id"]} for fornecedor in fornecedores]}, 200


@app.route('/fornecedores', methods=['POST'])
def cadastrar_fornecedor():
    dados = request.json
    campos_obrigatorios = ["nome", "email", "cnpj"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400
    nome = dados['nome']
    email = dados['email']
    cnpj = dados['cnpj']
    conn = None
    cursor = None
    fornecedor_id = None
    error = None

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_fornecedores (nome, email, cnpj) VALUES (%s, %s, %s)"
            values = (nome,email,cnpj)
            cursor.execute(sql, values)
            conn.commit()
            fornecedor_id = cursor.lastrowid
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"mensagem": f"fornecedor de nome {nome} cadastrado com sucesso! o id é {fornecedor_id}, guarde esse valor para realizar buscas!"}, 201

@app.route('/fornecedores/<int:idd>', methods=['GET'])
def buscar_fornecedor(idd):
    conn = None
    cursor = None
    fornecedor = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_fornecedores WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            fornecedor = cursor.fetchone()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not fornecedor:
        return {"error": "ID especificado não encontrado"}, 404
    return {"nome": fornecedor['nome'], "email": fornecedor["email"], "cnpj": fornecedor["cnpj"], "id": fornecedor["id"]}, 200

@app.route('/fornecedores/<int:idd>', methods=['PUT'])
def editar_fornecedor(idd):
    dados = request.json
    campos_obrigatorios = ["nome", "email", "cnpj"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400

    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE tbl_fornecedores SET nome = %s, email = %s, cnpj = %s WHERE id = %s"
            values = (dados['nome'], dados['email'], dados['cnpj'], idd)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado cheque as informações"}, 400
    return {"mensagem": "fornecedor editado com sucesso"}, 200

@app.route('/fornecedores/<int:idd>', methods=['DELETE'])
def deletar_fornecedor(idd):
    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM tbl_fornecedores WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado, cheque as informações"}, 400
    return {"mensagem": "fornecedor deletado com sucesso"}, 200

# CARRINHO ===================================

@app.route('/carrinhos', methods=["GET"])
def lista_carrinhos():
    conn = None
    cursor = None
    error = None
    
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_carrinhos"
            cursor.execute(sql)
            carrinhos = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"carrinhos": [{"produto_id": carrinho["produto_id"], "quantidade": carrinho["quantidade"], "cliente_id": carrinho['cliente_id']} for carrinho in carrinhos]}, 200


@app.route('/carrinhos', methods=['POST'])
def cadastrar_carrinho():
    dados = request.json
    campos_obrigatorios = ["produto_id", "quantidade", "cliente_id"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400
    nome = dados['nome']
    quantidade = dados['quantidade']
    cliente_id = dados['cliente_id']
    conn = None
    cursor = None
    carrinho_id = None
    error = None

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_carrinhos (produto_id, quantidade, cliente_id) VALUES (%s, %s, %s)"
            values = (nome,quantidade,cliente_id)
            cursor.execute(sql, values)
            conn.commit()
            carrinho_id = cursor.lastrowid
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"mensagem": f"carrinho cadastrado com sucesso! o id é {carrinho_id}, guarde esse valor para realizar buscas!"}, 201

@app.route('/carrinhos/<int:idd>', methods=['GET'])
def buscar_carrinho(idd):
    conn = None
    cursor = None
    carrinho = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_carrinhos WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            carrinho = cursor.fetchone()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not carrinho:
        return {"error": "ID especificado não encontrado"}, 404
    return {"produto_id": carrinho['produto_id'], "quantidade": carrinho["quantidade"], "cliente_id": carrinho["cliente_id"], "id": carrinho["id"]}, 200

@app.route('/carrinhos/<int:idd>', methods=['PUT'])
def editar_carrinho(idd):
    dados = request.json
    campos_obrigatorios = ["produto_id", "quantidade", "cliente_id"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400

    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE tbl_carrinhos SET produto_id = %s, quantidade = %s, cliente_id = %s WHERE id = %s"
            values = (dados['produto_id'], dados['quantidade'], dados['cliente_id'], idd)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado cheque as informações"}, 400
    return {"mensagem": "carrinho editado com sucesso"}, 200

@app.route('/carrinhos/<int:idd>', methods=['DELETE'])
def deletar_carrinho(idd):
    conn = None
    cursor = None
    error = None
    rows_affected = 0

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM tbl_carrinhos WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            conn.commit()
            rows_affected = cursor.rowcount
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if rows_affected == 0:
        return {"error": "ID especificado não encontrado, cheque as informações"}, 400
    return {"mensagem": "carrinho deletado com sucesso"}, 200

@app.route('/carrinhos/cliente/<int:idd>', methods=['GET'])
def buscar_carrinho_cliente(idd):
    conn = None
    cursor = None
    carrinho = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_carrinhos WHERE cliente_id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            carrinhos = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not carrinho:
        return {"error": "ID especificado não encontrado"}, 404
    return {f"carrinhos de cliente com id {idd}": [{"produto_id": carrinho["produto_id"], "quantidade": carrinho["quantidade"], "cliente_id": carrinho['cliente_id']} for carrinho in carrinhos]}, 200

# PEDIDOS =======================================================

@app.route('/pedidos', methods=["GET"])
def lista_pedidos():
    conn = None
    cursor = None
    error = None
    
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_pedidos"
            cursor.execute(sql)
            pedidos = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"pedidos": [{"cliente_id": pedido["cliente_id"], "carrinho_id": pedido["carrinho_id"], "data_e_hora": pedido["data"], "status": pedido['status'], "id": pedido["id"]} for pedido in pedidos]}, 200


@app.route('/pedidos', methods=['POST'])
def cadastrar_pedido():
    dados = request.json
    campos_obrigatorios = ["cliente_id", "carrinho_id", "status"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return {"error": f"Campo: {campo} faltando"}, 400
    cliente_id = dados['cliente_id']
    carrinho_id = dados['carrinho_id']
    status = dados['status']
    conn = None
    cursor = None
    pedido_id = None
    error = None

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO tbl_pedidos (cliente_id, carrinho_id, status) VALUES (%s, %s, %s)"
            values = (cliente_id, carrinho_id, status)
            cursor.execute(sql, values)
            conn.commit()
            pedido_id = cursor.lastrowid
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    return {"mensagem": f"pedido cadastrado com sucesso! o id é {pedido_id}, guarde esse valor para realizar buscas!"}, 201

@app.route('/pedidos/<int:idd>', methods=['GET'])
def buscar_pedido(idd):
    conn = None
    cursor = None
    pedido = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_pedidos WHERE id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            pedido = cursor.fetchone()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not pedido:
        return {"error": "ID especificado não encontrado"}, 404
    return {"cliente_id": pedido['cliente_id'], "carrinho_id": pedido["carrinho_id"], "status": pedido["status"], "id": pedido["id"]}, 200

@app.route('/pedidos/cliente/<int:idd>', methods=['GET'])
def buscar_pedido_cliente(idd):
    conn = None
    cursor = None
    pedido = None
    error = None
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM tbl_pedidos WHERE cliente_id = %s"
            values = (idd,)
            cursor.execute(sql, values)
            pedidos = cursor.fetchall()
    except Error as err:
        error = str(err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    if error:
        return {"error": error}, 500
    if not conn:
        return {"error": "Failed to connect to the database"}, 500
    if not pedido:
        return {"error": "ID especificado não encontrado"}, 404
    return {f"pedidos de cliente com id {idd}": [{"cliente_id": pedido["cliente_id"], "carrinho_id": pedido["carrinho_id"], "id": pedido['id']} for pedido in pedidos]}, 200


if __name__ == '__main__':
    app.run(debug=True)