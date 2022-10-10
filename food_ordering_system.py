from abc import ABC , abstractmethod
import mysql.connector as mycon
import time
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


#1)Authentication:-
class Auth:#auth-authentication.

    def user_signup():
        
        print("\nSIGNUP...",end="")

        #creating a user_info table inside MySQL database.
        cmd='''CREATE TABLE IF NOT EXISTS user_info(user_name VARCHAR(20),
                                                    user_pass VARCHAR(20),
                                                    user_id   VARCHAR(20),
                                                    user_adrs VARCHAR(100))'''#adrs-address.
        
        cursor.execute(cmd)
        db.commit()
        
        while True:

            #user details input.
            user_name=input("\nCREATE A NAME:")
            user_pass=input("CREATE A PASSOWRD:")
            pass_check=input("CONFIRM YOUR PASSWORD:")
            user_id=input("ENTER YOUR EMAIL-ID:")

            cmd="SELECT user_id FROM user_info where user_id='%s'"%(user_id)
            cursor.execute(cmd)
            result=cursor.fetchall()
            if result==[]:#it means the email_id is unique.

                if user_pass==pass_check:
                
                    #address input.
                    print("\nENTER YOUR ADDRESS BELOW:")
                    house=input("ENTER HOUSE No.:")#house number
                    landmark=input("ENTER ANY LANDMARK:")#landmark
                    city=input("ENTER YOUR CITY (e.g. Rohini):")#city
                    pincode=input("ENTER PINCODE:")#pincode
                    #combining the adrs.
                    user_adrs="HOUSE NO.:"+house+",NEAR:"+landmark+",CITY:"+city+",PINCODE:"+pincode
                                    
                    insert_cmd='''INSERT INTO user_info(user_name,user_pass,user_id,user_adrs)
                                  VALUES('{}','{}','{}','{}')'''.format(user_name,user_pass,user_id,user_adrs)
                    cursor.execute(insert_cmd)#inserting values inside user table created above.
                    
                    #creating user's promo-code table for storing promo code info.
                    cmd="CREATE TABLE "+user_id+"_promo(promo_code VARCHAR(6),status INT)"
                    cursor.execute(cmd)

                    #adding promo code to promo_code table.
                    cmd1='''INSERT INTO '''+user_id+'''_promo(promo_code,status)
                                                       VALUES('SAVE50',0)'''
                    
                    cursor.execute(cmd1)
                    cmd2='''INSERT INTO '''+user_id+'''_promo(promo_code,status)
                                                       VALUES('SAVE20',0)'''
                    
                    cursor.execute(cmd2)

                    db.commit()#make sure everything is saved properly inside database.
                    
                    print("\nWOHOO! YOU ARE GOOD TO GO.")
                    return True
                else:
                    print("\nOOPS! LOOKS LIKE YOUR PASSWORD DOESN'T MATCHED.")
                    print("TRY AGAIN...")
                    continue
            
            else:#it means email_id is already in use.
                print("\nSORRY, THIS EMAIL ID IS ALREADY IN USE, TRY AGAIN.")
                continue

    def user_login():
        
        print("\nLOGIN...",end="")
        while True:
            
            user_id=input("\nENTER YOUR EMAIL-ID:")
            user_pass=input("ENTER YOUR PASSWORD:")
            cmd="SELECT * FROM user_info WHERE user_id='%s'"%(user_id)
            cursor.execute(cmd)
            result=cursor.fetchall()
            
            if result==[]:#result==[] means no entry found in database.
                print("\nSORRY,NO EMAIL-ID FOUND.")
                print("TRY AGAIN...")
            else:
                if result[0][1]==user_pass:#result[0][1] is user_pass.
                    print("\n----------------")
                    print('WELCOME ',result[0][0].upper(),',',sep="")#result[0][0] is user_name.

                    Auth.user_id=user_id
                    
                    return user_id
                else:#if wrong password entered by the user.
                    print("PASSWORD IS INCORRECT")
                    print("TRY AGAIN...")
                    continue

    #class 'Auth' ends.



#2)Order:-
#using 'INHERITANCE'.

