

!pip install docling[ocr] --quiet
!apt-get install -y poppler-utils > /dev/null

from docling.document_converter import DocumentConverter
from google.colab import files


uploaded = files.upload()
pdf_path = list(uploaded.keys())[0]


converter = DocumentConverter()
result = converter.convert(pdf_path)
doc = result.document


def find_block_attribute(page):
    for attr in dir(page):
        if not attr.startswith("_"):
            val = getattr(page, attr)
            if isinstance(val, list) and len(val) > 0:
                first = val[0]
                if hasattr(first, "block_type"):
                    return attr
    return None


for page_num, page in doc.pages.items():
    print(f"\n--- Page {page_num} ---")
    block_attr = find_block_attribute(page)
    if not block_attr:
        print("No readable content found on this page.")
        continue
    blocks = getattr(page, block_attr)
    for block in blocks:
        if block.block_type == "table":
            print("[Table]")
            for row in block.rows:
                print("\t".join(cell.text.strip().replace("\n", " ") for cell in row.cells))
        else:
            print(block.text.strip())
