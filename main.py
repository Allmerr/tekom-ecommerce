import json, os, time, getpass
from rich.console import Console
from rich.table import Table

# global variable to store the user data
USER = {
    "ID": "",
    "EMAIL": "",
    "CURRECT_PAGE": "" # EXIT, MAIN, MY_PRODUCT, MY_WISHLIST, HISTORY_PRODUCT, BUY_PRODUCT
}
console = Console()
custom_theme = {"success" : "bold white on green", "error" : "bold white on red"}

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
        console.print("Login Gagal", style=custom_theme["error"])
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

    console.print("Register Berhasil", style=custom_theme["success"])
    time.sleep(1)

# autheticate page return the USER["ID"] if the user is authenticated
def page_authenticate():
    console.print("[green]---Selamat Datang Di Aplikasi Tekom Eccomerce---[/]\nPilih Menu:\n1. Login\n2. Register\n3. Exit")
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

    console.print("Produk Berhasil Ditambahkan", style=custom_theme["success"])
    time.sleep(1)

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
     
        console.print("[green]---Produk Saya - Lihat Produk---[/]")
        utils_display_table(produks)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(1)
        return None

# read the product from the database and update the selected product by user from the database
def page_my_product_update():
    utils_clear_screen()
    produks = utils_get_data("produk")
    #check if the product is not empty and has product from the current user
    if len(produks) > 0:        
        # filter the product based on the user id and remove the user id from the product   
        produks = [produk for produk in produks if produk['user_id'] == USER["ID"]]
        for produk in produks:
            del produk['user_id']    
        
        if produks == []:
            print("Tidak Ada Produk Yang Ditemukan")
            time.sleep(1)
            return None
        
        console.print("[green]---Produk Saya - Lihat Produk Yang Ingin Diubah---[/]")
        utils_display_table(produks)

        produk_id = input("Masukan Produk Id Produk Yang Ingin Di Ubah: ")

        name = input("Masukkan Nama Produk: ")
        price = input("Masukkan Harga Produk: ")
        stock = input("Masukkan Stok Produk: ")
        category = input("Masukkan Kategori Produk: ")

        produks = utils_get_data("produk")
        produks = [produk for produk in produks if produk['id'] != int(produk_id)]
        produks.append({
            "id": int(produk_id),
            "user_id": USER["ID"],
            "name": name,
            "price": price,
            "stock": stock,
            "category": category
        })

        utils_save_data("produk", produks)

        console.print("Produk Berhasil Diubah", style=custom_theme["success"])
        time.sleep(1)
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(1)
        return None

#  read prduct from database and delete the selected product by user from the database
def page_my_product_delete():
    utils_clear_screen()
    # filter the product based on the user id and remove the user id from the product   
    produks = utils_get_data("produk")
    produks = [produk for produk in produks if produk['user_id'] == USER["ID"]]

    if len(produks) > 0:        
        
        console.print("[green]---Produk Saya - Lihat Produk Yang Ingin Dihapus[/]")
        utils_display_table(produks)

        produk_id = input("Masukan Produk Id Produk Yang Ingin Di Hapus: ")
        produks = [produk for produk in produks if produk['id'] != int(produk_id)]

        utils_save_data("produk", produks)

        print("Produk Berhasil Dihapus")
        time.sleep(1)
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(1)
        return None

# main my product page to display the menu of my product
def page_my_product():
    while USER["CURRECT_PAGE"] == "MY_PRODUCT":
        utils_clear_screen()
        console.print("[green]---Produk Saya---[/]\nPilih Menu:\n1. Tambah Produk\n2. Lihat Produk\n3. Mengubah Produk\n4. Menghapus Produk\n5. Kembali Ke Main Menu")
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
        console.print("[green]---Keranjang Saya---[/]\nPilih Menu:\n1. Lihat Keranjang\n2. Hapus Produk Dari Keranjang \n3. Kembali Ke Main Menu")
        choice = input("Masukan Pilihan: ")
        if choice == "1":
            page_my_wishlist_read()
        elif choice == "2":
            page_my_wishlist_delete()
        elif choice == "3":
            USER["CURRECT_PAGE"] = "MAIN"
            return None
        else:
            print("Pilihan Tidak Ada")
            return None

