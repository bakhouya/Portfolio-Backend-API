# Portfolio Backend API

A robust, scalable, and RESTful backend API engineered with **Django 6.0** and **Django REST Framework (DRF)**. This application serves as the centralized data layer for a professional portfolio, managing dynamic content including projects, professional experience, skills, and contact mechanisms.

Designed with **Clean Architecture** principles, it emphasizes modularity, security, and performance optimization through caching and signal-based automation.

## Unique Features & Technical Highlights

Beyond standard CRUD operations, this repository implements several advanced architectural patterns and security measures:

### Security & Input Sanitization
- **XSS Prevention:** Utilizes **Bleach** to sanitize incoming text data. This ensures that descriptions in projects or contact messages are stripped of malicious HTML tags and scripts before storage.
- **JWT Authentication:** Implements stateless authentication using `djangorestframework_simplejwt`, securing administrative endpoints while keeping public read-access open.

### Performance & Caching
- **Redis Integration:** Configured with `django-redis` to handle caching strategies. This reduces database hits for high-traffic read endpoints (like fetching the skills list or profile settings).
- **Optimized Querying:** Uses `django-filter` within specific apps (`projects`, `educations`, `experiences`) to allow efficient database filtering without over-fetching data.

### Advanced Architecture & Signals
- **Automated File Management:** Leveraging Django `signals.py` (found in `accounts`, `educations`, `experiences`), the system automatically handles filesystem hygiene. When an image (e.g., a project thumbnail or profile picture) is updated, the previous file is physically deleted from storage to prevent orphan files.
- **Modular App Structure:** The project is strictly decoupled into granular applications (`educations`, `experiences`, `services`, etc.), ensuring that business logic remains isolated and maintainable.
- **Business Rules Layer:** Specific apps contain `rules.py`, suggesting a separation of complex permission logic or business constraints from the standard Views and Models.

### Documentation
- **Auto-Generated Swagger UI:** Integrated with `drf-yasg` to provide real-time, interactive API documentation, making frontend integration seamless.


## Tech Stack

*   **Framework:** Python 3.x, Django 6.0
*   **API Toolkit:** Django REST Framework (DRF) 3.16
*   **Authentication:** PyJWT, SimpleJWT
*   **Database:** SQLite (Dev) / PostgreSQL (Recommended for Prod)
*   **Caching:** Redis, Django-Redis
*   **Image Processing:** Pillow
*   **Sanitization:** Bleach
*   **Documentation:** drf-yasg (OpenAPI Generator)
*   **Utilities:** Django-Filter, Django-Cors-Headers

---

## Installation & Usage

### Prerequisites
*   Python 3.10+
*   Redis (required for caching)

### Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/bakhouya/Portfolio-Backend-API.git
    cd Portfolio-Backend-API
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory (refer to `config/settings.py` for required variables, typically `SECRET_KEY`, `DEBUG`, `DB_CONFIG`).

5.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.

---



