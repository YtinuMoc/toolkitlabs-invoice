# toolkitlabs-invoice

Free invoice / receipt generator — fill in the browser, print or save as PDF. No account, no upload.

## Web (free)

Open in any browser:

**https://ytinumoc.github.io/toolkitlabs-invoice/**

Enter seller, buyer, line items, and tax — then **Print / Save as PDF**.

**Receipt:** https://ytinumoc.github.io/toolkitlabs-invoice/receipt.html — payment-received receipt, same print-to-PDF flow.

## Gumroad CSV batch (paid pack, EUR 9)

Gumroad exports sales CSV but not bulk invoice PDFs. Same workflow as paid converters (e.g. csv2invoice.com):

**https://ytinumoc.github.io/toolkitlabs-invoice/gumroad/**

```bash
python3 gumroad_batch.py gumroad-sample.csv -o ./invoices/ --seller-name "Your Co"
```

Buy the Gumroad batch CLI pack (one-time):

**https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=readme-gumroad-v1**

## Batch CLI (paid pack, EUR 9)

Generate dozens of invoices from a CSV:

```bash
python3 invoice_batch.py sample.csv -o ./output/
```

Buy the batch CLI pack (one-time, no subscription):

**https://buy.stripe.com/3cI4gA8X44HGgbI6JT5Ne0j?client_reference_id=npm-invoice-batch**

Each row becomes a standalone HTML file you can print to PDF.

## Why this exists

Freelancers and shopkeepers need a simple bill every week. Hosted invoicing tools charge monthly for what a static page does locally. This is CC0 — use it anywhere.

CC0 1.0 · [Toolkit Labs](https://toolkitlabs.org/)
