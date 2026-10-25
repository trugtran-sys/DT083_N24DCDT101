# -*- coding: utf-8 -*-
"""
demo.py — DT083: Biểu diễn cây nhị phân và ba thứ tự duyệt
Sinh viên: Trần Tiến Trung — N24DCDT101 — D24CQDT01-N

Chạy:  py demo.py
Mỗi ví dụ in: input rõ ràng, kết quả mong đợi, kết quả thực tế, và lần vết.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from cay_nhi_phan import giai_bai, tao_cay, duyet_truoc, duyet_giua, duyet_sau, Nut

# ──────────────────────────────────────────────────────────────
# Hàm tiện ích in kết quả
# ──────────────────────────────────────────────────────────────

def in_phan_cach(title: str = "", ky_tu: str = "=", do_rong: int = 62):
    if title:
        side = (do_rong - len(title) - 2) // 2
        print(ky_tu * side + f" {title} " + ky_tu * side)
    else:
        print(ky_tu * do_rong)


def in_ket_qua(ma_ca, mo_ta, n, danh_sach, goc,
               pre_exp, ino_exp, post_exp):
    """In một ca kiểm/demo với đầy đủ thông tin."""
    in_phan_cach(ma_ca, "-")
    print(f"Mô tả  : {mo_ta}")
    print(f"Input  : n={n}, goc={goc}")
    print(f"         danh_sach={danh_sach}")
    print(f"Kỳ vọng: truoc={pre_exp}, giua={ino_exp}, sau={post_exp}")
    try:
        pre, ino, post = giai_bai(n, danh_sach, goc)
        print(f"Thực tế: truoc={pre}, giua={ino}, sau={post}")
        ok = (pre == pre_exp and ino == ino_exp and post == post_exp)
        print(f"Kết quả: {'✓ PASS' if ok else '✗ FAIL'}")
    except ValueError as e:
        print(f"ValueError: {e}")
        # Nếu kỳ vọng là lỗi thì coi là PASS
        if pre_exp is None:
            print("Kết quả: ✓ PASS (kỳ vọng lỗi)")
        else:
            print("Kết quả: ✗ FAIL (không kỳ vọng lỗi)")


# ──────────────────────────────────────────────────────────────
# Hàm vẽ cây dạng ASCII (hỗ trợ lần vết)
# ──────────────────────────────────────────────────────────────

def ve_cay(g, prefix="", is_left=True):
    """In sơ đồ cây dạng văn bản để minh họa cấu trúc."""
    if g is None:
        return
    connector = "├── " if is_left else "└── "
    print(prefix + connector + f"[id={g.id} val={g.gia_tri}]")
    new_prefix = prefix + ("│   " if is_left else "    ")
    if g.trai or g.phai:
        ve_cay(g.trai,  new_prefix, is_left=True)
        ve_cay(g.phai, new_prefix, is_left=False)


def in_cay(danh_sach, goc):
    """In sơ đồ ASCII cho cây đã cho."""
    cay = tao_cay(danh_sach, goc)
    if cay is None:
        print("  (cây rỗng)")
        return
    print(f"  ROOT [id={cay.id} val={cay.gia_tri}]")
    prefix = "  "
    if cay.trai or cay.phai:
        ve_cay(cay.trai, prefix, is_left=True)
        ve_cay(cay.phai, prefix, is_left=False)


# ──────────────────────────────────────────────────────────────
# Lần vết tay (Trace) — A01/A02 được minh họa thủ công dưới đây
# ──────────────────────────────────────────────────────────────

def in_lan_vet_vi_du1():
    """
    Lần vết tay Ví dụ 1:
      goc=1; nut=[(1,2,2,3),(2,1,0,0),(3,3,0,0)]
      Cây:      2(id1)
               / \
           1(id2)  3(id3)

    Duyệt trước (Preorder): Gốc→Trái→Phải
      thăm id1(val=2) → kết quả: [2]
      đệ quy trái id2(val=1) → thăm id2 → kết quả: [2,1]
        đệ quy trái None → []
        đệ quy phải None → []
      đệ quy phải id3(val=3) → thăm id3 → kết quả: [2,1,3]
        đệ quy trái None → []
        đệ quy phải None → []
      → truoc = [2, 1, 3]

    Duyệt giữa (Inorder): Trái→Gốc→Phải
      đệ quy trái id2 → [1]
      thăm id1(val=2) → [1,2]
      đệ quy phải id3 → [1,2,3]
      → giua = [1, 2, 3]

    Duyệt sau (Postorder): Trái→Phải→Gốc
      đệ quy trái id2 → [1]
      đệ quy phải id3 → [1,3]
      thăm id1(val=2) → [1,3,2]
      → sau = [1, 3, 2]
    """
    in_phan_cach("LẦN VẾT TAY — Ví dụ 1", "═")
    print(__doc_vet1 := """
  Cây:       2 (id=1, gốc)
            / \\
       1(id=2)  3(id=3)

  DUYỆT TRƯỚC (Gốc → Trái → Phải):
  ┌──────┬──────────────────────────────┬────────────┐
  │ Bước │ Nút đang xử lý               │ Kết quả    │
  ├──────┼──────────────────────────────┼────────────┤
  │  1   │ id1(val=2) — thêm val vào kq │ [2]        │
  │  2   │ id2(val=1) — thêm val vào kq │ [2, 1]     │
  │  3   │ trai(id2)=None → trả []      │ [2, 1]     │
  │  4   │ phai(id2)=None → trả []      │ [2, 1]     │
  │  5   │ id3(val=3) — thêm val vào kq │ [2, 1, 3]  │
  │  6   │ trai(id3)=None → trả []      │ [2, 1, 3]  │
  │  7   │ phai(id3)=None → trả []      │ [2, 1, 3]  │
  └──────┴──────────────────────────────┴────────────┘
  → preorder  = [2, 1, 3]

  DUYỆT GIỮA (Trái → Gốc → Phải):
  ┌──────┬────────────────────────────────┬────────────┐
  │ Bước │ Nút đang xử lý                 │ Kết quả    │
  ├──────┼────────────────────────────────┼────────────┤
  │  1   │ đệ quy trái id1 → id2          │            │
  │  2   │   trai(id2)=None → []          │            │
  │  3   │   thăm id2(val=1)              │ [1]        │
  │  4   │   phai(id2)=None → []          │ [1]        │
  │  5   │ thăm id1(val=2)                │ [1, 2]     │
  │  6   │ đệ quy phải id1 → id3          │            │
  │  7   │   trai(id3)=None → []          │            │
  │  8   │   thăm id3(val=3)              │ [1, 2, 3]  │
  │  9   │   phai(id3)=None → []          │ [1, 2, 3]  │
  └──────┴────────────────────────────────┴────────────┘
  → inorder   = [1, 2, 3]

  DUYỆT SAU (Trái → Phải → Gốc):
  ┌──────┬────────────────────────────────┬────────────┐
  │ Bước │ Nút đang xử lý                 │ Kết quả    │
  ├──────┼────────────────────────────────┼────────────┤
  │  1   │ đệ quy trái id1 → id2          │            │
  │  2   │   trai(id2)=None, phai=None    │            │
  │  3   │   thăm id2(val=1)              │ [1]        │
  │  4   │ đệ quy phải id1 → id3          │            │
  │  5   │   trai(id3)=None, phai=None    │            │
  │  6   │   thăm id3(val=3)              │ [1, 3]     │
  │  7   │ thăm id1(val=2)                │ [1, 3, 2]  │
  └──────┴────────────────────────────────┴────────────┘
  → postorder = [1, 3, 2]
