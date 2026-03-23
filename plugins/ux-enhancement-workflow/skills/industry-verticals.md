# UX Industry Verticals Knowledge Base

**Scope:** Reference guide for UX-Atlas and its specialists when applying industry-specific patterns, compliance requirements, and design priorities to a user's product context.

**Usage:** When the user specifies an industry vertical, load the relevant section below and apply its patterns, typical users, and compliance constraints before producing flows, critiques, or specs.

---

## Healthcare

- **Key UX Patterns**
  - Progressive disclosure for clinical data (show summary first, detail on demand)
  - Medication reminder flows with confirmation steps to prevent errors
  - Emergency-access affordances always visible (not hidden in menus)
  - Plain-language result summaries alongside clinical values
  - Offline-first or graceful degradation for clinical settings with poor connectivity

- **Typical Users**
  Patients aged 40+, medical staff (nurses, physicians, pharmacists), family caregivers, administrative staff, medical billers

- **Regulatory / Compliance**
  HIPAA (US, data privacy and minimum necessary), HITECH, FDA 21 CFR Part 11 (electronic records), GDPR Article 9 (special-category health data, EU), HL7 FHIR integration requirements, ADA Section 508 for federally funded systems

- **Design Priorities**
  1. Trust signals (institutional branding, verified provider badges)
  2. Error prevention and safety (confirmations, read-back patterns)
  3. Accessibility and cognitive load reduction

- **Accessibility Considerations**
  Large tap targets for older users with motor impairments; high-contrast mode for clinical environments with variable lighting; screen-reader compliance for visually impaired patients; cognitive accessibility for patients under stress or with low health literacy

- **Common Pitfalls**
  - Hiding emergency actions behind multi-step navigation
  - Displaying raw lab values without reference ranges or plain-language context
  - Designing only for "healthy" power users while ignoring stressed or cognitively fatigued patients

---

## Finance / Banking

- **Key UX Patterns**
  - Stepwise onboarding with KYC/identity verification milestones
  - Balance and transaction history with strong data visualisation (sparklines, category breakdowns)
  - Multi-factor authentication integrated naturally into flows, not bolted on
  - Spend categorization with editable labels for transparency
  - Confirmation dialogs with irreversibility warnings for transfers

- **Typical Users**
  Retail banking customers (18–65), high-net-worth individuals, SME owners, financial advisors, fraud investigators, compliance officers

- **Regulatory / Compliance**
  PSD2 / Open Banking (EU), GDPR, CCPA, PCI-DSS (card data), KYC/AML regulations, SOX (US public companies), MiFID II (investment products), WCAG 2.1 AA (EU accessibility directive)

- **Design Priorities**
  1. Security cues (lock icons, SSL indicators, session timeout warnings)
  2. Data accuracy and precision (no rounding errors in display)
  3. Transparency (clear fee disclosure, exchange rate visibility)

- **Accessibility Considerations**
  Colour-independent status indicators (never use colour alone for account status); large font options for statement views; keyboard-navigable transaction tables; clear focus states for screen-reader users navigating fund-transfer flows

- **Common Pitfalls**
  - Dark patterns on fee disclosure (buried in small print or overlays)
  - Automatic session logout without a save-state mechanism, losing filled forms
  - Complex re-authentication flows that cause users to abandon high-value transactions

---

## E-Commerce

- **Key UX Patterns**
  - Persistent cart with cross-device sync
  - Progressive checkout (address → shipping → payment → review) with progress indicator
  - Social proof integration (reviews, ratings, "X people viewing this")
  - Wishlist and save-for-later to reduce abandoned carts
  - Guest checkout option alongside registered account flow

- **Typical Users**
  Occasional bargain shoppers, frequent brand loyalists, mobile-first shoppers, B2B procurement buyers, gift purchasers

- **Regulatory / Compliance**
  GDPR / CCPA (tracking cookies, consent banners), PCI-DSS, distance-selling regulations (EU Consumer Rights Directive, UK CRA), WCAG 2.1 AA, country-specific digital sales tax disclosure

