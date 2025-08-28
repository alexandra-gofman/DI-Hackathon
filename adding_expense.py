from db_connection import connection_to_db, show_categories

class Expense:

    def __init__(self, date, amount, currency, category_id, amount_ils=None, rate_ils_per_unit=None):
        self.date = date
        self.amount = amount
        self.currency = currency
        self.category_id = category_id
        self.amount_ils = amount_ils
        self.rate_ils_per_unit = rate_ils_per_unit

    def adding_ils_expense_to_db(self):
        connection = connection_to_db()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO expenses (date, amount, currency, amount_ils, rate_ils_per_unit, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''',
                    (self.date, self.amount, self.currency, self.amount_ils, self.rate_ils_per_unit, self.category_id))

        connection.commit()
        return 'Expense added sucsessfully'

    def find_category_by_id(self):
        category_dict = show_categories()
        return category_dict[self.category_id]
