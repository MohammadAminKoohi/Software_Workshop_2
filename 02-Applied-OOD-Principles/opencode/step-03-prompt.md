# Build invocation — Step 3 only

Continue the approved Build and implement only **Step 3 — Extract receipt
presentation** from the corrected Plan.

Current expected revision: `1f0fc23`.

Requirements:

- Add `store/receipt.py` with a focused `ReceiptPrinter` that preserves every
  existing receipt line, item spacing, numeric format, and ordering.
- Add one minimal receipt-presenter contract and require it in
  `OrderService.__init__` with no default/fallback.
- Delegate the existing receipt call and remove `OrderService._print_receipt`.
- Wire `ReceiptPrinter` in `store/main.py` and adapt only constructor/wiring
  helpers required by this approved API change.
- Add focused tests for exact simple and bundle receipt output, injected
  presenter arguments, and unchanged overall demo output/order.
- Run focused tests, all discovered tests, compilation, and smoke from the
  applied workspace; inspect/report the full scoped diff and actual metrics.
- Do not alter message formatting, payment/discount logic, notification
  inheritance, bundle inheritance, protected sources, or begin Step 4. Do not
  add Cash Payment or commit.
