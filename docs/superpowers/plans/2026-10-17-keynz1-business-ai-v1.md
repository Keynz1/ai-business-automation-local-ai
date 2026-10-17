# Keynz1 Business AI v1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing AI Business Automation demo into a sellable Windows desktop application that runs without Python, works with or without Ollama, exports Excel/CSV, and ships as `Keynz1-Business-AI-v1.0.0.zip` with buyer documentation and storefront assets.

**Architecture:** Keep the current processor/exporter core intact and add a thin desktop stack: Ollama availability probe -> service layer -> pure controller/view model -> CustomTkinter window. Build the Windows app with PyInstaller one-folder mode, keep user exports under `Documents\Keynz1 Business AI\Exports`, and generate reproducible buyer/storefront assets from scripts. Commercial implementation work must live on an isolated local branch/worktree and must not be pushed to the public origin unless explicitly approved.

**Tech Stack:** Python 3.12, requests, openpyxl, CustomTkinter 5.x, Pillow, pytest 8.x, PyInstaller 6.x, ReportLab 4.x, Windows PowerShell.

**Spec:** `docs/superpowers/specs/2026-10-17-keynz1-business-ai-v1-design.md`

## Global Constraints

- Product name: `Keynz1 Business AI`.
- Initial release: `v1.0.0`.
- Initial UI language: English.
- One desktop window; one request at a time.
- No buyer-side Python requirement.
- Ollama is optional; absence, timeout, invalid output, or failure must fall back to Smart offline mode.
- Default local model remains compatible with `qwen2:1.5b`.
- No paid AI API dependency.
- Default export root: `Documents\Keynz1 Business AI\Exports`.
- Windows packaging: PyInstaller one-folder unless implementation testing proves it unsuitable.
- No accounts, cloud backend, subscriptions, DRM, CRM/email integration, auto-updater, installer wizard, or Russian localization in v1.0.
- Working launch price: USD 19; planned normal price: USD 29.
- Public GitHub remains a portfolio/demo; do not push commercial GUI/release source to public origin without explicit approval.

## Review Focus

1. **Whitespace-only or very large pasted request:** reject empty/whitespace input cleanly; accept long normal text without crashing or freezing the UI.
2. **Ollama port reachable but service malformed/hanging:** UI must remain responsive and fall back instead of exposing a traceback.
3. **Documents/export path unavailable or read-only:** show a concise user-facing export error; never lose the current analysis result.
4. **Unicode/non-ASCII customer text:** analysis, copy, CSV, and XLSX must preserve Unicode correctly.
5. **Repeated exports and repeated launches:** files must remain readable with one header row and no path leakage into the package.

---

## File Structure

### Existing files to modify

- `ai_client.py` — add fast Ollama availability probe; keep existing classification/fallback behavior.
- `processor.py` — allow an injected classifier so Smart offline mode can bypass a slow/unavailable Ollama call without duplicating processing logic.
- `requirements.txt` — add runtime GUI dependency.
- `.gitignore` — ignore commercial build/release outputs while keeping source/docs tracked.

### New runtime files

- `app_paths.py` — Windows user export directory creation and folder opening.
- `desktop_service.py` — AI mode detection, analysis orchestration, and CSV/XLSX export API.
- `desktop_controller.py` — input validation, current-result state, view-model formatting, export commands.
- `desktop_gui.py` — CustomTkinter window, background analysis execution, button callbacks, status/error presentation.
- `desktop_main.py` — application entry point and non-GUI `--smoke-test` path.
- `assets/app_icon.png` / `assets/app_icon.ico` — product icon.

### New tests

- `tests/test_ai_mode.py`
- `tests/test_app_paths.py`
- `tests/test_desktop_service.py`
- `tests/test_desktop_controller.py`
- `tests/test_desktop_gui.py`
- `tests/test_packaging_contract.py`

### New build/release source

