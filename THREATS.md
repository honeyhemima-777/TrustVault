# TrustVault – DocShield
## Threat Model and Security Analysis

### 1. Project Overview

TrustVault is a secure document-sharing application built using Flask and SQLite. It allows document owners to upload, share, replace and manage access to documents. It maintains an audit trail of important activities.

### 2. Assets to Protect

- Uploaded documents and their contents.
- User accounts and password hashes.
- Document-sharing permissions.
- Viewer-specific access passwords.
- Audit log records.
- User sessions and authentication data.

### 3. Threats and Mitigations

| Threat | Risk | Mitigation |
|---|---|---|
| Unauthorized login | Attackers access user accounts | Password hashing and session-based authentication |
| Unauthorized document download | Private files are exposed | Login and document permission checks |
| Unauthorized document replacement | Documents are modified without permission | EDIT permission checks |
| READ user attempting EDIT actions | Read-only access is bypassed | Server-side permission validation |
| Unauthorized sharing | Documents are shared without owner approval | Owner-only sharing controls |
| Access after revocation | Former viewers retain document access | Revoke-sharing functionality |
| Invalid file upload | Malicious or unsupported files are uploaded | File extension and content validation, 10 MB size limit |
| Viewer account compromise | Shared documents are exposed | Separate viewer access password protection |
| Password exposure | Credentials are compromised | Password hashes are stored instead of plaintext passwords |
| Missing accountability | Suspicious actions cannot be investigated | Audit logs record important activities |

### 4. Security Controls

- Role-based access for Admin, Owner and Viewer.
- Password hashing using Werkzeug.
- Session-based login protection.
- Separate password verification for viewers.
- READ and EDIT permission enforcement.
- Server-side access checks for download and replacement.
- File type and content validation.
- Private storage using generated filenames.
- Audit logging for important actions.

### 5. Security Testing

The following security checks were performed during development:

1. Verified that the application requires authentication.
2. Tested document upload and download.
3. Tested document sharing and permission management.
4. Tested that a READ-only viewer is blocked from document replacement in a local security test.
5. Tested viewer access password verification.
6. Tested document replacement with EDIT permission.
7. Checked that document replacement activity appears in the audit logs.

Some additional negative tests, including revocation and READ-only download/replacement checks, still require complete verification.

### 6. Limitations and Future Improvements

- Add rate limiting to login and password verification.
- Add stronger protection against CSRF attacks.
- Use persistent storage for uploaded documents in production.
- Add automated security tests.
- Improve monitoring and alerting for suspicious access attempts.

### 7. Conclusion
# TrustVault – DocShield
## Threat Model and Security Analysis

### 1. Project Overview

TrustVault is a secure document-sharing application built using Flask and SQLite. It allows document owners to upload, share, replace and manage access to documents. It maintains an audit trail of important activities.

### 2. Assets to Protect

- Uploaded documents and their contents.
- User accounts and password hashes.
- Document-sharing permissions.
- Viewer-specific access passwords.
- Audit log records.
- User sessions and authentication data.

### 3. Threats and Mitigations

| Threat | Risk | Mitigation |
|---|---|---|
| Unauthorized login | Attackers access user accounts | Password hashing and session-based authentication |
| Unauthorized document download | Private files are exposed | Login and document permission checks |
| Unauthorized document replacement | Documents are modified without permission | EDIT permission checks |
| READ user attempting EDIT actions | Read-only access is bypassed | Server-side permission validation |
| Unauthorized sharing | Documents are shared without owner approval | Owner-only sharing controls |
| Access after revocation | Former viewers retain document access | Revoke-sharing functionality |
| Invalid file upload | Malicious or unsupported files are uploaded | File extension and content validation, 10 MB size limit |
| Viewer account compromise | Shared documents are exposed | Separate viewer access password protection |
| Password exposure | Credentials are compromised | Password hashes are stored instead of plaintext passwords |
| Missing accountability | Suspicious actions cannot be investigated | Audit logs record important activities |

### 4. Security Controls

- Role-based access for Admin, Owner and Viewer.
- Password hashing using Werkzeug.
- Session-based login protection.
- Separate password verification for viewers.
- READ and EDIT permission enforcement.
- Server-side access checks for download and replacement.
- File type and content validation.
- Private storage using generated filenames.
- Audit logging for important actions.

### 5. Security Testing

The following security checks were performed during development:

1. Verified that the application requires authentication.
2. Tested document upload and download.
3. Tested document sharing and permission management.
4. Tested that a READ-only viewer is blocked from document replacement in a local security test.
5. Tested viewer access password verification.
6. Tested document replacement with EDIT permission.
7. Checked that document replacement activity appears in the audit logs.

Some additional negative tests, including revocation and READ-only download/replacement checks, still require complete verification.

### 6. Limitations and Future Improvements

- Add rate limiting to login and password verification.
- Add stronger protection against CSRF attacks.
- Use persistent storage for uploaded documents in production.
- Add automated security tests.
- Improve monitoring and alerting for suspicious access attempts.

### 7. Conclusion

TrustVault follows a security-focused approach to document sharing by combining authentication, authorization, file validation, viewer access protection and audit logging. The threat model helps identify risks and guide future security improvements
