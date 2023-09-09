import sqlite3
from time import time

start = time()
conn = sqlite3.connect('gmbl.db')
cursor = conn.cursor()
cursor.execute("Select * from last100")
last100 = cursor.fetchall()
cursor.execute("Select * from profitchart")
profitchart = [row[0] for row in cursor.fetchall()]
cursor.execute("Select * from poolsettings")
poolsettings = cursor.fetchall()[0]

print(f'Data is ready. Preperation time for data is {(time()-start)*1000}ms')

while True:
    match input('Welcome Admin, What would you like to do?\n>> ').lower():
        case "profit sum": print(f"Your casino's profit is: | {sum(profitchart)}$ |\n--------------------------------")
        case "max profit": print(f"You earned maximum of | {max(profitchart)}$ | in one bet!\n--------------------------------")
        case "max loss": print(f"You lost maximum of | {abs(min(profitchart))} | in one bet!\n--------------------------------")
        case 'set data limit':
            try:
                cursor.execute("UPDATE adminsettings SET DataCount=?",(int(input("Set the new Data limit(input anything but integer to quit the menu.): ")),))
                conn.commit()
            except ValueError: print('Only use INTEGERS.')
        case 'set profit multiplier':
            try:
                cursor.execute("UPDATE adminsettings SET ProfitMultiplier=?", (float(input('Set the new Profit Multiplier:')),))
                conn.commit()
            except ValueError: print('Only use FLOATS.Integers are also accepted. Use dot(.) and not comma(,)!')
        case 'set profit mode':
            new_mode = input('Profit Mode Selection (pool or limit):  ').upper()
            if new_mode not in ['POOL','LIMIT']:
                print('Only use pool or limit. do not use other keywords!')
            cursor.execute("UPDATE adminsettings SET ProfitMode=?",(new_mode,))
            conn.commit()
        case 'reset pool':
            cursor.execute("UPDATE poolsettings SET CurrentPool=?",(0,))
            conn.commit()
        case 'set pool profit':
            try:
                cursor.execute("UPDATE poolsettings SET PoolExpectation=?",(int(input("New Pool Expectation: ")),))
                conn.commit()
            except ValueError:
                print('Only use INTEGERS. No floats or strings allowed!')
        case "see pool earnings":
            print(f"Current profit is: {poolsettings[1]} in pool mode!")
        case "exit":
            print('See you soon, Admin!')
            break
        case _:
            print('Unknown command. Commands are:\n|| profit sum - max profit - max loss - exit - set profit multiplier - set data limit - set profit mode ||')
            print("||  reset pool - set pool profit - see pool earnings")




