# TrustVault – DocShield
## AI Usage and Prompt Engineering Record

### 1. Purpose

AI was used as a development assistant while building TrustVault. I directed the requirements, reviewed suggested implementations, reported errors, tested application behavior and requested corrections.

This document is a reconstructed summary of the development interactions, not a verbatim transcript of every prompt.

### 2. Development and Prompt History

#### Entry 1 – 06 November 2026
**Task:** Initial application and secure document sharing

**What I asked AI:**
Help me build a Flask and SQLite document-sharing application with Admin, Owner and Viewer roles, login, document uploads and secure sharing. Guide me through the implementation step by step.

**What AI produced:**
An initial Flask application structure and document-sharing functionality.

**Issue identified during development:**
The initial implementation needed to be checked against the actual role and permission requirements rather than assuming that a working interface meant secure access.

**What I did:**
I continued testing the application with different user roles and requested changes based on the actual behavior.

**Commit:** [5ee90e7 – Add TrustVault secure document sharing application](https://github.com/honeyhemima-777/TrustVault/commit/5ee90e7)

#### Entry 2 – 06 November 2026
**Task:** Dashboard usability and document management

**What I asked AI:**
Improve the Owner Dashboard and make document management actions understandable and accessible.

**What AI produced:**
An improved dashboard interface with document management controls.

**Issue identified during development:**
The interface needed to clearly reflect document-sharing and management state. Displaying controls alone was not sufficient to establish that an operation had succeeded.

**What I did:**
I checked the actual document records and tested the available actions through the application.

**Commit:** [b173e0e – Improve owner dashboard UI and update README](https://github.com/honeyhemima-777/TrustVault/commit/b173e0e)

#### Entry 3 – 06 November 2026
**Task:** Debugging document download and shared-document display

**What I asked AI:**
Investigate the HTTP 500 error encountered during document download and help resolve the issue where a shared document existed in the server-side debug output but was not appearing correctly on the viewer page.

**What AI produced:**
Debugging guidance and corrections to the affected application code.

**Issue identified during development:**
The download route contained an accidental SQL/code syntax error. The shared-document display also did not initially match the data returned by the server.

**What I did:**
I reported the observed errors, checked terminal output and debug information, applied corrections and tested the affected functionality again.

**Commit reference:** [5ee90e7 – Secure document-sharing application](https://github.com/honeyhemima-777/TrustVault/commit/5ee90e7)

#### Entry 4 – 07 November 2026
**Task:** Authorization and permission enforcement

**What I asked AI:**
Implement READ and EDIT document permissions. A READ-only viewer must not be able to replace a document by directly submitting a request to the replacement route.

**What AI produced:**
Server-side permission checks for document operations.

**Security consideration:**
Hiding the Replace button in the interface would not be sufficient. The server must independently verify the user's permission.

**What I did:**
I tested a replacement request as a READ-only viewer. The local security test returned HTTP 403, confirming that the tested unauthorized replacement was blocked.

**Commit reference:** [5ee90e7 – Secure document-sharing application](https://github.com/honeyhemima-777/TrustVault/commit/5ee90e7)

#### Entry 5 – 07 November 2026
**Task:** Audit trail and accountability

**What I asked AI:**
Help implement audit logging for important activities such as login attempts, document downloads, sharing, revocation and document replacement.

**What AI produced:**
Database-backed audit records and an Admin audit history page.

**Security consideration:**
A success message alone does not provide an audit trail. Important actions need recorded events that can be inspected later.

**What I did:**
I opened the Admin Audit Logs page and verified that a document replacement event appeared after the operation.

**Commit reference:** [5ee90e7 – Secure document-sharing application](https://github.com/honeyhemima-777/TrustVault/commit/5ee90e7)

#### Entry 6 – 07 November 2026
**Task:** Separate viewer access password protection

**What I asked AI:**
Add an additional password for each viewer. Store the password as a hash and require verification before the viewer accesses shared documents.

**What AI produced:**
A viewer access-password management workflow, password verification and session-based verification checks.

**Security consideration:**
Normal account login alone was not the additional document-access protection requested. The separate viewer verification needed to be enforced before protected document operations.

**What I did:**
I tested the owner password-setting workflow, signed in as the viewer, completed the separate password verification and accessed the shared document. I also tested document replacement with EDIT permission.

**Commit:** [97b02f2 – Add separate viewer access password protection](https://github.com/honeyhemima-777/TrustVault/commit/97b02f2)

#### Entry 7 – 07 November 2026
**Task:** Deployment and production debugging

**What I asked AI:**
Help deploy the Flask application on Render and investigate database initialization problems during deployment.

**What AI produced:**
Deployment configuration guidance, Gunicorn setup and database initialization corrections.

**Issue identified during development:**
The deployed environment required database initialization to work correctly, independently of the local development environment.

**What I did:**
I reported the deployment issue, applied the correction, checked the Render deployment history and tested the live application. I verified owner login, document upload, document listing and document download.

**Commits:**
- [a9437c2 – Add Gunicorn for Render deployment](https://github.com/honeyhemima-777/TrustVault/commit/a9437c2)
- [3aca5f6 – Fix database initialization for Render deployment](https://github.com/honeyhemima-777/TrustVault/commit/3aca5f6)

### 3. How I Evaluated AI Suggestions

During development, I:

- Reviewed generated code before using it.
- Ran Python syntax checks.
- Tested login and document operations.
- Reported unexpected HTTP errors.
- Used terminal output and debug information to investigate problems.
- Tested authorization using different user roles.
- Checked the Admin audit history.
- Verified important functionality on the deployed website.

### 4. Lessons Learned

The development process taught me that:

- A visible button does not prove server-side authorization.
- Authentication and authorization are different security responsibilities.
- File validation must inspect content, not just filenames.
- Debug output and database inspection help identify application problems.
- Local testing and production deployment can expose different issues.
- AI-generated code must be reviewed and tested before it is trusted.

### 5. Conclusion

AI assisted with planning, implementation, debugging and documentation. I directed the requirements, reported observed problems, tested the application and reviewed the results.

TrustVault demonstrates how AI can support individual software development while keeping human review, security testing and responsibility central to the process.