from db_connection import db_creation, show_categories, check_null_in_amount_ils, connect_to_the_line, update_the_line
from api_currency_Frankfurter import return_currencies_from_api, exchange_money, check_exchange_rates, check_connection
from adding_expense import Expense


# dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    db_creation()  # db creation
    while True:
        print('''Please choose the option:
    1. Show categories
    2. Add expense (ILS)
    3. Add expense with conversion (YOUR CURRENCY → ILS)
    4. Recalculate pending conversions (fill amount_ils for rows where it’s NULL)
    5. Show last N expenses
    6. Monthly report (totals & by category)
    7. Export monthly report (JSON/CSV)
    8. Seed demo data (Faker)
    9. Clear all of table "expenses" data
    10. Exit''')

        while True:
            first_user_input = input('Your answer: ').strip()
            try:
                first_user_input = int(first_user_input)
                if 1 <= first_user_input <= 10:
                    break
                else:
                    print('Please enter a number between 1 an 10')
            except ValueError:
                print('Please enter a number between 1 an 10')

        if first_user_input == 1:
            '''1. Show categories'''

            rows = show_categories()
            for cid, name in rows.items():
                print(f'    {cid}) {name}')
            break

        if first_user_input == 2:
            '''2. Add expense (ILS)'''

            print('Adding a new expense in ILS...')
            user_date = input('    Please enter a date in format YYYY-MM-DD: ').strip()
            user_amount = int(input('    Please enter amount in ILS: '))
            while True:
                user_category = input('    Please enter a category of the expense: ').strip()
                user_category = user_category.capitalize()
                rows = show_categories()
                if user_category not in rows.values():
                    print('    Your category does not exist. Please choose one from the list:')
                    for cid, name in rows.items():
                        print(f'    {cid}) {name}')
                else:
                    break
            name_to_id = {v: k for k, v in rows.items()} #reverse dict
            user_category_id = int(name_to_id.get(user_category))
            user_expense = Expense(user_date, user_amount, 'ILS', user_category_id, amount_ils=user_amount)
            user_expense.adding_ils_expense_to_db()
            print('Your expense was successfully added to DB Table')

        if first_user_input == 3:
            '''3. Add expense with conversion (YOUR CURRENCY → ILS)'''
            print('Adding a new expense in other currency...')

            user_date = input('    Please enter a date in format YYYY-MM-DD: ').strip()
            user_amount = int(input('    Please enter amount in other currency: '))

            while True:
                currency_list = return_currencies_from_api()
                user_currency = input('    Please enter currency: ')
                user_currency = user_currency.upper()
                if user_currency not in currency_list:
                    print(f'    Please choose one currency from the list.\n List of supported currencies: {currency_list}')
                else:
                    break

            while True:
                user_category = input('    Please enter a category of the expense: ').strip()
                user_category = user_category.capitalize()
                rows = show_categories()
                if user_category not in rows.values():
                    print('    Your category does not exist. Please choose one from the list:')
                    for cid, name in rows.items():
                        print(f'    {cid}) {name}')
                else:
                    break

            name_to_id = {v: k for k, v in rows.items()}  # reverse dict
            user_category_id = name_to_id.get(user_category)

            user_amount_ils = exchange_money(user_date, user_amount, user_currency)
            user_rate_ils_per_unit = check_exchange_rates(user_date, user_currency)

            user_expense = Expense(user_date, user_amount, user_currency, user_category_id, user_amount_ils, user_rate_ils_per_unit)

            user_expense.adding_ils_expense_to_db()
            print('Your expense was successfully added to DB Table')

        if first_user_input == 4:
            if check_connection():
                null_dict = check_null_in_amount_ils()
                if null_dict != {}:
                    for key in null_dict.keys():
                        list_of_rows = connect_to_the_line(key)
                        user_amount_ils_new = exchange_money(list_of_rows[1], list_of_rows[2], list_of_rows[3])
                        user_rate_ils_per_unit_new = check_exchange_rates(list_of_rows[1], list_of_rows[3])
                        list_of_rows.append(user_amount_ils_new)
                        list_of_rows.append(user_rate_ils_per_unit_new)
                        update_the_line(list_of_rows)
                    print('NULLs fixed!')
                else:
                    print('There are no NULLs')
            else:
                print('Please check your connection')

        if first_user_input == 5:
            pass
        if first_user_input == 6:
            pass
        if first_user_input == 7:
            pass
        if first_user_input == 8:
            pass
        if first_user_input == 9:
            pass
        if first_user_input == 10:
            break


main()
