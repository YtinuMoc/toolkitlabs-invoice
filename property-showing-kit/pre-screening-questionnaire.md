# Pre-Screening Questionnaire

Clone of Orion trsoxh ($39 Gumroad) module 1.

## Copy-paste questions (email / SMS / platform DM)

**Block A — timeline & occupants**
1. Desired move-in date?
2. Number of occupants (names + relationship)?
3. Any co-signer if income is borderline?

**Block B — financial fit**
4. Combined gross monthly income? (Must meet 3× rent = $____)
5. Employment status + employer name (verify if needed)?
6. Current address + reason for moving?

**Block C — rental history**
7. Evictions or broken leases in last 3 years?
8. Landlord reference contact (optional before showing)?

**Block D — pets & vehicles**
9. Pets (type, weight, count)? Policy: ____
10. Vehicles needing parking? Spaces included: ____

**Block E — showing logistics**
11. Can you attend a 15-minute showing at [ADDRESS] on [DATES]?
12. Government-issued ID required at showing (policy)?

## AI qualification prompt

```plaintext
Inquiry: "[PASTE]"
Property: [BEDS]BR, $[RENT]/mo, available [DATE], pets [POLICY], parking [N], income min $[3×RENT].

Task: (1) Score lead 1–5 on qualification likelihood. (2) List red flags. (3) Draft a reply with only the questions still missing from Blocks A–E. (4) If score ≤2, draft a polite decline without showing. Fair-housing compliant.
```

## Disqualify without a showing (template)

> Thanks for your interest in [ADDRESS]. Based on [specific requirement], this unit may not be the right fit. I recommend searching for [alternative suggestion]. Wishing you luck in your search.
