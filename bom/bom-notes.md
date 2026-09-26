# BOM notes

- Item numbers match the exploded view (`media/exploded.png`), Table 1 of the design precis (CPD-PRC-001) and drawing CPD-DWG-001. Item 16 is not modelled.
- Every line is priced. Prices are indicative estimates in USD for single-unit prototype quantities, by supplier type; none is a supplier quote.
- Total: $303 against `budget_usd: 300` (raised from $250 by Amish's decision of 2026-09-25, CPD-DDR-001 D10, and kept at $300 by CPD-DDR-002). The BOM is $3 over budget; the options are awaiting Amish (CPD-DDR-002, N3). The VIPs (item 4) and the thermosiphon (item 7) remain the largest price uncertainties. The total is checked by `docs/04-calcs/sizing.py` (CPD-CAL-001, L2).
- Changes at TRL 3: item 7 now covers the evaporator can and a charged loop thermosiphon sized in CPD-CAL-001 ($12 to $28); item 8 is the lower-current TEC1-12703 class ($6 to $5); item 12 names a filtered buck driver; item 6 uses a printed rack.
- Changes from the recommendations Amish accepted on 2026-09-25 (CPD-DDR-002): item 2 adds the 1.5 mm aluminium lid cold plate ($8 to $12, with $1 less filament for the 5 mm cap); item 14 adds the 3 °C liner cut-out ($10 to $13); item 12 uses a buck-boost Peltier driver ($22 to $26); items 1 and 10 use thinner printed walls ($18 to $17 and $8 to $6). Total $295 to $303.
- The payload (insulin pens or vaccines) is not supplied and not costed.
- The SwapCell pack is not used by ColdPod, so no shared SwapCell cost applies.
