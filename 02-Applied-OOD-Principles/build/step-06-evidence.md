# Step 6 Evidence — Narrow Notification Channels

## Attribution and traceability

This step was implemented and reviewed by the coordinator after OpenCode was
stopped at the user's request. No OpenCode completion is claimed.

| Plan requirement | Accepted implementation |
|---|---|
| Remove false subtype | `SmsOnlyNotifier` no longer inherits `NotificationService` |
| Advertise supported behavior only | SMS-only object exposes `send_sms`; no email or push methods |
| Retain narrow checkout dependencies | Existing `EmailSender` and `SmsSender` contracts remain separate |
| Preserve production behavior | Composition root continues to use `NotificationService` for both channels |
| Record intentional API correction | Characterization now asserts absence instead of `NotImplementedError` |

## Measurements before this evidence document

- Production file modified: `notification.py`, 3 insertions, 6 deletions
- Existing test file modified: 4 insertions, 8 deletions
- Focused test file added: `test_notification_channels.py`, 58 lines, 5 tests
- Full suite: 68 tests

## Verification

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_notification_channels.py -v` | 0 | 5/5 passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | 0 | 68/68 passed |
| `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-step6-review-pycache python3 -m compileall -q store tests` | 0 | No output |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | 0 | Email/SMS and complete demo output preserved |
| `git diff --quiet HEAD -- store 01-Without-OOD-Principles` | 0 | Protected sources untouched |

The removal of unsupported methods is the one approved observable API
correction; no production demo caller used those operations.
