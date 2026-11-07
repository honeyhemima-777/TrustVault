# TrustVault – DocShield
## AI Usage and Prompt Engineering Record

### 1. Purpose

AI was used as a development assistant during the creation of TrustVault. I directed the development process, reviewed generated suggestions, tested the implementation and corrected errors.

The following entries are reconstructed summaries of the prompts and development instructions used during the project. They are not claimed to be verbatim transcripts.

### 2. Prompt and Development History

#### Entry 1 – 01 November 2026
**Task:** Project planning and architecture

**Prompt summary:**
Help me build a secure document-sharing web application using Flask and SQLite. It should support Admin, Owner and Viewer roles, document uploads, sharing and permission management. Explain the implementation step by step.

**My contribution:**
I selected the project direction, clarified the requirements and requested a distinctive implementation rather than a generic template.

**Outcome:**
Established the TrustVault architecture and initial application structure.

#### Entry 2 – 02 November 2026
**Task:** Authentication and role-based access

**Prompt summary:**
Help implement secure login using password hashing and Flask sessions. Admin, Owner and Viewer users should have different dashboard access. Prevent unauthorized users from accessing protected routes.

**My contribution:**
I reviewed the role-based navigation and tested login behavior with different accounts.

**Outcome:**
Implemented authentication, password hashing and role-based dashboards.

#### Entry 3 – 03 November 2026
**Task:** Secure document uploads

**Prompt summary:**
Implement document uploads with file type validation, file size restrictions and private storage. Do not trust the file extension alone; validate file contents too.

**My contribution:**
I tested valid and invalid uploads and checked whether document records were saved correctly.

**Outcome:**
Implemented upload validation, a 10 MB limit and generated storage filenames.

#### Entry 4 – 04 November 2026
**Task:** Document sharing and authorization

**Prompt summary:**
Implement document sharing with READ and EDIT permissions. Ensure that a READ-only viewer cannot replace a document, even if they manually submit a request to the replacement URL.

**My contribution:**
I tested authorization at the route level instead of relying only on hiding buttons in the interface.

**Outcome:**
Implemented server-side permission checks. A local security test confirmed that a READ user attempting replacement was blocked with HTTP 403.

#### Entry 5 – 05 November 2026
**Task:** Audit trail

**Prompt summary:**
Help implement an audit log that records important TrustVault activities, including login attempts, document downloads, sharing, revocation and document replacement.

**My contribution:**
I checked the audit history through the Admin dashboard and verified that document replacement activity appeared.

**Outcome:**
Implemented audit logging and an admin-only audit history page.

#### Entry 6 – 06 November 2026
**Task:** Additional viewer password protection

**Prompt summary:**
Add a separate access password for each viewer. Store password hashes rather than plaintext passwords and require verification before accessing shared documents.

**My contribution:**
I tested the owner password-setting workflow, viewer verification and access to shared documents. I checked database records without exposing stored password hashes.

**Outcome:**
Implemented separate viewer access password protection.

#### Entry 7 – 07 November 2026
**Task:** Deployment and final verification

**Prompt summary:**
Help deploy the Flask application on Render, resolve deployment and database initialization issues, and verify the latest GitHub commit.

**My contribution:**
I checked the Render deployment history, tested the live login, uploaded a document and successfully downloaded it.

**Outcome:**
Deployed TrustVault and updated the Snovasys submission with the latest website and GitHub links.

### 3. How I Evaluated AI Suggestions

I did not blindly accept generated code. I:

- Reviewed suggested code before adding it.
- Ran Python syntax checks.
- Tested application routes using different user roles.
- Investigated database and deployment errors.
- Corrected issues when the actual application behavior differed from expectations.
- Tested unauthorized document replacement and confirmed that the server blocked the request.
- Verified the deployed application through the live website.

### 4. Limitations and Lessons Learned

AI-generated code can contain incorrect assumptions, implementation mistakes or incomplete security checks.

During development, I learned to:

- Verify authorization on the server side.
- Test both permitted and denied actions.
- Inspect database records when behavior is unexpected.
- Avoid treating a successful deployment as proof that every security requirement has passed.
- Review and improve generated code based on actual test results.

### 5. Conclusion

AI supported the development process, but project direction, requirement clarification, code review, testing and final verification were part of my own development work.

TrustVault demonstrates the use of AI as a development assistant combined with independent testing and security-focused decision-making.