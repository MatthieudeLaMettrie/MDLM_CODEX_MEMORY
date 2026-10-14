# French Expats Investment — Cal.com Booking Integration

_Last updated: 14 October 2026_

## Project Overview

- **Website**: https://www.frenchexpatsinvestment.com
- **Source repository**: https://github.com/MatthieudeLaMettrie/FEI-Website
- **Firebase Hosting project**: `fei-website-f16b0`
- **Verified Booking Endpoint**: `https://cal.com/matthieu-de-la-mettrie-zzf1ym/30min`

---

## Architecture & Integration Points

### 1. Contact Page (`FEI-Website/pages/Contact.tsx`)
* Luxury-styled **Agenda en Direct** card:
  - Heading: *« Réservez un audit de 30 minutes »*
  - CTA Button: *« Prendre rendez-vous »* linking directly to Cal.com.
  - Sits alongside the traditional written inquiry form so clients have zero friction choosing an immediate appointment or sending detailed written inquiries.

### 2. Cross-Border Financial Simulators (`FEI-Website/app/tools/`)
* Integrated 1-click Cal.com booking consultation CTAs across all 4 financial calculator tools:
  - `RentalTaxSimulator.tsx` (Simulateur fiscal France/Australie)
  - `BorrowingCapacityTool.tsx` (Capacité d'emprunt cross-border)
  - `IncomeTaxComparator.tsx` (Comparateur d'impôt France/Australie)
  - `SuperPlannerTool.tsx` (Simulateur Superannuation)
* Expats who model their property taxes or borrowing capacity can immediately book a 30-minute consultation with Matthieu.

### 3. Copy Harmonization
* All references across `pages/Contact.tsx`, `pages/Home.tsx`, `pages/Services.tsx`, and `app/seo.ts` harmonized to **30 minutes**.
* Simplified button label on contact page to cleanly read *« Prendre rendez-vous »*.

---

## Technical & Behavioral Facts

1. **Host Auto-Completion vs. Client Behavior**:
   - When the host (Matthieu) opens their own scheduling link while signed into Cal.com, the app auto-populates their name and email for testing convenience.
   - For all external visitors and prospective clients, the fields are completely blank with standard placeholders (`John Doe`, `you@example.com`).
2. **Localization**:
   - The Cal.com link automatically detects the visitor's browser language, presenting French UI to French speakers and English UI to English speakers.
