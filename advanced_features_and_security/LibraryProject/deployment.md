1. Certificates
- Created a development TLS certificate and key using mkcert:
  - Files: C:\nginx\certs\library.crt, C:\nginx\certs\library.key
  - mkcert commands: `mkcert -install` then `mkcert localhost 127.0.0.1 ::1`.
- (Alternative method: OpenSSL with SAN config, stored at C:\nginx\certs\library.crt and library.key)

2. Nginx configuration
- Edited C:\nginx\conf\nginx.conf to add:
  - HTTP server listening on port 80 that redirects to HTTPS.
  - HTTPS server listening on port 443 configured with above certificate files.
  - Reverse proxy to Django at http://127.0.0.1:8000.

3. Django settings
- settings.py changes:
  - DEBUG = False
  - ALLOWED_HOSTS = ['localhost', '127.0.0.1']
  - SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  - SECURE_SSL_REDIRECT = True
  - SESSION_COOKIE_SECURE = True
  - CSRF_COOKIE_SECURE = True
  - (HSTS disabled for local testing)

4. Commands run
- Start nginx: `cd C:\nginx && start nginx`
- Restart nginx: `nginx -s reload`
- Run Django: `python manage.py runserver 127.0.0.1:8000`
- Generate mkcert: `mkcert -install` && `mkcert localhost 127.0.0.1 ::1`

5. Verification
- Accessed https://localhost in browser (no warning using mkcert).
- Verified `request.is_secure()` in Django returns True.
- Confirmed HTTP -> HTTPS redirect works.