# URL-shortener---Midterm-SWE
Repository Design pattern for a minimal URL shortener

Install Dependencies:

```bash
poetry install
```
Setup Database (Strict Requirement): The document explicitly forbids docker-compose. You must use docker run:

```bash
docker run --name url-shortener-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=12345678 -e POSTGRES_DB=shortener_db -p 5432:5432 -d postgres
```
Configure Environment: Copy the example env file and update it with your DB credentials:

```bash
cp .env.example .env
```
Initialize Alembic (Migrations): Run this command inside your project root to create the migration folder structure:

```bash
poetry run alembic init migrations
```
Note: You will then need to edit migrations/env.py to import your Base model so Alembic can detect your tables.

Run the Server:

```bash
poetry run uvicorn app.main:app --reload
```