- `requirements-build.txt` — PyInstaller/ReportLab build-only dependencies.
- `Keynz1BusinessAI.spec` — PyInstaller one-folder recipe including CustomTkinter data and product icon.
- `build_release.ps1` — deterministic release build, smoke test, file copy, and ZIP creation.
- `version_info.txt` — Windows executable version metadata for 1.0.0.
- `generate_app_icon.py` — reproducible PNG/ICO generation.
- `generate_customer_pdf.py` — buyer README PDF generation.
- `generate_storefront_assets.py` — product cover image generation.
- `capture_storefront_screenshots.py` — deterministic real-window screenshots for product listing.

### New commercial content source

- `commercial/README_customer.md`
- `commercial/LICENSE.txt`
- `commercial/examples/sample_requests.txt`
- `commercial/storefront/product_copy.md`

Generated release files go under ignored `release/` and `dist/` directories.

---

### Task 1: Add explicit AI-mode detection and injectable offline classification

**Files:**
- Modify: `ai_client.py`
- Modify: `processor.py`
- Create: `tests/test_ai_mode.py`
- Modify: `tests/test_processor.py`

**Interfaces:**
- Produces: `ollama_available(ollama_url: str = "http://127.0.0.1:11434", timeout: float = 1.0) -> bool`
- Produces: `Classifier = Callable[[str, str], BusinessRequest]`
- Produces: `process_request(text: str, *, model: str = "qwen2:1.5b", endpoint: str | None = None, classifier: Classifier | None = None) -> ProcessedRequest`
- Behavior: when `classifier is None`, preserve current call to `classify_request`; when provided, call `classifier(text, model)` and continue through the existing enrichment/response pipeline.

- [ ] **Step 1: Write failing Ollama availability tests**

Add tests named:
- `test_ollama_available_true_for_valid_tags_response`
- `test_ollama_available_false_for_connection_error`
- `test_ollama_available_false_for_non_200_or_invalid_json`

Mock `requests.get`; assert the probe uses `<base>/api/tags`, respects the supplied short timeout, and returns only `True`/`False` without raising.

- [ ] **Step 2: Run the AI-mode tests and verify failure**

Run: `python -m pytest tests/test_ai_mode.py -q`

Expected: FAIL because `ollama_available` does not exist.

- [ ] **Step 3: Implement `ollama_available(...) -> bool` in `ai_client.py`**

Use `GET /api/tags`; require HTTP success and a JSON object response. Catch `requests.RequestException`, `ValueError`, and JSON-decoding/type failures and return `False`.

- [ ] **Step 4: Add failing processor injection tests**

In `tests/test_processor.py`, add:
- `test_process_request_uses_injected_classifier_without_calling_ollama`
- `test_process_request_preserves_unicode_from_injected_classifier`

The first test must fail if the global `classify_request` is called. The second uses Unicode customer/summary text and asserts it survives the processed record.

- [ ] **Step 5: Run the processor tests and verify failure**

Run: `python -m pytest tests/test_processor.py -q`

Expected: new injection tests FAIL because `classifier` is not accepted.

- [ ] **Step 6: Implement the injectable classifier in `processor.py`**

Add the `Classifier` alias and optional keyword argument exactly as defined above; keep the existing default behavior unchanged.

- [ ] **Step 7: Run core regression tests**

Run: `python -m pytest tests/test_ai_mode.py tests/test_processor.py tests/test_end_to_end.py -q`

Expected: PASS.

- [ ] **Step 8: Commit Task 1**

```powershell
git add ai_client.py processor.py tests/test_ai_mode.py tests/test_processor.py
git commit -m "feat: add explicit local AI mode detection"
```

---

### Task 2: Add product paths and desktop service orchestration

**Files:**
- Create: `app_paths.py`
- Create: `desktop_service.py`
- Create: `tests/test_app_paths.py`
- Create: `tests/test_desktop_service.py`

