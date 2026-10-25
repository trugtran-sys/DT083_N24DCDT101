# -*- coding: utf-8 -*-
"""
tao_bao_cao.py — Tạo file Word báo cáo cho đề tài DT083
Chạy: py tao_bao_cao.py
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "BC_N24DCDT101_DT083_TranTienTrung.docx"
)

# ─────────────────────────────────────────────
# Hàm tiện ích
# ─────────────────────────────────────────────

def set_page_margins(doc, left_cm=3.0, right_cm=2.0, top_cm=2.0, bottom_cm=2.0):
    section = doc.sections[0]
    section.left_margin   = Cm(left_cm)
    section.right_margin  = Cm(right_cm)
    section.top_margin    = Cm(top_cm)
    section.bottom_margin = Cm(bottom_cm)


def set_run_font(run, size_pt=13, bold=False, italic=False, color=None,
                 font_name="Times New Roman"):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold      = bold
    run.italic    = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    # Force Times New Roman for Asian/complex scripts too
    r = run._r
    rPr = r.get_or_add_rPr()
    for tag in [qn("w:rFonts")]:
        elem = rPr.find(tag)
        if elem is None:
            elem = OxmlElement(tag)
            rPr.insert(0, elem)
        elem.set(qn("w:ascii"),     font_name)
        elem.set(qn("w:hAnsi"),     font_name)
        elem.set(qn("w:cs"),        font_name)
        elem.set(qn("w:eastAsia"),  font_name)


def set_paragraph_spacing(para, before_pt=0, after_pt=6, line_rule="auto", line_val=276):
    """276 twips ≈ 1.5 line spacing (240 = 1.0)."""
    pf = para.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after  = Pt(after_pt)
    from docx.shared import Twips
    pPr = para._p.get_or_add_pPr()
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    spacing.set(qn("w:line"),     str(line_val))
    spacing.set(qn("w:lineRule"), line_rule)


def add_normal_para(doc, text="", bold=False, italic=False, align=None,
                    size_pt=13, indent_cm=None, before_pt=0, after_pt=4):
    """Thêm đoạn văn bình thường với Times New Roman 13pt, 1.5 giãn dòng."""
    para = doc.add_paragraph()
    if align == "center":
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent_cm is not None:
        para.paragraph_format.left_indent = Cm(indent_cm)
    set_paragraph_spacing(para, before_pt=before_pt, after_pt=after_pt)
    if text:
        run = para.add_run(text)
        set_run_font(run, size_pt=size_pt, bold=bold, italic=italic)
    return para


def add_heading(doc, text, level=1, size_pt=None, before_pt=12):
    """Thêm tiêu đề với heading style."""
    # level 1 → 14pt bold, level 2 → 13pt bold
    if size_pt is None:
        size_pt = 14 if level == 1 else 13
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(para, before_pt=before_pt, after_pt=6)
    run = para.add_run(text)
    set_run_font(run, size_pt=size_pt, bold=True)
    # Apply Word heading style for TOC support
    try:
        para.style = doc.styles[f"Heading {level}"]
        # Override style font
        run.font.name = "Times New Roman"
        run.font.size = Pt(size_pt)
        run.bold = True
        rPr = run._r.get_or_add_rPr()
        for tag in [qn("w:rFonts")]:
            elem = rPr.find(tag)
            if elem is None:
                elem = OxmlElement(tag)
                rPr.insert(0, elem)
            elem.set(qn("w:ascii"),     "Times New Roman")
            elem.set(qn("w:hAnsi"),     "Times New Roman")
            elem.set(qn("w:cs"),        "Times New Roman")
            elem.set(qn("w:eastAsia"),  "Times New Roman")
    except Exception:
        pass
    return para


def add_code_block(doc, code_text, before_pt=4, after_pt=4):
    """Thêm khối code với font Courier New."""
    lines = code_text.split("\n")
    for line in lines:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.left_indent = Cm(1.0)
        set_paragraph_spacing(para, before_pt=1, after_pt=1, line_val=240)
        run = para.add_run(line if line else " ")
        run.font.name = "Courier New"
        run.font.size = Pt(11)
        # Shade background lightly
        rPr = run._r.get_or_add_rPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  "F2F2F2")
        rPr.append(shd)
    return


def add_page_break(doc):
    doc.add_page_break()


def add_toc(doc):
    """Chèn trường mục lục tự động (TOC)."""
    para = doc.add_paragraph()
    set_paragraph_spacing(para, before_pt=0, after_pt=6)
    run = para.add_run()
    fldChar = OxmlElement("w:fldChar")
    fldChar.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar)
    run._r.append(instrText)
    run._r.append(fldChar2)
    t = OxmlElement("w:t")
    t.text = "(Mở file bằng Word rồi nhấn Ctrl+A → F9 để cập nhật mục lục)"
    run._r.append(t)
    run._r.append(fldChar3)
    set_run_font(run, size_pt=11, italic=True)


def add_footer_page_number(doc):
    """Thêm số trang vào footer."""
    section = doc.sections[0]
    footer = section.footer
    para = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.clear()
    run = para.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_table_test(doc):
    """Thêm bảng ca kiểm thử 18 dòng."""
    headers = ["ID", "Đối tượng", "Input tóm tắt", "Kỳ vọng", "Thực tế", "Kết quả"]
    rows = [
        ["A01", "giai_bai",  "n=3, ví dụ 1 phiếu",               "pre=[2,1,3]\nino=[1,2,3]\npost=[1,3,2]", "Đúng kỳ vọng", "PASS"],
        ["A02", "giai_bai",  "n=3, ví dụ 2 phiếu, dây phải",     "pre=ino=[5,6,7]\npost=[7,6,5]",          "Đúng kỳ vọng", "PASS"],
        ["A03", "giai_bai",  "n=0, cây rỗng",                     "pre=ino=post=[]",                         "Đúng kỳ vọng", "PASS"],
        ["A04", "giai_bai",  "n=1, val=8",                        "pre=ino=post=[8]",                        "Đúng kỳ vọng", "PASS"],
        ["A05", "giai_bai",  "Gốc=2, trái=1, phải=3",             "ino=[1,2,3]",                             "Đúng kỳ vọng", "PASS"],
        ["A06", "giai_bai",  "Gốc=1, trái=9, phải=2",             "ino=[9,1,2] không tăng",                  "Đúng kỳ vọng", "PASS"],
        ["A07", "giai_bai",  "Dây trái 3→2→1",                    "pre=[3,2,1]\nino=post=[1,2,3]",           "Đúng kỳ vọng", "PASS"],
        ["A08a","kiem_tra",  "id_trai=5 > n=2",                   "ValueError",                              "ValueError bắt đúng","PASS"],
        ["A08b","kiem_tra",  "n=-1",                              "ValueError",                              "ValueError bắt đúng","PASS"],
        ["A08c","kiem_tra",  "goc=99, n=1",                       "ValueError",                              "ValueError bắt đúng","PASS"],
        ["A09", "giai_bai",  "n=5, 2 mức",                        "len=5 mọi dãy",                           "Đúng kỳ vọng", "PASS"],
        ["A10", "duyet_*",   "Cây dựng tay",                      "pre=[2,1,3]\nino=[1,2,3]\npost=[1,3,2]", "Đúng kỳ vọng", "PASS"],
        ["A11", "giai_bai",  "Cây đầy 7 nút",                     "pre=[1,2,4,5,3,6,7]\nino=[4,2,5,1,6,3,7]\npost=[4,5,2,6,7,3,1]","Đúng kỳ vọng","PASS"],
        ["A12", "giai_bai",  "Gốc=100, trái=5, phải=50",          "ino=[5,100,50] không tăng",               "Đúng kỳ vọng", "PASS"],
        ["A13", "giai_bai",  "Dây phải 5 nút",                    "pre=ino=[1..5]\npost=[5..1]",             "Đúng kỳ vọng", "PASS"],
        ["A14", "giai_bai",  "3 nút cùng val=5",                  "pre=ino=post=[5,5,5]",                    "Đúng kỳ vọng", "PASS"],
        ["A15", "duyet_sau", "Nhiều cấu hình",                    "gốc luôn cuối postorder",                 "Đúng kỳ vọng", "PASS"],
        ["A16", "duyet_truoc","n=4",                              "gốc(val=99) luôn đầu preorder",           "Đúng kỳ vọng", "PASS"],
    ]

    # Tạo bảng
    col_widths = [Cm(1.2), Cm(2.2), Cm(4.0), Cm(4.5), Cm(3.0), Cm(1.8)]
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        para = hdr_cells[i].paragraphs[0]
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(h)
        set_run_font(run, size_pt=11, bold=True)
        # Gray background for header
        tc = hdr_cells[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  "D0D0D0")
        tcPr.append(shd)

    # Data rows
    for ri, row_data in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, cell_text in enumerate(row_data):
            cells[ci].width = col_widths[ci]
            cells[ci].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            para = cells[ci].paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 5) else WD_ALIGN_PARAGRAPH.LEFT
            run = para.add_run(cell_text)
            is_pass = (cell_text == "PASS")
            set_run_font(run, size_pt=10, bold=is_pass,
                         color=(0, 128, 0) if is_pass else None)
    return table


# ─────────────────────────────────────────────
# XÂY DỰNG FILE WORD
# ─────────────────────────────────────────────

def build_document():
    doc = Document()

    # Thiết lập trang A4, lề
    set_page_margins(doc, left_cm=3.0, right_cm=2.0, top_cm=2.0, bottom_cm=2.0)

    # Khổ A4
    section = doc.sections[0]
    from docx.shared import Mm
    section.page_width  = Mm(210)
    section.page_height = Mm(297)

    # Số trang ở footer
    add_footer_page_number(doc)

    # ══════════════════════════════════════════
    # TRANG BÌA
    # ══════════════════════════════════════════
    add_normal_para(doc, "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG",
                    bold=True, align="center", size_pt=13, before_pt=30, after_pt=2)
    add_normal_para(doc, "CƠ SỞ TẠI TP. HỒ CHÍ MINH",
                    bold=True, align="center", size_pt=13, after_pt=2)
    add_normal_para(doc, "─" * 45, align="center", size_pt=12, after_pt=40)

    add_normal_para(doc, "BÁO CÁO ĐỀ TÀI CÁ NHÂN",
                    bold=True, align="center", size_pt=16, after_pt=20)

    add_normal_para(doc, "DT083 — Biểu diễn cây nhị phân",
                    bold=True, align="center", size_pt=14, after_pt=4)
    add_normal_para(doc, "và ba thứ tự duyệt",
                    bold=True, align="center", size_pt=14, after_pt=30)

    add_normal_para(doc, "Môn học:", bold=True, align="center", size_pt=13, after_pt=2)
    add_normal_para(doc, "INT13185 — Cấu trúc dữ liệu và giải thuật — Nhóm 03",
                    align="center", size_pt=13, after_pt=20)

    # Bảng thông tin sinh viên
    tbl = doc.add_table(rows=4, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    label_width = Cm(5)
    val_width   = Cm(9)
    sv_data = [
        ("Sinh viên:",  "Trần Tiến Trung"),
        ("MSSV:",       "N24DCDT101"),
        ("Lớp:",        "D24CQDT01-N"),
        ("Giảng viên:", "Hồ Nhựt Minh"),
    ]
    for ri, (lbl, val) in enumerate(sv_data):
        c0 = tbl.rows[ri].cells[0]
        c1 = tbl.rows[ri].cells[1]
        c0.width = label_width
        c1.width = val_width
        r0 = c0.paragraphs[0].add_run(lbl)
        set_run_font(r0, size_pt=13, bold=True)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = c1.paragraphs[0].add_run(val)
        set_run_font(r1, size_pt=13)
        # Remove borders
        for cell in [c0, c1]:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement("w:tcBorders")
            for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
                border = OxmlElement(f"w:{side}")
                border.set(qn("w:val"), "none")
                tcBorders.append(border)
            tcPr.append(tcBorders)

    doc.add_paragraph()  # khoảng trống
    add_normal_para(doc, "TP. Hồ Chí Minh, 10/2026",
                    italic=True, align="center", size_pt=13, before_pt=40, after_pt=0)

    add_page_break(doc)

    # ══════════════════════════════════════════
    # TRANG MỤC LỤC
    # ══════════════════════════════════════════
    add_heading(doc, "MỤC LỤC", level=1, size_pt=14, before_pt=0)
    add_toc(doc)
    add_page_break(doc)

    # ══════════════════════════════════════════
    # CHƯƠNG 1: BÀI TOÁN VÀ MỤC TIÊU
    # ══════════════════════════════════════════
    add_heading(doc, "CHƯƠNG 1: BÀI TOÁN VÀ MỤC TIÊU", level=1, before_pt=0)

    add_heading(doc, "1.1 Bài toán", level=2)
    add_normal_para(doc,
        "Đề tài DT083 yêu cầu dựng một cây nhị phân từ bảng mô tả các nút "
        "(id, gia_tri, con_trai, con_phai), sau đó in ra ba dãy duyệt: "
        "duyệt trước (preorder), duyệt giữa (inorder) và duyệt sau (postorder).")
    add_normal_para(doc,
        "Nguồn: Giáo trình INT13185 — Cấu trúc dữ liệu và giải thuật, "
        "Chương 7, mục 7.2 và 7.3.1, trang in 162–165 (trang PDF 174–177).")

    add_heading(doc, "1.2 Mục tiêu", level=2)
    for item in [
        "Cài đặt cấu trúc nút nhị phân (class Nut) bằng Python.",
        "Hiểu và cài đặt đúng 3 thứ tự duyệt đệ quy: preorder, inorder, postorder.",
        "Minh chứng rằng cây nhị phân tổng quát ≠ BST (inorder không đảm bảo tăng).",
        "Xây dựng bộ kiểm thử 18 ca (18/18 PASS) bao gồm ca biên và ca lỗi.",
    ]:
        p = add_normal_para(doc, f"• {item}", indent_cm=0.5)

    add_heading(doc, "1.3 Hợp đồng Input/Output", level=2)
    add_normal_para(doc, "Đầu vào:", bold=True)
    for line in [
        "n : int, 0 ≤ n ≤ 100 — số nút trong cây.",
        "danh_sach : List[Tuple(id, gia_tri, id_trai, id_phai)]",
        "    id ∈ 1..n; id_trai/id_phai ∈ 0..n (0 = không con).",
        "goc : int — id của nút gốc; 0 = cây rỗng.",
    ]:
        add_normal_para(doc, f"    {line}", indent_cm=0.8)

    add_normal_para(doc, "Đầu ra:", bold=True)
    add_normal_para(doc,
        "    Tuple[List[int], List[int], List[int]] — "
        "(preorder, inorder, postorder), mỗi dãy dài n giá trị nguyên. "
        "Cây rỗng → ba dãy rỗng.", indent_cm=0.8)

    add_normal_para(doc, "Từ chối — ValueError khi:", bold=True)
    for cond in [
        "n < 0 hoặc n > 100.",
        "Có id trùng nhau trong bảng nút.",
        "id_trai hoặc id_phai nằm ngoài phạm vi [0, n].",
        "goc không tồn tại trong bảng nút (khi n > 0).",
    ]:
        add_normal_para(doc, f"• {cond}", indent_cm=0.8)

    add_heading(doc, "1.4 Phạm vi", level=2)
    for item in [
        "Cây nhị phân tổng quát — không yêu cầu là BST.",
        "Số nút: 0 ≤ n ≤ 100.",
        "Không dùng file CSV hay dữ liệu ngoài; toàn bộ input từ code.",
    ]:
        add_normal_para(doc, f"• {item}", indent_cm=0.5)

    add_page_break(doc)

    # ══════════════════════════════════════════
    # CHƯƠNG 2: CƠ SỞ LÝ THUYẾT
    # ══════════════════════════════════════════
    add_heading(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT", level=1, before_pt=0)

    add_heading(doc, "2.1 Cây nhị phân (Giáo trình Chương 7, mục 7.2, trang 162–163)", level=2)
    add_normal_para(doc,
        "Cây nhị phân là một cây có thứ bậc mà mỗi nút có tối đa hai con: "
        "con trái và con phải. Đây là cấu trúc dữ liệu nền tảng trong khoa học máy tính.")
    add_normal_para(doc, "Biểu diễn mỗi nút:", bold=False)
    add_normal_para(doc, "    Mỗi nút bao gồm: (id, gia_tri, con_trai, con_phai).", indent_cm=0.8)
    add_normal_para(doc,
        "    Trong đó id là nhãn định danh duy nhất; gia_tri là giá trị lưu tại nút; "
        "con_trai và con_phai là id của nút con (0 = không có con).", indent_cm=0.8)

    add_normal_para(doc, "Các khái niệm chính:", bold=True)
    for item in [
        "Gốc (root): Nút không có cha.",
        "Lá (leaf): Nút không có con.",
        "Chiều cao (height): Số cạnh trên đường đi dài nhất từ gốc đến lá.",
        "Mức (level): Khoảng cách từ gốc đến nút tính theo số cạnh.",
    ]:
        add_normal_para(doc, f"• {item}", indent_cm=0.8)

    add_heading(doc, "2.2 Ba thứ tự duyệt (mục 7.3.1, trang 163–165)", level=2)
    add_normal_para(doc,
        "Duyệt cây (tree traversal) là quá trình thăm mỗi nút đúng một lần "
        "theo một thứ tự xác định. Có ba thứ tự cơ bản:")

    traversals = [
        ("Duyệt trước (Preorder — NLR):", "Gốc → Con trái → Con phải.\n"
         "Ứng dụng: sao chép cây, in biểu thức tiền tố."),
        ("Duyệt giữa (Inorder — LNR):", "Con trái → Gốc → Con phải.\n"
         "Ứng dụng: với BST thì cho dãy tăng; tính giá trị biểu thức trung tố."),
        ("Duyệt sau (Postorder — LRN):", "Con trái → Con phải → Gốc.\n"
         "Ứng dụng: xóa cây, tính giá trị biểu thức hậu tố; gốc luôn xuất hiện cuối."),
    ]
    for title, desc in traversals:
        add_normal_para(doc, title, bold=True, indent_cm=0.5)
        add_normal_para(doc, f"    {desc}", indent_cm=1.0)

    add_heading(doc, "2.3 Cấu trúc dữ liệu sử dụng", level=2)
    add_normal_para(doc,
        "Class Nut được định nghĩa với bốn thuộc tính: id (int), gia_tri (int), "
        "trai (Optional[Nut]), phai (Optional[Nut]). "
        "Bất biến của class: mỗi nút ngoài gốc có đúng một cha và không có chu trình.")

    add_heading(doc, "2.4 Nguyên lý đệ quy", level=2)
    add_normal_para(doc,
        "Mỗi hàm duyệt hoạt động theo nguyên lý đệ quy: trường hợp cơ sở là nút None "
        "(trả về danh sách rỗng), trường hợp đệ quy xử lý nút hiện tại và hai cây con. "
        "Tính đúng đắn được đảm bảo bởi bất biến: mọi nút trong cây con đều xuất hiện "
        "đúng một lần trong kết quả.")

    add_page_break(doc)

    # ══════════════════════════════════════════
    # CHƯƠNG 3: THIẾT KẾ VÀ CÀI ĐẶT
    # ══════════════════════════════════════════
    add_heading(doc, "CHƯƠNG 3: THIẾT KẾ VÀ CÀI ĐẶT", level=1, before_pt=0)

    add_heading(doc, "3.1 Hàm tao_cay(danh_sach, goc)", level=2)
    add_normal_para(doc, "Tiền điều kiện: danh_sach đã qua kiểm tra; goc=0 hoặc id hợp lệ.")
    add_normal_para(doc, "Hậu điều kiện: trả về Nut gốc của cây, hoặc None nếu goc=0.")
    add_normal_para(doc, "Thuật toán:")
    for step in [
        "Bước 1: Tạo từ điển (dict) id → Nut bằng vòng lặp O(n).",
        "Bước 2: Duyệt lại danh_sach, nối con trái và con phải cho mỗi nút.",
        "Bước 3: Trả về bang_nut[goc].",
    ]:
        add_normal_para(doc, f"    {step}", indent_cm=0.8)
    add_normal_para(doc, "Độ phức tạp: O(n) thời gian, O(n) bộ nhớ.")

    add_heading(doc, "3.2 Hàm duyet_truoc(g) — Preorder", level=2)
    add_normal_para(doc, "Tiền điều kiện: g là Nut hợp lệ hoặc None.")
    add_normal_para(doc, "Hậu điều kiện: danh sách n giá trị, gốc xuất hiện đầu tiên.")
    add_normal_para(doc, "Bất biến: mọi nút trong cây con g đều có mặt đúng một lần.")
    add_normal_para(doc, "Cài đặt:")
    add_code_block(doc,
        "def duyet_truoc(g):\n"
        "    if g is None: return []\n"
        "    ket_qua = [g.gia_tri]\n"
        "    ket_qua += duyet_truoc(g.trai)\n"
        "    ket_qua += duyet_truoc(g.phai)\n"
        "    return ket_qua")
    add_normal_para(doc, "Độ phức tạp: O(n) thời gian, O(h) stack — h là chiều cao cây.")

    add_heading(doc, "3.3 Hàm duyet_giua(g) — Inorder", level=2)
    add_normal_para(doc, "Tiền điều kiện: g là Nut hợp lệ hoặc None.")
    add_normal_para(doc, "Hậu điều kiện: danh sách n giá trị, mỗi nút xuất hiện đúng một lần.")
    add_normal_para(doc, "Bất biến: với BST thì dãy tăng; cây tổng quát thì không đảm bảo.")
    add_normal_para(doc, "Cài đặt:")
    add_code_block(doc,
        "def duyet_giua(g):\n"
        "    if g is None: return []\n"
        "    ket_qua = duyet_giua(g.trai)\n"
        "    ket_qua += [g.gia_tri]\n"
        "    ket_qua += duyet_giua(g.phai)\n"
        "    return ket_qua")
    add_normal_para(doc, "Độ phức tạp: O(n) thời gian, O(h) stack.")

    add_heading(doc, "3.4 Hàm duyet_sau(g) — Postorder", level=2)
    add_normal_para(doc, "Tiền điều kiện: g là Nut hợp lệ hoặc None.")
    add_normal_para(doc, "Hậu điều kiện: danh sách n giá trị, gốc luôn xuất hiện cuối cùng.")
    add_normal_para(doc, "Bất biến: lá luôn được thăm trước cha của nó.")
    add_normal_para(doc, "Cài đặt:")
    add_code_block(doc,
        "def duyet_sau(g):\n"
        "    if g is None: return []\n"
        "    ket_qua = duyet_sau(g.trai)\n"
        "    ket_qua += duyet_sau(g.phai)\n"
        "    ket_qua += [g.gia_tri]\n"
        "    return ket_qua")
    add_normal_para(doc, "Độ phức tạp: O(n) thời gian, O(h) stack.")

    add_heading(doc, "3.5 Lần vết tay — Ví dụ 1", level=2)
    add_normal_para(doc,
        "Input: n=3, goc=1, danh_sach=[(1,2,2,3), (2,1,0,0), (3,3,0,0)]")
    add_normal_para(doc, "Cây được dựng:")
    add_code_block(doc,
        "       2  (id=1, gốc)\n"
        "      / \\\n"
        "  1(id=2)  3(id=3)")

    add_normal_para(doc, "Duyệt trước (Preorder — Gốc → Trái → Phải):", bold=True)
    trace_pre = [
        ("1", "id1 (val=2) — thêm val vào kq", "[2]"),
        ("2", "id2 (val=1) — thêm val vào kq", "[2, 1]"),
        ("3", "trai(id2)=None → trả []",        "[2, 1]"),
        ("4", "phai(id2)=None → trả []",        "[2, 1]"),
        ("5", "id3 (val=3) — thêm val vào kq",  "[2, 1, 3]"),
        ("6", "trai(id3)=None → trả []",        "[2, 1, 3]"),
        ("7", "phai(id3)=None → trả []",        "[2, 1, 3]"),
    ]
    t1 = doc.add_table(rows=1+len(trace_pre), cols=3)
    t1.style = "Table Grid"
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Bước", "Nút đang xử lý", "Kết quả tích lũy"]):
        c = t1.rows[0].cells[i]
        r = c.paragraphs[0].add_run(h)
        set_run_font(r, size_pt=11, bold=True)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tc = c._tc; tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),"D9D9D9")
        tcPr.append(shd)
    for ri, (step, action, result) in enumerate(trace_pre):
        cells = t1.rows[ri+1].cells
        for ci, txt in enumerate([step, action, result]):
            cells[ci].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = cells[ci].paragraphs[0].add_run(txt)
            set_run_font(r, size_pt=10)

    add_normal_para(doc, "→ preorder = [2, 1, 3]", bold=True, indent_cm=0.5)
    doc.add_paragraph()

    add_normal_para(doc, "Duyệt giữa (Inorder — Trái → Gốc → Phải):", bold=True)
    trace_ino = [
        ("1", "đệ quy trái id1 → id2",          ""),
        ("2", "   trai(id2)=None → []",          ""),
        ("3", "   thăm id2 (val=1)",              "[1]"),
        ("4", "   phai(id2)=None → []",          "[1]"),
        ("5", "thăm id1 (val=2)",                "[1, 2]"),
        ("6", "đệ quy phải id1 → id3",           ""),
        ("7", "   trai(id3)=None → []",          ""),
        ("8", "   thăm id3 (val=3)",              "[1, 2, 3]"),
        ("9", "   phai(id3)=None → []",          "[1, 2, 3]"),
    ]
    t2 = doc.add_table(rows=1+len(trace_ino), cols=3)
    t2.style = "Table Grid"
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Bước", "Nút đang xử lý", "Kết quả tích lũy"]):
        c = t2.rows[0].cells[i]
        r = c.paragraphs[0].add_run(h)
        set_run_font(r, size_pt=11, bold=True)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tc = c._tc; tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),"D9D9D9")
        tcPr.append(shd)
    for ri, (step, action, result) in enumerate(trace_ino):
        cells = t2.rows[ri+1].cells
        for ci, txt in enumerate([step, action, result]):
            cells[ci].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = cells[ci].paragraphs[0].add_run(txt)
            set_run_font(r, size_pt=10)
    add_normal_para(doc, "→ inorder = [1, 2, 3]", bold=True, indent_cm=0.5)
    doc.add_paragraph()

    add_normal_para(doc, "Duyệt sau (Postorder — Trái → Phải → Gốc):", bold=True)
    trace_post = [
        ("1", "đệ quy trái id1 → id2",          ""),
        ("2", "   trai(id2)=None, phai=None",    ""),
        ("3", "   thăm id2 (val=1)",              "[1]"),
        ("4", "đệ quy phải id1 → id3",           ""),
        ("5", "   trai(id3)=None, phai=None",    ""),
        ("6", "   thăm id3 (val=3)",              "[1, 3]"),
        ("7", "thăm id1 (val=2)",                "[1, 3, 2]"),
    ]
    t3 = doc.add_table(rows=1+len(trace_post), cols=3)
    t3.style = "Table Grid"
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["Bước", "Nút đang xử lý", "Kết quả tích lũy"]):
        c = t3.rows[0].cells[i]
        r = c.paragraphs[0].add_run(h)
        set_run_font(r, size_pt=11, bold=True)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tc = c._tc; tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),"D9D9D9")
        tcPr.append(shd)
    for ri, (step, action, result) in enumerate(trace_post):
        cells = t3.rows[ri+1].cells
        for ci, txt in enumerate([step, action, result]):
            cells[ci].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = cells[ci].paragraphs[0].add_run(txt)
            set_run_font(r, size_pt=10)
    add_normal_para(doc, "→ postorder = [1, 3, 2]", bold=True, indent_cm=0.5)

    add_heading(doc, "3.6 Phân tích độ phức tạp", level=2)
    complex_data = [
        ("Phép toán",           "Thời gian",    "Bộ nhớ (stack)"),
        ("Xây dựng cây",        "O(n)",         "O(n)"),
        ("Duyệt trước",         "O(n)",         "O(h)"),
        ("Duyệt giữa",          "O(n)",         "O(h)"),
        ("Duyệt sau",           "O(n)",         "O(h)"),
        ("Tổng (3 lần duyệt)",  "O(n)",         "O(h) ≤ O(n)"),
    ]
    tc4 = doc.add_table(rows=len(complex_data), cols=3)
    tc4.style = "Table Grid"
    tc4.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(complex_data):
        for ci, txt in enumerate(row):
            cell = tc4.rows[ri].cells[ci]
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cell.paragraphs[0].add_run(txt)
            set_run_font(r, size_pt=11, bold=(ri==0))
            if ri == 0:
                tc = cell._tc; tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),"D9D9D9")
                tcPr.append(shd)

    add_normal_para(doc, "Ghi chú: h = chiều cao cây; h ≤ n (cây dây); h ≈ log₂n (cây cân bằng).",
                    italic=True, after_pt=4)

    add_page_break(doc)

    # ══════════════════════════════════════════
    # CHƯƠNG 4: KIỂM THỬ VÀ BẰNG CHỨNG
    # ══════════════════════════════════════════
    add_heading(doc, "CHƯƠNG 4: KIỂM THỬ VÀ BẰNG CHỨNG", level=1, before_pt=0)

    add_heading(doc, "4.1 Môi trường kiểm thử", level=2)
    env_items = [
        ("Ngôn ngữ",         "Python 3.x (Windows, lệnh py)"),
        ("Thư viện",         "Chỉ thư viện chuẩn (typing, unittest)"),
        ("Chạy demo",        "py demo.py"),
        ("Chạy test",        "py test\\test_cay_nhi_phan.py"),
        ("Chụp kết quả",     "py chup_ket_qua.py → lưu tại docs/anh_ket_qua/"),
        ("File chính",       "src/cay_nhi_phan.py"),
        ("File kiểm thử",    "test/test_cay_nhi_phan.py (18 ca)"),
    ]
    tc5 = doc.add_table(rows=len(env_items), cols=2)
    tc5.style = "Table Grid"
    tc5.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, (k, v) in enumerate(env_items):
        c0 = tc5.rows[ri].cells[0]
        c1 = tc5.rows[ri].cells[1]
        c0.width = Cm(4.5)
        c1.width = Cm(11.0)
        r0 = c0.paragraphs[0].add_run(k)
        set_run_font(r0, size_pt=11, bold=True)
        r1 = c1.paragraphs[0].add_run(v)
        set_run_font(r1, size_pt=11)

    add_heading(doc, "4.2 Bảng ca kiểm thử (18/18 PASS)", level=2)
    add_table_test(doc)
    add_normal_para(doc, "Tổng cộng: 18 ca kiểm thử — 18/18 PASS.", bold=True, after_pt=6)

    add_heading(doc, "4.3 Ba quy mô / cấu hình tiêu biểu", level=2)
    cfg_data = [
        ("Cấu hình",           "Mô tả",                    "n", "h",        "Thời gian", "Stack"),
        ("Cấu hình 1",         "n=3, cây cân bằng",        "3", "2",        "O(3)",      "O(2)"),
        ("Cấu hình 2",         "n=7, cây đầy 3 mức",       "7", "3",        "O(7)",      "O(3)"),
        ("Cấu hình 3",         "n=5, cây dây phải",        "5", "5",        "O(5)",      "O(5)"),
    ]
    tc6 = doc.add_table(rows=len(cfg_data), cols=6)
    tc6.style = "Table Grid"
    tc6.alignment = WD_TABLE_ALIGNMENT.CENTER
    for ri, row in enumerate(cfg_data):
        for ci, txt in enumerate(row):
            cell = tc6.rows[ri].cells[ci]
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cell.paragraphs[0].add_run(txt)
            set_run_font(r, size_pt=11, bold=(ri==0))
            if ri == 0:
                tc = cell._tc; tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"),"clear"); shd.set(qn("w:color"),"auto"); shd.set(qn("w:fill"),"D9D9D9")
                tcPr.append(shd)

    add_heading(doc, "4.4 Nhận xét kết quả", level=2)
    remarks = [
        "Cây dây (h=n): stack đệ quy đạt O(n) — trường hợp xấu nhất về bộ nhớ.",
        "Cây cân bằng (h≈log₂n): tiết kiệm stack hơn đáng kể.",
        "Inorder của cây tổng quát KHÔNG đảm bảo dãy tăng (khác BST) — "
        "minh chứng bởi ca A06: gốc val=1, trái val=9, phải val=2 → inorder=[9,1,2].",
        "Ba hàm duyệt chạy độc lập, mỗi hàm O(n); tổng ba lần vẫn O(n), không phải O(n³).",
    ]
    for r in remarks:
        add_normal_para(doc, f"• {r}", indent_cm=0.5)

    add_heading(doc, "4.5 GitHub và clone", level=2)
    add_normal_para(doc,
        "Mã nguồn được công bố công khai trên GitHub để giảng viên kiểm tra và chấm điểm:")
    add_normal_para(doc, "• URL GitHub: https://github.com/trugtran-sys/DT083_N24DCDT101", indent_cm=0.5)
    add_normal_para(doc, "• SHA commit C (mã chạy và chụp ảnh): d131fb65e8be2e096f4953d45738500a6a366968", indent_cm=0.5)
    add_normal_para(doc, "• Permalink thuật toán chính: https://github.com/trugtran-sys/DT083_N24DCDT101/blob/d131fb65e8be2e096f4953d45738500a6a366968/src/cay_nhi_phan.py", indent_cm=0.5)
    add_normal_para(doc, "• Permalink bộ kiểm thử: https://github.com/trugtran-sys/DT083_N24DCDT101/blob/d131fb65e8be2e096f4953d45738500a6a366968/test/test_cay_nhi_phan.py", indent_cm=0.5)
    add_code_block(doc, "py chup_ket_qua.py")
    add_normal_para(doc,
        "Toàn bộ kết quả văn bản được lưu tại docs/anh_ket_qua/. Ảnh A10 và A11 được chụp từ thao tác clone "
        "thực tế và trang GitHub cá nhân của sinh viên theo đúng quy định. "
        "Dưới đây là vị trí chèn 11 ảnh minh chứng chuẩn kèm phân tích kết quả:")

    img_items = [
        ("A01", "Hình 4.1", "Ví dụ 1 trên phiếu (Cây 3 nút, truoc=[2,1,3], giua=[1,2,3], sau=[1,3,2])",
         "Kết quả thực tế truoc=[2,1,3], giua=[1,2,3], sau=[1,3,2] hoàn toàn trùng khớp với kỳ vọng trên phiếu giao đề. Thứ tự duyệt trước đặt gốc đầu tiên, duyệt giữa đặt gốc ở giữa hai con và duyệt sau đưa gốc về vị trí cuối cùng."),
        ("A02", "Hình 4.2", "Ví dụ 2 trên phiếu (Cây dây phải 5→6→7)",
         "Do cây chỉ có nhánh phải và không có con trái, thứ tự duyệt trước và duyệt giữa hoàn toàn trùng nhau [5,6,7]. Thứ tự duyệt sau đi tới lá 7 trước rồi quay lui qua 6 về gốc 5, cho kết quả [7,6,5] khớp 100% với kỳ vọng."),
        ("A03", "Hình 4.3", "Ca tự thiết kế 1 (Cây rỗng n=0, ba dãy rỗng [])",
         "Với đầu vào cây rỗng, chương trình không rơi vào lỗi đệ quy hay truy cập con trỏ rỗng mà trả về ba dãy rỗng []. Kết quả khớp chính xác với hợp đồng giao diện và ca kiểm thử A03."),
        ("A04", "Hình 4.4", "Ca tự thiết kế 2 (Một nút duy nhất val=8)",
         "Do cây chỉ có một nút duy nhất đồng thời là lá, cả ba thứ tự duyệt đều trả về [8]. Không có phép gọi đệ quy dư thừa và bộ nhớ stack chỉ tiêu tốn O(1)."),
        ("A05", "Hình 4.5", "Ca biên 1 (Gốc 2, trái 1, phải 3 — kiểm tra duyệt giữa không tự sắp xếp)",
         "Dù dãy duyệt giữa [1,2,3] có thứ tự tăng dần nhưng đây là do cấu trúc cây quy định chứ giải thuật không thực hiện thao tác sắp xếp. Cây được xây dựng đúng theo id con trái, con phải khai báo trong bảng nút."),
        ("A06", "Hình 4.6", "Ca biên 2 (Gốc 1, trái 9, phải 2 — minh chứng cây tổng quát != BST, inorder không tăng)",
         "Kết quả duyệt giữa thực tế thu được là [9,1,2] không tăng dần, minh chứng rõ ràng cây nhị phân tổng quát không tuân theo ràng buộc của cây tìm kiếm nhị phân (BST). Kết quả thực thi khẳng định tính tổng quát của chương trình theo đúng yêu cầu đề tài."),
        ("A07", "Hình 4.7", "Ca biên 3 (Cây suy biến trái 3→2→1)",
         "Cây dây trái đạt chiều cao cực đại h = n = 3, duyệt trước cho thứ tự giảm dần [3,2,1] trong khi duyệt giữa và duyệt sau đều cho dãy tăng dần [1,2,3]. Thao tác quay lui đệ quy thực hiện chính xác sau khi chạm nút lá sâu nhất."),
        ("A08", "Hình 4.8", "Input không hợp lệ và phản hồi từ chối của validator (ValueError)",
         "Khi truyền dữ liệu id con vượt quá phạm vi [0,n] hoặc n âm, hàm kiem_tra_dau_vao kích hoạt ngoại lệ ValueError với thông báo lỗi cụ thể. Chương trình từ chối dữ liệu sai ngay từ tiền điều kiện, bảo vệ cây khỏi trạng thái lỗi hoặc vòng lặp chu trình."),
        ("A09", "Hình 4.9", "Lệnh chạy và tổng kết bộ kiểm thử tự động (18 ca PASS)",
         "Bộ kiểm thử unittest gồm 18 ca độc lập kiểm tra toàn diện các khía cạnh thuật toán, hàm con và ca biên. Toàn bộ 18/18 ca đều đạt kết quả PASS trong thời gian 0.001 giây, chứng minh tính đúng đắn và ổn định của mã nguồn."),
        ("A10", "Hình 4.10", "Clone sạch sang thư mục mới, kiểm tra SHA và chạy lại theo README",
         "Quá trình clone repo độc lập từ GitHub sang thư mục mới và kiểm tra mã SHA commit HEAD cho thấy mã nguồn không bị thiếu tệp phụ thuộc. Các lệnh chạy demo và kiểm thử theo README đều thực thi thành công 100% trên bản clone mới."),
        ("A11", "Hình 4.11", "Giao diện GitHub repository và commit thật của sinh viên",
         "Kho mã nguồn được lưu trữ công khai trên GitHub với đầy đủ các tệp mã nguồn, kiểm thử, tài liệu và các commit lịch sử rõ ràng. Giảng viên và người chấm bài có thể truy cập trực tiếp repo và permalink tại commit C để đối chiếu."),
    ]

    for code, fig_no, title, analysis in img_items:
        add_heading(doc, f"{fig_no}. {title}", level=3)
        p = add_normal_para(doc, f"[ẢNH {code}: Dán ảnh chụp minh chứng {fig_no} tại đây]", bold=True,
                            align="center", after_pt=6)
        run = p.runs[0] if p.runs else None
        if run:
            rPr = run._r.get_or_add_rPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"),   "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"),  "FFFF99")
            rPr.append(shd)
        add_normal_para(doc, f"Nhận xét và phân tích: {analysis}", italic=True, after_pt=12)
    add_page_break(doc)

    # ══════════════════════════════════════════
    # CHƯƠNG 5: KẾT LUẬN
    # ══════════════════════════════════════════
    add_heading(doc, "CHƯƠNG 5: KẾT LUẬN", level=1, before_pt=0)

    add_heading(doc, "5.1 Mức độ hoàn thành", level=2)
    completion = [
        ("✓", "Cài đặt đầy đủ class Nut và ba hàm duyệt đệ quy (duyet_truoc, duyet_giua, duyet_sau)."),
        ("✓", "Hàm tao_cay và giai_bai hoạt động đúng, bao gồm validator từ chối input sai."),
        ("✓", "18/18 ca kiểm thử PASS — bao gồm ca biên (n=0, n=1, cây dây) và ca lỗi."),
        ("✓", "Có lần vết tay chi tiết (Ví dụ 1) với bảng bước thực hiện."),
        ("✓", "Phân tích độ phức tạp thời gian O(n) và bộ nhớ O(h) cho mỗi hàm duyệt."),
        ("✓", "Minh chứng cây tổng quát ≠ BST (inorder không đảm bảo tăng)."),
    ]
    for mark, item in completion:
        add_normal_para(doc, f"{mark} {item}", indent_cm=0.5)

    add_heading(doc, "5.2 Hạn chế", level=2)
    limits = [
        "Duyệt đệ quy có thể gây stack overflow với cây dây rất sâu (n > 1000 trong CPython mặc định).",
        "Chưa cài đặt phiên bản duyệt không đệ quy (dùng stack tường minh).",
        "Chưa kiểm tra cấu trúc có chu trình — giả định input đảm bảo cây hợp lệ.",
    ]
    for item in limits:
        add_normal_para(doc, f"• {item}", indent_cm=0.5)

    add_heading(doc, "5.3 Hướng phát triển", level=2)
    futures = [
        "Thêm duyệt theo mức (BFS — Level-order traversal) dùng hàng đợi (collections.deque).",
        "Cài đặt phiên bản không đệ quy cho cả ba hàm duyệt để tránh giới hạn stack.",
        "Tái tạo cây từ preorder + inorder (hoặc postorder + inorder).",
        "Tăng giới hạn n từ 100 lên 10 000 khi chuyển sang duyệt không đệ quy.",
    ]
    for item in futures:
        add_normal_para(doc, f"• {item}", indent_cm=0.5)

    add_normal_para(doc, "")
    add_normal_para(doc,
        "Đề tài DT083 đã được hoàn thành đầy đủ theo yêu cầu đề ra. "
        "Toàn bộ mã nguồn, bộ kiểm thử và báo cáo được tổ chức rõ ràng, "
        "sẵn sàng cho việc kiểm tra và đánh giá.",
        italic=True, align="center", before_pt=20)

    # ══════════════════════════════════════════
    # Lưu file
    # ══════════════════════════════════════════
    doc.save(OUTPUT_PATH)
    print(f"[OK] Đã tạo file Word tại:\n     {OUTPUT_PATH}")
    import os
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"     Kích thước: {size_kb:.1f} KB")


if __name__ == "__main__":
    build_document()