def page_my_wishlist_read():
    utils_clear_screen()

    keranjangs = utils_get_data("keranjang")
    keranjangs = [keranjang for keranjang in keranjangs if 'user_id' in keranjang and keranjang['user_id'] == USER["ID"]]

    for keranjang in keranjangs:
        del keranjang['user_id']

    if len(keranjangs) > 0:
        print("=Keranjang Saya - Lihat Keranjang=")
        utils_display_table(keranjangs)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Barang Di Keranjang Yang Ditemukan")
        time.sleep(1)
        return None

def page_my_wishlist_delete():
    utils_clear_screen()

    keranjangs = utils_get_data("keranjang")
    keranjangs = [keranjang for keranjang in keranjangs if 'user_id' in keranjang and keranjang['user_id'] == USER["ID"]]

    if len(keranjangs) > 0:
        print("=Keranjang Saya - Lihat Keranjang Yang Ingin Dihapus=")
        utils_display_table(keranjangs)

        keranjang_id = input("Masukan Keranjang Id Yang Ingin Di Hapus: ")
        keranjangs = [keranjang for keranjang in keranjangs if keranjang['id'] != int(keranjang_id)]

        utils_save_data("keranjang", keranjangs)

        print("Keranjang Berhasil Dihapus")
        time.sleep(1)
        return None
    
def page_history_product():
    return None

def page_buy_product_read():
    utils_clear_screen()
    produks = utils_get_data("produk")

    produks = [produk for produk in produks if produk['user_id'] != USER["ID"]]
    
    users = utils_get_data("user")
    for produk in produks:
        user = next((user for user in users if user["id"] == produk["user_id"]), None)
        if user:
            produk["user_email"] = user["email"]
    
    for produk in produks:
        del produk['user_id']

    console.print("[green]---Beli Produk - Lihat Produk---[/]")
    utils_display_table(produks)

    while True:
        produk_ids = input("Masukkan ID Produk yang Ingin Dibeli (pisahkan dengan : untuk kuantitas) atau ketik 'back' untuk kembali ke menu: ")
        if produk_ids.lower() == 'back':
            return None
        if ":" not in produk_ids:
            console.print("Format ID Produk Salah", style=custom_theme["error"])
            time.sleep(1)
            return None
        produk_id = produk_ids.split(":")[0]
        produk_qty = produk_ids.split(":")[1]
        produk = next((produk for produk in produks if produk["id"] == int(produk_id)), None)
        if produk:
            keranjangs = utils_get_data("keranjang")
            if(len(keranjangs) == 0):
                keranjang_id = 1
            else:
                keranjang_id = keranjangs[len(keranjangs) - 1]['id'] + 1
            
            #check apakah kuantitas yang diinputkan lebih dari stok
            if int(produk_qty) > int(produk["stock"]):
                console.print("Kuantitas Yang Dimasukkan Melebihi Stok", style=custom_theme["error"])
                time.sleep(1)
                return None
            
            # check if the product is already in the cart
            if next((keranjang for keranjang in keranjangs if keranjang["produk_id"] == produk_id and keranjang["user_id"] == USER["ID"]), None):
                console.print("Produk Sudah Ada Di Keranjang, Silahkan Hapus Dahulu", style=custom_theme["error"])
                time.sleep(1)
                return None

            keranjangs.append({
                "id": keranjang_id,
                "user_id": USER["ID"],
                "produk_id": produk_id,
                "qty": produk_qty,
                "is_checkout": False
            })

            utils_save_data("keranjang", keranjangs)

            console.print("Produk Berhasil Ditambahkan Ke Keranjang", style=custom_theme["success"])
            time.sleep(1)
            return None
        else:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(1)
            return None

