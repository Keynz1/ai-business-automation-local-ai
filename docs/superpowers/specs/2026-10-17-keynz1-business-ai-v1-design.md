# Keynz1 Business AI v1.0 — Design Specification

Date: 2026-10-17
Status: Approved design, implementation not started
Repository: `Keynz1/ai-business-automation-local-ai`

## 1. Goal

Turn the existing portfolio/demo repository into a sellable Windows desktop product for Lemon Squeezy and similar storefronts.

The product must feel like a finished business tool rather than a Python demo. A buyer should be able to download a ZIP, unpack it, launch a Windows executable, paste a business request, analyze it, review a structured result and generated response, and export the result without installing Python or using a terminal.

## 2. Product Name

Working commercial name: **Keynz1 Business AI**

Initial release: **v1.0.0**

## 3. Target User

Small businesses, freelancers, and office users who receive repetitive requests by email, forms, or chat and want a lightweight local-first tool to structure them and export results to spreadsheet files.

The first release is intentionally narrow: one request at a time, one desktop window, no accounts, no cloud backend, and no CRM integration required.

## 4. Core User Flow

1. Launch `Keynz1 Business AI.exe`.
2. Paste a customer/business request into the main input box.
3. Click **Analyze Request**.
4. Review extracted fields and generated response.
5. Copy the response and/or export the processed record to Excel or CSV.
6. Optionally open the exports folder from the application.

The application must never require a command prompt for normal use.

## 5. AI Modes

The product must work even if Ollama is not installed.

### 5.1 Local AI mode

If a local Ollama service is reachable at the configured local endpoint, the application uses the configured local model for classification and extraction.

Default model remains compatible with the current repository configuration (`qwen2:1.5b`) unless changed during implementation for reliability.

UI status: **Local AI active**.

### 5.2 Smart offline mode

If Ollama is missing, unavailable, returns invalid output, or times out, the application uses the deterministic parser/fallback logic already present in the project.

UI status: **Smart offline mode**.

The absence of Ollama must not prevent the product from opening, processing a request, or exporting results.

## 6. Reuse of Existing Core

The existing processing pipeline remains the core business logic:

- request classification/extraction;
- request normalization;
- optional API enrichment;
- response generation;
- CSV export;
- Excel export;
- processing report generation.

The commercial desktop layer should call the existing processor rather than duplicate classification logic in the GUI.

The current `run_demo.py` remains useful as a development/demo path, but the sellable product gets a dedicated desktop entry point.

## 7. Desktop Interface

The first release uses one English-language desktop window.

### 7.1 Layout

Top bar:
- product name;
- current AI mode indicator.

Left/main input area:
- heading: **Business Request**;
- multi-line text input;
- **Analyze Request** button.

Right analysis area:
- request type;
- priority;
- customer name;
- email;
- summary;
- requested action;
- confidence if useful and readable.

Bottom response area:
- generated response text;
- **Copy Response**;
- **Export Excel**;
- **Export CSV**;
- **Open Folder**.

### 7.2 Visual Direction

- modern dark interface;
- clean spacing and clear hierarchy;
- no developer/debug controls in the main screen;
- no exposed stack traces;
- readable at standard Windows desktop scaling;
- no elements extending outside the visible window.

The UI must look commercial but remain simple enough for v1.0.

## 8. Export Behavior

User-generated exports must not be written beside the executable.

Default export root:

`Documents\Keynz1 Business AI\Exports`

The application creates required folders automatically.

Exports include at minimum:
- `.xlsx`;
- `.csv`.

A readable processing report may remain available if it is useful to the buyer, but it is not required to be a primary UI action in v1.0.

Repeated exports must not corrupt files or duplicate spreadsheet headers incorrectly.

## 9. Error Handling

Normal user-facing failures must be converted into concise messages inside the application.

Examples:
- empty input;
- Ollama unavailable;
- invalid AI output;
- export path unavailable;
- Excel/CSV write failure;
- optional REST endpoint unavailable.

The application must not crash because optional AI or API integrations are absent.

## 10. Windows Packaging

The commercial build will be produced with PyInstaller in **one-folder** mode unless implementation testing shows a stronger reason to change.

Reasons for one-folder:
- faster startup than a self-extracting one-file build;
- easier troubleshooting and updates;
- generally fewer antivirus false positives;
- predictable bundled dependencies.

