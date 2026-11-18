# KindredPath

A private inquiry, intent-tracking and meeting-coordination workspace.

## Scope
- Public inquiry pages for family planning and professional development.
- Hidden source attribution via `?agent=...`, `?campaign=...`, and `?post=...`.
- Explicit optional WhatsApp opt-in; consent text and timestamp stored with the inquiry.
- Private admin pipeline, internal notes, follow-up tasks and activity history.
- Candidate-specific analysis is internal meeting preparation only. No product/tax recommendation is displayed or emailed to candidates.
- Email notifications through Resend API; WhatsApp through official Meta Cloud API and an approved template.

## Deploy on Render
Create a free PostgreSQL instance, then a free Docker web service using this repository with:
- Docker context: `kindredpath`
- Dockerfile: `kindredpath/Dockerfile`
- Environment: `DATABASE_URL`, `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASSWORD`
- Optional email: `RESEND_API_KEY`, `FROM_EMAIL`, `LEAD_EMAIL_TO`
- Optional WhatsApp: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_TEMPLATE_NAME`, `WHATSAPP_TEMPLATE_LANG`

Use a long, unique admin password and a random secret key. Configure the WhatsApp template with two body text parameters: candidate name and meeting details.

## Important free-tier limitation
Render Free Postgres expires 30 days after creation, has 1 GB storage and no managed backups. Export records before expiry and upgrade or migrate if the system will hold ongoing business leads. Render Free web services spin down after 15 minutes idle.

## Local run
```bash
pip install -r requirements.txt
export DATABASE_URL='postgresql://...'
export SECRET_KEY='replace-me'
export ADMIN_USER='admin'
export ADMIN_PASSWORD='replace-with-a-long-password'
python app.py
```

## Privacy
Collect only information needed to arrange a conversation. Do not collect Social Security numbers, account numbers, detailed health information or sensitive financial documents. Provide a privacy notice and retention policy before public launch.
