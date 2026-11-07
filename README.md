# TrustVault 🔐

### Secure Document Sharing with a Real Audit Trail

TrustVault is a Flask-based secure document-sharing application designed to protect uploaded documents through role-based access control, permission management, file validation, separate viewer access verification, and activity tracking.

Built for the **Snovasys Fresher Hiring Challenge 2026 — RISE**.

## ✨ Features

### 1. User Authentication
- Secure login using password hashing.
- Role-based access for administrators, owners, and viewers.
- Session-based authentication.

### 2. Secure Document Management
- Upload PDF, TXT, PNG, JPG, and JPEG files.
- Organize documents by category.
- Download uploaded documents.
- Replace existing documents when authorized.
- Private file storage using generated filenames.

### 3. Document Sharing
- Share documents with registered users.
- Assign READ or EDIT permissions.
- Update existing sharing permissions.
- Revoke document access.
- Restrict sharing operations to document owners.

### 4. Role-Based Access Control

| Role | Responsibilities |
|---|---|
| Admin | View the administrative dashboard and audit history. |
| Owner | Upload, manage, share, replace, and revoke access to documents. Set viewer access passwords. |
| Viewer | Access shared documents after additional password verification, according to assigned permissions. |

### 5. Additional Viewer Password Protection
- Owners can set a separate access password for each viewer.
- Viewers must verify this password before accessing shared documents.
- Passwords are stored securely as hashes.
- Changing the password requires verification again.
- READ and EDIT permissions remain enforced.

### 6. Audit Trail
- Record successful logins and failed login attempts.
- Track document downloads.
- Track document sharing and access revocation.
- Record document replacement activity.
- Record viewer password updates.
- Display timestamps and activity details.
- Restrict audit history to administrators.

### 7. File Security
- Validate supported file extensions.
- Validate actual file contents.
- Reject empty files.
- Enforce a 10 MB upload limit.
- Prevent unauthorized document replacement and downloads.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask 3.1.3 | Web framework |
| SQLite | Database |
| HTML | Page structure |
| Jinja2 | Template rendering |
| CSS | User interface |
| Werkzeug | Password hashing and secure filename handling |

## 📁 Project Structure

```text
TrustVault_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── audit_logs.html
│   ├── dashboard.html
│   ├── my_documents.html
│   ├── shared_documents.html
│   ├── upload.html
│   └── verify_access.html
│
└── private_uploads/
```

The SQLite database and private uploaded files are created locally and excluded from Git.

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or later
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/honeyhemima-777/TrustVault.git
cd TrustVault
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the secret key

Windows PowerShell:

```powershell
$env:TRUSTVAULT_SECRET_KEY = "replace-with-a-long-random-secret"
```

Never publish your actual secret key in GitHub.

### 4. Start the application

```bash
python app.py
```

### 5. Open in your browser

http://127.0.0.1:5002

## 🔑 Demo Login Credentials

| Role | Username | Login Password |
|---|---|---|
| Admin | admin | Honey12345 |
| Owner | owner | Honey12345 |
| Viewer | viewer | Honey12345 |

**Note:** These are demonstration credentials only. Change default passwords before production use. The viewer's additional access password is configured separately by the owner and should not be published.

## 🧪 Test Cases

| Test ID | Test Scenario | Expected Result |
|---|---|---|
| TC01 | Admin login | Admin dashboard opens successfully. |
| TC02 | Owner login | Owner dashboard opens successfully. |
| TC03 | Viewer login | Viewer account opens successfully. |
| TC04 | Upload a supported document | Document uploads successfully. |
| TC05 | Upload an unsupported file | Upload is rejected. |
| TC06 | Upload an empty file | Upload is rejected. |
| TC07 | Share with READ permission | Viewer can download but cannot replace. |
| TC08 | Share with EDIT permission | Viewer can replace the permitted document. |
| TC09 | Set viewer access password | Password is stored as a hash. |
| TC10 | Access shared documents without verification | Viewer is redirected to verification. |
| TC11 | Enter incorrect access password | Access is denied. |
| TC12 | Enter correct access password | Shared documents become accessible. |
| TC13 | Revoke document access | Viewer loses access. |
| TC14 | Unauthorized document replacement | HTTP 403 is returned. |
| TC15 | Download an authorized document | Document downloads successfully. |
| TC16 | Unauthorized audit log access | Access is denied. |
| TC17 | Upload invalid PDF contents | Upload is rejected. |
| TC18 | Upload a file exceeding 10 MB | Upload is rejected. |
| TC19 | Access an invalid document ID | HTTP 404 is returned. |
| TC20 | Review audit history | Recorded activities can be reviewed by an administrator. |

## 🔒 Security Testing

The following security checks have been performed during development:

- READ permission cannot replace a document.
- EDIT permission allows authorized replacement.
- Viewers cannot share another user's document.
- Unauthorized users cannot access administrative audit logs.
- Revoked users cannot download documents.
- Unsupported file extensions are rejected.
- Empty files are rejected.
- Invalid PDF contents are rejected.
- Files exceeding 10 MB are rejected.
- Invalid document IDs return HTTP 404.
- Document operations are recorded in the audit history.

## 🎯 Project Objective

TrustVault provides a secure and transparent document-sharing environment where users control access to their files and administrators can review recorded activities.

It combines permission management, additional viewer verification, and activity tracking to improve accountability and document security.

## 🚀 Future Enhancements

- Email-based account verification.
- Multi-factor authentication.
- Expiring document-sharing links.
- Encrypted file storage.
- Advanced audit filtering and export.
- Cloud deployment and backup support.

## 👩‍💻 Developed For

**Snovasys Fresher Hiring Challenge 2026 — RISE**

**Project:** TrustVault  
**Domain:** Web Application Development / Information Security  
**Backend:** Python Flask  
**Database:** SQLite

---

*TrustVault — Share securely. Track transparently.*