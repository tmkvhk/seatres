
def loadReservationFile():
    dataDictionary = {}
    dataFile = open('reservation.txt')
    dataArray = []
    for i in range(0,10):
        _dataArray = ['O' for j in range(0,5)]
        dataArray.append(_dataArray)

    for data in dataFile.readlines():
        data = data.split(',')
        name = data[0]
        row = int(data[1].strip())
        column = int(data[2].strip())
        id = data[3].strip()
        dataArray[row][column] = 'X'
        dataDictionary[id] = [name,row,column,id]

    dataFile.close()
    return dataArray,dataDictionary

def displayChart(data):
    for i in data:
        print('[',end=' ')
        for j in i:
            print(j,end=' ')
        print(']',end='\n')


def loginAdmin(username,psw):
    adminFile = open('admins.txt')
    for admin in adminFile.readlines():
        admin = admin.split(',')
        user = admin[0].strip()
        password = admin[1].strip()
        if (user == username) and (password == psw):
            return True
    return False

 
def confirmationCode(firstName, courseCode):
    code = ['' for i in range(0,50)]
    counter = 0
    for first in firstName:
        code[counter] = first
        counter += 2
    counter = 1
    for first in courseCode:
        code[counter] = first
        counter += 2
    return ''.join(code)

def reserveASeat(reservation,row,column):
    checkSeat = reservation[row][column]
    if checkSeat != 'X':
        reservation[row][column] = 'X'
        return True
    else:
        return False


def writeToFile(dataDict):
    fileWrite = open('reservation.txt','w')
    for key, value in dataDict.items():
        data = value[0]+','+str(value[1])+','+str(value[2])+','+value[3]+'\n'
        fileWrite.write(data)
    fileWrite.close()

def get_seating_costs():
    seat_matrix = [[300, 200, 100, 200, 300] for row in range(10)]
    return seat_matrix


def calculateCost(seatsPrice, reservation):
    price = 0
    for index, i in enumerate(reservation):
        for index2, j in enumerate(i):
            if j == 'X':
                price += seatsPrice[index][index2]
    return price


def menu():
    print('''
1. Administrator Login Portal
2. Make a Reservation
3. Close Application
    ''')

def main():
    reservation,dataDict = loadReservationFile()
    seatsCost = get_seating_costs()
    while True:
        menu()
        option = int(input('What would you like to do? '))
        if option in [1,2,3]:
            if option == 1:
                print('Administrator Login Portal')
                print('---------------------------')
                while True:
                    username = input('Enter Username: ')
                    password = input('Enter Password: ')
                    canLogin = loginAdmin(username,password)
                    if canLogin:
                        print('\nPrinting the Seating Chart...')
                        displayChart(reservation)
                        sales = calculateCost(seatsCost, reservation)
                        print('Total Sales:','$'+str(sales))
                        print('You are logged out now!')
                        break
                    else:
                        print('Error: Invalid username/password combination')
            elif option == 2:
                print('Make a Reservation')
                print('--------------------')
                firstName = input('Enter Passenger First Name: ')
                lastName = input('Enter Passenger Last Name: ')
                print('Printing the Seating Chart...')
                displayChart(reservation)
                while True:
                    row = int(input('Which row would you like to sit in? '))
                    column = int(input('Which seat column would you like to sit in? ' ))
                    seatReserved = reserveASeat(reservation,row-1,column-1)
                    if seatReserved:
                        code = confirmationCode(firstName, 'INFOTC1040')
                        dataDict[code] = [firstName,row-1,column-1,code]
                        print('Success! Your requested seat: Row:2 Seat:1 has been assigned.')
                        writeToFile(dataDict)
                        reservation,dataDict = loadReservationFile()
                        print('Printing the Flight Map...')
                        displayChart(reservation)
                        print('Congratulations Leroy Collins! Your trip is now booked! Enjoy!')
                        print('Your confirmation code is:',code)
                        break
                    else:
                        print('Row:'+str(row)+' Seat:'+str(column)+ ' is not available. Please choose again.')
            elif option == 3:
                print('Thank you for choosing Mizzou IT Airlines! Goodbye!')
                break
        else:
            print('ERROR: Not a valid selection! Select 1 or 2 or 3')
main()