**Interfaces:**
- Consumes: `ollama_available(...)`, `process_request(..., classifier=...)`, `fallback_parse(text)` and existing `append_csv` / `append_excel`.
- Produces: `PRODUCT_DIR_NAME = "Keynz1 Business AI"`
- Produces: `default_export_dir(documents_dir: Path | None = None) -> Path`
- Produces: `ensure_export_dir(documents_dir: Path | None = None) -> Path`
- Produces: `open_folder(path: Path) -> None`
- Produces: `AIMode = Literal["local", "offline"]`
- Produces: `@dataclass(frozen=True) AnalysisOutcome` with `item: ProcessedRequest` and `ai_mode: AIMode`
- Produces: `BusinessAIService(model="qwen2:1.5b", ollama_url="http://127.0.0.1:11434", endpoint=None, export_dir: Path | None = None)`
- Produces: `BusinessAIService.detect_mode() -> AIMode`
- Produces: `BusinessAIService.analyze(text: str) -> AnalysisOutcome`
- Produces: `BusinessAIService.export_excel(item: ProcessedRequest) -> Path`
- Produces: `BusinessAIService.export_csv(item: ProcessedRequest) -> Path`
- Produces: `BusinessAIService.open_export_folder() -> None`

- [ ] **Step 1: Write failing path tests**

Tests:
- `test_default_export_dir_uses_documents_product_exports`
- `test_ensure_export_dir_creates_nested_directory`
- `test_open_folder_uses_windows_startfile`
- `test_export_dir_failure_is_propagated_as_oserror`

Use an injected `documents_dir` under `tmp_path` for deterministic path checks.

- [ ] **Step 2: Run path tests and verify failure**

Run: `python -m pytest tests/test_app_paths.py -q`

Expected: FAIL because `app_paths.py` does not exist.

- [ ] **Step 3: Implement `app_paths.py`**

Default documents path is `Path.home() / "Documents"`; export path is exactly `<Documents>/Keynz1 Business AI/Exports`. `open_folder` uses `os.startfile(str(path))` on Windows.

- [ ] **Step 4: Write failing service tests**

Tests:
- `test_service_local_mode_uses_default_processor`
- `test_service_offline_mode_uses_fallback_classifier`
- `test_service_ollama_failure_after_probe_still_returns_processed_result`
- `test_service_exports_csv_and_excel_to_configured_directory`
- `test_service_preserves_unicode_through_both_exports`
- `test_service_repeated_exports_keep_single_header`

Inject/monkeypatch mode detection and processor calls; do not make live network calls.

- [ ] **Step 5: Run service tests and verify failure**

Run: `python -m pytest tests/test_desktop_service.py -q`

Expected: FAIL because `desktop_service.py` does not exist.

- [ ] **Step 6: Implement `BusinessAIService`**

If `detect_mode()` is `offline`, call `process_request` with an injected classifier that delegates to `fallback_parse`. If the initial mode is `local` but normal processing unexpectedly raises a recoverable request/AI failure, retry once with the fallback classifier and return `ai_mode="offline"`; do not duplicate exporter logic.

- [ ] **Step 7: Run Task 2 tests and exporter regression**

Run: `python -m pytest tests/test_app_paths.py tests/test_desktop_service.py tests/test_exporters.py -q`

Expected: PASS.

- [ ] **Step 8: Commit Task 2**

```powershell
git add app_paths.py desktop_service.py tests/test_app_paths.py tests/test_desktop_service.py
git commit -m "feat: add desktop business service"
```

---

### Task 3: Add pure controller and user-facing state/errors

**Files:**
- Create: `desktop_controller.py`
- Create: `tests/test_desktop_controller.py`

**Interfaces:**
- Consumes: `BusinessAIService` and `AnalysisOutcome` from Task 2.
- Produces: `class UserInputError(ValueError)`
- Produces: `class NoAnalysisError(RuntimeError)`
- Produces: `@dataclass(frozen=True) DisplayState` fields: `ai_status`, `request_type`, `priority`, `customer_name`, `company`, `email`, `summary`, `requested_action`, `confidence`, `response_text`.
- Produces: `BusinessAIController(service: BusinessAIService)`
- Produces: `BusinessAIController.analyze(text: str) -> DisplayState`
- Produces: `BusinessAIController.export_excel() -> Path`
- Produces: `BusinessAIController.export_csv() -> Path`
- Produces: `BusinessAIController.open_export_folder() -> None`
- Produces: `BusinessAIController.current_item: ProcessedRequest | None`

