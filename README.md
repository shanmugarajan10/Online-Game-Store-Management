# Online-Game-Store-Management
An end-to-end web application built for managing digital game sales, user accounts, and purchase history. The platform enables users to browse games, manage carts, perform secure checkouts, and access their digital library. Admins can add, update, and manage game inventory, categories, and user transactions.

## Features

- 🎮 Browse games by categories
- 🔍 Search and filter games
- 🛒 Shopping cart functionality
- 👤 User authentication and profiles
- 💳 Secure checkout process
- 📱 Responsive design
- 🎨 Cyberpunk-themed UI
- 📊 Admin dashboard for game management

## Tech Stack

- **Backend**: Django 5.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5, Custom Cyberpunk CSS
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Django's built-in auth system
- **Forms**: Crispy Forms with Bootstrap 5
- **Icons**: Font Awesome, Bootstrap Icons

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shanmugarajan10/Online-Game-Store-Management
cd Online-Game-Store-Management
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://localhost:8000 in your browser

## Project Structure

```
Online-Game-Store-Management/
├── game_store/          # Project settings
├── store/              # Main application
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded files
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── registration/  # Auth templates
│   └── store/         # Store templates
└── manage.py          # Django management script
```

## Key Features Implementation

### Game Management
- Games are organized by categories
- Each game has detailed information including price, description, and system requirements
- Stock management system
- Featured games section

### User Features
- User registration and authentication
- Shopping cart functionality
- Order history
- Profile management

### Admin Features
- Game management (CRUD operations)
- Category management
- Order management
- User management

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Font Awesome
- All contributors and supporters

## Contact

For any queries or support, please open an issue in the GitHub repository.

---

Made with ❤️ by Shanmugarajan 
