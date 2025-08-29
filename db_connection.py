import psycopg2
from connect import DATABASE, USER, PASSWORD,HOST, PORT

def connection_to_db():
    connection = psycopg2.connect(database=DATABASE,
                                  user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT)
    return connection

def db_creation():
    connection = connection_to_db()
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    date DATE NOT NULL,
                    amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
                    currency VARCHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
                    amount_ils NUMERIC(12,2),
                    rate_ils_per_unit NUMERIC(18,8),
                    category_id INTEGER NOT NULL,
                    CONSTRAINT fk_expenses_category
                        FOREIGN KEY (category_id) REFERENCES categories(id));''')

    cursor.execute('''INSERT INTO categories (name) VALUES
                    ('Food'), ('Transport'), ('Home'),
                    ('Entertainment'), ('Health'),
                    ('Shopping'), ('Travel')
                    ON CONFLICT (name) DO NOTHING;''')


    connection.commit()


def show_categories():
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT id, name FROM categories;')
    rows = cursor.fetchall()
    return dict(rows)

def show_expenses():
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM expenses;')
    table = cursor.fetchall()
    return table

def check_null_in_amount_ils():
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT id, amount_ils FROM expenses WHERE amount_ils IS NULL')
    rows = cursor.fetchall()
    return dict(rows)

def connect_to_the_line(eid):
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT id, date, amount, currency, amount_ils, rate_ils_per_unit, category_id FROM expenses WHERE id = %s ORDER BY date', (eid,))
    output = cursor.fetchone()
    user_id = output[0]
    user_date = output[1].isoformat()
    user_amount = float(output[2])
    user_currency = output[3]
    if output[4] == None:
        user_amount_ils = None
    else:
        user_amount_ils = float(output[4])
    if output[5] == None:
        user_rate_ils_per_unit = None
    else:
        user_rate_ils_per_unit = float(output[5])
    user_category_id = output[6]
    user_list = [user_id, user_date, user_amount, user_currency, user_amount_ils, user_rate_ils_per_unit, user_category_id]
    return user_list

def update_the_line(list_of_new_data):
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('''UPDATE expenses
                    SET amount_ils = %s,
                        rate_ils_per_unit = %s
                    WHERE id = %s''',
                   (list_of_new_data[4], list_of_new_data[5], list_of_new_data[0]))
    connection.commit()

def count_num_of_lines():
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM expenses;')
    total = cursor.fetchone()[0]
    return total

def last_n_expenses(n):
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('''SELECT id, date, amount, currency, amount_ils, rate_ils_per_unit, category_id
                        FROM expenses
                        ORDER BY date DESC, id DESC 
                        LIMIT %s;''', (n))
    rows = cursor.fetchall()
    return list(rows)

def return_monthly_report(date):
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('''WITH bounds AS (
                      SELECT make_date(%s, %s, 1) AS d1,
                             make_date(%s, %s, 1) + INTERVAL '1 month' AS d2
                      )
                    SELECT
                      COALESCE(c.name, 'TOTAL') AS category,
                      ROUND(SUM(e.amount_ils), 2) AS total_ils
                    FROM expenses e
                    JOIN categories c ON c.id = e.category_id
                    JOIN bounds b ON true
                    WHERE e.amount_ils IS NOT NULL
                      AND e.date >= b.d1 AND e.date < b.d2
                    GROUP BY ROLLUP (c.name)
                    ORDER BY (c.name IS NULL), total_ils DESC;
                        ''', (date[0], date[1], date[0], date[1]))
    rows = cursor.fetchall()
    return rows

print(return_monthly_report(['2025', '8']))



# IN THE END OF THE PROJECT, LAST STEP IS: CREATE A requirements.txt FILE:
# ON THE TERMINAL RUN: py -m pip freeze > requirements.txt 
# the requirements file SHOULD be pushed to github