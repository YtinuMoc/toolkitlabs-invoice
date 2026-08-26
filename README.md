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

## Generic batch CLI (EUR 9)

```bash
python3 invoice_batch.py sample.csv -o ./output/
```

**https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=npm-invoice-batch**

CC0 1.0 · [Toolkit Labs](https://toolkitlabs.org/)
