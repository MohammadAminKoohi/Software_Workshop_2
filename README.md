# گزارش آزمایشگاه مهندسی نرم‌افزار ۲ — OpenCode و بازآرایی SOLID

## ۱. هدف و اعضای تیم

هدف این آزمایش، مقایسهٔ کنترل‌شدهٔ هزینهٔ افزودن قابلیت جدید به طراحی اولیه با
فرایند شناسایی و اصلاح موارد واقعی نقض اصول SOLID است. مراحل کار به‌صورت
تدریجی انجام شد: ثبت خط مبنا، افزودن Cash Payment بدون بهبود معماری، تحلیل
SOLID، طراحی و آزمون Skill، تولید و بازبینی Plan، اجرای بازآرایی تأییدشده و
ارزیابی صادقانهٔ نتیجهٔ OpenCode.

| نقش | عضو | مسئولیت ثبت‌شده |
|---|---|---|
| مالک مخزن و هماهنگ‌کننده | [محمدامین کوهی (Mohammad Amin Koohi)](https://github.com/MohammadAminKoohi) | تعیین محدوده، تأییدها، اصلاحات دستی، پیاده‌سازی بخش‌های واگذارشده، آزمون نهایی و تکمیل گزارش |
| هم‌تیمی | [عرشیا ایزدی (Arshia Izadi)](https://github.com/arshiaizd) | مشارکت در گردش‌کار GitHub و ادغام واقعی PRهای #44 و #45 |
| عامل OpenCode | OpenCode 1.18.3 با مدل `opencode/big-pickle` | تحلیل و پیاده‌سازی Cash، اجرای آزمون‌های Skill، تولید Plan و اجرای مراحل ۰ تا ۳ Build و شروع مرحلهٔ ۴ |
| دستیار کدنویسی هوشمند | Codex | بازبینی شواهد، اصلاح Skill و Plan، تکمیل دستی پس از توقف OpenCode، آزمون و مستندسازی |

GitHub ادغام واقعی PRهای #44 و #45 را توسط عرشیا ایزدی ثبت کرده است؛ با این
حال، برای PR #45 هیچ review رسمی ثبت‌شده‌ای وجود ندارد. در این گزارش «ادغام
توسط هم‌تیمی» به‌اشتباه «review رسمی» نامیده نمی‌شود و هیچ فعالیت ساختگی به
اعضای تیم نسبت داده نشده است.

## ۲. راه‌اندازی پروژه و OpenCode و ثبت خط مبنا

پروژهٔ اولیه یک برنامهٔ Python با هفت فایل در `store/`، تعداد ۱۰ کلاس صریح،
۱۹ تابع/متد صریح و ۲۱۴ خط فیزیکی کد بود. کلاس `OrderService` وابستگی‌های
قیمت‌گذاری، پرداخت، اعلان و ذخیره‌سازی را مستقیماً می‌ساخت و کل فرایند checkout
را هماهنگ می‌کرد. پروژهٔ اولیه فایل وابستگی، پیکربندی package، اسکریپت build یا
مجموعه‌آزمون ریشه نداشت.

گزارش کامل خط مبنا در
[`docs/baseline-verification.md`](docs/baseline-verification.md) نگهداری شده است.

| مورد | نتیجه و مدرک |
|---|---|
| commit پروژهٔ اولیه | [`c34b3aa`](https://github.com/MohammadAminKoohi/Software_Workshop_2/commit/c34b3aa95f7ca84e3b01b36c6ff48bd08096002b) |
| commit نقطهٔ کنترل | [`ace844f`](https://github.com/MohammadAminKoohi/Software_Workshop_2/commit/ace844f31cb5e39c2e0fc48faecabe07d60f30f0) |
| tag خط مبنا | `baseline-initial` با شیء annotated برابر `57ad6260c3990934e6ccd67d6183882cc289654e` |
| مقصد tag | `ace844f31cb5e39c2e0fc48faecabe07d60f30f0` |
| نسخهٔ ابزارها | Python 3.13.2 و Git 2.39.5 (Apple Git-154) |
| bytecode compilation | خروج موفق با کد ۰ |
| کشف آزمون در ریشه | خروج با کد ۵؛ تعداد آزمون صفر و پیام `NO TESTS RAN` |
| اجرای demo | خروج با کد ۰؛ مجموع سفارش ساده `$819.99` و bundle برابر `$5.00` |

نتیجهٔ صفر آزمون یک محدودیت واقعی پروژهٔ اولیه است و به‌عنوان «موفقیت آزمون»
گزارش نشده است. سفارش bundle شامل سفارش‌هایی با مجموع `$1194.99` است، اما به
علت وراثت نامناسب و `items` خالی، `subtotal` آن `$0.00` و مبلغ نهایی آن تنها
هزینهٔ ارسال `$5.00` است.

قالب‌های Issue و PR در `.github/` و Skill محلی پروژه در
`.opencode/skills/solid-refactoring/` ثبت شده‌اند. هیچ secret، وابستگی تولیدشده
یا framework آزمون خارجی به پروژه اضافه نشده است.

## ۳. آزمایش افزودن Cash Payment به طراحی اولیه

نسخهٔ موردنیاز آزمایش در پوشهٔ دقیق
[`01-Without-OOD-Principles/`](01-Without-OOD-Principles/) نگهداری می‌شود. در
این مرحله Cash Payment عمداً پیش از هرگونه اصلاح SOLID و در همان معماری
شرطی اولیه اضافه شد.

OpenCode ابتدا فقط تحلیل کرد، `PaymentProcessor.process` را تنها محل ضروری
تغییر production تشخیص داد، فایل‌های اختیاری آزمون/demo را جدا کرد و پیش از
پیاده‌سازی در دروازهٔ تأیید متوقف شد. قرارداد تأییدشده چنین بود:

- selector برابر `payment_method == "cash"`؛
- خروجی کنسول `[payment] Receiving cash {amount:.2f}`؛
- token رسید `paid_by_cash:{amount:.2f}`؛
- استفاده از `unittest` داخلی Python؛
- ممنوعیت Strategy، Factory، Interface، DI، تغییر demo یا بازآرایی نامرتبط.

OpenCode در Build همین محدوده را پیاده‌سازی کرد و یک آزمون خود را که خروجی
کنسول را capture نمی‌کرد اصلاح کرد. بازبینی انسانی به اصلاح production دیگری
نیاز نداشت و `store/` ریشه بدون تغییر باقی ماند.

شواهد این مرحله:

- [prompt تحلیل](01-Without-OOD-Principles/opencode/cash-payment-analysis-prompt.md)
  و [خروجی کامل](01-Without-OOD-Principles/opencode/cash-payment-analysis-output.md)؛
- [بازبینی و تأیید انسانی](01-Without-OOD-Principles/analysis/cash-payment-analysis-review.md)؛
- [prompt پیاده‌سازی](01-Without-OOD-Principles/opencode/cash-payment-implementation-prompt.md)
  و [خروجی کامل](01-Without-OOD-Principles/opencode/cash-payment-implementation-output.md)؛
- [اندازه‌گیری تغییرات](01-Without-OOD-Principles/analysis/cash-payment-change-report.md)؛
- [Issue #29](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/29)
  و PRهای ادغام‌شدهٔ [#39](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/39)
  و [#40](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/40).

## ۴. جدول تغییرات طراحی اولیه و دلیل ضرورت آن‌ها

مقایسه بین نسخهٔ ذخیره‌شدهٔ پیش از Build در `469cbbb` و نتیجهٔ کامل آزمایش
انجام شده است.

| فایل/کلاس | نوع تغییر | دلیل ضرورت |
|---|---|---|
| `01-Without-OOD-Principles/store/payment.py` / `PaymentProcessor.process` | تغییر یک متد موجود و افزودن یک شرط `elif` و ۴ خط production | قابلیت Cash باید در همان dispatcher رشته‌ای و معماری ضعیف موجود اضافه می‌شد. |
| `tests/test_payment.py` / `CashPaymentTest` | افزودن کلاس آزمون | پیام دقیق کنسول و token رسید Cash را تثبیت می‌کند. |
| `tests/test_payment.py` / `ExistingPaymentRegressionTest` | افزودن کلاس آزمون | رفتار credit card، PayPal و Bitcoin را در برابر regression حفظ می‌کند. |
| `tests/test_payment.py` / `UnknownPaymentMethodTest` | افزودن کلاس آزمون | ادامهٔ رخ دادن `ValueError` برای selector ناشناخته را ثابت می‌کند. |

| معیار | نتیجه |
|---|---:|
| فایل‌های تغییرکرده | ۲ |
| فایل production اصلاح‌شده | ۱ |
| کلاس موجود اصلاح‌شده | ۱ |
| متد موجود اصلاح‌شده | ۱ |
| شرط افزوده‌شده | ۱ |
| کلاس production جدید | ۰ |
| کلاس آزمون جدید | ۳ |
| تغییر وابستگی production | ۰ |
| خطوط افزوده/حذف‌شدهٔ کل | ۹۰ / ۰ |
| خطوط افزوده/حذف‌شدهٔ production | ۴ / ۰ |

این نتیجه مدرک تجربی نقض OCP است: افزودن یک روش پرداخت جدید، تغییر مستقیم کد
پایدار dispatch را الزامی کرد.

## ۵. تحلیل اصول SOLID در طراحی اولیه

تحلیل خط‌به‌خط در [`docs/solid-analysis.md`](docs/solid-analysis.md)،
[Issue #31](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/31)
و [PR #41](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/41)
نگهداری می‌شود.

| اصل | رعایت شده؟ | محل دقیق | نتیجه |
|---|---|---|---|
| SRP | خیر | `store/order_service.py`، متدهای `process_order` و `_print_receipt` | orchestration سفارش هم‌زمان validation، سیاست ارسال، پیام اعلان و نمایش رسید را بر عهده داشت؛ این‌ها دلایل مستقل تغییر هستند. |
| OCP | خیر | `PaymentProcessor.process` و `DiscountCalculator.calculate` | هر نوع پرداخت یا تخفیف جدید نیازمند ویرایش زنجیره‌های شرطی پایدار بود؛ آزمایش Cash این هزینه را نشان داد. |
| LSP | خیر | `BundleOrder` و `SmsOnlyNotifier` | bundle مقادیر موروثی ناسازگار با سفارش‌های درون خود داشت؛ notifier پیامکی عملیات base را با `NotImplementedError` رد می‌کرد. |
| ISP | خیر | `NotificationService` / `SmsOnlyNotifier` | پیاده‌سازی فقط-SMS مجبور به ارائهٔ email و push پشتیبانی‌نشده بود. |
| DIP | خیر | importها و `OrderService.__init__` | workflow سطح‌بالا concrete collaboratorها را import و ایجاد می‌کرد و به رفتار انتزاعی کوچک وابسته نبود. |

مواردی که آگاهانه نقض SOLID تلقی نشدند شامل فیلدهای `Customer`، تفاوت نام
`MySqlDatabase` با ذخیره‌سازی dictionary و نبود interface صریح برای همهٔ
کلاس‌های Python هستند؛ هیچ smell عمومی بدون شاهد رفتاری به‌عنوان نقض گزارش
نشده است.

## ۶. علت نقض، روش اصلاح و دلیل انتخاب راهکار

| اصل | علت نقض | اصلاح اعمال‌شده | دلیل انتخاب |
|---|---|---|---|
| SRP | سیاست ارسال و قالب‌بندی رسید در orchestrator قرار داشت. | `ShippingCalculator` و `ReceiptPrinter` استخراج و inject شدند. | دلایل واقعی تغییر جدا شدند، بدون اینکه هر خط به کلاس مستقل یا framework جدید تبدیل شود. |
| OCP | روش‌های پرداخت و قوانین تخفیف در شرط‌های متوالی hard-code شده بودند. | registry قابل inject برای handlerهای پرداخت و فهرست مرتب ruleهای تخفیف ایجاد شد. | variant آزمایشی جدید بدون ویرایش الگوریتم پایدار اضافه می‌شود و priority/rounding/output حفظ می‌گردد. |
| LSP — Bundle | `BundleOrder(Order)` شامل سفارش‌ها بود ولی رفتار scalar آن از `items` خالی ارث می‌رسید. | وراثت با composition جایگزین و رفتار فعلی `$5.00` حفظ شد. | رابطهٔ نوعی صادقانه شد، بدون اختراع قانون جدید برای تجمیع و قیمت‌گذاری bundle. |
| LSP/ISP — Notifier | `SmsOnlyNotifier` عملیات email/push را به ارث می‌برد اما رد می‌کرد. | به پیاده‌سازی مستقل SMS تبدیل و قراردادهای email/SMS جدا شدند. | هر client فقط عملیات پشتیبانی‌شده را می‌بیند و subtype ناقص حذف می‌شود. |
| DIP | `OrderService` concrete dependencyها را انتخاب و ایجاد می‌کرد. | قراردادهای structural کوچک از constructor دریافت و `main.py` به composition root تبدیل شد. | workflow سطح‌بالا به رفتار موردنیاز وابسته شد و انتخاب concrete در مرز برنامه قرار گرفت. |

Cash Payment در نسخهٔ SOLID، تغییر قیمت bundle، framework validation، DI
container، plugin framework، سلسله‌مراتب base-class گسترده و تغییر نام
`MySqlDatabase` خارج از محدوده بودند و اجرا نشدند.

## ۷. طراحی و آزمون Skill اصول SOLID

Skill نهایی پروژه در
[`solid-refactoring`](.opencode/skills/solid-refactoring/SKILL.md) قرار دارد.
طراحی و چهار اجرای اصلاحی آن در
[`docs/opencode/solid-skill/README.md`](docs/opencode/solid-skill/README.md)،
[Issue #32](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/32)
و [PR #42](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/42)
ثبت شده است.

### هدف Skill

Skill مانع آن می‌شود که smellهای عمومی بدون مدرک به‌عنوان نقض SOLID گزارش
شوند، پیش از شناخت رفتار redesign گسترده رخ دهد یا Agent قبل از تأیید کاربر
فایل‌ها را تغییر دهد.

### اطلاعاتی که در اختیار Agent قرار می‌گیرد

ورودی‌های اجباری شامل scope، موارد خارج از scope، revision، وضعیت repository،
callerها، implementationها، آزمون‌ها، رفتار مشاهده‌شده، mode و وضعیت تأیید
است. Skill همچنین قواعد مدرک برای هر اصل، نحوهٔ بیان uncertainty، probeهای
بدون side effect، approval gate، workflow تدریجی Build و قالب خروجی دقیق را
تعریف می‌کند.

### دلیل ساختار انتخاب‌شده

- هر ادعا باید فایل، کلاس/متد و شاهد دقیق داشته باشد.
- completion guard مانع پایان زودهنگام بدون جدول، پیشنهاد، tradeoff و درخواست
  تأیید می‌شود.
- proposal check از اصلاحات ظاهری مانند جابه‌جایی صرف شرط یا نگه‌داشتن default
  concrete مخفی جلوگیری می‌کند.
- approval gate تشخیص را از اجازهٔ ویرایش جدا می‌کند.
- Build فقط پس از تأیید، به‌صورت تدریجی و همراه با diff و آزمون focused/full
  مجاز است.

### نتیجهٔ آزمون Skill

`opencode debug skill` کشف Skill را تأیید کرد. چهار اجرای Plan-mode بدون
ویرایش مجاز source انجام شد:

| نسخه | مشاهده | اصلاح |
|---|---|---|
| 0.1 | source را بررسی کرد ولی پاسخ نهایی اجباری را نداد. | completion guard و probe budget افزوده شد. |
| 0.2 | DIP را جا انداخت، `__pycache__` ایجاد کرد و حذف خطرناک/اعداد حدسی پیشنهاد داد. | قواعد safe-probe، بررسی همهٔ اصول، dead-code و ادعای عددی افزوده شد. |
| 0.3 | کامل و بدون side effect بود، اما برای تخفیف راهکار غیرقابل‌گسترش و برای DIP راهکار ناقص داد. | کنترل اعتبار پیشنهاد و tradeoff تقویت شد. |
| 1.0 | جدول شواهد، false positiveها، پیشنهادهای محدود، approval gate و وضعیت یکسان قبل/بعد را کامل ارائه داد. | با یک اصلاح دستی دربارهٔ مبلغ تقریبی و بی‌مدرک bundle پذیرفته شد. |

[Prompt پذیرش](docs/opencode/solid-skill/acceptance-test-prompt.md) و
[خروجی پذیرش](docs/opencode/solid-skill/acceptance-test-output.md) به‌صورت کامل
نگهداری شده‌اند. در این Task هیچ بازآرایی production انجام نشد.

## ۸. Plan اولیهٔ OpenCode، بازبینی و اصلاح آن

OpenCode 1.18.3 در Plan mode و session
`ses_fd4fd85bfffepTQyqsyt0U4c3F` با
[prompt دقیق Plan](02-Applied-OOD-Principles/opencode/plan-prompt.md) اجرا شد.
[خروجی اولیه](02-Applied-OOD-Principles/opencode/original-plan-output.md) پیش
از بازبینی نگهداری شد.

| اشکال Plan اولیه | اصلاح دستی | دلیل |
|---|---|---|
| DIP در نگاشت violation به step نبود. | DIP به مراحل injection و composition root متصل شد. | همهٔ مراحل باید به نقض تأییدشده قابل‌ردیابی باشند. |
| یک smoke command در ریشه اجرا شد ولی به workspace applied نسبت داده شد. | فقط به‌عنوان مدرک baseline نگه داشته و cwd آینده صریح شد. | محل اجرای command باید دقیق باشد. |
| تعداد آزمون آینده تخمین زده شد. | تخمین حذف و ثبت تعداد مشاهده‌شده الزامی شد. | اندازه‌گیری نباید اختراع شود. |
| قرارداد repository شامل `load_order` استفاده‌نشده بود. | فقط `save_order` موردنیاز client حفظ شد. | از ایجاد نقض جدید ISP جلوگیری می‌شود. |
| ساخت پیام یک‌خطی هم استخراج شده بود. | در orchestrator باقی ماند؛ فقط shipping و receipt استخراج شدند. | دلیل تغییر مستقل برای abstraction جدید وجود نداشت. |
| registry/rule می‌توانست پشت default مخفی بماند. | collectionهای constructor-supplied و wiring در composition root اجباری شد. | default مخفی اصلاح DIP/OCP را ناقص می‌کرد. |
| پیشنهادهای bundle یا LSP را حل نمی‌کردند یا pricing را تغییر می‌دادند. | composition با حفظ صفرها و مبلغ `$5.00` انتخاب شد. | رابطهٔ نوع اصلاح شد بدون تغییر business rule. |
| Cash برای آزمون extension پیشنهاد شده بود. | variant مصنوعی فقط در test جایگزین شد و Cash حذف شد. | Cash متعلق به آزمایش طراحی اولیه بود. |

[بازبینی کامل](02-Applied-OOD-Principles/planning/review-notes.md)،
[Plan اصلاح‌شده](02-Applied-OOD-Principles/planning/corrected-plan.md)،
[نقشهٔ فایل‌ها](02-Applied-OOD-Principles/planning/affected-files.md)،
[ریسک‌ها](02-Applied-OOD-Principles/planning/risk-register.md) و
[برنامهٔ آزمون](02-Applied-OOD-Principles/planning/test-plan.md) موجود است.
مالک مخزن مراحل اصلاح‌شدهٔ ۰ تا ۸ را با ادغام
[PR #43](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/43)
در commit `db4e8450763aeadc20ab987cc423c48c8470f43c` تأیید کرد. GitHub برای آن
PR review رسمی ثبت نکرده است؛ این merge فقط تصمیم تأیید مالک محسوب می‌شود.

## ۹. اجرای Build و بازآرایی در طراحی اصلاح‌شده

[Prompt دقیق Build](02-Applied-OOD-Principles/opencode/build-prompt.md) فقط
اجرای Plan اصلاح‌شده در
[`02-Applied-OOD-Principles/`](02-Applied-OOD-Principles/) را مجاز می‌کرد.

| مرحله | نتیجه | commit | انتساب واقعی |
|---:|---|---|---|
| ۰ | افزودن ۲۶ characterization test | `ff28085` | OpenCode؛ بازبینی و اصلاح انتظارها توسط هماهنگ‌کننده |
| ۱ | inject کردن dependencyهای کوچک checkout | `9ea62b0` | OpenCode؛ بازبینی هماهنگ‌کننده |
| ۲ | استخراج shipping calculation | `1f0fc23` | OpenCode؛ اصلاح syntax آزمون DI و import گمشده |
| ۳ | استخراج receipt presentation | `8b3f2ba` | OpenCode؛ اصلاح duplicate discovery، قرارداد fake، فاصله‌ها و caller |
| ۴ | جایگزینی شرط پرداخت با handler dispatch | `7ff1ff2` | OpenCode فقط import ناقص را آغاز کرد؛ هماهنگ‌کننده مرحله را کامل کرد |
| ۵ | ruleهای مرتب و inject‌شدهٔ تخفیف | `49a7cbf` | پیاده‌سازی دستی پس از دستور کاربر برای توقف OpenCode |
| ۶ | جداسازی قراردادهای notification | `efb353d` | پیاده‌سازی دستی پس از توقف OpenCode |
| ۷ | جایگزینی وراثت bundle با composition | `040d774` | پیاده‌سازی دستی پس از توقف OpenCode |
| مدرک نهایی | ثبت verification و checkpoint | `88a17f0` | هماهنگ‌کننده |

OpenCode مراحل ۰ تا ۳ را در session
`ses_fd4dceb8bffeRJxcTrv1Y9YGMG` کامل کرد و مرحلهٔ ۴ را ناقص آغاز کرد. کاربر
سپس صریحاً دستور توقف OpenCode داد؛ بنابراین مراحل بعدی به‌درستی به کار دستی
نسبت داده شده‌اند و **ادعا نمی‌شود که OpenCode کل Plan را اجرا کرده است**.

[جدول ردیابی Plan](02-Applied-OOD-Principles/build/plan-traceability.md)،
[اصلاحات دستی](02-Applied-OOD-Principles/build/manual-corrections.md) و مدارک
هر مرحله در `build/step-00-evidence.md` تا `step-07-evidence.md` موجود است.

اندازه‌گیری نهایی production:

| معیار | نتیجه |
|---|---:|
| فایل production تغییرکرده | ۸ |
| فایل موجود اصلاح‌شده | ۶ |
| فایل جدید | ۲ |
| خطوط افزوده | ۲۴۲ |
| خطوط حذف‌شده | ۶۶ |
| ماژول آزمون focused | ۸ |
| تعداد آزمون نهایی | ۷۴ |

tag annotated با نام `solid-refactored` دارای شیء
`76be03a3a3cbb4f2917fe39e8770b1958ae6e84a` و مقصد
`88a17f0e2389dd74fb21bbf1b21054386ce1dce9` است.
[Issue #34](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/34)
با [PR #44](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/44)
بسته شد. عرشیا ایزدی این PR را واقعاً merge کرد، اما review رسمی ثبت‌شده‌ای
وجود ندارد و چنین reviewای ادعا نمی‌شود.

## ۱۰. ارزیابی عملکرد OpenCode

### ۱۰.۱. OpenCode چه بخش‌هایی را درست تحلیل کرد؟

- جریان string-based پرداخت را درست ردیابی کرد و برای Cash فقط یک محل ضروری
  production را مشخص کرد.
- معماری ضعیف مرحلهٔ اول را آگاهانه حفظ کرد و پیش از Build برای تأیید متوقف شد.
- در آزمون Skill شواهد واقعی SRP، OCP، LSP، ISP و DIP را یافت و false
  positiveهای عمومی را رد کرد.
- Plan را با characterization test آغاز کرد، مبالغ `$819.99` و `$5.00`،
  priority تخفیف، متن خطا و output پرداخت را حفظ کرد.
- مراحل ۰ تا ۳ Build پایهٔ regression و مرزهای dependency، shipping و receipt
  مناسبی ایجاد کردند.

### ۱۰.۲. کدام پاسخ‌های Agent نیازمند اصلاح بودند؟

- Skill نسخهٔ ۰.۱ پاسخ اجباری نهایی را نداد؛ نسخهٔ ۰.۲ DIP را جا انداخت و
  bytecode تولید کرد؛ نسخهٔ ۰.۳ پیشنهاد ناقص OCP/DIP داشت.
- پاسخ پذیرفته‌شدهٔ Skill هنوز یک مبلغ تقریبی bundle بدون rule قطعی ذکر کرد؛
  در گزارش فقط جهت مشکل حفظ شد، نه عدد بی‌مدرک.
- Plan اولیه نگاشت DIP را حذف کرده، cwd یک command را اشتباه نسبت داده، تعداد
  آزمون را حدس زده و قرارداد repository را بیش از نیاز گسترش داده بود.
- characterization در Build ابتدا مقادیر demo و فاصلهٔ receipt را اشتباه ثبت
  کرد؛ در مراحل بعد syntax نامعتبر، import گمشده، duplicate discovery، fake
  نامعتبر و caller اصلاح‌نشده پیدا شد.
- مرحلهٔ ۴ هنگام توقف OpenCode ناقص بود و در صورت پذیرش، classهای ناموجود را
  import می‌کرد.

### ۱۰.۳. مهم‌ترین Promptهای استفاده‌شده چه بودند؟

1. [Prompt تحلیل Cash](01-Without-OOD-Principles/opencode/cash-payment-analysis-prompt.md)
   که inspection، فهرست فایل‌ها، حفظ معماری و approval gate را اجباری کرد.
2. [Prompt Build مربوط به Cash](01-Without-OOD-Principles/opencode/cash-payment-implementation-prompt.md)
   که stringها، محدودهٔ فایل و آزمون‌ها را دقیق مشخص کرد.
3. [Prompt پذیرش Skill](docs/opencode/solid-skill/acceptance-test-prompt.md)
   که مدرک مستقل برای هر پنج اصل و ممنوعیت edit را خواست.
4. [Prompt Plan](02-Applied-OOD-Principles/opencode/plan-prompt.md)
   که مراحل تدریجی، invariantها، dependency، risk، test و approval را الزام کرد.
5. [Prompt Build](02-Applied-OOD-Principles/opencode/build-prompt.md)
   که هر اجرا را به یک مرحلهٔ تأییدشده محدود کرد.

### ۱۰.۴. طراحی Skill چه اثری بر کیفیت پاسخ داشت؟

Skill خروجی را evidence-based و قابل‌بازبینی کرد: هر ادعا به محل دقیق، درجهٔ
اطمینان، false positive، کوچک‌ترین refactoring، tradeoff، وضعیت edit و دروازهٔ
تأیید متصل شد. آزمون نسخه‌های مختلف نشان داد نوشتن دستور به‌تنهایی کافی نیست و
completion guard، کنترل side effect و proposal-validity باید با مشاهدهٔ شکست
واقعی اضافه شوند. مهم‌ترین بهبود، جداسازی «الگوی ظاهراً مناسب» از اصلاحی بود
که واقعاً extension/dependency boundary می‌سازد.

### ۱۰.۵. اگر آزمایش تکرار شود چه چیزی را تغییر می‌دهیم؟

- از ابتدا session دارای permission مناسب و cwd صریح برای OpenCode انتخاب می‌کنیم.
- پیش از پیشنهاد production، characterization testها را کامل می‌کنیم.
- summary قابل‌پردازش شامل command، exit code و test count برای هر مرحله می‌خواهیم.
- completion، side effect و اعتبار proposal مربوط به Skill را پیش از استفادهٔ
  اصلی آزمایش می‌کنیم.
- رفتار مبهم دامنه، به‌ویژه pricing مربوط به bundle، را پیش از Plan مشخص می‌کنیم.
- review رسمی GitHub را پیش از merge برنامه‌ریزی و ثبت آن را جداگانه بررسی می‌کنیم.
- هر زمان کاربر اجازهٔ ابزار را لغو کرد، Agent را فوراً متوقف، diff ناقص را حفظ
  و ادامهٔ دستی را جداگانه ثبت می‌کنیم.

## ۱۱. نتیجه‌گیری و راستی‌آزمایی نهایی

مخزن نهایی هر دو پوشهٔ دقیق موردنیاز، آزمایش Cash روی طراحی اولیه، تحلیل
مبتنی‌برکد SOLID، Skill قابل‌استفادهٔ مجدد، Plan اولیه و اصلاح‌شده، commitهای
تدریجی Build، اصلاحات دستی و ارزیابی صادقانهٔ OpenCode را در خود دارد.
بازآرایی، SRP، OCP، LSP، ISP و DIP را در محدودهٔ تأییدشده بهبود داد و رفتار
قابل‌مشاهدهٔ demo را تغییر نداد.

### نتایج اجرای نهایی

| محدوده | command | exit | نتیجه |
|---|---|---:|---|
| ریشهٔ baseline | `PYTHONPYCACHEPREFIX=/private/tmp/swe-lab2-final-fa-root python3 -m compileall -q store` | ۰ | بدون خطا |
| ریشهٔ baseline | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v` | ۵ | صفر آزمون؛ محدودیت شناخته‌شدهٔ baseline |
| ریشهٔ baseline | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | ۰ | `$819.99` و `$5.00` |
| آزمایش Cash | `python3 -m compileall -q store tests` با cache خارجی | ۰ | بدون خطا |
| آزمایش Cash | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | ۰ | ۶ آزمون موفق |
| آزمایش Cash | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | ۰ | `$819.99` و `$5.00` |
| طراحی applied | `python3 -m compileall -q store tests` با cache خارجی | ۰ | بدون خطا |
| طراحی applied | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | ۰ | ۷۴ آزمون موفق |
| طراحی applied | `PYTHONDONTWRITEBYTECODE=1 python3 -m store.main` | ۰ | `$819.99` و `$5.00` |
| repository | `git diff --check` | ۰ | خطای whitespace وجود ندارد |
| hygiene | `find . -name __pycache__ -o -name '*.pyc'` | ۰ | فایل تولیدشده در مخزن وجود ندارد |

کد خروج ۵ برای آزمون ریشه عمداً حفظ شده است، زیرا نشان‌دهندهٔ نبود test suite
در starter است؛ آزمون‌های واقعی آزمایش Cash و طراحی اصلاح‌شده به‌ترتیب ۶ و ۷۴
مورد هستند و همگی موفق‌اند.

### وضعیت GitHub و repository

| مورد | وضعیت راستی‌آزمایی‌شده |
|---|---|
| `main` پیش از اصلاح فارسی گزارش | `c651c4f97c6c4b8e6674fc5886483f974f115c46`، merge commit مربوط به PR #45 |
| زمان راستی‌آزمایی نهایی | `2026-08-23 02:15:46 +0330` (Asia/Tehran) |
| پوشه‌های الزامی | `01-Without-OOD-Principles/` و `02-Applied-OOD-Principles/` هر دو با نام دقیق موجودند |
| گزارش | `README.md` در ریشه و به زبان فارسی موجود است |
| tag خط مبنا | annotated و مقصد آن `ace844f31cb5e39c2e0fc48faecabe07d60f30f0` است |
| tag بازآرایی | annotated و مقصد آن `88a17f0e2389dd74fb21bbf1b21054386ce1dce9` است |
| Task نهایی | [Issue #36](https://github.com/MohammadAminKoohi/Software_Workshop_2/issues/36) در وضعیت `closed/completed` است |
| گزارش نهایی قبلی | [PR #45](https://github.com/MohammadAminKoohi/Software_Workshop_2/pull/45) در `2026-08-22T22:37:27Z` توسط `arshiaizd` merge شد |
| review رسمی PR #45 | صفر؛ requested reviewer و merge واقعی وجود دارد، اما submitted review وجود ندارد |
| PRهای مراحل | PRهای #38 تا #45 merge شده‌اند |
| CI | فایلی در `.github/workflows/` وجود ندارد؛ بنابراین check خودکار CI ادعا نمی‌شود |
| اصلاح فعلی | طبق دستور مالک، ترجمه و تکمیل گزارش مستقیماً روی `main` commit و push می‌شود و PR جدیدی ساخته نمی‌شود |

### ساختار نهایی مخزن

```text
.
├── .github/
├── .opencode/skills/solid-refactoring/
├── 01-Without-OOD-Principles/
│   ├── analysis/
│   ├── opencode/
│   ├── store/
│   └── tests/
├── 02-Applied-OOD-Principles/
│   ├── build/
│   ├── opencode/
│   ├── planning/
│   ├── store/
│   └── tests/
├── docs/
│   ├── baseline-verification.md
│   ├── opencode/solid-skill/
│   └── solid-analysis.md
├── store/
└── README.md
```

### چک‌لیست نهایی تحویل

- [x] گزارش طبق ترتیب ۱۱‌بخشی Issue #36 نوشته شده است.
- [x] نام اعضای تیم، محمدامین کوهی و عرشیا ایزدی، به‌صورت صریح ثبت شده است.
- [x] هر دو پوشهٔ الزامی با نام دقیق وجود دارند.
- [x] promptها، outputها، approvalها، اصلاحات، آزمون‌ها، اندازه‌گیری‌ها، commitها
  و tagها قابل‌ردیابی هستند.
- [x] هر پنج پرسش ارزیابی OpenCode با مثال واقعی پاسخ داده شده‌اند.
- [x] کار OpenCode، بازبینی AI، تصمیم‌های انسانی و merge هم‌تیمی از یکدیگر
  تفکیک شده‌اند.
- [x] مراحل ۰ تا ۳ OpenCode، شروع ناقص مرحلهٔ ۴ و تکمیل دستی مراحل ۴ تا ۷
  بدون انتساب نادرست ثبت شده‌اند.
- [x] آزمون‌های baseline، Cash و applied دوباره اجرا و نتایج دقیق ثبت شده‌اند.
- [x] نبود CI و نبود submitted review پنهان یا جعل نشده است.
- [x] Issue #36 بسته و PR #45 توسط عرشیا ایزدی merge شده است.
- [x] هیچ secret، credential، bytecode یا فایل تولیدشدهٔ نامرتبط در تحویل وجود ندارد.