#a)'View' is a child class of parent class 'Order'.               
class View:

    #$$ using abstract method.
    @abstractmethod#$$
    def process(self):
        pass
    
    def display_address(user_id):#displays user address.
        
        print("\nAddress.")
        cmd="SELECT user_adrs FROM user_info WHERE user_id='%s'"%(user_id)#command to fetch user address from database.
        cursor.execute(cmd)
        address=cursor.fetchall()[0][0].split(",")#fetching result and splitting them according to ','(commas).
        for line in address:
            print(line)

    def display_restaurants(address):

        cmd="select * from restaurants_info"
        cursor.execute(cmd)
        resto=cursor.fetchall()

        #counting total number of restaurants in your city
        cmd2="SELECT COUNT(*) FROM restaurants_info"
        cursor.execute(cmd2)
        restocount=cursor.fetchall()
        print("\nWE HAVE FOUND",restocount[0][0],"RESTAURANTS IN YOUR CITY.")#restocount[0][0] is total no. of restaurants.

        count=0
        for i in resto:
            count=count+1
            print("\n(",count,")")
            print("'",i[0],"' ","R-ID:",i[8],sep="")#i[0] is restaurant name and i[8] is restaurant unique id.
            print("Speciality:",i[1])#i[1] is restaurant speciality.
            print("Location: ",i[2],",",i[3],sep="")#i[2] is location and i[3] is landmark.
            print(" "*10,i[4],",",i[5],sep="")#i[4] is city and i[5] is pincode.
            print("OPENS BETWEEN",i[6],"&",i[7])#i[6] is opening time and i[7] is closing time.
            print("DELIVERS IN 5 Minutes.")#Delivery time.
            
        return

    def display_menu():

        #finding restaurant's menu with the help of unique restaurant id (R-ID).
        while True:
            print()
            R_id=int(input("ENTER RESTAURANT ID (SEE THE RESTAURANT NAME ABOVE THERE IS AN R-ID):"))
            cmd="SELECT code from restaurants_info where code='%s'"%(R_id)
            cursor.execute(cmd)
            result=cursor.fetchall()
            if result==[]:

                #if wrong R-id is entered.
                print("\nSORRY, NO RESTAURANT WITH THIS R-ID.")
                continue
                
            else:
                #if correct R-id is entered.
                cmd="SELECT * from menu_"+str(R_id)#fetching menu from database with the help of restaurant id.
                cursor.execute(cmd)
                menu_list=cursor.fetchall()
                print("\nMENU,")
                print("ITEM-No. | DISH-NAME | QUANTITY | PRICE(IN Rs.)")
                for i in menu_list:
                    print(i[0],",",i[1],", Qty.",i[2],"Units , Rs.",i[3])#i[0] is dish no,
                                                                         #i[1] is dish name,
                                                                         #i[2] is quantity,
                                                                         #i[3] is price.
                    
                    
                print("\n----------------------------------------------------")
                print("IF YOU WANT TO ORDER FROM THIS RESTAURANT ENTER [1]:")
                print("IF YOU WANT TO CHANGE RESTAURANT ENTER [2]:")
                print("----------------------------------------------------")
                choice=input("ENTER CHOICE HERE:")
                if choice=="1":
                    return R_id
                else: 
                    return True
                
    #Class 'View' ends.

#b)'Cart' is a child class of parent class 'Order'.
class Cart:

    def additem():
        
        #adding items to cart by taking input from user.
        while True:

            print()
            itemno=int(input("ENTER ITEM No.:"))
            #fetching item details from database with the help of restaurant id.
            cmd="SELECT * from menu_"+str(Order.R_id)+" WHERE dishno=%s"%(itemno)
            cursor.execute(cmd)
            item_details=cursor.fetchall()
            if item_details==[]:#[] is rempty result.
                
                #if wrong item no. is given.
                print("\nSORRY, NO SUCH DISH IN MENU.")
                continue

            else:
                
                #if correct item no. is given
                itemqty=int(input("ENTER QUANTITY:"))
                
                itemname=item_details[0][1]
                itemprice=item_details[0][3]
                Order.cart.append([itemno,itemname,itemqty,itemprice])#appending item details to cart.

                print()
                choice=input("WOULD YOU LIKE TO ENTER MORE ITEMS? [y/n]:")
                if choice=="y":
                    continue
                else:
                    return
                    
    def display_cart():

        print("\nYOUR CART,")

        for details in Order.cart:

            #details[1] is itemname,
            #details[2] is item quantity,
            #details[3] is item price.
            print(details[1],", Qty: ",details[2],", Price: ",details[3]*details[2],sep="")
            #details[3]*details[2] is (item_price x item_quantity).

            #appending price to list so that we can easily add the item price in future.
            Order.total_price.append(details[3]*details[2])#price*qty

        #clearing the cart so that we can use it further.
        Order.cart=[]

        return

    #class 'Cart' ends.
            
