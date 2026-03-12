# UniEats

University of Glasgow ITECH Coursework - University Restaurant Review Platform

## About

UniEats is a web application that allows university students to browse nearby restaurants, register accounts, and share dining reviews with ratings.

## Tech Stack

- **Backend**: Django
- **Frontend**: Bootstrap 5.3.2, Bootstrap Icons 1.11.3
- **Database**: SQLite

## Features

- User registration and login/logout
- Browse restaurant list with category and average rating
- View restaurant details (address, description, reviews)
- Write reviews with 1-5 star ratings (login required)
- Responsive design for mobile, tablet, and desktop
- WCAG 2.1 Level AA accessibility support

## Getting Started

### 1. Set Up Environment

```bash
git clone <repository-url>
cd UniEats

python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install django
```

### 2. Initialize Database

```bash
python manage.py migrate
python populate_data.py
```

### 3. Run Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

Optionally, create an admin account to manage data at `/admin/`:

```bash
python manage.py createsuperuser
```

## Project Structure

```
UniEats/
├── manage.py                        # Django management entry point
├── populate_data.py                 # Sample data seeding script
├── README.md
├── reviews_app/                     # Main application
│   ├── models.py                    # Models: Category, Restaurant, Review
│   ├── views.py                     # View functions
│   ├── urls.py                      # URL routing
│   ├── forms.py                     # ReviewForm
│   ├── admin.py                     # Admin site registration
│   ├── tests.py                     # Unit tests
│   ├── templates/reviews_app/
│   │   ├── base.html                # Base template with navbar and footer
│   │   ├── restaurant_list.html     # Homepage - restaurant listing
│   │   ├── restaurant_detail.html   # Restaurant details and reviews
│   │   ├── add_review.html          # Write a review form
│   │   ├── login.html               # Login page
│   │   └── register.html            # Registration page
│   └── static/css/
│       └── style.css                # Custom styles and accessibility
└── unieats_project/                 # Project configuration
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Testing

```bash
python manage.py test
```

## License

University of Glasgow ITECH coursework project.
