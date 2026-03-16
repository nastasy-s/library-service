<img width="1773" height="1045" alt="Screenshot 2026-03-16 at 19 25 45" src="https://github.com/user-attachments/assets/4bf9e322-126b-4f30-93af-d3c979b2a56c" />
<img width="369" height="456" alt="Screenshot 2026-03-16 at 19 28 38" src="https://github.com/user-attachments/assets/00ab689e-f451-4e42-8719-cc93545fa74b" />
<img width="1761" height="900" alt="Screenshot 2026-03-16 at 19 29 08" src="https://github.com/user-attachments/assets/ad489f95-8a2e-4af9-b9cb-9199c21ea91b" />
# Library Service API

Online management system for book borrowings.

## Features

- Books management (CRUD)
- User authentication (JWT)
- Borrowings management
- Telegram notifications
- Swagger documentation

## Technologies

- Django + Django REST Framework
- PostgreSQL
- Redis + Celery
- Docker + Docker Compose
- JWT Authentication
- Telegram Bot API

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```
   git clone https://github.com/nastasy-s/library-service.git
   cd library-service
```

2. Create `.env` file:
```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_HOST=db
   DB_NAME=library_db
   DB_USER=library_user
   DB_PASSWORD=library_pass
   DB_PORT=5432
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   TELEGRAM_CHAT_ID=your-chat-id
```

3. Run with Docker:
```
   docker-compose up --build
```

4. Create superuser:
```
   docker-compose exec web python manage.py createsuperuser
```

5. Load initial data (optional):
```
   docker-compose exec web python manage.py loaddata books/fixtures/books_data.json
```

6. Open in browser:
   - API: http://localhost:8000/api/
   - Swagger: http://localhost:8000/api/doc/swagger/
   - Admin: http://localhost:8000/admin/

## API Endpoints

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create book (admin only)
- `GET /api/books/{id}/` - Book details
- `PUT /api/books/{id}/` - Update book (admin only)
- `DELETE /api/books/{id}/` - Delete book (admin only)

### Users
- `POST /api/users/register/` - Register new user
- `POST /api/users/token/` - Get JWT token
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/me/` - Get current user profile

### Borrowings
- `GET /api/borrowings/` - List borrowings
- `POST /api/borrowings/` - Create borrowing
- `GET /api/borrowings/{id}/` - Borrowing details
- `POST /api/borrowings/{id}/return/` - Return book

## Running Tests
```
docker-compose exec web python manage.py test
```

## Test Coverage
```
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

## Author
Anastasiia Savchenko
