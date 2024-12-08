# To-do

- [x] Models
- [x] Views
- [x] Authentication
- [x] Throttling
- [x] Search, Filtering, and Ordering
- [x] Pagination
- [x] Make everything class-based
- [ ] Caching
- [ ] User profile management
- [x] Documentation
- [x] File upload
- [ ] Testing
- [x] Versioning
- [ ] Deployment


# Environment variables

- `SECRET_KEY`
- `ALLOWED_HOSTS` (seperated by comma)
- **Database**:
    - `DB_ENGINE`
    - `DB_NAME`
    - `DB_USER`
    - `DB_PASS`
    - `DB_PORT`
    - `DB_HOST`
    - *If not provided, **sqlite** will be used.*
- `TIME_ZONE` (Default: `UTC`)
- `DEBUG`
- `CSRF_COOKIE_SECURE`
- `SESSION_COOKIE_SECURE`
- `SECURE_SSL_REDIRECT`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`
