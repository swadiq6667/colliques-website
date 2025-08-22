# Colliques Website

An e-commerce Django application with:
- User roles (Admin, Customer)
- Product catalog, variants, cart, and orders
- Payment method support (COD, online payments)

## Installation

```bash
git clone https://github.com/swadiq6667/colliques-website.git
cd colliques-website
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
