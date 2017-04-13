import csv
import os

def overwrite():
    if(os.path.isfile('places.csv')):
        os.remove('places.csv')
    append()

def append():
    with open('places.csv', 'a', newline='') as file:
        w = csv.writer(file)
        go = True
        while go:
            print('Name of place')
            name = input()
            if name == '':
                go = False
                exit()
            print('X, y')
            xy = input().split(',')
            w.writerow([name,xy[0],xy[1]])

def main():
    print('Overwrite existing csv? Y/n')
    over = input()
    if(over == 'y'):
        overwrite()
    else:
        append()

if __name__ == '__main__':
    main()