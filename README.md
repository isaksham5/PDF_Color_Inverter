This purpose of this project is to have a Python program/script and selectively invert pages while keeping some snippets uninverted for making pdf's print friendly.

# PDF Inverter & Question Collage Tool

A Windows command-line tool that:

- Inverts PDFs (white background to dark) for easier night reading
- Inverts only selected regions of a page (page-wise edits)
- Enhances brightness and contrast of scanned pages
- Converts images (PNG/JPG/JPEG) into a single PDF
- Builds a "question collage": crop snippets from pages and paste them onto A4 sheets
- Prints the collage to the default printer, with optional preview

## Requirements

- Windows (uses `pywin32` and Windows paths)
- Python 3.8+
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases), extracted somewhere and its `bin` folder added to your PATH (needed by `pdf2image`)

## Installation

```
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
```

## Usage

```
python pdf_inverter.py
```

1. A file dialog opens. Select one or more PDFs, or images.
2. For each PDF, answer the y/n prompts (press the key, no Enter needed):
   - Invert the entire PDF?
   - Are page-wise edits required? (a window opens; drag a box over the area to invert, then press Enter or Space)
   - Enhance the PDF?
   - Make a snippet collage? (drag a box over each snippet to crop)
   - Print the collage to the default printer?
3. For images, enter a name for the output PDF, then choose whether to invert and/or enhance.

## Output

All files are saved in your `Downloads` folder:

| Folder | Contents |
|---|---|
| `Inverted_PDF` | Final PDFs and collage PDFs |
| `Inverted` | Inverted page images and collage pages |
| `UnInverted` | Original (or enhanced) page images |

## Notes

- The `keyboard` library reads key presses globally; if prompts don't respond, try running the terminal as administrator.
- Very large PDFs may take a while to process, since every page is converted to an image.
