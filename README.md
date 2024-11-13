## Tentang Tekom Ecommerce

Aplikasi e-commerce shopping adalah platform yang memudahkan pengguna untuk mencari, membeli, dan memesan berbagai produk. Aplikasi ini memungkinkan pengguna untuk menelusuri berbagai kategori produk, menambahkannya ke keranjang belanja, dan melakukan transaksi pembayaran. 

## Teknologi

### Produksi
-   [python 3.x](https://www.python.org/)

## Table Of Database
### User

| field | type_data    |
| :---:  | :---:  |
| id |    pk, auto-increment, int   |
| email |    unique, string   |
| password |    string   |

### Produk

| field | type_data    |
| :---:  | :---:  |
| id |    pk, auto-increment, int   |
| user_id |    fk, int   |
| name |    string   |
| price |    int   |
| stock |    int   |
| category(perlu buat table kategori njir) |    string   |


## Kontibutor
<a href="https://github.com/allmerr/tekom-ecommerce/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=allmerr/tekom-ecommerce" />
</a>