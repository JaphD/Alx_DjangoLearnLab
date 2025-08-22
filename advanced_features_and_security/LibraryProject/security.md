## Security Configuration Overview

1. DEBUG=False  
   - Hides detailed error pages in production.

2. Host Whitelisting  
   - `ALLOWED_HOSTS` prevents Host header attacks.

3. XSS & MIME Protections  
   - `SECURE_BROWSER_XSS_FILTER`  
   - `SECURE_CONTENT_TYPE_NOSNIFF`

4. Clickjacking Defense  
   - `X_FRAME_OPTIONS = 'DENY'`

5. Cookie Security  
   - `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`

6. Static & Media  
   - WhiteNoise for static files  
   - `MEDIA_URL`/`MEDIA_ROOT` and URL patterns for media