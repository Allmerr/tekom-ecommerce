import json, os, time, getpass
from rich.console import Console
from rich.table import Table

# global variable to store the user data
USER = {
    "ID": "",
    "EMAIL": "",
    "CURRECT_PAGE": "" # EXIT, MAIN, MY_PRODUCT, MY_WISHLIST, HISTORY_PRODUCT, BUY_PRODUCT
}

# get data from json file required string of the file name like "user" to get the data from ./db/user.json
def utils_get_data(name_of_file):
    with open(f'./db/{name_of_file}.json') as data:
        return json.load(data)
# save data to json file required string of the file name like "user" and dict of data to save the data to ./db/user.json
def utils_save_data(name_of_file, data):
    with open(f'./db/{name_of_file}.json', 'w') as file:
        json.dump(data, file)

# utilitys to clean terminal screen
def utils_clear_screen(numlines=100):
    if os.name == "posix":
        # Unix, Linux, macOS, BSD, etc.
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print('\n' * numlines)

# display table using rich library required columns and data to display the table  
def utils_display_table(data_tables):
    # display the table
    columns = []
    for key in data_tables[0]:
        columns.append({"header": key.capitalize()})

    rows = []
    for produk in data_tables:
        row = []
        for key in produk:
            row.append(str(produk[key]))
        
        rows.append(tuple(row))

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    
    for column in columns:
        table.add_column(column['header'], style=column.get('style', 'dim'), justify=column.get('justify', 'left'), width=column.get('width', None))

    for row in rows:
        table.add_row(*row)

    console.print(table)

# login page to authenticate the user base of ./db/user.json give 3 chances to login and return the USER["ID"] if the user is authenticated
def page_login():
    users = utils_get_data("user")
    
    chances = 3
    while chances > 0:
        utils_clear_screen()
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
        time.sleep(1)

#register page to register the user base of ./db/user.json and return None 
def page_register():
    users = utils_get_data("user")
    
    utils_clear_screen()
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
    
    utils_save_data("user", users)

    print("Register Berhasil")
    time.sleep(.5)

# autheticate page return the USER["ID"] if the user is authenticated
def page_authenticate():
    print("Selamat Datang Di Aplikasi Tekom Eccomerce\nPilih Menu:\n1. Login\n2. Register\n3. Exit")
    choice = input("Masukan Pilihan: ")
    if choice == "1":
        page_login()
    elif choice == "2":
        page_register()
    elif choice == "3":
        utils_clear_screen()
        print("Terima Kasih Telah Menggunakan Aplikasi Ini")
        exit()
    else:
        print("Pilihan Tidak Ada")

# create the product and save it to the database
def page_my_product_create():
    utils_clear_screen()
    print("=Tambah Produk=")
    name = input("Masukkan Nama Produk: ")
    price = input("Masukkan Harga Produk: ")
    stock = input("Masukkan Stok Produk: ")
    category = input("Masukkan Kategori Produk: ")

    produks = utils_get_data("produk")

    for produk in produks:
        if produk['name'] == name:
            print("Nama Produk Sudah Ada")
            time.sleep(.5)
            return

    if(len(produks) == 0):
        produk_id = 1
    else:
        produk_id = produks[len(produks) - 1]['id'] + 1

    produks.append({
        "id": produk_id,
        "user_id": USER["ID"],
        "name": name,
        "price": price,
        "stock": stock,
        "category": category
    })

    utils_save_data("produk", produks)

    print("Produk Berhasil Ditambahkan")
    time.sleep(.5)

    return None

# read the product from the database and display it to the user
def page_my_product_read():
    utils_clear_screen()
    
    produks = utils_get_data("produk")
    # filter the product based on the user id and remove the user id from the product   
    produks = [produk for produk in produks if produk['user_id'] == USER["ID"]]
    for produk in produks:
        del produk['user_id']

    if len(produks) > 0:        
     
        print("=Produk Saya - Lihat Produk=")
        utils_display_table(produks)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(1)
        return None


def page_my_product_update():
    return None
def page_my_product_delete():
    return None

def page_my_product():
    while USER["CURRECT_PAGE"] == "MY_PRODUCT":
        utils_clear_screen()
        print("=Produk Saya=\nPilih Menu:\n1. Tambah Produk\n2. Lihat Produk\n3. Mengubah Produk\n4. Menghapus Produk\n5. Kembali Ke Main Menu")
        choice = input("Masukan Pilihan: ")
        if choice == "1":
            page_my_product_create()
        elif choice == "2":
            page_my_product_read()
        elif choice == "3":
            page_my_product_update()
        elif choice == "4":
            page_my_product_delete()
        elif choice == "5":
            USER["CURRECT_PAGE"] = "MAIN"
            return None
        else:
            print("Pilihan Tidak Ada")
            return None

def page_my_wishlist():
    while USER["CURRECT_PAGE"] == "MY_WISHLIST":
        utils_clear_screen()

        keranjangs = utils_get_data("keranjang")

        keranjangs = [keranjang for keranjang in keranjangs if keranjangs['user_id'] == USER["ID"]]
        for keranjang in keranjangs:
            del keranjang['user_id']

    if len(keranjangs) > 0:        
     
        print("=Keranjang Saya - Lihat Kerajang=")
        utils_display_table(keranjangs)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Barang Di Keranjang Yang Ditemukan")
        time.sleep(1)
        return None
    
def page_my_wishlist_create():
    produks = utils_get_data("produk")

    id_target = "1"
    data_keranjang = None

    for produk in produks:
        if produk.get('id') == id_target:
            data_keranjang = produk
            break
    
    if data_keranjang:
        with open(f'./db/keranjang.json') as tujuan_keranjang:
            json.dump(data_keranjang, tujuan_keranjang, indent=4)
        print(f"Produk sudah ditambahkan ke keranjang")
    else:
        print(f"Produk dengan id {id_target} tidak ditemukan")
            
def page_history_product():
    return None

def page_buy_product():
    return None 

def page_main():
    print("=Main Menu Tekom Eccomerce=\nPilih Menu:\n1. Belanja Produk\n2. Produk Saya\n3. Keranjang Saya\n4. History Belanja\n5. Logout")
    choice = input("Masukan Pilihan: ")
    if choice == "1":
        page_buy_product()
    elif choice == "2":
        USER["CURRECT_PAGE"] = "MY_PRODUCT"
        page_my_product()
    elif choice == "3":
        page_my_wishlist()
    elif choice == "4":
        page_history_product()
    elif choice == "5":
        utils_clear_screen()
        print("Terima Kasih Telah Menggunakan Tekom Ecoomerce")
        exit()
    else:
        print("Pilihan Tidak Ada")
    
def start():
    # authenticate the user before going to the main page 
    while not USER["ID"]:
        utils_clear_screen()
        page_authenticate()

    # main page
    while USER["CURRECT_PAGE"] != "EXIT":
        utils_clear_screen()
        page_main()

start()
