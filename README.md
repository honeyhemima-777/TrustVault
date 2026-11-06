# TrustVault 🔐

### Secure Document Sharing with a Real Audit Trail



TrustVault is a Flask-based secure document-sharing application designed to protect uploaded documents through role-based access control, permission management, file validation, and activity tracking.



Built for the **Snovasys Fresher Hiring Challenge 2026 — RISE**.



# ✨ Features



\### 1. User Authentication

\- Secure login using password hashing.

\- Role-based access for administrators and regular users.

\- Session-based authentication.



### 2. Secure Document Management

\- Upload PDF, TXT, PNG, JPG, and JPEG files.

\- Organize documents by category.

\- Download uploaded documents.

\- Replace existing documents when authorized.

\- Private file storage using generated filenames.



### 3. Document Sharing

\- Share documents with registered users.

\- Assign READ or EDIT permissions.

\- Update existing sharing permissions.

\- Revoke document access.

\- Restrict sharing operations to document owners.



### 4. Role-Based Access Control

\- **Admin:** View administrative dashboard and audit history.

\- **Owner:** Upload, manage, share, replace, and revoke access to owned documents.

\- **Viewer:** Access documents shared with them according to assigned permissions.



### 5. Audit Trail

\- Record successful login events and failed login attempts.

\- Track document downloads.

\- Track document sharing and access revocation.

\- Record document replacement activity.

\- Display timestamps and activity details.

\- Restrict audit history to administrators.



### 6. File Security

\- Allow only supported file extensions.

\- Validate file contents, not just filenames.

\- Reject empty files.

\- Enforce a 10 MB upload limit.

\- Prevent unauthorized document replacement and downloads.



# 🛠️ Technology Stack



| Technology | Purpose |

|---|---|

| Python | Backend programming |

| Flask 3.1.3 | Web framework |

| SQLite | Database |

| HTML | Page structure |

| Jinja2 | Template rendering |

| CSS | User interface |

| Werkzeug | Password hashing and secure filename handling |



# 📁 Project Structure



`text

TrustVault\_Project/

│

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── templates/

│   ├── login.html

│   ├── admin\_dashboard.html

│   ├── audit\_logs.html

│   ├── my\_documents.html

│   ├── shared\_documents.html

│   └── upload.html

│

└── private\_uploads/

`



The SQLite database and private uploaded files are created locally and excluded from Git.



# ⚙️ Installation and Setup



### Prerequisites

\- Python 3.10 or later

\- pip

\- Git



### 1. Clone the repository



`bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd TrustVault\_Project

`



### 2. Install dependencies



`bash

python -m pip install -r requirements.txt

`



### 3. Configure the secret key



**Windows PowerShell:**



`powershell

$env:TRUSTVAULT\_SECRET\_KEY = "replace-with-a-long-random-secret"

`



Use a strong, private secret key. Never publish it in GitHub.



### 4. Start the application



`bash

python app.py

`



### 5. Open in your browser



`text

http://127.0.0.1:5002

`



# 🔒 Security Testing



The following checks have been performed during development:



\- READ permission cannot replace a document.

\- EDIT permission can replace a document.

\- Viewers cannot share another user's document.

\- Unauthorized users cannot access administrative audit logs.

\- Revoked users cannot download documents.

\- Unsupported file extensions are rejected.

\- Empty files are rejected.

\- Invalid PDF contents are rejected.

\- Files exceeding 10 MB are rejected.

\- Invalid document IDs return HTTP 404.

\- Document operations are recorded in the audit history.



# 🎯 Project Objective



The main objective of TrustVault is to provide a secure and transparent document-sharing environment where users can control access to their files and administrators can review recorded activities.



Unlike basic file-sharing applications, TrustVault combines permission management with an audit trail to improve accountability and document security.



# 🚀 Future Enhancements



\- Email-based account verification.

\- Multi-factor authentication.

\- Expiring document-sharing links.

\- Encrypted file storage.

\- Advanced audit filtering and export.

\- Cloud deployment and backup support.



# 👩‍💻 Developed For



**Snovasys Fresher Hiring Challenge 2026 — RISE**



**Project:** TrustVault  

**Domain:** Web Application Development / Information Security  

**Backend:** Python Flask  

**Database:** SQLite



\---



*TrustVault — Share securely. Track transparently.*

