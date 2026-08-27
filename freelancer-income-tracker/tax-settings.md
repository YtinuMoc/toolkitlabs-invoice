# Tax settings — PattyBun Settings tab clone

Open `freelancer_dashboard.py` and edit these constants (60-second setup):

| Setting | Default | PattyBun equivalent |
|---------|---------|---------------------|
| `FEDERAL_RATE` | 0.22 (22%) | Federal income tax bracket |
| `STATE_RATE` | 0.05 (5%) | State income tax |
| `SE_TAX_RATE` | 0.153 (15.3%) | Self-employment tax |
| `IRS_MILEAGE_RATE` | 0.67 | IRS standard mileage rate |

Everything recalculates on the next CLI run when you change rates.

Multi-currency: log amounts in your primary currency (USD, CAD, GBP, EUR, AUD). Rates apply to logged numbers as-is.
