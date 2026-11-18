# KindredPath

**Explore. Imagine. Prepare.**

KindredPath is an interactive family financial-education experience designed to help people explore questions across children and education, family protection, healthcare and Medicare, aging parents, savings and retirement, home stability, and legacy.

## Experience
- Curiosity-driven homepage organized around life questions rather than products.
- **Family Journey** with plain-language explanations and practical scenarios.
- **Future Lab** with interactive sliders and illustrative what-if calculators.
- Product/category concepts including term life, whole life, universal life, IUL, 529 plans, Medicare/Medigap, long-term care, retirement accounts, annuities, disability, critical illness, and estate concepts.
- Email-only conversation request flow.
- Responsive design for desktop and mobile.
- No database or persistent form storage.

## Future Lab
Current interactive tools:
1. Monthly savings future-value explorer.
2. Children's education-cost explorer.
3. Household protection/runway explorer.

The calculators are deliberately simplified illustrations. They are not forecasts, quotes, financial recommendations, insurance recommendations, tax advice, legal advice, or investment advice.

## Privacy
- No application database or lead-management system.
- No persistent visitor profile.
- Do not request Social Security numbers, account numbers, medical details, or sensitive financial information.
- Routine hosting logs may exist outside the application.

## Email configuration
Render environment variables:
- `RESEND_API_KEY`
- `FROM_EMAIL`

The coordinator email is configured in `app.py`.

## Deploy
Repository: `sachintechpro/KindredPath`
Branch: `main`
Render configuration: `render.yaml`

## Local run
```bash
pip install -r requirements.txt
export RESEND_API_KEY='your-resend-key'
export FROM_EMAIL='verified-sender@your-domain.com'
python app.py
```