- **Design Priorities**
  1. Conversion optimisation (remove friction from purchase funnel)
  2. Trust and security cues at checkout
  3. Search and filter performance for large catalogues

- **Accessibility Considerations**
  Keyboard-navigable product carousels; alt text on all product images; accessible CAPTCHA alternatives in checkout; sufficient colour contrast on CTA buttons; focus management on modal pop-ups (size guides, quick views)

- **Common Pitfalls**
  - Forcing account creation before completing checkout
  - Surprise shipping cost revelation at the last checkout step
  - Auto-playing video ads that disorient keyboard and screen-reader users

---

## Education

- **Key UX Patterns**
  - Spaced-repetition and progress-tracking dashboards (streaks, completion %)
  - Scaffolded content delivery (module → lesson → exercise → assessment)
  - Collaborative tools: discussion boards, peer review assignments
  - Adaptive difficulty signals (pass/fail thresholds with remediation paths)
  - Offline content access for low-bandwidth learners

- **Typical Users**
  K-12 students (6–18), adult learners / continuing education, university students, corporate L&D trainees, educators / instructors, parents monitoring progress

- **Regulatory / Compliance**
  COPPA (US, under-13 data), FERPA (US, student records), GDPR (EU student data, special attention to minors), WCAG 2.1 AA, IDEA (US, students with disabilities), local data-residency requirements for public schools

- **Design Priorities**
  1. Motivation and engagement (gamification, badges, streaks)
  2. Clarity in instructions and no cognitive overload
  3. Parental controls and guardian visibility for minors

- **Accessibility Considerations**
  Dyslexia-friendly font options and adjustable line spacing; closed captions on all video content; screen-reader compatible quiz formats; keyboard-only navigation for test-taking environments; colour-blind safe progress indicators

- **Common Pitfalls**
  - Gamification loops that reward time-on-platform over actual learning
  - Video-heavy content without transcripts, blocking audio-disabled or hearing-impaired learners
  - Overly complex navigation that distracts students from the learning task

---

## Travel & Hospitality

- **Key UX Patterns**
  - Date-range pickers with calendar visualisation and price-per-day indicators
  - Itinerary builder with drag-and-drop reordering
  - Map-integrated search for hotels, restaurants, and activities
  - Consistent availability status (real-time inventory, cancellation badges)
  - Multi-currency and multi-language content adaption

- **Typical Users**
  Leisure travellers (solo, couple, family), business travellers, travel agents / OTA operators, hotel / airline staff, accessibility-needs travellers

- **Regulatory / Compliance**
  GDPR / CCPA (booking data, tracking), PCI-DSS (card at point of booking), Disability Discrimination Act / ADA (accessible travel information), IATA standards for flight data display, EU Package Travel Directive

- **Design Priorities**
  1. Speed and reliability (fast search results, no stale inventory)
  2. Price transparency (total cost inclusive of taxes and fees upfront)
  3. Flexibility messaging (cancellation, change policies prominent)

- **Accessibility Considerations**
  Accessible booking flows for mobility-impaired users who need to select accessible rooms; colour-contrast on price differentials in calendar grids; clear keyboard focus for date pickers; screen-reader friendly seat selection maps

- **Common Pitfalls**
  - Hidden fees surfacing only at payment step
  - Date pickers that are keyboard-inaccessible or screen-reader incompatible
  - Overloading search results with upsell overlays that block the decision flow

---

## Legal & Compliance

- **Key UX Patterns**
  - Document review interfaces with annotation, comment, and version-diff views
  - Clause library with search and smart tagging
  - Approval and e-signature workflow with audit trail
  - Risk scoring dashboards with drill-down to source clauses
  - Matter management timelines with deadline alerts

- **Typical Users**
  In-house legal counsel, external law firm attorneys, paralegals, compliance officers, contract managers, executives approving contracts

- **Regulatory / Compliance**
  GDPR / CCPA (PII in legal documents), attorney-client privilege requirements (data isolation), e-IDAS / ESIGN Act (electronic signatures), SOC 2 Type II (SaaS law tools), WCAG 2.1 AA, bar association data ethics rules

