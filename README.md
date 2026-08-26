# toolkitlabs-invoice

Free invoice / receipt generator — fill in the browser, print or save as PDF. No account, no upload.

Clone of [csv2invoice.com](https://www.csv2invoice.com/) workflows (they charge €10/month). **EUR 9 one-time** per platform batch CLI pack.

## Web (free)

**https://ytinumoc.github.io/toolkitlabs-invoice/**

Enter seller, buyer, line items, and tax — then **Print / Save as PDF**.

**Receipt:** https://ytinumoc.github.io/toolkitlabs-invoice/receipt.html

## Platform CSV batch packs (EUR 9 one-time)

Paid converters like csv2invoice.com ship the same export → bulk invoice shape. Pick your processor:

| Platform | Landing | CLI |
|----------|---------|-----|
| Stripe | https://ytinumoc.github.io/toolkitlabs-invoice/stripe/ | `python3 stripe_batch.py stripe-sample.csv -o ./invoices/` |
| PayPal | https://ytinumoc.github.io/toolkitlabs-invoice/paypal/ | `python3 paypal_batch.py paypal-sample.csv -o ./invoices/` |
| Gumroad | https://ytinumoc.github.io/toolkitlabs-invoice/gumroad/ | `python3 gumroad_batch.py gumroad-sample.csv -o ./invoices/` |
| Lemon Squeezy | https://ytinumoc.github.io/toolkitlabs-invoice/lemon/ | `python3 lemon_batch.py lemon-sample.csv -o ./invoices/` |
| ThriveCart | https://ytinumoc.github.io/toolkitlabs-invoice/thrivecart/ | `python3 thrivecart_batch.py thrivecart-sample.csv -o ./invoices/` |
| Shopify | https://ytinumoc.github.io/toolkitlabs-invoice/shopify/ | `python3 shopify_batch.py shopify-sample.csv -o ./invoices/` |

Buy any platform batch CLI pack (one-time, no subscription):

**https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=readme-all-platforms-v2-run9**

Add `--seller-name "Your Co"` (and address/tax if needed). Each row becomes HTML you print to PDF locally — your CSV never leaves your machine.

## Seller ledger — Gumroad + Stripe CSV merge (EUR 9 one-time)

Clone of [SellerLedger on Gumroad ($17)](https://nexusai82.gumroad.com/l/kfyuh) — merge both CSV exports into one profit ledger with fee rows and quarterly set-aside estimate.

**Who it's for:** solo Gumroad/Stripe sellers, freelancers who want organized income/expense records without accounting software, anyone who exports CSVs but can't see net profit after fees. **30-day money-back guarantee** — email support@toolkitlabs.org with your Stripe receipt (clone of Orion Gumroad refund policy).

**https://ytinumoc.github.io/toolkitlabs-invoice/ledger/** — [3-step setup guide](https://ytinumoc.github.io/toolkitlabs-invoice/ledger/#setup) (clone of Orion Gumroad PDF promise)

Free sample CSVs (clone of Orion Gumroad pre-checkout delivery): [gumroad-sample.csv](https://ytinumoc.github.io/toolkitlabs-invoice/ledger/gumroad-sample.csv) · [stripe-sample.csv](https://ytinumoc.github.io/toolkitlabs-invoice/ledger/stripe-sample.csv)

```bash
python3 seller_ledger.py gumroad-sample.csv stripe-sample.csv -o ledger.csv --tax-rate 0.28
```

**https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=readme-seller-ledger-v2-run15**

Walkthroughs (free, dev.to):

- [Ledger walkthrough](https://dev.to/toolkitlabs/gumroad-stripe-seller-ledger-from-csv-real-net-profit-without-a-17-spreadsheet-46ii)
- [Tax tracking](https://dev.to/toolkitlabs/solo-gumroad-seller-tax-tracking-from-csv-income-fees-quarterly-set-aside-without-a-17-sheet-4fhj)
- [Product 4 build log](https://dev.to/toolkitlabs/product-4-on-my-gumroad-stack-a-17-income-tracker-and-the-eur-9-csv-ledger-i-use-instead-1gb6)
- [5 tools stack](https://dev.to/toolkitlabs/5-tools-every-gumroad-seller-actually-needs-real-costs-no-referral-hype-iij)
- [Free tools list](https://dev.to/toolkitlabs/best-free-tools-for-solo-gumroad-sellers-in-2026-tested-ranked-real-limits-1f5d)
- [Why sellers feel broke](https://dev.to/toolkitlabs/the-real-reason-gumroad-sellers-feel-broke-after-a-good-month-its-almost-never-the-fees-37e6)
- [5 templates](https://dev.to/toolkitlabs/5-templates-every-gumroad-seller-needs-and-why-most-skip-them-until-quarter-end-2ngo)
- [Honest build log](https://dev.to/toolkitlabs/shipping-a-gumroad-seller-ledger-cli-in-public-honest-numbers-not-eu10kmonth-hype-5g9d)
- [4-product launch log](https://dev.to/toolkitlabs/i-shipped-4-digital-seller-tools-in-2-weeks-heres-exactly-what-each-one-does-and-the-honest-g20) (clone of Orion4217862)

## Generic batch CLI (EUR 9)

```bash
python3 invoice_batch.py sample.csv -o ./output/
```

**https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=npm-invoice-batch**

CC0 1.0 · [Toolkit Labs](https://toolkitlabs.org/)
