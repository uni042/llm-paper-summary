# Legacy paper-quality criteria v10

Status: RETIRED / restoration snapshot

This directory preserves the exact pre-v11 paper-quality implementation that was active immediately before the Library-first quality-responsibility split on 2026-09-28.

Do not use these files as current workflow instructions. Current policy lives in:
- `.survey/docs/survey-workflow/paper-quality-audit.md`
- `.survey/docs/survey-workflow/worker-router.md`
- Library `/LLM-paper-summary-library-first/PAPER-QUALITY-GUIDE.md`

## What this snapshot preserves

The retired gate enforced, among other things:
- UTF-8 size >= 4,500 bytes
- prose >= 2,200 characters
- >= 10 prose paragraphs
- >= 4 method paragraphs
- >= 2 paragraphs per method component when 3+ components exist
- Japanese ratio FAIL below 70%, WARN below 80%
- zero replaceable bare English technical terms
- 45-180 character list summaries with language/style checks
- overview representative-result detection
- structured-record semantic depth requirements

These criteria were retired from the GitHub publication/upload side because a GitHub uploader cannot safely repair semantic failures without rereading the paper, and some measurements are not reliably available to Scheduled Chat workers.

## Restoration

To restore the old behavior, copy the desired `.legacy` files back to their Source paths and restore the old workflow wiring together. Prefer restoring the whole coherent set rather than only one script.

Source snapshot:
- `.survey/docs/survey-workflow/paper-quality-audit.md` — blob `c7cfc3c90c59991ab4627782d10f15f46ba6502f`
- `.survey/scripts/audit_paper_quality.py` — blob `fcb6a95cca3c0898542e3252c951620c2990aeb6`
- `.survey/scripts/japanese_style.py` — blob `f8c250e21b41e1671dcab0427a76288ddd4617d4`
- `.survey/scripts/list_summary.py` — blob `a52d78a005bca93626363cfd2c73a6974545edc8`
- `.survey/scripts/audit_list_summary_quality.py` — blob `584f56df98a4eaab79b6b9ad012a446c171d5706`
- `.survey/scripts/audit_overview_results.py` — blob `124619d8dea162d05a261bfa35b62829ff0fdb54`
- `.survey/scripts/paper_quality_gate.py` — blob `f96be74cc0fd676f854f2558fdf9b1cc8e59bd1e`
- `.survey/scripts/assemble_research_record.py` — blob `65828be318287e7b42f24b516ec6a6b41825c4ae`
- `.survey/scripts/render_paper.py` — blob `8d3cd7acdd8b90ca00104372d1616719ac1514c5`
- `.survey/scripts/research_quality_selfcheck.py` — blob `b7a0c107d6252123c2abb35ad64ac3a7bd89bfe1`
- `.survey/scripts/research_quality_preflight.py` — blob `a6cc27456b9ee6dced6a83b9279910ee996e96cf`
- `.github/workflows/paper-quality-audit.yml` — blob `f7c7c8f7e0aae2b85ddc7ce9c8f81707ba92dedc`
