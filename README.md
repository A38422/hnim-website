## ✨ Cách sử dụng

> Download code với lệnh sau (cài đặt `git` trước ghi thực hiên đoạn lệnh)

```bash
$ git clone https://github.com/A38422/hnim-website.git
$ cd hnim-website
```

<br />

### 👉 Thiết lập môi trường 

> Cài đặt các module qua `VENV` 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

> Nếu dùng `CONDA`

```
$ conda create --name hnim-website
$ conda activate hnim-website
$ pip install -r requirements.txt
```

<br />

> Thiết lập cơ sở dữ liệu

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Thực hiện đoạn lệnh sau để chạy chương trình

```bash
$ python manage.py runserver
```

Chương trình mặc định sẽ chạy ở `http://127.0.0.1:8000/`. 

<br />

## ✨ Tạo tài khoản người dùng

- Truy cập vào link dưới để tạo `tài khoản người dùng`
  - `http://127.0.0.1:8000/register/`
- Truy cập vào link dưới để đăng nhập
  - `http://127.0.0.1:8000/login/`

## ✨ Tạo tài khoản admin

```bash
$ python manage.py createsuperuser
```

- Truy cập vào link sau để truy cập trang `admin`
  - `http://127.0.0.1:8000/admin/`