""")


# ──────────────────────────────────────────────────────────────
# A01 — Ví dụ 1 trên phiếu (Preorder ≠ Inorder vì cây không BST)
# ──────────────────────────────────────────────────────────────
def chay_A01():
    in_phan_cach("A01 — Ví dụ 1 trên phiếu")
    n = 3
    danh_sach = [(1, 2, 2, 3), (2, 1, 0, 0), (3, 3, 0, 0)]
    goc = 1
    pre_exp  = [2, 1, 3]
    ino_exp  = [1, 2, 3]
    post_exp = [1, 3, 2]
    print("Sơ đồ cây:")
    in_cay(danh_sach, goc)
    in_ket_qua("A01", "Cây 3 nút, gốc=2, trái=1, phải=3 (không phải BST)",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)
    print("→ Chú ý: inorder=[1,2,3] trùng tăng nhưng ĐÂY KHÔNG PHẢI BST vì")
    print("  cây được xây theo id, không theo giá trị.")


# ──────────────────────────────────────────────────────────────
# A02 — Ví dụ 2 trên phiếu (Cây chỉ có nhánh phải)
# ──────────────────────────────────────────────────────────────
def chay_A02():
    in_phan_cach("A02 — Ví dụ 2 trên phiếu")
    n = 3
    danh_sach = [(1, 5, 0, 2), (2, 6, 0, 3), (3, 7, 0, 0)]
    goc = 1
    pre_exp  = [5, 6, 7]
    ino_exp  = [5, 6, 7]
    post_exp = [7, 6, 5]
    print("Sơ đồ cây:")
    in_cay(danh_sach, goc)
    in_ket_qua("A02", "Cây dây phải: 5→6→7; pre=ino, post=đảo ngược",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)
    print("→ Cây chỉ có nhánh phải nên truoc=giua; sau đi tới lá rồi quay lại.")


# ──────────────────────────────────────────────────────────────
# A03 — Cây rỗng (ca biên: n=0)
# ──────────────────────────────────────────────────────────────
def chay_A03():
    in_phan_cach("A03 — Ca sinh viên tự thiết kế: Cây rỗng")
    n = 0
    danh_sach = []
    goc = 0
    pre_exp = post_exp = ino_exp = []
    in_ket_qua("A03", "Cây rỗng → ba dãy rỗng",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)


# ──────────────────────────────────────────────────────────────
# A04 — Cây một nút
# ──────────────────────────────────────────────────────────────
def chay_A04():
    in_phan_cach("A04 — Ca sinh viên tự thiết kế: Một nút")
    n = 1
    danh_sach = [(1, 8, 0, 0)]
    goc = 1
    pre_exp = ino_exp = post_exp = [8]
    in_ket_qua("A04", "Một nút val=8 → ba dãy đều [8]",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)


# ──────────────────────────────────────────────────────────────
# A05 — Ca biên: Gốc 2, trái 1, phải 3 (đảm bảo inorder = [1,2,3])
# ──────────────────────────────────────────────────────────────
def chay_A05():
    in_phan_cach("A05 — Ca biên: Kiểm inorder không tự sắp")
    n = 3
    # Gốc val=2, trái val=1, phải val=3
    danh_sach = [(1, 2, 2, 3), (2, 1, 0, 0), (3, 3, 0, 0)]
    goc = 1
    pre_exp  = [2, 1, 3]
    ino_exp  = [1, 2, 3]
    post_exp = [1, 3, 2]
    in_ket_qua("A05", "Gốc=2, trái=1, phải=3 → inorder=[1,2,3] nhưng KHÔNG phải BST",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)


# ──────────────────────────────────────────────────────────────
# A06 — Ca biên: Gốc 1, trái 9, phải 2 (inorder không tăng)
# ──────────────────────────────────────────────────────────────
def chay_A06():
    in_phan_cach("A06 — Ca biên: inorder không đảm bảo tăng")
    n = 3
    danh_sach = [(1, 1, 2, 3), (2, 9, 0, 0), (3, 2, 0, 0)]
    goc = 1
    pre_exp  = [1, 9, 2]
    ino_exp  = [9, 1, 2]
    post_exp = [9, 2, 1]
    in_ket_qua("A06", "Gốc val=1, trái val=9, phải val=2 → inorder=[9,1,2] không tăng",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)
    print("→ Minh chứng: duyệt giữa KHÔNG đảm bảo tăng với cây tổng quát.")


# ──────────────────────────────────────────────────────────────
# A07 — Ca biên: Cây dây trái (3→2→1)
# ──────────────────────────────────────────────────────────────
def chay_A07():
    in_phan_cach("A07 — Ca biên: Dây trái 3→2→1")
    n = 3
    danh_sach = [(1, 3, 2, 0), (2, 2, 3, 0), (3, 1, 0, 0)]
    goc = 1
    pre_exp  = [3, 2, 1]
    ino_exp  = [1, 2, 3]
    post_exp = [1, 2, 3]
    print("Sơ đồ cây:")
    in_cay(danh_sach, goc)
    in_ket_qua("A07", "Dây trái: pre=[3,2,1], ino=[1,2,3], post=[1,2,3]",
               n, danh_sach, goc, pre_exp, ino_exp, post_exp)


# ──────────────────────────────────────────────────────────────
# A08 — Input sai: id_trai ngoài phạm vi
# ──────────────────────────────────────────────────────────────
def chay_A08():
    in_phan_cach("A08 — Input sai và phản hồi kiểm tra")
    print("Thử input n=2 nhưng id_trai=5 ngoài [0,2]:")
    try:
        giai_bai(2, [(1, 10, 5, 0), (2, 20, 0, 0)], goc=1)
        print("Kết quả: ✗ FAIL (phải bắt lỗi)")
    except ValueError as e:
        print(f"  ValueError: {e}")
        print("Kết quả: ✓ PASS (bắt lỗi đúng)")

    print()
    print("Thử n âm:")
    try:
        giai_bai(-1, [], 0)
        print("Kết quả: ✗ FAIL (phải bắt lỗi)")
    except ValueError as e:
        print(f"  ValueError: {e}")
        print("Kết quả: ✓ PASS (bắt lỗi đúng)")

    print()
    print("Thử goc không tồn tại trong bảng:")
    try:
        giai_bai(1, [(1, 5, 0, 0)], goc=99)
        print("Kết quả: ✗ FAIL (phải bắt lỗi)")
    except ValueError as e:
        print(f"  ValueError: {e}")
        print("Kết quả: ✓ PASS (bắt lỗi đúng)")


# ──────────────────────────────────────────────────────────────
# A09 — Tổng kết bộ kiểm thử (chạy file test riêng)
# ──────────────────────────────────────────────────────────────
def chay_A09():
    in_phan_cach("A09 — Lệnh chạy và tổng kết bộ kiểm thử")
    print("Lệnh chạy bộ kiểm thử đầy đủ (≥12 ca):")
    print("  py test\\test_cay_nhi_phan.py")
    print()
    print("Thống kê (sẽ được in trong file test):")
    # Chạy trực tiếp bộ test và đếm
    import subprocess, sys
    result = subprocess.run(
        [sys.executable,
         os.path.join(os.path.dirname(__file__), "test", "test_cay_nhi_phan.py")],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(result.stdout)
    if result.returncode == 0:
        print("→ Toàn bộ ca kiểm đều PASS.")
    else:
        print(result.stderr)


# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    in_phan_cach("DT083 — BIỂU DIỄN CÂY NHỊ PHÂN VÀ BA THỨ TỰ DUYỆT", "═")
    print("Sinh viên : Trần Tiến Trung — N24DCDT101 — D24CQDT01-N")
    print("Môn học   : INT13185 — Cấu trúc dữ liệu và giải thuật — Nhóm 03")
    print("Giáo trình: Chương 7, mục 7.2 và 7.3.1 — trang in 162–165")
    in_phan_cach()

    in_lan_vet_vi_du1()

    chay_A01()
    print()
    chay_A02()
    print()
    chay_A03()
    print()
    chay_A04()
    print()
    chay_A05()
    print()
    chay_A06()
    print()
    chay_A07()
    print()
    chay_A08()
    print()
    chay_A09()

    in_phan_cach("KẾT THÚC DEMO", "═")


if __name__ == "__main__":
    main()