- **Design Priorities**
  1. Accuracy and traceability (every action logged with timestamp and user)
  2. Security and confidentiality (access controls, data compartmentalisation)
  3. Efficiency (minimise time-per-review-cycle)

- **Accessibility Considerations**
  High-density document views must support font scaling without layout breakage; annotation toolbars must be keyboard accessible; colour-coded risk tiers must have non-colour secondary indicators (icons, labels)

- **Common Pitfalls**
  - Autosave behaviour that overwrites accepted contract text without warning
  - Surfacing non-binding commentary alongside binding clauses without clear visual distinction
  - Inaccessible PDF viewer embedded in a web app, undermining WCAG compliance

---

## Manufacturing & Industrial

- **Key UX Patterns**
  - Shop-floor dashboards: real-time machine status, OEE metrics, alert queues
  - Work-order management with step-by-step task checklists
  - Barcode / QR scan integration for inventory and parts tracking
  - Preventive maintenance scheduling calendars
  - Role-based views (operator vs. supervisor vs. plant manager)

- **Typical Users**
  Machine operators (often non-desk workers), floor supervisors, maintenance engineers, plant managers, quality inspectors, ERP / MES integration specialists

- **Regulatory / Compliance**
  OSHA safety recordkeeping, ISO 9001 (quality management traceability), ISO 45001 (occupational health), GDPR for EU plant workers' data, environmental reporting (EPA, EU ETS), FDA 21 CFR Part 820 for medical device manufacturing

- **Design Priorities**
  1. Glanceability (status at-a-glance, minimal reading required)
  2. Error alerting clarity (machine stops, threshold breaches)
  3. Rugged environment compatibility (touch targets for gloved hands, sunlight-readable contrast)

- **Accessibility Considerations**
  Large tap targets for gloved-hand use; high-contrast UI for bright factory-floor lighting; minimal text input (scan + select preferred); auditory alert fallbacks for noisy environments; simple navigation for operators with varying digital literacy

- **Common Pitfalls**
  - UI designed for desktop that is deployed on a tablet in a noisy, bright environment
  - Alert fatigue from undifferentiated critical vs. informational notifications
  - Requiring complex data entry during time-sensitive operations

---

## Government & Public Sector

- **Key UX Patterns**
  - Step-by-step guided forms with save-and-resume for complex applications
  - Plain-language templates replacing bureaucratic boilerplate
  - Multi-channel parity (web + mobile + in-person kiosk)
  - Status tracking for applications and service requests (reference number + timeline)
  - Accessible document downloads (PDF tagged for screen readers, HTML alternatives)

- **Typical Users**
  General public (all ages and literacy levels), civil servants / case workers, elected officials, journalists requesting public records, businesses applying for licenses

- **Regulatory / Compliance**
  WCAG 2.1 AA mandatory (EU Web Accessibility Directive, US Section 508), GDPR / national privacy laws, FISMA (US federal systems), Government Digital Service (GDS) standards (UK), eIDAS for identity (EU), Freedom of Information Act (FOIA)

- **Design Priorities**
  1. Inclusivity — design for the least digitally-literate user
  2. Trust and official legitimacy (government branding, anti-phishing cues)
  3. Reliability and permanence (no beta features without stable fallback)

- **Accessibility Considerations**
  WCAG 2.1 AA as a legal baseline, not a target; reading-level: plain language (Flesch-Kincaid grade 8 or below); multilingual support for minority language communities; screen magnification compatibility; forms must work without JavaScript for older devices

- **Common Pitfalls**
  - PDF-only application forms that are inaccessible to screen readers and mobile users
  - Session timeouts that expire form data without warning
  - Jargon-heavy error messages that do not tell users what action to take

---

## Media & Entertainment

- **Key UX Patterns**
  - Content discovery via algorithmic carousels with genre/mood filters
  - Continuous playback with autoplay and queue management
  - Social sharing and reaction features embedded in content experience
  - Offline download management (episode count, storage indicator)
  - Parental controls and content rating enforcement

