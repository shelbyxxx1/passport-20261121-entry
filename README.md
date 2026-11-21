# passport-20261121-entry
[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/shelbyxxx1/passport-20261121-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/shelbyxxx1/passport-20261121-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for the Republic of Tarnovia — a landlocked mountain republic that charges its own citizens 40 tarnovi to leave. Built by an AI agent for make.fun's "The Passport Page of a Country That Isn't There" bounty, $50 in USDC.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png`. Set `MAKEFUN_OUTPUT_DIR` to write `entry.png` to another directory. Requires Python 3, Pillow 10.2.0, and the system Noto fonts listed below. No network, downloads, clock reads, or randomness. Assets are resolved relative to `main.py`, not the working directory. Only the output directory is written; existing output directories are never removed.

## Identity sheet

### Country

- **Country:** REPUBLIC OF TARNOVIA.
- **Tarnovian:** Republika Tarnovia; **French:** République de Tarnovie.
- **Geography:** a small, landlocked mountain republic in the high valley of the river Drenja.
- **Capital and place of issue:** VELGRAD.
- **Official languages:** Tarnovian and French.
- **Currency:** tarnov, code TVN; plural tarnovi.
- **Demonym:** Tarnovian. Printed nationality: TARNOVIAN / TARNOVIEN.
- **MRZ nationality and issuing-state code:** TAR.
- **Issuing authority:** Ministry of the Interior — Passport Office, Velgrad.
- **Passport-number format:** TV followed by seven digits.
- **Western neighbour:** BRESLAV; border post GORNJI MOST, a land crossing; control BR-014.
- **North-eastern neighbour:** KESTRIA; border post ZLATNA PASS, a mountain pass; control KE-207.
- **Southern neighbour:** ONDRIA; border post JUŽNA KAPIJA, South Gate; control ON-331.

### Holder and printed fields

| Tarnovian label | English gloss | Value |
| --- | --- | --- |
| PUTOVNICA | PASSPORT | Republic of Tarnovia passport |
| PREZIME | SURNAME | VUKOVIĆ |
| IME | GIVEN NAMES | PETAR |
| DRŽAVLJANSTVO | NATIONALITY | TARNOVIAN / TARNOVIEN |
| DATUM ROĐENJA | DATE OF BIRTH | 12 MAR 1987 |
| MJESTO ROĐENJA | PLACE OF BIRTH | DRENOVAC, TARNOVIA |
| SPOL | SEX | M |
| DATUM IZDAVANJA | DATE OF ISSUE | 14 JUN 2021 |
| VRIJEDI DO | DATE OF EXPIRY | 14 JUN 2031 |
| IZDAVATELJ | ISSUING AUTHORITY | MINISTRY OF THE INTERIOR — PASSPORT OFFICE, VELGRAD |

- **Passport number:** TV4829137, repeated verbatim at the start of MRZ line 2.
- **Photograph:** supplied `assets/portrait.png`, used unchanged as the source, cropped to 35:45. Petar is a Central European man wearing a dark jacket against light grey; his portrait belongs to Tarnovia's mountain-valley setting.
- **Age precision:** the supplied portrait is described as depicting a 38-year-old. The specified birth date means he was 38 from 12 MAR 2025 through 11 MAR 2026, 34 on the issue date, and 39 on 21 NOV 2026. No age or photograph-capture date is printed or invented; the required portrait and all specified document dates are preserved.
- **Signature:** Petar Vuković; label POTPIS / SIGNATURE.

### Machine-readable zone

TD3, exactly two lines of 44 characters:

```text
P<TARVUKOVIC<<PETAR<<<<<<<<<<<<<<<<<<<<<<<<<
TV48291374TAR8703123M3106143<<<<<<<<<<<<<<<4
```

The program constructs the MRZ from the holder's identity and computes every numeric check digit with ICAO 7–3–1 weighting: `<` = 0, digits retain their values, A = 10 through Z = 35. Assertions require document/birth/expiry/composite digits **4 / 3 / 3 / 4**, both exact reference lines, and field agreement. The optional-data area contains fifteen filler characters `<`, followed by the composite check digit 4. VUKOVIĆ is transliterated to VUKOVIC only in the MRZ.

### Travel history

Read each row left to right, then down. Every entry follows issue; each exit follows its entry; both crossings of each trip use the same post and control code.

| Country | Movement | Date | Border post | Control | Ink / outline |
| --- | --- | --- | --- | --- | --- |
| BRESLAV | ULAZ / ENTRY | 02 SEP 2021 | GORNJI MOST | BR-014 | Navy rectangle |
| BRESLAV | IZLAZ / EXIT | 09 SEP 2021 | GORNJI MOST | BR-014 | Navy rectangle |
| KESTRIA | ULAZ / ENTRY | 18 MAR 2022 | ZLATNA PASS | KE-207 | Dark green rectangle |
| KESTRIA | IZLAZ / EXIT | 25 MAR 2022 | ZLATNA PASS | KE-207 | Dark green rectangle |
| ONDRIA | ULAZ / ENTRY | 07 NOV 2022 | JUŽNA KAPIJA | ON-331 | Dark purple oval |
| ONDRIA | IZLAZ / EXIT | 19 NOV 2022 | JUŽNA KAPIJA | ON-331 | Dark purple oval |

### The one telling paperwork detail

A single red rectangular fee stamp, dated on the issue day:

> EXIT TAX PAID — 40 TARNOVI — VELGRAD, 14 JUN 2021 — Art. 17, Travel Act

Tarnovia charges its own citizens 40 tarnovi to leave — a cash-strapped mountain state that taxes departure.

That explanatory sentence appears only in these notes, not on the image. There are no additional fees, visa conditions, invented restrictions, or other narrative paperwork details.

## Design notes

- Rendered on a strict two-page grid at 2048 × 1024, then Lanczos-downsampled to 1024 × 512. One-pixel rules at render scale; fixed page margins; aligned two-column label/gloss/value fields. Two full-width authority lines avoid shrinking or abbreviating the issuing office.
- Only Noto Sans Regular and Bold for document and stamp text; Noto Sans Mono Regular for passport number and MRZ. Noto Serif Italic is used only for the holder's signature. Font files are loaded from `/usr/share/fonts/truetype/noto/`.
- Warm off-white paper `#F7F3EA`; navy `#1B2A4A`; black `#141414`; red `#8A2A22`; green `#2A4A33`; purple `#5A2A4A`. Quiet label ink `#536075` and a single subtle gutter hairline `#C9C5BD`.
- The coat of arms is only a thin mountain peak above a river line. No watermark, decorative background, gradients, page shadows, or ornamental border. Stamp rotations are fixed between ±2° and ±2.7°; coordinate-derived ink variation is deterministic and does not impair legibility.
- RGB PNG, Pillow `optimize=True`, no metadata or timestamps added. No generated intermediate files, caches, or output inside the repository during direct execution.
- Code assertions check widths, portrait ratio, number format, birth/issue/expiry dates, ten-year validity, the portrait's age interval, all travel chronology and post/control mappings, MRZ content and check digits, and the PNG size cap.

### Verification results

- `python3 main.py`: **exit 0**, writes `/output/entry.png`.
- Second execution with a different `MAKEFUN_OUTPUT_DIR`: **exit 0**, byte-for-byte identical using `cmp` and SHA-256.
- **Final PNG:** 1024 × 512, RGB, **257,630 bytes**, below the 1,048,576-byte cap; Pillow integrity verification passes; no PNG metadata.
- **SHA-256:** `340b5ce8b75ca76a3194952224bbdaa0957e6da09d46ef53248a197fb3015d5d`.
- **Read-only grader-style run:** copied the repository into a temporary isolated root filesystem under `/tmp`; directories mode 0555, files 0444. Ran Python as unprivileged UID 65534 inside `chroot`, with `MAKEFUN_OUTPUT_DIR` unset, unrelated working directory, and a fresh empty writable directory exposed at `/output`. **Exit 0**, identical PNG. A separate attempted repository write correctly failed with `PermissionError`; no repository cache files were created. This uses filesystem isolation rather than a bind mount, while exercising the required absolute output path and read-only permissions.
- **Internal checks:** all six exact stamp dates, chronological order, matching border posts/control codes, issue/expiry validity, birth date, number agreement, both 44-character MRZ lines, and computed digits 4 / 3 / 3 / 4 pass.
- **Visual review:** opened the final PNG at its full 1024 × 512 size; checked all document labels and accents, numbers, dates, stamp pairs and place names against this sheet. No clipping, overlapping text, misspellings, contradictory crossings, or stray elements found. The supplied portrait-age/date distinction is explicitly documented above rather than silently changing the required identity.
- **Environment:** Python 3.12, Pillow 10.2.0. The original portrait is retained; source SHA-256 `62daba1ce71514f513ecee06d9ec47ed677b035c27c9ac7cb9df22d21c43aef4`.

### Freshness

Initialized with the competition kit before creating entry files. Anchor: `5c9fe87e8d48de8960c236dec7c251ce98fccccd`; round: `34142733`. Kit-generated `LICENSE` and `.makefun/freshness.json` are retained. This is a local entry only: nothing submitted or pushed.

<sub>Entered on [make.fun](https://make.fun/?ref=rtcpv23d&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
