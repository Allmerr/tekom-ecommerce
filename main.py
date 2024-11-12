import json, os, time, getpass

USER = {
    "ID": "",
    "EMAIL": "",
}

def clearscreen(numlines=100):
  if os.name == "posix":
    # Unix, Linux, macOS, BSD, etc.
    os.system('clear')
  elif os.name in ("nt", "dos", "ce"):
    # DOS/Windows
    os.system('CLS')
  else:
    # Fallback for other operating systems.
    print('\n' * numlines)

def login():
    with open('./db/user.json') as user:
        users = json.load(user)
    
    chances = 3
    while chances > 0:
        clearscreen()
        print("=Login=")
        email = input("Masukkan Username: ")
        password = getpass.getpass("Masukkan Password: ")
        for user in users:
            if user['email'] == email and user['password'] == password:
                print("Login Berhasil")
                USER["ID"] = user["id"]
                USER["EMAIL"] = user["email"]
                return None
        print("Login Gagal")
        chances -= 1
        time.sleep(.5)

def register():
    with open('./db/user.json') as user:
        users = json.load(user)
    
    clearscreen()
    print("=Register=")
    email = input("Masukkan Email: ")
    password = getpass.getpass("Masukkan Password: ")
    password_confirm = getpass.getpass("Masukkan Password Lagi: ")

    if password != password_confirm:
        print("Password Tidak Sama")
        time.sleep(.5)
        return None
    
    for user in users:
        if user['email'] == email:
            print("Email Sudah Terdaftar")
            time.sleep(.5)
            return None

    if(len(users) == 0):
        user_id = 1
    else:
        user_id = users[len(users) - 1]['id'] + 1

    users.append({
        "id": user_id,
        "email": email,
        "password": password
    })
    with open('./db/user.json', 'w') as user:
        json.dump(users, user)
    print("Register Berhasil")
    time.sleep(.5)


def authenticate():
    print("Selamat Datang Di Aplikasi Tekom Eccomerce\nPilih Menu:\n1. Login\n2. Register\n3. Exit")
    choice = input("Masukan Pilihan: ")
    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        exit()
    else:
        print("Pilihan Tidak Ada")

def start():
    # authenticate the user 
    while not USER["ID"]:
        clearscreen()
        authenticate()

    clearscreen()
    print("== Main Program ==")
    print(USER)

start()