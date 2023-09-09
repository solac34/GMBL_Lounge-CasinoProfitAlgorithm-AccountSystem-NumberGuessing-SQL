import sqlite3
from random import choice,randint
from string import ascii_lowercase, ascii_uppercase
import yagmail

conn = sqlite3.connect('gmbl.db')
cursor = conn.cursor()

cursor.execute("Select * from adminsettings")
adminsettings = cursor.fetchall()[0]


# ACCOUNT SYSTEMS
def get_login_datas():
    cursor.execute("Select * from login_datas")
    return cursor.fetchall()


def login(username, password):
    for data in get_login_datas():
        if username in data:
            if password in data:
                print(f"Welcome to the lounge, {data[1]}")
                play_game(data[0])
                return True
    if input(
            "There are no matches with the credentials you supplied.Input l to try again- anything but l to quit\nType Here: ").lower() == 'l':
        login(input("Username: "), input("Password: "))


def username_check(username):
    for data in login_datas:
        if username == data[1]: return username_check(input("This username already exists!\nUsername: "))
    if username.lower() == 'q':
        print('We hope you will change your mind and register!')
        exit(0)
    if not 2 < len(username) < 13:
        return username_check(input("Length must be 3 to 12 characters long!\nUsername: "))
    return username


def password_check(password):
    if password.lower() == 'q':
        print('We hope you will change your mind and register!')
        exit(0)
    pw_checklist = [False, False, False]  # lowercase - uppercase - number

    if not 5 < len(password) < 17: return password_check(input("Length must be 6 to 16 characters long!\nPassword: "))
    for letter in password:
        if letter in ascii_lowercase:
            pw_checklist[0] = True
        elif letter in ascii_uppercase:
            pw_checklist[1] = True
        elif letter in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            pw_checklist[2] = True
    if all(pw_checklist):
        return password
    else:
        return password_check(
            input("Password must contain Uppercase,Lowercase letters and at least a number!\nPassword: "))

def code_verifier(code,email):
    yagmail.SMTP("yourmail@gmail.com","yourAppPassword").send(email,"Complete Registration for my test app",f"Welcome to app!\n-------------\nHere is Your Code: {code}")
    try:
        if int(input("Enter the code you just received from us via emaiL: ")) == code:
            return 1
        else: return 0
    except ValueError:
        print("Please only use INTEGERS. No other formats are allowed!!")
        code_verifier(code,email)


def email_check(email):
    if email.lower() == 'q':
        print('We hope you will change your mind and register!')
        exit(0)
    if email[-4:] != '.com':
        return email_check(input("Email must end with .com!\nEmail: "))
    if '@' not in email or '@' in email[:3]:
        return email_check(input("Email must contain @!\nEmail: "))
    if code_verifier(randint(1000,9999),email):
        return email
    else:
        if input("Incorrect code supplied. If you want to quit signing up, enter anything but s , to continue, enter s\nType here: ").loewr() == 's':
            return email_check(input('Email: '))
        else:
            exit(0)


def signup():
    cursor.execute("INSERT INTO login_datas(id,username,password,email) VALUES(?,?,?,?)",
                   (len(login_datas),
                    username_check(input("Username must be between 3-12 characters long.\nUsername: ")),
                    password_check(input(
                        "Password must contain an uppercase, a lowercase letter and a number.Length must be 6-16 characters long.\nPassword: ")),
                    email_check(input("Only .com domain emails are accepted.\nEmail: "))))
    conn.commit()
    cursor.execute("INSERT INTO balancechart(id,balance) VALUES(?,?)", (len(login_datas), 100))
    conn.commit()
    print('You successfully signed up, Welcome to our Lounge!')
    login(*get_login_datas()[-1][1:3])

######################################################################################################################


def guesscheck(guess, multiplier, amount):
    try:  # see if user inputted true form of a guess.
        guess = int(guess)
        total_range = {2: 10, 5: 50, 15: 100, 50: 300, 100: 500, 1000: 1000}[
            multiplier]  # convert the multiplier to the max. range num
        if not 0 <= guess < total_range:
            return guesscheck(input(f'Please only guess in range >>1-{total_range}<<!\nYour Guess: '), multiplier,
                              amount)
        return guess, total_range
    except ValueError:
        return guesscheck(input('Please only use numbers!\nYour Guess: '), multiplier, amount)




def truenum(guess, multiplier, amount):  # returns the true number.
    guess, total_range = guesscheck(guess, multiplier, amount)
    cursor.execute("Select * from last100")  # fetch the data from last100 table.
    last100 = cursor.fetchall()  # returns a list which containts TUPLES for each COLUMN.
    if len(last100) > adminsettings[1] - 1:  # if the data has reached limit bets, reset the table and return impossible
        cursor.execute("DELETE FROM last100")  # delete all the data in last100 table
        conn.commit()
        result = choice(
            [i for i in range(0, total_range) if i != guess])  # return number which is impossible to be guess.
    else:  # if there is sufficient data
        if amount * multiplier > sum(
                [row[2] for row in last100]) / adminsettings[
            0]:  # if the user's gains is bigger than total profit x 1.20, lose him
            result = choice([i for i in range(0, total_range) if i != guess])  # same list as above.
        else:  # if user won't make casino go bankrupt give them 4x chance to win
            result = choice([guess, guess, guess, *(i for i in range(0, total_range))])

    print(f'-------------\nYou guessed: | {guess} |\nTrue number is: | {result} |')
    return 1 if guess == result else 0


