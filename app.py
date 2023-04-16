import os
import json
from flask import Flask, jsonify, request
import mysql.connector
from datetime import date, datetime

app = Flask(__name__)

# Configura as variáveis de ambiente para conexão com o banco de dados
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
AUTH_PLUGIN = os.environ["AUTH_PLUGIN"]

# Cria a conexão com o banco de dados
connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    auth_plugin=AUTH_PLUGIN,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Cria a tabela 'patient' no banco de dados, caso ainda não exista
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            disease VARCHAR(255) NOT NULL,
            data_internacao DATE NOT NULL,
            PRIMARY KEY (id)
        )
    """)

# Testar se o App está no ar: http://127.0.0.1:5000/
# Deve retornar: API is running! no Browser
@app.route("/")
def index():
    return "API is rodando"

# Seleciona todos os registros da tabela 'patient'
# No Browser acesse: http://127.0.0.1:5000/patient
# para ver os produtos no navegador
@app.route("/patient", methods=["GET"])
def get_patient():
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM patient')
            records = cursor.fetchall()
            data = [{'id': record[0], 'name': record[1], 'disease': record[2], 'data_internacao': record[3].strftime('%Y-%m-%d')} for record in records]
            return jsonify(data)
    except Error as e:
        print(e)
        return jsonify({'message': 'Erro ao buscar registros da tabela patient.'}), 500

# Insere registros no Banco (API)
@app.route("/patient", methods=["POST"])
def create_patient():
    # Obtém os dados enviados na requisição
    data = request.get_json()
    name = data["name"]
    disease = data["disease"]
    data_internacao = data["data_internacao"]

    # Insere os dados na tabela 'patient'
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO patient (name, disease, data_internacao)
            VALUES (%s, %s, %s)
        """, (name, disease, data_internacao))
        connection.commit()

    # Retorna uma mensagem de sucesso como resposta
    return {"message": "Registro inserido com sucesso!"}

# Atualiza registros no Banco (API)
@app.route("/patient/<int:id>", methods=["PUT"])
def update_patient(id):
    # Obtém os dados enviados na requisição
    data = request.get_json()
    name = data["name"]
    disease = data["disease"]
    data_internacao = data["data_internacao"]

    # Atualiza os dados do registro com o ID especificado na tabela 'patient'
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE patient
            SET name=%s, disease=%s, data_internacao=%s
            WHERE id=%s
        """, (name, disease, data_internacao, id))
        connection.commit()

    # Retorna uma mensagem de sucesso como resposta
    return {"message": "Registro atualizado com sucesso!"}

# Deleta registros no Banco (API)
@app.route("/patient/<int:id>", methods=["DELETE"])
def delete_patient(id):
    # Deleta o registro com o ID especificado na tabela 'patient'
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM patient
            WHERE id=%s
        """, (id,))
        connection.commit()

    # Retorna uma mensagem de sucesso como resposta
    return {"message": "Registro deletado com sucesso!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
