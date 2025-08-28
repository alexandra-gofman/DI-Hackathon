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
    eid = str(eid)
    connection = connection_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM expenses WHERE id = %s', eid)
    output = cursor.fetchone()
    user_id = output[0]
    user_date = output[1].isoformat()
    user_amount = float(output[2])
    user_currency = output[3]
    user_list = [user_id, user_date, user_amount, user_currency]
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



# IN THE END OF THE PROJECT, LAST STEP IS: CREATE A requirements.txt FILE:
# ON THE TERMINAL RUN: py -m pip freeze > requirements.txt 
# the requirements file SHOULD be pushed to github