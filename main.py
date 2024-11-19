from random import Random
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
    # make error if the file is not exist
    if not os.path.exists(f'./db/{name_of_file}.json'): 
        return []   
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

def utils_get_non_empty_input(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        else:
            print("Input tidak boleh kosong. Silakan coba lagi.")

# login page to authenticate the user base of ./db/user.json give 3 chances to login and return the USER["ID"] if the user is authenticated
def page_login():
    users = utils_get_data("user")
    
    chances = 3
    while chances > 0:
        utils_clear_screen()
        console.print("---Login---", style="green")
        email = utils_get_non_empty_input("Masukkan Username: ")
        password = getpass.getpass("Masukkan Password: ")
        for user in users:
            if user['email'] == email and user['password'] == password:
                print("Login Berhasil")
                USER["ID"] = user["id"]
                USER["EMAIL"] = user["email"]
                return None
        console.print("Email Atau Password Salah", style=custom_theme["error"])
        chances -= 1
        time.sleep(2)

#register page to register the user base of ./db/user.json and return None 
def page_register():
    users = utils_get_data("user")
    
    utils_clear_screen()
    console.print("---Register---", style="green")
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
    time.sleep(2)

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
    print("---Tambah Produk---")
    name = utils_get_non_empty_input("Masukkan Nama Produk: ")
    price = utils_get_non_empty_input("Masukkan Harga Produk: ")
    stock = utils_get_non_empty_input("Masukkan Stok Produk: ")
    category = utils_get_non_empty_input("Masukkan Kategori Produk: ")

    produks = utils_get_data("produk")

    if((type(price) == str and price.isdigit() == False) or (type(stock) == str and stock.isdigit() == False)):
        console.print("Harga dan Stok Harus Angka", style=custom_theme["error"])
        time.sleep(2)
        return None

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
    time.sleep(2)

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
        time.sleep(2)
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
            time.sleep(2)
            return None
        
        console.print("[green]---Produk Saya - Lihat Produk Yang Ingin Diubah---[/]")
        utils_display_table(produks)

        produk_id = utils_get_non_empty_input("Masukan Produk Id Produk Yang Ingin Di Ubah: ")

        produks = utils_get_data("produk")
        produk = next((produk for produk in produks if str(produk['id']) == produk_id and str(produk['user_id']) == str(USER["ID"])), None)
        if not produk:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(2)
            return None

        name = utils_get_non_empty_input("Masukkan Nama Produk: ")
        price = utils_get_non_empty_input("Masukkan Harga Produk: ")
        stock = utils_get_non_empty_input("Masukkan Stok Produk: ")
        category = utils_get_non_empty_input("Masukkan Kategori Produk: ")

        if((type(price) == str and price.isdigit() == False) or (type(stock) == str and stock.isdigit() == False)):
            console.print("Harga dan Stok Harus Angka", style=custom_theme["error"])
            time.sleep(2)
            return None

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
        time.sleep(2)
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(2)
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
        produks = utils_get_data("produk")
        produk = next((produk for produk in produks if str(produk['id']) == produk_id and str(produk['user_id']) == str(USER["ID"])), None)
        if not produk:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(2)
            return None
        produks = [produk for produk in produks if produk['id'] != int(produk_id)]

        utils_save_data("produk", produks)

        print("Produk Berhasil Dihapus")
        time.sleep(2)
        return None
    else:
        print("Tidak Ada Produk Yang Ditemukan")
        time.sleep(2)
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

def page_my_wishlist_checkout():
    utils_clear_screen()

    keranjangs = utils_get_data("keranjang")
    keranjangs = [keranjang for keranjang in keranjangs if 'user_id' in keranjang and keranjang['user_id'] == USER["ID"] and keranjang['is_checkout'] == False]
    produks = utils_get_data("produk")
    for keranjang in keranjangs:
        produk = next((produk for produk in produks if str(produk["id"]) == keranjang["produk_id"]), None)
        if produk:
            keranjang["produk_name"] = produk["name"]
            keranjang["price"] = produk["price"]
            keranjang["total"] = int(produk["price"]) * int(keranjang["qty"])
        del keranjang['user_id']
        del keranjang['is_checkout']

    if(len(keranjangs) == 0):
        console.print("Tidak Ada Produk di Keranjang Yang Ditemukan", style=custom_theme["error"])
        time.sleep(2)
        return None
    utils_display_table(keranjangs)
    
    keranjang_ids = input("Masukan Id Keranjang Yang Ingin Di Checkout: (pisahkan dengan , untuk lebih dari 1 keranjang): ")
    creadit_card = input("Masukan Nomor Kartu Kredit Anda: ")
    keranjang_ids = keranjang_ids.split(",")
    
    keranjangs = utils_get_data("keranjang")
    for keranjang in keranjangs:
        if str(keranjang['id']) in keranjang_ids:
            keranjang['is_checkout'] = True
    
    utils_save_data("keranjang", keranjangs)

    # update the stock of the product
    produks = utils_get_data("produk")
    for keranjang in keranjangs:
        produk = next((produk for produk in produks if str(produk["id"]) == str(keranjang["produk_id"])), None)
        if produk:
            produk["stock"] = int(produk["stock"]) - int(keranjang["qty"])
    utils_save_data("produk", produks)  

    transactions = utils_get_data("transaksi")
    
    transkasi_code = Random().randint(100000, 999999)
    for keranjang_id in keranjang_ids:
        keranjang = next((keranjang for keranjang in keranjangs if str(keranjang['id']) == keranjang_id), None)
        if keranjang:
            if len(transactions) == 0:
                transaction_id = 1
            else:
                transaction_id = transactions[len(transactions) - 1]['id'] + 1
            transactions.append({
                "id": transaction_id,
                "user_id": USER["ID"],
                "produk_id": keranjang["produk_id"],
                "transaksi_code": transkasi_code,
                "credit_card": creadit_card,
                "qty": keranjang["qty"],
                "date": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            transaction_id += 1

    utils_save_data("transaksi", transactions)

    console.print("Checkout Berhasil", style=custom_theme["success"])
    time.sleep(2)
    
def page_my_wishlist():
    while USER["CURRECT_PAGE"] == "MY_WISHLIST":
        utils_clear_screen()
        console.print("[green]---Keranjang Saya---[/]\nPilih Menu:\n1. Lihat Keranjang\n2. Hapus Produk Dari Keranjang \n3. Checkout Kerajang\n4. Kembali Ke Main Menu")
        choice = input("Masukan Pilihan: ")
        if choice == "1":
            page_my_wishlist_read()
        elif choice == "2":
            page_my_wishlist_delete()
        elif choice == "3":
            page_my_wishlist_checkout()
        elif choice == "4":
            USER["CURRECT_PAGE"] = "MAIN"
            return None
        else:
            print("Pilihan Tidak Ada")
            return None

def page_my_wishlist_read():
    utils_clear_screen()

    keranjangs = utils_get_data("keranjang")
    keranjangs = [keranjang for keranjang in keranjangs if 'user_id' in keranjang and keranjang['user_id'] == USER["ID"] and keranjang['is_checkout'] == False]

    for keranjang in keranjangs:
        del keranjang['user_id']

    if len(keranjangs) > 0:
        console.print("---Keranjang Saya - Lihat Keranjang---", style="green")
        # change produk id to produk name
        produks = utils_get_data("produk")
        for keranjang in keranjangs:
            produk = next((produk for produk in produks if str(produk["id"]) == keranjang["produk_id"]), None)
            if produk:
                keranjang["produk_name"] = produk["name"]
                keranjang["price"] = produk["price"]
                keranjang["total"] = int(produk["price"]) * int(keranjang["qty"])

            del keranjang['is_checkout']
        utils_display_table(keranjangs)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Barang Di Keranjang Yang Ditemukan")
        time.sleep(2)
        return None

def page_my_wishlist_delete():
    utils_clear_screen()

    keranjangs = utils_get_data("keranjang")
    keranjangs = [keranjang for keranjang in keranjangs if 'user_id' in keranjang and keranjang['user_id'] == USER["ID"] and keranjang['is_checkout'] == False]

    if len(keranjangs) > 0:
        console.print("---Keranjang Saya - Lihat Keranjang Yang Ingin Dihapus---", style="green")
        # change produk id to produk name
        produks = utils_get_data("produk")
        for keranjang in keranjangs:
            produk = next((produk for produk in produks if str(produk["id"]) == keranjang["produk_id"]), None)
            if produk:
                keranjang["produk_name"] = produk["name"]
                keranjang["price"] = produk["price"]
                keranjang["total"] = produk["price"] * keranjang["qty"]

            del keranjang['is_checkout']

        utils_display_table(keranjangs)

        keranjang_id = input("Masukan Keranjang Id Yang Ingin Di Hapus: ")
        if(keranjang_id.isdigit() == False):
            console.print("Keranjang ID Harus Angka", style=custom_theme["error"])
            time.sleep(2)
            return None
        keranjangs = [keranjang for keranjang in keranjangs if keranjang['id'] != int(keranjang_id)]

        utils_save_data("keranjang", keranjangs)

        print("Keranjang Berhasil Dihapus")
        time.sleep(2)
        return None
    
def page_history_product():
    utils_clear_screen()

    transactions = utils_get_data("transaksi")
    transactions = [transaction for transaction in transactions if transaction['user_id'] == USER["ID"]]

    if len(transactions) > 0:
        print("=Riwayat Belanja=")
        for transaction in transactions:
            del transaction["user_id"]
        
        produks = utils_get_data("produk")
        for transaction in transactions:
            produk = next((produk for produk in produks if str(produk["id"]) == str(transaction["produk_id"])), None)
            if produk:
                del transaction["produk_id"]
                transaction["total_price"] = int(produk["price"]) * int(transaction["qty"])
                transaction["produk_name"] = produk["name"]
        
        utils_display_table(transactions)

        input("Tekan Enter Untuk Kembali Ke Menu")
        return None
    else:
        print("Tidak Ada Riwayat Belanja Yang Ditemukan")
        time.sleep(3)
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

    console.print("[green]---Tambahkan Ke Keranjang Produk - Lihat Produk---[/]")

    if(len(produks) == 0) :
        console.print("Produk Tidak Tersedia", style=custom_theme["error"])
        time.sleep(2)
        return None

    utils_display_table(produks)

    while True:
        produk_ids = input("Masukkan ID Produk yang Ingin Dibeli (pisahkan dengan : untuk kuantitas) atau ketik 'back' untuk kembali ke menu: ")
        if produk_ids.lower() == 'back':
            return None
        if ":" not in produk_ids:
            console.print("Format ID Produk Salah", style=custom_theme["error"])
            time.sleep(2)
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
            
            if int(produk_qty) > int(produk["stock"]):
                console.print("Kuantitas Yang Dimasukkan Melebihi Stok", style=custom_theme["error"])
                time.sleep(2)
                return None
            
            if next((keranjang for keranjang in keranjangs if keranjang["produk_id"] == produk_id and keranjang["user_id"] == USER["ID"]), None):
                console.print("Produk Sudah Ada Di Keranjang, Silahkan Hapus Dahulu", style=custom_theme["error"])
                time.sleep(2)
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
            time.sleep(2)
            return None
        else:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(2)
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
        time.sleep(2)
        return None

    while True:
        produk_ids = input("Masukkan ID Produk yang Ingin Dibeli (pisahkan dengan : untuk kuantitas) atau ketik 'back' untuk kembali ke menu: ")
        if produk_ids.lower() == 'back':
            return None
        if ":" not in produk_ids:
            console.print("Format ID Produk Salah", style=custom_theme["error"])
            time.sleep(2)
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
                time.sleep(2)
                return None
            
            if next((keranjang for keranjang in keranjangs if keranjang["produk_id"] == produk_id and keranjang["user_id"] == USER["ID"]), None):
                console.print("Produk Sudah Ada Di Keranjang, Silahkan Hapus Dahulu", style=custom_theme["error"])
                time.sleep(2)
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
            time.sleep(2)
            return None
        else:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(2)
            return None

def page_buy_product_category():
    utils_clear_screen()
    category = input("Masukkan Kategori Produk yang Ingin Dicari: ").lower()
    
    produks = utils_get_data("produk")
    produks = [produk for produk in produks if produk['user_id'] != USER["ID"]]
    
    users = utils_get_data("user")
    for produk in produks:
        user = next((user for user in users if user["id"] == produk["user_id"]), None)
        if user:
            produk["user_email"] = user["email"]
    
    for produk in produks:
        del produk['user_id']
    
    filtered_produks = [produk for produk in produks if category in produk['category'].lower()]
    
    if len(filtered_produks) > 0:
        console.print("[green]---Beli Produk - Hasil Pencarian---[/]")
        utils_display_table(filtered_produks)
    else:
        console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
        time.sleep(2)
        return None

    while True:
        produk_ids = input("Masukkan ID Produk yang Ingin Dibeli (pisahkan dengan : untuk kuantitas) atau ketik 'back' untuk kembali ke menu: ")
        if produk_ids.lower() == 'back':
            return None
        if ":" not in produk_ids:
            console.print("Format ID Produk Salah", style=custom_theme["error"])
            time.sleep(2)
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
            
            if int(produk_qty) > int(produk["stock"]):
                console.print("Kuantitas Yang Dimasukkan Melebihi Stok", style=custom_theme["error"])
                time.sleep(2)
                return None
            
            if next((keranjang for keranjang in keranjangs if keranjang["produk_id"] == produk_id and keranjang["user_id"] == USER["ID"]), None):
                console.print("Produk Sudah Ada Di Keranjang, Silahkan Hapus Dahulu", style=custom_theme["error"])
                time.sleep(2)
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
            time.sleep(2)
            return None
        else:
            console.print("Produk Tidak Ditemukan", style=custom_theme["error"])
            time.sleep(2)
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
        USER["CURRECT_PAGE"] = "HISTORY_PRODUCT"
        page_history_product()
    elif choice == "5":
        utils_clear_screen()
        console.print("---Terima Kasih Telah Menggunakan Tekom Ecoomerce---", style="green")
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