- [ ] **Step 1: Write failing controller tests**

Tests:
- `test_controller_rejects_empty_and_whitespace_input`
- `test_controller_maps_processed_request_to_display_state`
- `test_controller_labels_local_and_offline_modes`
- `test_controller_export_requires_analysis_first`
- `test_controller_export_keeps_current_result_after_oserror`
- `test_controller_accepts_large_request_text`

Use exact user-facing AI labels: `Local AI active` and `Smart offline mode`.

- [ ] **Step 2: Run controller tests and verify failure**

Run: `python -m pytest tests/test_desktop_controller.py -q`

Expected: FAIL because the controller does not exist.

- [ ] **Step 3: Implement `desktop_controller.py`**

Whitespace-only input raises `UserInputError("Enter a business request before analyzing.")`. Export before analysis raises `NoAnalysisError("Analyze a request before exporting.")`. Confidence display is a percentage string with no more than one decimal place.

- [ ] **Step 4: Run controller and service tests**

Run: `python -m pytest tests/test_desktop_controller.py tests/test_desktop_service.py -q`

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```powershell
git add desktop_controller.py tests/test_desktop_controller.py
git commit -m "feat: add desktop application controller"
```

---

### Task 4: Build the CustomTkinter desktop window and launcher

**Files:**
- Create: `desktop_gui.py`
- Create: `desktop_main.py`
- Create: `tests/test_desktop_gui.py`
- Modify: `requirements.txt`

**Interfaces:**
- Consumes: `BusinessAIController` and `DisplayState` from Task 3.
- Produces: `class BusinessAIWindow(customtkinter.CTk)` with constructor `BusinessAIWindow(controller: BusinessAIController)`.
- Produces callbacks: `_on_analyze()`, `_render_state(state: DisplayState)`, `_on_copy_response()`, `_on_export_excel()`, `_on_export_csv()`, `_on_open_folder()`.
- Produces: `desktop_main.PRODUCT_VERSION = "1.0.0"`
- Produces: `desktop_main.main(argv: Sequence[str] | None = None) -> int`
- Hidden verification behavior: `python desktop_main.py --smoke-test` prints `Keynz1 Business AI 1.0.0 smoke ok` and exits 0 without creating a GUI window.

- [ ] **Step 1: Add the runtime GUI dependency**

Add `customtkinter>=5.2,<6` to `requirements.txt`.

Run: `python -m pip install -r requirements.txt`

Expected: install completes without dependency conflicts.

- [ ] **Step 2: Write failing GUI contract tests**

Tests:
- `test_window_has_required_title_and_buttons`
- `test_render_state_populates_analysis_and_response_fields`
- `test_copy_response_uses_clipboard`
- `test_gui_turns_controller_error_into_visible_message`
- `test_analyze_runs_off_main_thread_and_restores_button_state`
- `test_smoke_flag_exits_without_creating_window`

On the Windows development machine, instantiate the window, immediately `withdraw()`, run `update_idletasks()`, then destroy it in `finally` blocks so tests do not leave windows open.

- [ ] **Step 3: Run GUI tests and verify failure**

Run: `python -m pytest tests/test_desktop_gui.py -q`

Expected: FAIL because runtime GUI files do not exist.

- [ ] **Step 4: Implement `BusinessAIWindow` layout**

Window content must match the approved design: product title + AI status top bar, Business Request input left, Analysis fields right, Generated Response bottom, and buttons `Analyze Request`, `Copy Response`, `Export Excel`, `Export CSV`, `Open Folder`. Use a dark theme; set a minimum usable size and grid weights so standard Windows scaling does not clip controls.

- [ ] **Step 5: Implement non-blocking analysis**

`_on_analyze()` disables the Analyze button, starts one daemon worker thread, calls only the controller from that worker, and schedules UI updates/errors back through `after(...)`. Never write widget state from the worker thread.

- [ ] **Step 6: Implement export/copy/folder callbacks and concise errors**

