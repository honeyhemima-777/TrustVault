# TrustVault – DocShield
## Threat Model and Security Analysis

### 1. Project Overview

TrustVault is a secure document-sharing application built using Flask and SQLite. It allows document owners to upload, share, replace and manage access to documents. It uses role-based authorization and maintains an audit trail of important activities.

### 2. Assets to Protect

- Uploaded documents and their contents.
- User accounts and password hashes.
- Document-sharing permissions.
- Viewer-specific access passwords.
- Audit log records.
- User sessions and authentication data.

### 3. Threats, Risks and Mitigations

| Threat | Risk | Mitigation | Testing Evidence / Status |
|---|---|---|---|
| Unauthorized login | Attackers may access user accounts | Password hashing and session-based authentication | Login flow tested |
| Unauthorized document download | Private files may be exposed | Authentication and document permission checks | Owner and viewer download tested; negative permission tests need further verification |
| Unauthorized document replacement | Documents may be modified without permission | Server-side EDIT permission checks | READ-only replacement attempt returned HTTP 403 locally |
| Unauthorized sharing | Documents may be shared without owner approval | Owner-only sharing controls | Sharing and permission management tested |
| Access after revocation | Former viewers may retain access | Revoke-sharing functionality | Complete negative test still pending |
| Invalid file upload | Unsupported or malicious files may be uploaded | File extension, content validation and 10 MB size limit | Upload functionality tested |
| Viewer account compromise | Shared documents may be exposed | Separate viewer access password verification | Viewer password verification tested |
| Password exposure | Credentials may be compromised | Password hashes instead of plaintext passwords | Password-hashing implementation included |
| Missing accountability | Suspicious actions may be difficult to investigate | Audit logs for important activities | Document replacement audit entry verified |

### 4. Security Controls

- Role-based access for Admin, Owner and Viewer.
- Password hashing using Werkzeug.
- Session-based login protection.
- Separate password verification for viewers.
- READ and EDIT permission enforcement.
- Server-side access checks for document download and replacement.
- File type and content validation.
- Private file storage using generated filenames.
- Audit logging for important activities.
- Owner-controlled permission management and revocation.

### 5. Security Testing

The following checks were performed during development:

1. Verified the application login and authentication flow.
2. Tested document upload and download.
3. Tested document sharing and permission management.
4. Tested that a READ-only viewer was blocked from document replacement; the local test returned HTTP 403.
5. Tested viewer access password verification.
6. Tested document replacement with EDIT permission.
7. Verified that document replacement activity appeared in the audit logs.

**Further verification required:**

- Complete negative testing after a share is revoked.
- Verify that a READ-only viewer cannot download a document if download is not permitted by the intended policy.
- Test additional unauthorized and invalid requests.
- Run a complete security regression test against the deployed application.

### 6. Limitations and Future Improvements

- Add rate limiting to login and password verification.
- Add stronger protection against CSRF attacks.
- Configure persistent storage for uploaded documents in production.
- Add automated security tests.
- Improve monitoring and alerting for suspicious access attempts.
- Consider secure backup and recovery procedures for documents and audit records.

### 7. Conclusion

TrustVault follows a security-focused approach to document sharing by combining authentication, role-based authorization, file validation, viewer access protection and audit logging. This threat model identifies potential risks, documents implemented controls and highlights areas requiring further verification and improvement.