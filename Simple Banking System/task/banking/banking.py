import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# cur.execute('DELETE FROM card')
# conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS card ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'number TEXT,'
            'pin TEXT,'
            'balance INTEGER DEFAULT 0);'
            )
conn.commit()

cur.execute('SELECT * FROM card;')
print(cur.fetchall())

isLogged = False


def print_menu():
    if not isLogged:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
    else:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")


def luhn(number):
    arr = [int(x) for x in number]
    for i in range(0, len(arr)):
        if i % 2 == 0:
            arr[i] *= 2
        if arr[i] > 9:
            arr[i] -= 9
    return sum(arr) % 10 == 0


def generate_account():
    number = '400000' + '{0:09}'.format(random.randrange(0, 999999999)) + str(random.randrange(0, 9))

    while not luhn(number):
        number = '400000' + '{0:09}'.format(random.randrange(0, 999999999)) + str(random.randrange(0, 9))

    pin = '{0:04}'.format(random.randrange(0, 9999))
    cur.execute(f"INSERT INTO card (number, pin) VALUES ({number}, {pin});")
    conn.commit()
    # accounts[number] = {'PIN': pin, 'balance': 0}

    print("\nYour card has been created")
    print(f"Your card number:\n{number}")
    print(f"Your card PIN:\n{pin}")


print_menu()

select = input()
current_number = None
current_pin = None

while select != '0':

    if select == '1' and not isLogged:
        generate_account()
        print()
        print_menu()

    elif select == '1' and isLogged:
        # print("\nBalance: " + str(accounts[current_number]['balance']))
        cur.execute(f"SELECT balance FROM card WHERE number={current_number}")
        res = cur.fetchone()

        print("\nBalance: " + str(res[0]))
        print()
        print_menu()

    elif select == '2' and not isLogged:
        print("\nEnter your card number:")
        current_number = input()
        print("Enter your PIN:")
        current_pin = input()

        cur.execute(f"SELECT * FROM card WHERE number={current_number}")
        res = cur.fetchone()

        if res is not None and res[2] == current_pin:
            isLogged = True
            print("\nYou have successfully logged in!\n")
            print_menu()
        else:
            print("\nWrong card number or PIN!\n")
            print_menu()

    elif select == '2' and isLogged:
        print("\nEnter income:")
        income = int(input())
        if income > 0:
            cur.execute(f"UPDATE card SET balance = balance + {income} WHERE number = {current_number}")
            conn.commit()
            print("Income was added!\n")
            print_menu()
        else:
            print("\nIncorrect value!\n")
            print_menu()

    elif select == '3' and isLogged:
        print("\nTransfer")

        cur.execute(f"SELECT balance FROM card WHERE number={current_number}")
        balance_from = cur.fetchone()[0]

        print("Enter card number:")
        card_to = input()
        cur.execute(f"SELECT * FROM card WHERE number = {card_to};")
        res = cur.fetchone()

        if not luhn(card_to):
            print("Probably you made a mistake in the card number. Please try again!\n")
            print_menu()
        elif res is None:
            print("Such a card does not exist.\n")
            print_menu()
        else:
            if current_number == card_to:
                print("You can't transfer money to the same account!\n")
                print_menu()
            else:
                print("Enter how much money you want to transfer:")
                value = int(input())

                if balance_from < value:
                    print("Not enough money!\n")
                    print_menu()
                else:
                    cur.execute(f"UPDATE card SET balance = balance - {value} WHERE number = {current_number};")
                    conn.commit()
                    cur.execute(f"UPDATE card SET balance = balance + {value} WHERE number = {card_to}")
                    conn.commit()
                    print("Success!\n")
                    print_menu()

    elif select == '4' and isLogged:
        cur.execute(f"DELETE FROM card WHERE number={current_number};")
        conn.commit()
        print("\nThe account has been closed!\n")
        isLogged = False
        print_menu()

    elif select == '5' and isLogged:
        isLogged = False
        print("\nYou have successfully logged out!\n")
        print_menu()

    else:
        print("\nNo such option!\n")
        print_menu()

    select = input()

print("Bye!")
