# Гүл дүкөнү — сайт (Django)

Гүл дүкөндөрү үчүн сайт: каталог, себет, жеткирүү күнү/убактысы, буйрутма базага сакталып, дүкөндүн WhatsApp'ына даяр билдирүү менен жөнөтүлөт. Дүкөндүн ээси товарларды, бааларды, сүрөттөрдү жана буйрутмаларды `/panel/` дарегиндеги башкаруу панелинен өзгөртөт.

## Компьютерде иштетүү (Windows)

```
cd gul_shop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000 · Дүкөн ээсинин панели: http://127.0.0.1:8000/owner/ (сайттын ылдыйында «🔒 Дүкөн ээси үчүн» шилтемеси бар) · Техникалык админка: /panel/

Тесттер: `python manage.py test shop`

## Жаңы дүкөнгө ыңгайлаштыруу

`/owner/` панелине кирип (createsuperuser менен түзүлгөн логин):
1. **Дүкөндүн жөндөөлөрү** — аты, ураан, WhatsApp номери (буйрутмалар ушул номерге келет), дарек, Instagram, жеткирүү баасы, таймердин күнү.
2. **Товарлар** — демо товарларды өчүрүп же өзгөртүп, дүкөндүн өз сүрөттөрүн жүктөңүз (чарчы сүрөт жакшы).
3. **Буйрутмалар** — келген буйрутмалар, абалын өзгөртүү, кардарга WhatsApp'тан жазуу.

## PythonAnywhere'ге коюу

1. pythonanywhere.com → Consoles → **Bash**:
   ```
   git clone <репозиторий> gul_shop   # же ZIP жүктөп, unzip
   cd gul_shop
   mkvirtualenv gulshop --python=python3.10
   pip install -r requirements.txt
   ```
2. **Web** → *Add a new web app* → *Manual configuration* → Python 3.10.
3. Virtualenv: `/home/<логин>/.virtualenvs/gulshop`
4. WSGI файлын ачып, ичин мындай кылыңыз:
   ```python
   import os, sys
   path = '/home/<логин>/gul_shop'
   if path not in sys.path:
       sys.path.insert(0, path)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
   os.environ['DJANGO_SECRET_KEY'] = '<узун кокустук сап>'
   os.environ['DJANGO_DEBUG'] = '0'
   os.environ['DJANGO_ALLOWED_HOSTS'] = '<логин>.pythonanywhere.com'
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   Кокустук сапты мындай алыңыз: `python -c "import secrets;print(secrets.token_urlsafe(50))"`
5. Ошол эле өзгөрмөлөр менен Bash'та:
   ```
   export DJANGO_DEBUG=0 DJANGO_ALLOWED_HOSTS=<логин>.pythonanywhere.com DJANGO_SECRET_KEY=<ошол эле сап>
   python manage.py migrate
   python manage.py seed_demo
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```
6. **Web** → *Static files*:
   - URL `/static/` → `/home/<логин>/gul_shop/staticfiles`
   - URL `/media/` → `/home/<логин>/gul_shop/media`
7. **Reload**.

Эскертүү: PythonAnywhere'дин акысыз планында бир гана сайт (web app) болот.
