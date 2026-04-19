Alembic migrations are optional for Level 1 while the schema is still moving quickly.

When you are ready:

1. `cd hyperlocal-backend`
2. `alembic init migrations` (if not already configured) or wire `alembic.ini` to `app.database.Base` and `sqlalchemy.url`.
3. `alembic revision --autogenerate -m "init"` then `alembic upgrade head`.

Until then, tables are created on startup via `Base.metadata.create_all`.
