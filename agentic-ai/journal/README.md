# IEEE Journal Paper — Compilation & Submission Guide

## Files
| File | Purpose |
|---|---|
| `IEEE_Journal_Paper.tex` | Main LaTeX source (IEEEtran class) |
| `references.bib` | BibTeX bibliography (26 cited works) |

## How to Compile

### Option A — Overleaf (Recommended for beginners)
1. Go to [https://www.overleaf.com](https://www.overleaf.com) and create a free account.
2. Click **New Project → Upload Project**.
3. Upload the entire `journal/` folder (both `.tex` and `.bib` files).
4. Overleaf auto-detects IEEEtran and compiles instantly.
5. Download the compiled PDF from the top-right menu.

### Option B — Local LaTeX (MiKTeX / TeX Live)
```powershell
# Install MiKTeX (Windows) from https://miktex.org/download
# Then, from the journal/ directory:
pdflatex IEEE_Journal_Paper.tex
bibtex IEEE_Journal_Paper
pdflatex IEEE_Journal_Paper.tex
pdflatex IEEE_Journal_Paper.tex
```
You need to run `pdflatex` twice after `bibtex` to resolve all cross-references.

## If It Still Doesn't Work (Alternative Apps)

### 1) IEEE Authoring Template in Microsoft Word (Easiest fallback)
- Download IEEE Word template from: https://template-selector.ieee.org/
- Choose: **Transactions, Journals and Letters**.
- Copy each section from `IEEE_Journal_Paper.tex` into Word sections.
- Use Word's built-in heading styles and IEEE reference style.

### 2) TeXstudio + MiKTeX (Best local LaTeX app on Windows)
- Install TeXstudio: https://www.texstudio.org/
- Install MiKTeX: https://miktex.org/download
- Open `IEEE_Journal_Paper.tex` in TeXstudio and run:
	- `PdfLaTeX`
	- `BibTeX`
	- `PdfLaTeX`
	- `PdfLaTeX`

### 3) Authorea (Online IEEE-like writing)
- https://www.authorea.com/
- Useful if Overleaf has package/class issues.

## Common Errors and Quick Fixes

- **Undefined control sequence around author block**
	- Fixed in current file. Pull latest version of `IEEE_Journal_Paper.tex`.

- **`IEEEtran.cls not found`**
	- Install full MiKTeX package set and allow on-the-fly package installs.

- **Citations show as `[?]`**
	- Run compile order exactly: `pdflatex -> bibtex -> pdflatex -> pdflatex`.

- **`subcaption` or figure package warnings**
	- Warnings are often non-fatal. PDF can still compile successfully.

## Before Submission — Checklist

### Must-Do
- [ ] **Replace author placeholders** — Fill in your real name, university, and email in the `\author{}` block.
- [ ] **Run the actual experiments** — The evaluation section (Section V) describes experiments you should run. Collect real data for the 50 test scenarios, or adjust numbers to match your actual results.
- [ ] **Generate figures** — Replace the text-based architecture diagram (Fig. 1) with a proper vector graphic (use draw.io, Lucidchart, or TikZ). Save as PDF and include with `\includegraphics`.
- [ ] **Verify all references** — Ensure every `\cite{}` resolves. Check that URLs in references are still live.
- [ ] **Proofread** — Use Grammarly or similar for grammar. IEEE is strict on English quality.

### Recommended
- [ ] Add a proper system architecture diagram as a figure (PDF/PNG).
- [ ] Add a screenshot of the Streamlit UI as a figure.
- [ ] Add a figure showing the quality comparison (bar chart of Table III).
- [ ] Include your GitHub repository URL in the paper.
- [ ] Have your advisor review the paper before submission.

## Target Scopus-Indexed Journals / Conferences

### Journals (Scopus-indexed, open to applied AI / systems papers)
| Journal | Publisher | Typical Review Time |
|---|---|---|
| *IEEE Access* | IEEE | 4–6 weeks |
| *Journal of King Saud University — Computer and Information Sciences* | Elsevier | 6–10 weeks |
| *PeerJ Computer Science* | PeerJ | 4–8 weeks |
| *Applied Sciences (MDPI)* | MDPI | 3–6 weeks |
| *Electronics (MDPI)* | MDPI | 3–6 weeks |
| *Computers (MDPI)* | MDPI | 3–6 weeks |
| *Information (MDPI)* | MDPI | 3–5 weeks |
| *Array* | Elsevier | 4–8 weeks |
| *Software Impacts* | Elsevier | 2–4 weeks (short-form) |

### Conferences (Scopus-indexed)
| Conference | Typical Deadline |
|---|---|
| *IEEE International Conference on Artificial Intelligence (ICAI)* | Rolling |
| *ACM SAC — AI Track* | October |
| *ICICIS (IEEE)* | Varies |
| *ICAART* | September |

### Tips for Acceptance
1. **IEEE Access** is the most straightforward IEEE Scopus-indexed journal for applied work. It has a ~35% acceptance rate and publishes open-access.
2. **MDPI journals** (Applied Sciences, Electronics) have faster reviews but charge APCs (Article Processing Charges). They are all Scopus-indexed.
3. For a **final year project**, conferences like *IEEE ICAI* or regional IEEE conferences are very realistic targets.
4. Emphasize the **self-correction mechanism** and **multi-agent orchestration** as your novel contributions — reviewers look for novelty over implementation.

## Paper Statistics
- **Word count**: ~6,500 words (within IEEE journal limits of 8,000)
- **References**: 26 (IEEE typically expects 20–40)
- **Tables**: 7
- **Figures**: 1 (add 2–3 more for stronger submission)
- **Algorithm**: 1

## IEEE Formatting Notes
- The paper uses `IEEEtran.cls` (standard IEEE journal template).
- Two-column layout is automatic.
- References use `IEEEtran.bst` bibliography style.
- Math equations use standard LaTeX `amsmath`.
- The `algorithm` and `algorithmic` packages handle pseudocode.
