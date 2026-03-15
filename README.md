# Project Name: Mapping Entities API

## Description
This project implements the backend API for a complex mapping system required by the assignment involving `Vendor`, `Product`, `Course`, and `Certification` entities. The API strictly uses Django REST Framework (DRF) and encompasses advanced validation to prevent data duplication.

## Architecture Highlights
- **BaseModel Driven:** All master entities securely inherit `id` (UUID), `is_active`, `created_at`, and `updated_at` from a central abstract `BaseModel`.
- **Soft Deletes:** Deletions only toggle the `is_active` flag, keeping the database history intact. Queries are routed through a custom `ActiveManager`.
- **Mapping Entities:** Manually tracked `ForeignKey` models for `VendorProductMapping`, `ProductCourseMapping`, and `CourseCertificationMapping`.
- **Dual Validation:**
  - *Database Level Check*: Implemented `UniqueConstraint` on mappings to physically block database duplication.
  - *Application Level Check*: Enforced the "only one primary_mapping per parent" rule via the strict DRF validation lifecycle within the `Serializers`.

## Tech Stack
- Python
- Django
- Django REST Framework (DRF)
- `python-decouple` (for `.env` management)
- `django-cors-headers` (for Cross-Origin requests setup)

## Setup Instructions

1.  **Clone the Repository**
2.  **Create a Virtual Environment & Install Dependencies:**
    
    *Option A: Using Standard pip (Slower)*
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
    pip install -r requirements.txt
    ```

    *Option B: Using uv by Astral (Faster)*
    ```bash
    # Ensure uv is installed (e.g., pip install uv)
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -r requirements.txt
    ```
4.  **Set Up Environment Variables:**
    - Navigate into the `backend/` directory.
    - Copy the `.env.example` file to create a new `.env` file (`cp .env.example .env`).
    - Update the variables inside `.env` with your secure credentials.
5.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6.  **Populate Database (Optional):**
    *To quickly test the APIs and Swagger documentation, run the seed script to auto-generate dummy Vendors, Products, Courses, Certifications and their mappings:*
    ```bash
    cd backend/
    python seed_db.py
    ```
7.  **Start the Local Server:**
    ```bash
    python manage.py runserver
    ```
8. **For Admin Dashboard (Optional):**
   '''bash
   python manage.py createsuperuser
   '''

## API Documentation
Interactive API documentation is automatically generated using `drf-yasg` and explicit `@swagger_auto_schema` decorators. Once the local server is running, you can explore and test the endpoints at:
- **Swagger UI:** `http://127.0.0.1:8000/swagger/`
- **ReDoc:** `http://127.0.0.1:8000/redoc/`

## API Endpoints Overview
*All endpoints are prefixed with `/api/` and utilize standard HTTP methods (GET, POST, PUT, PATCH, DELETE).*

- `GET /api/vendors/` -> List all active vendors
- `POST /api/vendors/` -> Create a vendor
- `PUT /api/vendors/<uuid>/` -> Full update on vendor
- `PATCH /api/vendors/<uuid>/` -> Partial update on vendor
- `DELETE /api/vendors/<uuid>/` -> Soft-delete vendor

(This identical structure applies to `/api/products/`, `/api/courses/`, `/api/certifications/`, `/api/vendor-product-mappings/`, `/api/product-course-mappings/`, and `/api/course-certification-mappings/`)
