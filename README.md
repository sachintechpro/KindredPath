# KindredPath

A public educational website with a simple, stateless meeting-request form.

## Visitor journey
1. A visitor arrives from a social-media call to action.
2. They explore general educational content on family priorities, financial confidence, and professional growth.
3. They submit their name, email, topic, and preferred meeting date/time.
4. KindredPath emails the request to the coordinator and sends a receipt to the visitor.
5. The coordinator follows up by email to confirm or propose another time.

## Privacy by design
- No database, lead dashboard, candidate account, CRM, or persistent form storage.
- No WhatsApp integration.
- No candidate-specific product recommendations, product comparisons, or tax analysis on the website.
- Form details are used only to compose the two requested emails.
- Do not ask visitors for Social Security numbers, account numbers, medical details, or sensitive financial information.
- The hosting provider may retain routine operational logs; this application does not write form submissions to application storage.

## Email configuration
Configure these Render environment variables:
- `RESEND_API_KEY`: Resend API key.
- `FROM_EMAIL`: A sender address verified with Resend (for example, a verified address on your domain).

The coordinator email is fixed in the application as `sachin.techpro@gmail.com`. Each valid request generates one email to the coordinator and one receipt email to the visitor.

## Meeting scheduling
The visitor chooses a preferred date and time in Pacific Time. This is a request, not a live calendar booking. The coordinator confirms availability by email. No calendar integration or appointment record is stored.

## Deploy on Render
Use the repository `sachintechpro/KindredPath`, branch `main`, and the root `render.yaml`. The service uses the free Docker web-service plan and requires the two email environment variables above. No database is needed.

## Local run
```bash
pip install -r requirements.txt
export RESEND_API_KEY='your-resend-key'
export FROM_EMAIL='verified-sender@your-domain.com'
python app.py
```