#Order is a parent class containing classes 'View' and 'Cart'.      
class Order(View,Cart):

    def __init__(self):#$$
        print("USER ADDRESS.")

    total_price=[]
    cart=[]

#class 'Order' ends.


#3)Payment:-
#using 'INHERITANCE'.

#'calculate_bill' is a child class of parent class 'Payemnt'.
class calculate_bill():

    def display_bill():#calculates and displays the bill to user.
        
        print("\nDELIVERY CHARGES: Rs.40")
        Order.total_price.append(40)#40 for delivery charges.
        print("YOUR TOTAL BILL IS OF Rs.",sum(Order.total_price),".",sep="")

        print("\n---------------------------------")
        print("TO PROCEED FOR PAYMENY ENTER [1]:")
        print("TO CANCEL THE CART ENTER [2]:")
        print("---------------------------------")
        choice=input("ENTER CHOICE HERE:")
        if choice=='1':#if user want to proceed for payment.
            
            #checking is total bill is above that Rs.100 i.e. minimum order value.
            if sum(Order.total_price)>=100:
                return True
            else:
                #if billing is lower than Rs.100.
                print("\nSORRY, THE BILLING AMOUNT SHOULD BE MORE THAN Rs.100 TO PROCEED.")
                Order.total_price=[]
                return False
        else:

            #if user cancels the cart the billing list must be set to zero(0).
            Order.total_price=[]
            return False

    def promo_code():

        #fetching promo codes from database if avaialable.
        cmd="SELECT promo_code FROM "+Auth.user_id+"_promo WHERE status=0"
        cursor.execute(cmd)
        promo=cursor.fetchall()
        if promo==[]:

            #if no promo code found.
            print("\nSORRY, NO PROMOCODES AVAILABLE FOR NOW.")
            return
        else:

            #if promocodes are avaialable.
            print("\nWE HAVE FOUND SOME PROMOCODES FOR YOU.")
            for i in promo:
                print(i[0])
                Payment.promo.append(i[0])
                
            while True:
                
                print()
                select_promo=input("ENTER A PROMOCODE:")
                #checking promo code.
                if ( select_promo in Payment.promo ):

                    #if user entered correct promocode.
                    if select_promo=='SAVE50':
                        Order.total_price.append(-50)
                        Payment.promoused='SAVE50'
                    else:
                        Order.total_price.append(-20)
                        Payment.promoused='SAVE20'
                        
                    print("\nHURRAY, PROMOCODE APPLIED.")
                    print("FINAL AMOUNT TO BE PAID:Rs",sum(Order.total_price),".",sep="")
                    return
                    
                else:

                    #if user entered wrong promocode.
                    print("\nNO SUCH PROMOCODE FOUND, TRY AGAIN.")
                    
                continue

    #class 'calculate_bill' ends.
                            
class payment_mode:

    def payment_option():
        
        print("\nPAY THORUGH:-")
        print("1) UPI,")
        print("2) NETBANKING,")
        print("3) DEBIT OR CREDIT CARD.")

        while True:
            print()
            choice=input("ENTER OPTION:")
            if choice=='1':
                print()
                upi_id=input("ENTER YOUR UPI-ID:")
                break
            elif choice=='2':
                print("\nTHIS PAYMENT MODE IS NOT ADDED YET.")
                continue
            elif choice=='3':
                print()
                cardno=input("ENTER YOUR 16 DIGIT CARD NO.:")
                expno=input("ENTER EXPIRY DATE MM/YY:")
                cvv=input("ENTER CVV:")
                break
            else:
                print("\nWRONG OPTION SELECTED, TRY AGAIN.")
                continue
            
        print("\nBRAVO,")
        print("PAYMENT OF Rs.",sum(Order.total_price)," IS SUCCESSFUL.",sep="")

        #clearing the price list.
        Order.total_price=[]

        #deleting the promo from database so that it can not be used later.
        if ( Payment.promoused=='SAVE50' or Payment.promoused=='SAVE20' ):
            cmd="UPDATE "+Auth.user_id+"_promo SET status=1 WHERE promo_code='%s'"%(Payment.promoused)
            cursor.execute(cmd)
            db.commit()
            return

    #class 'payment_mode' ends.
           