The buyer must not need Python installed.

The executable should have a product icon and version metadata where practical.

## 11. Customer Package

Initial downloadable archive:

```text
Keynz1-Business-AI-v1.0.0.zip
│
├─ Keynz1 Business AI.exe
├─ [PyInstaller runtime files/folders]
├─ README.pdf
├─ LICENSE.txt
├─ examples/
│  ├─ sample_requests.txt
│  └─ sample_output.xlsx
└─ exports/   (optional empty starter folder; runtime exports use Documents by default)
```

Exact one-folder PyInstaller layout may differ, but the top-level package must remain understandable to a non-developer.

## 12. Buyer Documentation

`README.pdf` should cover:
- what the app does;
- how to launch it;
- how to analyze a request;
- where exports are saved;
- what **Local AI active** means;
- what **Smart offline mode** means;
- optional Ollama setup for enhanced local AI;
- basic troubleshooting;
- privacy note: local mode keeps request text on the buyer's own machine, except when an optional external API endpoint is explicitly configured.

Documentation should be in English for the initial international storefront release.

## 13. Licensing

v1.0 uses a simple commercial license file, not DRM.

Initial license intent:
- one purchaser may use the product for personal/business operations;
- redistribution, resale, sublicensing, or rebranding as the purchaser's own product is prohibited;
- first-version updates may be included at the seller's discretion;
- source code is not part of the standard commercial package unless sold separately later.

Lemon Squeezy license-key integration is explicitly deferred to a future release.

## 14. Public GitHub vs Paid Product

The public GitHub repository remains a portfolio/demo implementation.

The paid value comes from the commercial packaging and usability layer:
- desktop GUI;
- Windows executable;
- no Python requirement;
- stable export locations;
- buyer documentation;
- commercial packaging;
- polished error handling;
- sample files;
- product artwork/screenshots;
- license terms.

The paid package should not rely on secrecy of the public demo source as its value proposition.

## 15. Storefront Assets

Before v1.0 is called ready for sale, prepare:
- primary cover image;
- 2–4 clean screenshots of the application;
- product title;
- short description;
- full description;
- feature list;
- system requirements;
- privacy/local-AI note;
- launch price copy;
- downloadable ZIP.

Working launch price: **USD 19**.

Planned normal price after launch: **USD 29**.

Optional custom setup/service may later be offered separately from **USD 99+**, but it is not part of the v1.0 software implementation.

## 16. Out of Scope for v1.0

Do not add unless the design is revised:
- user accounts;
- cloud backend;
- subscriptions;
- online activation/DRM;
- built-in payment processing;
- CRM integration;
- Gmail/Outlook integration;
- batch inbox processing;
- multi-user/team mode;
- installer wizard;
- auto-updater;
- Russian localization;
- database history browser;
- mandatory Ollama installation.

These can be considered after the first sellable release is tested with real buyers.

## 17. Definition of Done

The product is not considered ready for sale until all of the following are verified:

1. Windows executable launches without Python installed.
2. Application works with Ollama absent.
3. Application uses local Ollama successfully when available.
4. Analyze action produces a structured result and generated response.
5. Excel export opens correctly.
6. CSV export opens correctly.
7. Copy Response works.
8. Open Folder opens the correct export directory.
9. Repeated runs/exports do not corrupt output or duplicate headers incorrectly.
10. User-facing errors do not expose raw tracebacks during normal operation.
11. No API keys, private credentials, personal data, or private development paths are bundled.
12. Release ZIP can be unpacked into a fresh folder and launched successfully.
13. UI remains usable at normal Windows display scaling and fits the target screen.
14. Basic local Windows Defender check shows no obvious packaging problem on the development machine.
15. README.pdf, LICENSE.txt, examples, screenshots, cover image, and storefront copy are complete.
16. Final archive is named/versioned consistently as `v1.0.0`.

## 18. Implementation Constraints

- Preserve existing tested core behavior where possible.
- Prefer small, testable adapters between GUI and core logic.
- Keep network use optional.
- Do not introduce paid API dependencies.
- Do not require buyer-side developer tooling.
- Keep v1.0 intentionally small enough to ship and sell quickly.

## 19. Success Criteria

The design succeeds when a non-technical Windows buyer can download the product, open the executable, paste a business request, receive a useful structured analysis and response, export the result, and understand whether local AI is active without reading developer instructions or installing Python.