def pool_truenum(guess, multiplier, amount):
    cursor.execute("Select * from poolsettings")
    poolsettings = cursor.fetchall()[0]
    guess, total_range = guesscheck(guess, multiplier, amount)
    if multiplier * amount < poolsettings[1] - poolsettings[
        0]:  # if the user's prize won't pool go under the limits, 100% winrate
        result = guess
    elif multiplier * amount < poolsettings[
        0] / 100:  # if that's not the case but the user's prize is lower than 1% of pool, 4x chance
        result = choice([guess, guess, guess, *(i for i in range(0, total_range))])
    else:
        result = choice(
            [i for i in range(0, total_range) if i != guess])  # return number which is impossible to be guess.

    print(f'-------------\nYou guessed: | {guess} |\nTrue number is: | {result} |')
    return 1 if guess == result else 0


def play_game(user_id):
    cursor.execute("Select balance from balancechart where id=?", (user_id,))
    balance = cursor.fetchall()[0][0]
    while 1:  # get the bet multipliler
        bet_kind = input(
            'Welcome to the Number Guess Game.These are the bets:\n> 2x for 1-10 <\n> 5x for 1-50 <\n> 15x for '
            '1-100 <\n> 50x for 1-300 <\n> 100x for 1-500 <\n> 1000x for 1-1000 <\nInput the multiplier:(2-1000 '
            'only from the list above.): ')
        if bet_kind not in ['2', '5', '15', '50', '100', '1000']:
            print('|||  PLEASE ONLY INPUT ACCEPTED MULTIPLIERS. ACCEPTED '
                  'MULTIPLIERS ARE: 2 & 5 & 15 & 50 & 100 & 1000  |||')
        else:
            bet_kind = int(bet_kind)
            break  # if bet kind is accepted, then end the loop and continue to next step

    while 1:  # how much money will the user bet on - find bugs
        try:
            print(f"Your current balance is {balance}")
            bet_amount = int(input("How much money will you bet on?:"))
            if not 0 < bet_amount <= balance:
                print('Please bet greater than 0 and less than your balance!')
                continue
            break
        except ValueError:
            print('---\nPlease only use numbers.No floats. INTEGERS ONLY.\n---')

    if adminsettings[2] == 'LIMIT':
        if truenum(input("Your guess: "), bet_kind, bet_amount):
            print(f'>>>>>>>>>>  You WON! <<<<<\n>> You earned: | {bet_amount * bet_kind}$ | <<\n-------------')
            profit = bet_kind * bet_amount
        else:
            print(f'>>>>>  You LOST! <<<<<\n>> You lost: | {bet_amount}$ | <<\n-------------')
            profit = -1 * bet_amount

        cursor.execute("insert into last100(Multiplier,Bet,Profit) VALUES(?,?,?)", (bet_kind, bet_amount, profit))
        conn.commit()
        cursor.execute("Insert into profitchart(Profit) VALUES(?)", (profit,))
        conn.commit()

    else:  # if the profit mode is POOL
        if pool_truenum(input("Your guess: "), bet_kind, bet_amount):
            print(f'>>>>>>>>>>  You WON! <<<<<\n>> You earned: | {bet_amount * bet_kind}$ | <<\n-------------')
            profit = bet_kind * bet_amount
        else:
            print(f'>>>>>  You LOST! <<<<<\n>> You lost: | {bet_amount}$ | <<\n-------------')
            profit = -1 * bet_amount

        cursor.execute("UPDATE poolsettings SET CurrentPool=CurrentPool + ?", (profit,))
        conn.commit()

    if profit + balance > 0: # if user haven't go bankrupt yet
        cursor.execute("UPDATE balancechart SET balance= balance + ? WHERE id=?", (profit, user_id))
        conn.commit()
        if input('input c to continue. - input anything but c to quit.').lower() == 'c':  play_game(user_id)
    else: # if user went bankrurpt
        print('YOU WENT BANKRUPT! You will not be able to play any games in further.Your account will be deleted, but you can create a new one if you desire! ')
        cursor.execute("DELETE from balancechart WHERE id=?", (user_id,))
        conn.commit()
        cursor.execute("DELETE FROM login_datas where id=?", (user_id,))
        conn.commit()




while True:
    match input(
        '||| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |||\n||         Welcome to GMBL Lounge! '
        'input l to log in - s to sign up          ||\n||| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
        '- - - - - - |||\nType Here: ').lower():
        case "l":
            login(input("Username: "), input("Password: "))
        case "s":
            login_datas = get_login_datas()
            signup()
        case "exit":
            break
        case _:
            print("Invalid command.")
            continue
    break