#Payment is a parent class containing classes 'calculate_bill' and 'payment_mode'. 
class Payment(calculate_bill,payment_mode):

    def __init__(self):#$$
        print("USER PROMOCODES")

    promoused=""
    promo=[]
    pass

#class 'Payment' ends.

#4)Tracking.
class Tracking:

    def display_notification():
        print("\nYOUR ORDER IS BEING PREPAIRED.")
        print("YOU WILL RECIEVE YOUR ORDER WITHIN 5 Minutes.") 

    def track():

        #user will recieve order in 5 minutes but if not he will proceed with an action.
        delivery_time=random.randint(0,600)#600sec is 10 minutes.
        time.sleep(delivery_time)
        if delivery_time>300:#300sec is 5 minues
            print("\nSORRY FOR THE DELAY.")
            choice=input("YOU CAN CANCEL THE ORDER OR YOU CAN RECIEVE IT [y/n]:")
            if choice=='y':
                print("THANKYOU FOR ORDERING WITH US.")
            else:
                print("\nORDER IS CANCELED,")
                print("SORRY FOR INCONVENIENCY.")
        else:
            print("THANKYOU FOR ORDERING WITH US.")
        
        return

    def ratings():

        print("GIVE A RATING FROM 1-5.")
        print("| 1 | 2 | 3 | 4 | 5 |")
        inp=input("ENTER RATING HERE:")
        print("\nTHANKYOU FOR YOUR FEEDBACK.")





#__main__

try:
    db_info=db_info_fetcher()#function call for getting database information.
    db=mycon.connect(host=db_info[0],user=db_info[1],password=db_info[2],database=db_info[3])#setting up a connection with the database.
    if (not db.is_connected()):#checks if connection stablished successfully or not.

        #if connection is not successful.
        print("ERROR:CHECK YOUR DATABASE INFO AND TRY AGAIN.")
        
    else:

        #if connection is successful.
        cursor=db.cursor()#sets up a cursor in database for fetching records.
        print("WELCOME TO FOOD ORDERING SYSTEM.")
        while True:
            print("\nFOR SIGNUP,PRESS [1].\nFOR LOGIN, PRESS [2].\n")
            choice=int(input("ENTER CHOICE HERE:"))
            if choice == 1:#for signup
                
                rep=Auth.user_signup()
                if rep==True:
                    continue
                
            elif choice == 2:#for login
                
#>>>----------->#main functioning of the code.
                user_id=Auth.user_login()#auth.user_login() will return user_id when login process is done.

                #Order is a parent class (View,Cart) inherits the features of Order.
                Order.display_address(user_id)#displays user address on top.      
                
                while True:
                    
                    Order.display_restaurants(user_id)#giving user_id as argument to function so that we can fetch
                                                      #restaurants from the database according to user address.
                    flag=Order.display_menu()
                    if flag!=True:#it means flag has recieved an R-id for adding items to cart.

                        Order.R_id=flag
                        
                        #using class 'Cart'.
                        Order.additem()

                        Order.display_cart()
                        
                        #reply will recieve if order has to be proceed or not.
                        #using class 'Payment'.
                        reply=Payment.display_bill()
                        if reply==True:#True means order has to proceed for payment.
                            Payment.promo_code()
                            Payment.payment_option()

                            #using class 'Tracking'.
                            Tracking.display_notification()
                            Tracking.track()
                            Tracking.ratings()

                        else:#it means that the billing amount is lower than Rs.100.
                            continue
                        
                        input("\nPRESS ENTER TO CONTINUE ORDERING FOOD.")
                        
                    else:
                        continue
                
            else:#for exception that not mentioned.
                print("\nINVALID CHOICE.")
                print("TRY AGAIN...")
                continue
        
        
        
except:#if any other exception occurs this print.
    print("UNKNOWN ERROR OCCURED, TRY AGAIN.")
