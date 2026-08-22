# Affected-File and Dependency Map

| File | Planned change | Confirmed reason |
|---|---|---|
| `store/order_service.py` | Require collaborators; delegate shipping and receipt; accept order or bundle | DIP, SRP, and bundle typing |
| `store/main.py` | Assemble concrete collaborators, payment registry, and ordered discount rules | Composition root required by DIP/OCP corrections |
| `store/contracts.py` (new) | Minimal client-owned structural contracts only | DIP and ISP; no unused `load_order` operation |
| `store/pricing.py` | Add shipping policy and ordered discount rules | SRP and discount OCP |
| `store/receipt.py` (new) | Preserve receipt presentation behind a focused collaborator | SRP |
| `store/payment.py` | Replace method conditional with injected handler registry | Payment OCP |
| `store/notification.py` | Remove `SmsOnlyNotifier` false inheritance | Notifier LSP and ISP |
| `store/models.py` | Model `BundleOrder` through composition with baseline-compatible behavior | Bundle LSP |
| `store/storage.py` | No production edit planned | Existing `save_order` satisfies the minimal repository contract |
| `tests/test_characterization.py` (new) | Pin all baseline observables before production changes | Behavior-preserving safety net |
| Focused `tests/test_*.py` files (new) | One regression group for injection, shipping/receipt, payments, discounts, notifications, and bundles | Step-specific checks and small commits |

## Dependency order

```text
characterization
      |
dependency injection + composition root
      |------------|------------|
   shipping     receipt     notifier split
      |            |             |
payment registry  discount rules |
      \____________|_____________/
                   |
          bundle composition
                   |
             final checks
```

The diagram is implementation order, not a claim that payment and discount
semantics depend on shipping or receipt internals.
