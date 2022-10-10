import mysql.connector as mycon
import random

#(db_info_fetcher)database information fetching function.
def db_info_fetcher():#fetches database info stored in 'db_info.txt' file.
    
    db_info_file=open('db_info.txt','r')
    result=db_info_file.readlines()#fetching entire result using 'readlines()' method.
    info_list=[]#db info stores in this list.
    count=0
    
    for info in result:
        info_list.append(info.split("=")[1].strip('\n'))

        #Multi_line_comment.      
        '''
           WORKING OF 'info_list.append(info.split("=")[1].strip('\n'))':
           
           1)spliting the data in list i.e in string form with respect to '=' using split() method.
           2)removing the newline charachter i.e '/n' from the string using strip() method.
           3)a list genrated for e.g ['host','localhost'] i.e. 'host=localhost' before but
             we have splitted them with '=' by using split() method
           4)appending list[1] (element on index 1) to our main info_list.
        '''
        
    return info_list#returning db information to function caller.


try:
    db_info=db_info_fetcher()#function call for getting database information.
    db=mycon.connect(host=db_info[0],user=db_info[1],password=db_info[2],database=db_info[3])#setting up a connection with the database.
    if (not db.is_connected()):#checks if connection stablished successfully or not.

        #if connection is not successful.
        print("ERROR:CHECK YOUR DATABASE INFO AND TRY AGAIN.")
        
    else:
        cursor=db.cursor()#sets up a cursor in database for fetching records.

        flag=True
        while flag==True:
        
            name=input("ENTER RESTAURANT/HOTEL NAME:")
            typ=input("ENTER SPECIALITY (e.g. PIZZA,BURGER,MOMOS,etc):")#type of restaurant or speciality of restaurant
            
            #address.
            print("\nENTER ADDRESS BELOW:")
            location=input("\nENTER HOTEL LOCATION (e.g. Rohini):")#house number
            landmark=input("ENTER ANY LANDMARK:")#landmark
            city=input("ENTER CITY (e.g. NEW DELHI):")#city
            pincode=input("ENTER PINCODE:")#pincode
            starttime=input("ENTER OPENING TIME (mention am & pm):")#opening time
            closingtime=input("ENTER CLOSING TIME (mention am & pm):")#closing time

            cmd='''CREATE TABLE IF NOT EXISTS restaurants_info(name        VARCHAR(20),
                                                               typ         VARCHAR(20),
                                                               location    VARCHAR(20),
                                                               landmark    VARCHAR(20),
                                                               city        VARCHAR(20),
                                                               pincode     VARCHAR(6),
                                                               starttime   VARCHAR(10),
                                                               closingtime VARCHAR(10),
                                                               code        INT)'''

            cursor.execute(cmd)
            
            while True:
                code=random.randint(1000,9999)
                cmd="SELECT code FROM restaurants_info"
                cursor.execute(cmd)
                result=cursor.fetchall()
                for i in result:
                    if i[0]==code:
                        continue
                    else:
                        break
                break


            insert_cmd='''INSERT INTO restaurants_info(name,typ,location,landmark,city,pincode,starttime,closingtime,code) 
                          VALUES('{}','{}','{}','{}','{}','{}','{}','{}',{})'''.format(name,typ,location,landmark,city,pincode,starttime,closingtime,code)

            cursor.execute(insert_cmd)
            db.commit()

            #menu_designing.
            print("\nTIME TO CREATE A MENU.")

            cmd='''CREATE TABLE IF NOT EXISTS menu_'''+str(code)+'''(dishno   INT,
                                                                     dishname VARCHAR(20),
                                                                     qty      INT,
                                                                     price    INT)'''

            cursor.execute(cmd)
            
            totaldishes=int(input("ENTER TOTAL NO. OF DISHES IN YOU RESTAURANT:"))
            for i in range(totaldishes):
                print("\nFOR DISH NO.",i+1)
                dishname=input("ENTER DISH NAME:")
                qty=int(input("ENTER QUANTITY:"))
                price=int(input("ENTER PRICE (IN Rs.):"))

                insert_cmd='''INSERT INTO menu_'''+str(code)+'''(dishno,dishname,qty,price) 
                              VALUES({},'{}',{},{})'''.format(i+1,dishname,qty,price)

                cursor.execute(insert_cmd)
                
            db.commit()
                
            #ENTER MORE RESTAURANTS.
            print()
            cont=input("ENTER MORE RESTAURANTS PRESS [y/n]:")
            if cont=='y':
                continue
            else:
                flag=False
        
        
        
except:#if any other exception occurs this will handle.
    print("ERROR:CHECK YOUR DATABASE INFO AND TRY AGAIN")

except:#if any other exception occurs this will handle.
    print("ERROR:CHECK YOUR DATABASE INFO AND TRY AGAIN")


    
