# 📘 README - Midterm Final Checklist

This README must remain in your repository and **must be fully
completed** before submitting the midterm.

---

## 1. API Test Coverage Table

Fill in the second column with the name of the student who implemented
and tested each API.

| # | API Endpoint / Feature | Implemented & Tested By (Student Name) |
|---|------------------------|----------------------------------------|
| 1 | Create Short Link - POST /links | Hadi                               |
| 2 | Redirect to Original URL - GET /{code} | Hadi                        |
| 3 | Get All Shortened Links - GET /links | Mehrnia                       |
| 4 | Delete Short Link - DELETE /links/{code} | Mehrnia                               |

---
​
## 2. Code Generation Method (Section 6.4)​
​
Check the method you used to generate the short code:​
- [ ] **1. Random Generation**​​
- [x] **2. ID → Base62 Conversion**​
- [ ] **3. Hash-based Generation**​​
(Only select the one you actually implemented.)​
​
---​
## 4. Postman Collection (Required)​
​
A **Postman Collection** has been created and includes all four API routes:​
​
- **POST /links**​
- **GET /{code}**​
- **GET /links**​
- **DELETE /links/{code}**​
​
### Screenshots (included in GitHub)​
​
For each route, two screenshots have been added:​
​
- Successful response (2xx) ​
- Error-handled response (4xx)​
​
Screenshots are located in:​
​
‍
‍```​
/postman​
```​
​
​
​
### Naming Example:​
​
```​
postman/​
post-links-201-success.png​
post-links-400-invalid-url.png​
get-code-302-redirect.png​
get-code-404-not-found.png​
get-links-200-success.png​
delete-code-200-success.png​
delete-code-404-not-found.png​​​

