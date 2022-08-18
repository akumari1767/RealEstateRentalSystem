import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 100)
connection = sqlite3.connect("rentalproperty.db")

def userid_validation(connection, email, password, option):
    """ validation function for checking the user is existing"""
    cur = connection.cursor()
    if option == 1:
        cur.execute(
            'select * from CUSTOMER where EMAIL = "' + str(email) + '";')
    elif option == 2:
        cur.execute(
            'select * from CUSTOMER where EMAIL = "' + str(email) + '" AND PASSWORD = "' + str(
                password) + '";')
    elif option == 3:
        cur.execute(
            'select * from ADMIN where ADMIN_USERNAME = "' + str(name) + '" AND ADMIN_PASSWORD = "' + str(
                password) + '";')
    results = cur.fetchall()
    cur.close()
    return results


def tenant_response(connection,Cursor,email,password):
    print()
    print(""" Choose the option:
                        (1) Booking
                        (2) Monthly Payment
                        """)
    TenantResponse = int(input("1, 2 : "))
    if TenantResponse == 1:
        dframe = pd.read_sql_query("SELECT * from BUILDING ", connection)
        print(dframe)
        print()
        print(""" Enter the BUILDING_ID if you would like to book an apartment
                                """)
        BuildingID = int(input("BUILDING_ID: "))
        dataf = pd.read_sql_query("SELECT APARTMENT_ID,APARTMENT_NAME,BUILDING_ID, FLOOR, APARTMENT_SIZE,PRICE "
                                  "from APARTMENT_LISTING where BUILDING_ID ==" + str(BuildingID) + " and BOOKING_FLAG = 'N' ;", connection)

        print()
        print("The apartments available in the BuildingID: " + str(BuildingID) + " are below")
        print(dataf)
        if dataf.shape[0] == 0:
            print()
            print("there is no apartment available in this building")
        else:
            print()
            print(""" Enter the APARTMENT_ID you would like to book""")
            ApartmentID = int(input("APARTMENT_ID: "))
            StartDate =input("Starting Date(yyyy-mm-dd): ")
            UpdateQueryFlag = 'UPDATE APARTMENT_LISTING SET BOOKING_FLAG = "Y" , BOOKED_DATE ="'+ str(datetime.today().strftime('%Y-%m-%d')) +'" WHERE APARTMENT_ID = ' + str(
                ApartmentID) + ' AND BUILDING_ID = ' + str(BuildingID) + ';'
            Cursor.execute(UpdateQueryFlag)
            Cursor.execute("COMMIT;")
            SelectQueryPrice = "SELECT PRICE FROM APARTMENT_LISTING WHERE APARTMENT_ID =" +str(ApartmentID)+" AND BUILDING_ID = " + str(BuildingID)+ ";"
            Cursor.execute(SelectQueryPrice)
            row = Cursor.fetchall()
            price = row[0][0]
            UpdateQueryFlag = 'UPDATE CUSTOMER SET BUILDING_ID ='+ str(BuildingID) +',APARTMENT_ID='+str(ApartmentID)+', MONTHLYRENT ='+str(price)+',START_DATE ="'+str(StartDate)+ '", DUE_AMOUNT = '+ str(price) +' WHERE EMAIL = "' + str(email) + '" AND PASSWORD = "' + str(password) + '";'
            print()
            print("Booking confirmed!")
            Cursor.execute(UpdateQueryFlag)
            Cursor.execute("COMMIT;")
    if TenantResponse == 2:
        SelectQueryPrice = 'SELECT DUE_AMOUNT FROM CUSTOMER WHERE EMAIL = "' + str(email) + '" AND PASSWORD = "' + str(password) + '";'
        Cursor.execute(SelectQueryPrice)
        row = Cursor.fetchall()
        price = row[0][0]
        print()
        print("Amount to be paid: ", price)
        AmountPaid = input("Enter the amount you would like to pay : ")
        Card = input("Enter the ATM Card number : ")
        CVV = input("Enter the CVV : ")
        UpdateQueryDueAmount = 'UPDATE CUSTOMER SET DUE_AMOUNT = DUE_AMOUNT - ' + str(AmountPaid) + ' WHERE EMAIL = "' + str(email) + '" AND PASSWORD = "' + str(
            password) + '";'
        Cursor.execute(UpdateQueryDueAmount)
        Cursor.execute("COMMIT;")
        print()
        print("payment is successfull")