Map `UserInputError`, `NoAnalysisError`, `OSError`, and unexpected normal-operation exceptions to a visible status/error label or message box without raw tracebacks.

- [ ] **Step 7: Implement `desktop_main.main(...)` and smoke mode**

Normal run constructs `BusinessAIService` -> `BusinessAIController` -> `BusinessAIWindow` and calls `mainloop()`. `--smoke-test` must avoid importing/creating a display-dependent window until after the flag is handled.

- [ ] **Step 8: Run GUI + full regression tests**

Run: `python -m pytest -q`

Expected: all tests PASS.

- [ ] **Step 9: Manual desktop smoke**

Run: `python desktop_main.py`

Verify: window fits screen, empty input shows a friendly message, sample request analyzes, UI stays responsive, copy works, both export buttons produce files, and `Open Folder` opens the export directory.

- [ ] **Step 10: Commit Task 4**

```powershell
git add requirements.txt desktop_gui.py desktop_main.py tests/test_desktop_gui.py
git commit -m "feat: add Keynz1 Business AI desktop interface"
```

---

### Task 5: Create buyer documentation, commercial license, examples, and product icon

**Files:**
- Create: `commercial/README_customer.md`
- Create: `commercial/LICENSE.txt`
- Create: `commercial/examples/sample_requests.txt`
- Create: `generate_customer_pdf.py`
- Create: `generate_app_icon.py`
- Create: `requirements-build.txt`
- Create: `assets/app_icon.png`
- Create: `assets/app_icon.ico`
- Create/Modify: `tests/test_packaging_contract.py`

**Interfaces:**
- Produces: `generate_customer_pdf(source: Path, output: Path) -> Path`
- Produces: `generate_app_icon(png_path: Path, ico_path: Path) -> tuple[Path, Path]`
- Build dependencies: `-r requirements.txt`, `pyinstaller>=6,<7`, `reportlab>=4,<5`.

- [ ] **Step 1: Write failing content/asset contract tests**

Assert:
- customer README includes launch, analyze, export location, Local AI active, Smart offline mode, optional Ollama setup, troubleshooting, privacy note;
- license prohibits redistribution/resale/rebranding and does not claim DRM;
- sample requests include at least data cleanup, automation, and reporting examples;
- generated icon files exist and PNG is at least 256x256;
- generated README PDF starts with `%PDF` and is non-empty.

- [ ] **Step 2: Run packaging contract tests and verify failure**

Run: `python -m pytest tests/test_packaging_contract.py -q`

Expected: FAIL because content/generators do not exist.

- [ ] **Step 3: Write `commercial/README_customer.md` and `commercial/LICENSE.txt`**

Keep English buyer language concise and consistent with the approved spec; do not promise cloud features, CRM/email integration, or mandatory Ollama.

- [ ] **Step 4: Add sample requests and build dependencies**

`requirements-build.txt` must include runtime requirements plus PyInstaller and ReportLab only; do not add runtime-only dependencies unnecessarily.

- [ ] **Step 5: Implement and run PDF/icon generators**

Run:
```powershell
python generate_app_icon.py
python generate_customer_pdf.py
```

Expected: `assets/app_icon.png`, `assets/app_icon.ico`, and generated buyer `README.pdf` in the build staging location.

- [ ] **Step 6: Run contract tests**

Run: `python -m pytest tests/test_packaging_contract.py -q`

Expected: PASS.

- [ ] **Step 7: Commit Task 5**

```powershell
git add commercial requirements-build.txt generate_customer_pdf.py generate_app_icon.py assets tests/test_packaging_contract.py
git commit -m "docs: add commercial buyer package assets"
```

---

### Task 6: Add PyInstaller one-folder build and deterministic release ZIP

**Files:**
- Create: `Keynz1BusinessAI.spec`
- Create: `version_info.txt`
- Create: `build_release.ps1`
- Modify: `.gitignore`
- Modify: `tests/test_packaging_contract.py`

