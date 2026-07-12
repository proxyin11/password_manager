import random                                                   #importing the random module
import string                                                   # importing the string module

passwords = {}

#load the file with the passwords
try:
    with open("passwords.txt", "r") as f:
        for line in f:
            key, value = line.strip().split(":")
            passwords[key] = value
except :
    pass

def generate_password():                                        #it will generate the password
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for i in range(8))
    return password

while True:
    print("1. Save a new password:")
    print("2. View saved passwords :")
    print("3. Generate a new password")
    print("4. Exit")

    choice = input("Enter your choice: ")
    
    if choice == "1":                                       #it save the password in the dictionary
        site = input("Enter the site name: ")
        password = input("Enter the password: ")
        passwords[site] = password  
        
    elif choice == "2":                                   #if not found these will print no saved password found
        if not passwords:
            print("No saved passwords found.")
            
        else:
            for site, password in passwords.items():
                print(f"{site}: {password}")
    
    elif choice == "3":                                   #it will generate the password        
        site =input("Enter the site name: ")
        password = generate_password()
        passwords[site] = password
        print(f"Generated password: {password}")
    
    elif choice == "4":                                   #it will exit
        print("Exiting the program.")
        break