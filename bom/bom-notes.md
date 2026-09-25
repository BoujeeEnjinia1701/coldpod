# BOM notes

- Item numbers match the exploded view (`media/exploded.png`), Table 1 of the design precis (CPD-PRC-001) and drawing CPD-DWG-001. Item 16 is not modelled.
- Every line is priced. Prices are indicative estimates in USD for single-unit prototype quantities, by supplier type; none is a supplier quote.
- Total: $295 against `budget_usd: 300` (raised from $250 by Amish's decision of 2026-09-25, CPD-DDR-001 D10). The margin is $5, so a supplier quote above estimate on the VIPs (item 4) or the thermosiphon (item 7) would put the BOM over budget. The total is checked by `docs/04-calcs/sizing.py` (CPD-CAL-001, L2).
- Changes at TRL 3: item 7 now covers the evaporator can and a charged loop thermosiphon sized in CPD-CAL-001 ($12 to $28); item 8 is the lower-current TEC1-12703 class ($6 to $5); item 12 names a filtered buck driver; item 6 uses a printed rack.
- Not in the BOM (proposed at TRL 3, awaiting Amish; see `docs/REVIEW.md`): a lid cold plate that seats on the can rim (about $5) and a second hardware cut-out on the liner (about $3).
- The payload (insulin pens or vaccines) is not supplied and not costed.
- The SwapCell pack is not used by ColdPod, so no shared SwapCell cost applies.