**Interfaces:**
- Consumes: `desktop_main.py`, CustomTkinter runtime data, app icon, generated README PDF, license/examples.
- Produces folder: `dist/Keynz1 Business AI/`
- Produces executable: `dist/Keynz1 Business AI/Keynz1 Business AI.exe`
- Produces archive: `release/Keynz1-Business-AI-v1.0.0.zip`
- Packaged smoke contract: `& '.\dist\Keynz1 Business AI\Keynz1 Business AI.exe' --smoke-test` exits 0 and prints `Keynz1 Business AI 1.0.0 smoke ok`.

- [ ] **Step 1: Add failing packaging recipe tests**

Tests assert:
- PyInstaller spec names the app `Keynz1 Business AI`;
- `console=False` / windowed build is used;
- CustomTkinter package data is collected;
- icon and Windows version metadata are referenced;
- release script targets exact version `1.0.0` and exact ZIP name;
- `.gitignore` excludes `/build/`, `/dist/`, `/release/`.

- [ ] **Step 2: Run contract tests and verify failure**

Run: `python -m pytest tests/test_packaging_contract.py -q`

Expected: FAIL on missing build files.

- [ ] **Step 3: Implement `version_info.txt` and `Keynz1BusinessAI.spec`**

Use one-folder, windowed mode. Explicitly include CustomTkinter data files required at runtime. Entry point is `desktop_main.py`; icon is `assets/app_icon.ico`.

- [ ] **Step 4: Implement `build_release.ps1`**

Script sequence: clear only known `build/`, `dist/`, `release/` outputs -> generate icon and README.pdf -> run PyInstaller spec -> run packaged `--smoke-test` -> stage buyer files/examples beside one-folder app -> create `release/Keynz1-Business-AI-v1.0.0.zip` -> fail fast on any non-zero exit.

- [ ] **Step 5: Run contract tests**

Run: `python -m pytest tests/test_packaging_contract.py -q`

Expected: PASS.

- [ ] **Step 6: Build the release**

Run:
```powershell
python -m pip install -r requirements-build.txt
powershell -ExecutionPolicy Bypass -File .\build_release.ps1
```

Expected: PyInstaller succeeds, packaged smoke test prints exact success line, ZIP exists.

- [ ] **Step 7: Inspect ZIP contents and absence of sensitive paths**

Run a PowerShell/Python inspection that asserts required files exist and searches text/config assets for `L:\FRANKENSTEIN`, `C:\Users\Predator`, API-token patterns, `.env`, and private credential strings.

Expected: no matches in the staged buyer package.

- [ ] **Step 8: Commit Task 6**

```powershell
git add Keynz1BusinessAI.spec version_info.txt build_release.ps1 .gitignore tests/test_packaging_contract.py
git commit -m "build: add Windows release packaging"
```

---

### Task 7: Produce storefront copy, cover, and real application screenshots

**Files:**
- Create: `commercial/storefront/product_copy.md`
- Create: `generate_storefront_assets.py`
- Create: `capture_storefront_screenshots.py`
- Modify: `tests/test_packaging_contract.py`
- Generated ignored/output assets: `release/storefront/cover_1600x1200.png`, `release/storefront/screenshot_main.png`, `release/storefront/screenshot_analysis.png`, `release/storefront/screenshot_offline.png`

**Interfaces:**
- Produces product title: `Keynz1 Business AI — Local Business Request Analyzer`
- Produces launch price copy: `USD 19 launch price`; normal price `USD 29`.
- Screenshot generator may inject a deterministic fake controller/result for repeatable visuals, but the pixels must come from the real `BusinessAIWindow`, not a drawn mockup.

- [ ] **Step 1: Write failing storefront contract tests**

Assert `product_copy.md` contains: concise headline, problem statement, key features, Windows requirement, no-Python statement, optional Ollama/local privacy note, export formats, launch price, normal price, and no unsupported feature claims.

- [ ] **Step 2: Write storefront copy**

Use buyer language, not developer language. Avoid claims such as “fully autonomous AI”, “guaranteed privacy”, or integrations not present in v1.0.

- [ ] **Step 3: Implement cover generator**