- **Typical Users**
  Casual consumers (binge-watchers, casual gamers), power users (playlist curators, live-stream viewers), content creators, advertisers / brand managers, children (under parental control)

- **Regulatory / Compliance**
  COPPA (US, under-13), GDPR / CCPA (tracking and ad targeting), AVMS Directive (EU video-on-demand), age gating for 18+ content, accessibility (CVAA for video content, ADA), music licensing metadata requirements

- **Design Priorities**
  1. Engagement and immersion (minimal chrome, content-forward design)
  2. Speed to content (sub-3-second time-to-first-frame for streaming)
  3. Personalisation accuracy without creepy over-targeting

- **Accessibility Considerations**
  Closed captions and audio descriptions on video content; pause/stop controls for motion-sensitive users (epilepsy); keyboard navigation of video controls; high-contrast overlaid UI on video players; reduced-motion mode for animated backgrounds

- **Common Pitfalls**
  - Autoplay with no option to opt out, causing issues for users on metered connections
  - Content recommended by engagement metrics alone, creating echo chambers that users report as bad UX
  - Captions that are available but hard to find or in an inaccessible font/size

---

## Real Estate

- **Key UX Patterns**
  - Map-first search with polygon drawing for custom area selection
  - Virtual tour and photo gallery with room-by-room navigation
  - Affordability calculator embedded in listing views
  - Saved search with push notification alerts for new listings
  - Agent contact and scheduling integrated directly on listing pages

- **Typical Users**
  First-time homebuyers, repeat buyers, property investors, renters, real estate agents / brokers, mortgage advisors, property managers

- **Regulatory / Compliance**
  Fair Housing Act (US, non-discriminatory advertising), GDPR / CCPA (user search data, lead data), State-level real estate licensing disclosure requirements, energy performance certificate display (EU), accessibility of listings for users with disabilities (ADA)

- **Design Priorities**
  1. Rich media quality (photography, virtual tour, floor plan)
  2. Information density balanced with scannability (key facts above the fold)
  3. Trust signals (verified agent badges, review scores, days-on-market)

- **Accessibility Considerations**
  Virtual tours must have keyboard-navigable hotspots; map interactions must have non-map list alternatives; mortgage calculators must be screen-reader compatible; photo galleries need descriptive alt text; contact forms must be operable without a mouse

- **Common Pitfalls**
  - Over-reliance on photos and virtual tours with no text description of property features
  - Map-only search results that exclude users who cannot interact with the map
  - Lead capture forms that interrupt browsing before the user has seen enough to be interested

---

## SaaS / B2B

- **Key UX Patterns**
  - Onboarding checklists with progress rings and quick-win tasks
  - Role-based dashboards (admin, manager, end user each see relevant KPIs)
  - In-app contextual help: tooltips, walkthrough overlays, empty-state guidance
  - Integration marketplace with one-click connect patterns
  - Usage analytics and seats management for admins

- **Typical Users**
  Individual contributors (daily tool users), team managers, IT / DevOps administrators, procurement / finance buyers evaluating ROI, C-suite exec selectively reviewing dashboards

- **Regulatory / Compliance**
  GDPR / CCPA (SaaS data processing agreements), SOC 2 Type II (audit requirements often shared with buyers), HIPAA if healthcare customers, WCAG 2.1 AA (enterprise buyers include accessibility in RFPs), ISO 27001

- **Design Priorities**
  1. Time-to-value (user must get a "first win" within the first session)
  2. Learnability without training (progressive disclosure of advanced features)
  3. Admin control without breaking end-user simplicity

- **Accessibility Considerations**
  Enterprise customers increasingly require VPAT / WCAG 2.1 AA compliance; complex data tables need proper headers and scope attributes; modal dialogs must trap focus correctly; keyboard shortcuts must not conflict with screen-reader shortcuts; provide sufficient contrast in data visualisations

- **Common Pitfalls**
  - Empty states that provide no guidance, leaving new users stranded
  - Feature overload in the main navigation, burying the 20% of features that 80% of users need
  - Admin settings that require developer knowledge, blocking non-technical admins

