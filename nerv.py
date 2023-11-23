import sqlite3
from datetime import datetime


db = sqlite3.connect('nerv_database.db')

cursor = db.cursor()


######## comment out block after first run
"""
cursor.execute('''
    CREATE TABLE pilots(id TEXT PRIMARY KEY, KPI TEXT,
                   	Pilot TEXT, Test_date DATETIME, Test_result INT)
''')
"""
######## comment out block after first run

kpi1 = 'Synch rate'


pilot1 = 'Rei Ayanami'
testdate1 = '2023-12-12 15:33:33'
result1 = 0.44
id1 = pilot1+kpi1+testdate1


pilot2 = 'Asuka Langley Soryu'
testdate2 = '2023-12-12 15:44:33'
result2 = 0.41
id2 = pilot2+kpi1+testdate2


pilot3 = 'Shinji Ikari'
testdate3 = '2023-12-12 15:55:33'
result3 = 0.47
id3 = pilot3+kpi1+testdate3


######## comment out block after first run
"""
cursor.execute('''INSERT INTO pilots(id, KPI, Pilot, Test_date, Test_result)
                  VALUES(?,?,?,?,?)''', (id1, kpi1, pilot1, testdate1, result1))

cursor.execute('''INSERT INTO pilots(id, KPI, Pilot, Test_date, Test_result)
                  VALUES(?,?,?,?,?)''', (id2, kpi1, pilot2, testdate2, result2))

cursor.execute('''INSERT INTO pilots(id, KPI, Pilot, Test_date, Test_result)
                  VALUES(?,?,?,?,?)''', (id3, kpi1, pilot3, testdate3, result3))

db.commit()
"""
######## comment out block after first run

# Defining functions

def enter_test():
    
    pilot_name = input("Enter pilot name: ")
    kpi_name = input("Enter KPI name: ")
    test_date = datetime.now()
    test_result = float(input("Enter result: "))
    id = pilot_name+kpi_name+(str(test_date))

    cursor = db.cursor()
    cursor.execute('''INSERT INTO pilots(id, KPI, Pilot, Test_date, Test_result)
                  VALUES(?,?,?,?,?)''', (id, kpi_name, pilot_name, test_date, test_result))
    db.commit()

def update_test():

    test_id = input("Enter ID of test to update information: ")
    fields_to_update = str(input("""Enter 1 to edit the KPI; 2 to edit the pilot; 3 to edit the date; 4 to edit the Result: """))
    cursor = db.cursor()
    if '1' in fields_to_update:
        new_kpi = input("Enter KPI: ")
        cursor.execute('''UPDATE pilots SET KPI = ? WHERE id = ? ''', (new_kpi, test_id))

        if '2' in fields_to_update:
            new_pilot = input("Enter pilot: ")
            cursor.execute('''UPDATE pilots SET Pilot = ? WHERE id = ? ''', (new_pilot, test_id))

            if '3' in fields_to_update:
                new_date = input("Enter date: ") # TODO format date properly
                cursor.execute('''UPDATE pilots SET Test_date = ? WHERE id = ? ''', (new_date, test_id))

                if '4' in fields_to_update:
                    new_result = float(input("Enter result: "))
                    cursor.execute('''UPDATE pilots SET Test_result = ? WHERE id = ? ''', (new_result, test_id))

    else:
        print("Update failed, ensure you have correctly entered the test ID and selected one or more of the options")

    db.commit()

def view_records():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM pilots')
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    print(column_names)
    for row in rows:
        print(row)

def delete_test():
    test_id = input("Enter ID of test to delete from the database: ")
    cursor = db.cursor()

    try:
        test_id = str(test_id)
        cursor.execute('''DELETE FROM pilots WHERE id = ?''', (test_id,))
        if cursor.rowcount > 0:
            print("Record deleted successfully.")
        else:
            print("No record found with the provided ID.")
    except ValueError:
        print("Invalid test ID. Please enter a valid ID.")

    db.commit()

def search_record():
    cursor = db.cursor()
    test_id = input("Enter ID of record to view from the database: ")
    cursor.execute('SELECT * FROM pilots WHERE id=?''', (test_id,))
    rows = cursor.fetchall()
    if not rows:
        print("Invalid ID. Please enter a valid ID.")
    else:
        column_names = [description[0] for description in cursor.description]
        print(column_names)
        for row in rows:

            print(row)

# Main loop begins

while True:
    print()
    menu = str(input('''Select one of the following options:
1. Enter test
2. Update test
3. Delete test
4. Search test
5. View records
0. Exit
: ''').lower())

    if menu == '1':
        enter_test()

    elif menu == '2':
        update_test()

    elif menu == '3':
        delete_test()
    
    elif menu == '4':
        search_record()

    elif menu == '5':
        view_records()

    elif menu == '0':
        print('Cya!')
        db.close()
        exit()

    else:
        print("You have made a wrong choice, Please Try again")