Start = True
while Start == True:
    print("")
    try:
        print("""Choose an option:
                  (1) Tenant
                  (2) Staff
                  (3) Quit
                  """)
        option = int(input("1, 2, 3 : "))
    except ValueError:
        continue
    Cursor = connection.cursor()
    Cursor.execute("CREATE TABLE IF NOT EXISTS CUSTOMER(CUSTOMER_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT,"
                   "NAME varchar(255) NOT NULL,EMAIL Varchar(100) NOT NULL, PASSWORD varchar(255) NOT NULL,"
                   "PHONE int NOT NULL,PROPERTY_ID int DEFAULT 0,ACCESS_COUNT int DEFAULT 0, BUILDING_ID int DEFAULT NULL,"
                   "APARTMENT_ID int DEFAULT NULL, MONTHLYRENT FLOAT DEFAULT NULL, START_DATE date DEFAULT NULL, "
                   "DUE_AMOUNT float DEFAULT 0);")

    Cursor.execute("CREATE TABLE IF NOT EXISTS BUILDING(BUILDING_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT, "
                   "BUILDING_NAME varchar(255) NOT NULL, NO_OF_FLOORS Integer NOT NULL, APARTMENT_SIZE varchar(255) "
                   "NOT NULL, STREET_ADDRESS varchar(255) NOT NULL, CITY varchar(255) NOT NULL, PROVINCE varchar(255) NOT NULL,"
                   " POSTAL_CODE varchar(255) NOT NULL, PRICE FLOAT NOT NULL);")

    Cursor.execute(
        "CREATE TABLE IF NOT EXISTS APARTMENT_LISTING(APARTMENT_ID Integer NOT NULL PRIMARY KEY AUTOINCREMENT, "
        "APARTMENT_NAME varchar(255) NOT NULL,BUILDING_ID Integer NOT NULL, FLOOR Integer NOT NULL, APARTMENT_SIZE "
        "varchar(255) NOT NULL, PRICE FLOAT NOT NULL, BOOKING_FLAG varchar(255) DEFAULT N, BOOKED_DATE date DEFAULT NULL );")

    if option == 1:
        try:
            category = "tenant"
            print()
            print("""Choose an option:
                              (1) Login
                              (2) Sign Up
                              """)
            print()
            tenant_option = int(input("1, 2 : "))
            if tenant_option == 1:
                print()
                email = input("Enter Email Address: ")
                password = input("Enter Password: ")
                validation = userid_validation(connection, email, password, tenant_option)
                if len(validation) == 1:
                    UpdateQueryCount = 'UPDATE CUSTOMER SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE EMAIL = "' + str(
                        email) + '" AND PASSWORD = "' + str(password) + '";'
                    Cursor.execute(UpdateQueryCount)
                    Cursor.execute("COMMIT;")
                    tenant_response(connection,Cursor,email,password)
                else:
                    print()
                    print("Invalid credentials. Please try again!")

            elif tenant_option == 2:
                print()
                name = input("Your Name: ")
                email = input("Email Address: ")
                phone = input("Phone Number: ")
                password = input("Create a password: ")
                access_count = 0
                validation = userid_validation(connection, email, password, tenant_option)
                if len(validation) != 0:
                    print()
                    print(" You already registered an account with this mail id! ")
                else:
                    InsertQuery = 'INSERT INTO CUSTOMER (NAME,EMAIL,PASSWORD,PHONE,ACCESS_COUNT) VALUES ("' + str(
                        name) + '","' + str(email) + '","' + str(password) + '","' + str(phone) + '",' + str(
                        access_count) + ');'
                    Cursor.execute(InsertQuery)
                    Cursor.execute("COMMIT;")
                    tenant_response(connection,Cursor,email,password)
        except ValueError:
            continue
    elif option == 2:
        try:
            print()
            name = input("username: ")
            password = input("Password: ")
            admin_option = 3
            validation = userid_validation(connection, name, password, admin_option)
            if len(validation) == 1:
                flag = True
                while flag == True:
                    UpdateQueryCount = 'UPDATE ADMIN SET ADMIN_ACCESS_COUNT = ADMIN_ACCESS_COUNT + 1 WHERE ADMIN_USERNAME = "' + str(
                        name) + '" AND ADMIN_PASSWORD = "' + str(password) + '";'
                    Cursor.execute(UpdateQueryCount)
                    Cursor.execute("COMMIT;")
                    print()
                    print("""Choose an option:
                                                  (1) Due Amounts by Customer
                                                  (2) Number of apartments booked in each building
                                                  (3) Number of bookings after a particular date
                                                  (4) Apartment details of a particular building
                                                  (5) Exit
                                                  """)
                    print()
                    staff_option = int(input("1, 2, 3, 4, 5: "))
                    if staff_option == 1:
                        DueData = pd.read_sql_query("select CUSTOMER_ID, DUE_AMOUNT FROM CUSTOMER;", connection)
                        ax = DueData.plot.bar(x='CUSTOMER_ID', y='DUE_AMOUNT', rot=0, title="Due Amounts by Customer")
                        plt.legend()
                        plt.show()
                    elif staff_option == 2:
                        ApartmentData = pd.read_sql_query("SELECT APARTMENT_ID, BUILDING_ID FROM APARTMENT_LISTING WHERE BOOKING_FLAG = 'Y';", connection)
                        ApartmentData = ApartmentData.groupby(['BUILDING_ID'])['BUILDING_ID'].size().reset_index(name='counts')
                        print("Number of apartments booked in each building")
                        print(ApartmentData)
                        ax = ApartmentData.plot.bar(x='BUILDING_ID', y='counts', rot=0, title="Number of apartments booked in each building")
                        plt.legend()
                        plt.show()
                    elif staff_option == 3:
                        print()
                        user_date = input("Number of bookings after Date(yyyy-mm-dd): ")
                        countsql='select count(*) from APARTMENT_LISTING where BOOKED_DATE > "'+ str(user_date)+'";'
                        Cursor.execute(countsql)
                        row = Cursor.fetchall()
                        count = row[0][0]
                        print()
                        print("Number of bookings after " + str(user_date) + " is :", count)
                        if count == 0:
                            print()
                            print("No bookings!!!")
                        else:
                            BookingData = pd.read_sql_query('select APARTMENT_ID, BOOKED_DATE FROM APARTMENT_LISTING where BOOKED_DATE > "'+ str(user_date)+'";', connection)
                            booking = BookingData['BOOKED_DATE'].value_counts()
                            booking.plot.pie(autopct=lambda x: '{:.0f}'.format(x * booking.sum() / 100))
                            plt.legend()
                            plt.title("Number of bookings by Date")
                            plt.show()
                    elif staff_option == 4:
                        print()
                        Building = int(input("BUILDING_ID: "))
                        apartmentData = pd.read_sql_query(
                            "SELECT APARTMENT_ID,APARTMENT_NAME, FLOOR, APARTMENT_SIZE,PRICE, BOOKING_FLAG "
                            "from APARTMENT_LISTING where BUILDING_ID = " + str(Building) + " ;", connection)
                        print()
                        print(apartmentData)
                        print()
                    else:
                        print()
                        print("Thank you for visiting!")
                        print()
                        flag = False
            else:
                print()
                print("Invalid credentials. Please try again!")
        except ValueError:
            continue
    else:
        try:
            print()
            print("Thank you for visiting!")
            print()
            Start = False
        except ValueError:
            continue
connection.close()
