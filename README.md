<p align="center">
  <img src="static/images/logo.png" alt="Aksum Nexus e_commerce Logo" width="120" style="border-radius:16px; box-shadow:0 2px 8px #0002; margin-bottom:8px;"/>
</p>

<h1 align="center" style="font-family:sans-serif; font-weight:700; color:#222; margin-top:0;">Aksum Nexus E_commerce</h1>

<p align="center">
  <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" alt="Django" width="200"/>
</p>

<!-- Essential Requirements and Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/django-5%2B-green.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/REST%20Framework-3.14%2B-orange.svg" alt="DRF">
  <img src="https://img.shields.io/badge/allauth-0.60%2B-9cf.svg" alt="django-allauth">
  <img src="https://img.shields.io/badge/psycopg2--binary-latest-blueviolet.svg" alt="psycopg2-binary">
  <img src="https://img.shields.io/badge/Tailwind_CSS-3.x-38bdf8?logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
</p>

## Requirements

- Python 3.10+
- Django 5+
- djangorestframework
- django-allauth (with Google & GitHub providers)
- psycopg2-binary (for PostgreSQL)
- Tailwind CSS (for UI)

Add these to your `requirements.txt`:

```
Django>=5.1
psycopg2-binary
# Django REST Framework
 djangorestframework
# Social authentication
 django-allauth[google,github]
```

## Project Structure

```
Ecommerce_platform/         # Django project settings and URLs
store/                     # Main app: models, views, serializers, signals, forms
management/commands/       # Custom management commands
media/                     # Uploaded product images
static/                    # Static files (css, js, images)
templates/                 # HTML templates (base, index, cart, checkout, etc.)
manage.py                  # Django management script
config.json                # Database and secret config
```

## Installation & Usage

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Ecommerce_platform
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install
```

### 4. Configure the database

- Edit `config.json` and set your PostgreSQL password and any other secrets.
- Make sure PostgreSQL is running and a database named `Ecommerce_platform` exists (or change the name in `settings.py`).

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Collect static files

```bash
python manage.py collectstatic
```

### 8. Run the development server

```bash
python manage.py runserver
```

### 9. Access the site

- Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Social Authentication Setup

- In the Django admin, go to **Sites** and set the domain to `127.0.0.1:8000` (or your dev domain).
- Go to **Social Apps** and add Google and GitHub with the correct client IDs, secrets, and callback URLs.
- Make sure `SITE_ID = 1` in `settings.py`.
- Users can now log in with Google or GitHub.

## Customization

- UI is built with Tailwind CSS (via CDN for dev, or npm for production).
- You can override allauth templates in `templates/account/`.
- Add more social providers by including them in `INSTALLED_APPS` and configuring in admin.

## API

- REST API endpoints are available for products, cart, and orders.
- Uses DRF authentication and permissions.

## Signals

- `store/signals.py` ensures a profile is created for every user (including social logins).

## Error Handling

- User feedback and error messages are styled and displayed in all forms.
- Common OAuth and Allauth errors are handled and explained in the UI.

## Responsive Design

- All templates use Tailwind CSS for full mobile and desktop responsiveness.
- Navigation, product grids, and forms adapt to all device sizes.

## License

MIT License

---

For more details, see the code and comments in each file. Contributions and issues are welcome!
