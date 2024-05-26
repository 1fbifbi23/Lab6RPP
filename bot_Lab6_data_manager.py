from flask import Flask, request, jsonify
import psycopg2
# from starlette.responses import JSONResponse



app = Flask(__name__)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    database='ershtrub_database',
    user='ershtrub_username',
    password='1234'
)
# Создание курсора для выполнения SQL- запросов
cur = conn.cursor()

# Создание таблицы currencies
cur.execute(
    "CREATE TABLE IF NOT EXISTS currencies("
    "id SERIAL NOT NULL,"
    "currency_name  VARCHAR (100) NOT NULL,"
    "rate NUMERIC NOT NULL)"
)
# Сохранение изменений в базе данных
conn.commit()


@app.route('/convert', methods=['GET'])
def convert_currency():
    cur = conn.cursor()

    data = request.json
    currency_name = data.get('currency_name')
    amount = data.get('amount')

    cur.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency_name,))
    result = cur.fetchone()

    if result:
        rate = result[0]
        converted_amount = float(amount) * float(rate)
        return jsonify({'converted_amount': converted_amount}), 200
    else:
        return jsonify({"error": 'Указанной валюты нет в списке. Пожалуйста, выберите из доступных валют'}), 400


@app.route('/currencies', methods=['GET'])
def get_currencies():
    cur = conn.cursor()
    cur.execute('SELECT * FROM currencies')
    currencies = cur.fetchall()
    conn.close()
    return jsonify({'currencies': currencies})


if __name__ == "__main__":
    app.run(port=5002)
