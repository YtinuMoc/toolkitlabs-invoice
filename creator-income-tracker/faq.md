# FAQ (clone of PattyBun rauxja Gumroad checkout)

Source: [pattybun.gumroad.com/l/rauxja](https://pattybun.gumroad.com/l/rauxja) ($14.99 checkout page).

**Q: Do I need any special software?**  
A: No. Our clone ships CSV + Python CLI (stdlib only). PattyBun's original works free in Google Sheets and opens in Excel.

**Q: Does it work with other platforms besides Gumroad, Etsy, Shopify, and Payhip?**  
A: Yes — use platform `other` and set a manual fee in notes as `fee=12.34`.

**Q: Is this updated automatically from my Gumroad/Etsy accounts?**  
A: No — you enter sales manually. The tracker does all fee math from there (same as PattyBun).

**Q: Can I add more products or platforms?**  
A: Yes — append rows to the revenue log CSV. No row cap in the CLI.

**Q: Does it include VAT or international tax?**  
A: The tax tab uses a 25% US set-aside default. Edit `TAX_SET_ASIDE_PCT` in `creator_dashboard.py` for your jurisdiction.