Generate a 1600x1200 PNG aligned with the product’s dark UI branding and feature copy. Reuse the app icon/brand elements rather than unrelated artwork.

- [ ] **Step 4: Implement deterministic real-window screenshot capture**

Create the actual `BusinessAIWindow`, inject a deterministic controller state, position it fully on screen, call `update()`, and use Pillow `ImageGrab` on the window bounds. Produce the three required screenshots and always destroy the window in `finally`.

- [ ] **Step 5: Generate and inspect storefront assets**

Run:
```powershell
python generate_storefront_assets.py
python capture_storefront_screenshots.py
```

Expected: four PNG files exist, dimensions are non-zero, text is readable, and no private paths/user data are visible.

- [ ] **Step 6: Run storefront/package contract tests**

Run: `python -m pytest tests/test_packaging_contract.py -q`

Expected: PASS.

- [ ] **Step 7: Commit Task 7**

```powershell
git add commercial/storefront generate_storefront_assets.py capture_storefront_screenshots.py tests/test_packaging_contract.py
git commit -m "feat: add storefront release assets"
```

---

### Task 8: Final v1.0 verification and sale-ready artifact

**Files:**
- No new product code unless verification finds a defect.
- Generated: `release/Keynz1-Business-AI-v1.0.0.zip`
- Generated: `release/storefront/*`

**Interfaces:**
- Consumes all previous tasks.
- Produces a verified sale-ready ZIP and storefront asset set; no public push of commercial branch/source.

- [ ] **Step 1: Run the full automated suite from a clean checkout/worktree**

Run: `python -m pytest -q`

Expected: all tests PASS.

- [ ] **Step 2: Build release from scratch**

Run: `powershell -ExecutionPolicy Bypass -File .\build_release.ps1`

Expected: clean successful build and exact ZIP filename.

- [ ] **Step 3: Verify packaged app without Python dependency in the launch path**

Run packaged `--smoke-test`, then launch the EXE normally from `dist/Keynz1 Business AI/`. Verify the app does not invoke system `python.exe`/`pythonw.exe` as a child process.

- [ ] **Step 4: Verify offline-mode user flow**

Stop/disable Ollama for this check. Launch EXE, confirm `Smart offline mode`, analyze an English request containing Unicode/non-ASCII text, copy response, export CSV/XLSX, reopen files, and verify content is intact.

- [ ] **Step 5: Verify local-AI user flow**

Start Ollama with the configured model available. Launch EXE, confirm `Local AI active`, analyze a sample request, and verify structured result plus exports.

- [ ] **Step 6: Verify export failure behavior**

Temporarily point a test instance at a read-only/unavailable export path. Confirm a concise error appears, app stays open, and the current result remains visible/copyable.

- [ ] **Step 7: Verify repeated launches/exports**

Run multiple analyses and exports across two application launches. Confirm CSV has one header, XLSX remains readable, and no output is written beside the EXE.

- [ ] **Step 8: Inspect the final ZIP on a fresh folder**

Extract to a new directory outside the repository and run the executable there. Confirm README.pdf, LICENSE.txt, examples, runtime folder, and EXE are understandable to a non-developer.

- [ ] **Step 9: Run local Windows Defender scan/check**

Use the installed Windows Security/Defender CLI or UI on the release folder/ZIP if available. Record any detection. Do not claim the build is clean unless the check completes with no detection.

- [ ] **Step 10: Final secret/private-path scan**

Search the final staged package and storefront files for credentials, token-like strings, personal data, development usernames, and repository drive paths.

Expected: no sensitive/private matches.

- [ ] **Step 11: Record release commit/tag locally**

After all checks pass:
```powershell
git status --short
git tag -a v1.0.0 -m "Keynz1 Business AI v1.0.0"
```

Do not push the commercial branch or tag to the public origin unless explicitly approved.

- [ ] **Step 12: Report sale-ready deliverables**

Provide exact local paths for the ZIP and storefront images, test count/results, build smoke result, Ollama/offline checks, Defender result, and any known limitation. Only then mark v1.0.0 ready for upload to Lemon Squeezy.