def page_buy_product_search():
    utils_clear_screen()
    keyword = input("Masukkan Kata Kunci Produk yang Ingin Dicari: ").lower()
    
    produks = utils_get_data("produk")
    produks = [produk for produk in produks if produk['user_id'] != USER["ID"]]
    
    users = utils_get_data("user")
    for produk in produks:
        user = next((user for user in users if user["id"] == produk["user_id"]), None)
        if user:
            produk["user_email"] = user["email"]
    
    for produk in produks:
        del produk['user_id']
    
    filtered_produks = [produk for produk in produks if keyword in produk['name'].lower() or keyword in produk['category'].lower()]
    
    if len(filtered_produks) > 0:
        console.print("[green]---Beli Produk - Hasil Pencarian---[/]")
        utils_display_table(filtered_produks)
    else:
        console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
        time.sleep(1)
        return None

    while True:
        produk_ids = input("Masukkan ID Produk yang Ingin Dibeli (pisahkan dengan : untuk kuantitas) atau ketik 'back' untuk kembali ke menu: ")
        if produk_ids.lower() == 'back':
            return None
        if ":" not in produk_ids:
            console.print("Format ID Produk Salah", style=custom_theme["error"])
            time.sleep(1)
            return None
        produk_id = produk_ids.split(":")[0]
        produk_qty = produk_ids.split(":")[1]
        produk = next((produk for produk in filtered_produks if produk["id"] == int(produk_id)), None)
        if produk:
            keranjangs = utils_get_data("keranjang")
            if(len(keranjangs) == 0):
                keranjang_id = 1
            else:
                keranjang_id = keranjangs[len(keranjangs) - 1]['id'] + 1
            
            if int(produk_qty) > int(produk["stock"]):
                console.print("Kuantitas Yang Dimasukkan Melebihi Stok", style=custom_theme["error"])
                time.sleep(1)
                return None
            
            if next((keranjang for keranjang in keranjangs if keranjang["produk_id"] == produk_id and keranjang["user_id"] == USER["ID"]), None):
                console.print("Produk Sudah Ada Di Keranjang, Silahkan Hapus Dahulu", style=custom_theme["error"])
                time.sleep(1)
                return None

            keranjangs.append({
                "id": keranjang_id,
                "user_id": USER["ID"],
                "produk_id": produk_id,
                "qty": produk_qty,
                "is_checkout": False
            })

            utils_save_data("keranjang", keranjangs)

            console.print("Produk Berhasil Ditambahkan Ke Keranjang", style=custom_theme["success"])
            time.sleep(1)
            return None
        else:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(1)
            return None

def page_buy_product_category():
    return None

def page_buy_product():
     while USER["CURRECT_PAGE"] == "BUY_PRODUCT":
        utils_clear_screen()
        console.print("[green]---Beli Produk---[/]\nPilih Menu:\n1. Lihat Produk\n2. Cari Produk\n3. Cari Kategori\n4. Kembali Ke Main Menu")
        choice = input("Masukan Pilihan: ")
        if choice == "1":
            page_buy_product_read()
        elif choice == "2":
            page_buy_product_search()
        elif choice == "3":
            page_buy_product_category()
        elif choice == "4":
            USER["CURRECT_PAGE"] = "MAIN"
            return None
        else:
            print("Pilihan Tidak Ada")
            return None

def page_main():
    console.print("[green]---Main Menu Tekom Eccomerce---[/]\nPilih Menu:\n1. Belanja Produk\n2. Produk Saya\n3. Keranjang Saya\n4. History Belanja\n5. Logout")
    choice = input("Masukan Pilihan: ")
    if choice == "1":
        USER["CURRECT_PAGE"] = "BUY_PRODUCT"
        page_buy_product()
    elif choice == "2":
        USER["CURRECT_PAGE"] = "MY_PRODUCT"
        page_my_product()
    elif choice == "3":
        USER["CURRECT_PAGE"] = "MY_WISHLIST"
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