---

## Retail / CPG (Consumer Packaged Goods)

- **Key UX Patterns**
  - In-store mode vs. online mode with unified loyalty account
  - Product comparison tables with attribute selectors (size, flavour, variant)
  - Subscription / replenishment flows with easy skip/pause options
  - Loyalty program integration: points balance visible on PDP (Product Detail Page)
  - Augmented Reality (AR) "try before you buy" for beauty, furniture, glasses

- **Typical Users**
  Everyday grocery shoppers, brand loyalists, bargain hunters / deal-seekers, health-conscious consumers, subscription repeat buyers, impulse purchasers

- **Regulatory / Compliance**
  GDPR / CCPA (loyalty data, purchase history), FDA labelling requirements (US, food and cosmetics), EU Consumer Rights Directive, PCI-DSS for payment, WCAG 2.1 AA, California Proposition 65 (hazardous ingredient disclosure)

- **Design Priorities**
  1. Product discovery and impulse buying (promotions visible, cross-sell adjacent)
  2. Transparency in ingredients, sourcing, and sustainability claims
  3. Frictionless repeat purchase (one-click reorder, subscription management)

- **Accessibility Considerations**
  AR features must have non-AR alternatives; product images need rich alt text describing colour and texture; subscription management flows must be keyboard navigable to avoid cancellation dark patterns; nutritional tables must be accessible (not image-only PDFs)

- **Common Pitfalls**
  - Subscription cancellation flows deliberately buried behind multiple steps (dark pattern)
  - Loyalty point expiry communications hidden in terms rather than proactively surfaced in-app
  - Ingredient / allergen information only available as an image, inaccessible to screen readers

---

## Cross-Cutting UX Principles (all verticals)

These principles apply regardless of industry. Layer them on top of vertical-specific patterns.

- **Progressive disclosure**: reveal complexity only when the user signals readiness. Applicable across all 12 verticals.
- **Error prevention over error recovery**: validate input inline; prefer constraints (date pickers, dropdowns) over free text where domain allows.
- **Consistent mental models**: reuse the same navigation patterns across areas of the same product; never reinvent wayfinding within a single app.
- **Feedback latency**: every user action must produce visible feedback within 100 ms (visual), 1 s (processing indicator), or 10 s (progress communicated).
- **Mobile-first but responsive**: begin with mobile constraints; scale up to desktop — not the reverse.
- **Internationalisation readiness**: design layouts that tolerate 30–40% text expansion for translated strings; avoid icon-only affordances that do not translate culturally.
- **Meaningful empty states**: every empty list, dashboard, or result set must communicate what to do next — not just "No data found".
- **Undo over confirm**: where reversible, prefer letting the user undo an action over blocking them with a confirmation dialog.

## Quick-Reference Matrix

| Vertical | Top Compliance | Mobile First | Accessibility Priority |
|---|---|---|---|
| Healthcare | HIPAA, GDPR Art.9 | Medium | High (elderly, impaired) |
| Finance | PCI-DSS, PSD2, GDPR | High | High (visually impaired) |
| E-Commerce | GDPR, PCI-DSS | High | Medium |
| Education | FERPA, COPPA, GDPR | Medium | High (minors, disabilities) |
| Travel | GDPR, PCI-DSS | High | Medium |
| Legal | GDPR, SOC 2, eIDAS | Low | Medium |
| Manufacturing | OSHA, ISO 9001 | Medium | High (gloved use, brightness) |
| Government | Section 508, Web Accessibility Dir. | High | Critical (all publics) |
| Media | AVMS, COPPA, GDPR | High | High (captions, motion) |
| Real Estate | Fair Housing, GDPR | High | Medium |
| SaaS / B2B | GDPR, SOC 2, WCAG | Medium | High (enterprise RFPs) |
| Retail / CPG | GDPR, FDA labelling | High | Medium |

---

*Last updated: 2026-03-23. Maintained by UX-Atlas and the ux-enhancement-workflow pack. Update when new compliance requirements are identified or new verticals are requested.*
