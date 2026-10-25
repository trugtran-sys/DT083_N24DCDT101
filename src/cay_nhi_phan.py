# -*- coding: utf-8 -*-
"""
DT083 — Biểu diễn cây nhị phân và ba thứ tự duyệt
Môn: Cấu trúc dữ liệu và giải thuật — INT13185 — Nhóm 03
Sinh viên: Trần Tiến Trung — MSSV: N24DCDT101 — Lớp: D24CQDT01-N
Giảng viên: Hồ Nhựt Minh
Giáo trình: Chương 7, 7.2; 7.3.1 Ba cách duyệt; trang in 162–165; trang PDF 174–177
"""

from typing import Optional, List, Tuple


# ============================================================
# CẤU TRÚC DỮ LIỆU: Nút cây nhị phân
# ============================================================

class Nut:
    """
    Biểu diễn một nút trong cây nhị phân.

    Thuộc tính:
        id (int)        : Nhãn định danh nút (1-based).
        gia_tri (int)   : Giá trị lưu tại nút.
        trai (Optional[Nut]): Con trỏ đến cây con trái (None nếu không có).
        phai (Optional[Nut]): Con trỏ đến cây con phải (None nếu không có).

    Bất biến: Mỗi nút ngoài gốc có đúng một cha; không chu trình.
    """

    def __init__(self, id: int, gia_tri: int):
        self.id: int = id
        self.gia_tri: int = gia_tri
        self.trai: Optional["Nut"] = None
        self.phai: Optional["Nut"] = None

    def __repr__(self) -> str:
        return f"Nut(id={self.id}, val={self.gia_tri})"


# ============================================================
# HỢP ĐỒNG INPUT / OUTPUT
# ============================================================
# Đầu vào:
#   n        : int, 0 ≤ n ≤ 100  — số nút trong cây
#   danh_sach: List[Tuple(id, gia_tri, id_trai, id_phai)]
#              id ∈ 1..n; id_trai/id_phai ∈ 0..n (0 = không con)
#   goc      : int — id của nút gốc; 0 = cây rỗng
#   Ràng buộc: tạo đúng một cây (không chu trình, mỗi nút ≠ gốc có đúng một cha).
#
# Đầu ra:
#   Tuple[List[int], List[int], List[int]]
#   (preorder, inorder, postorder) — danh sách giá trị theo thứ tự duyệt.
#   Cây rỗng → ba dãy rỗng.
#
# Từ chối:
#   - n < 0 hoặc n > 100  → ValueError
#   - id trùng            → ValueError
#   - id_trai/id_phai ngoài 0..n → ValueError
#   - Gốc không có trong bảng (n>0) → ValueError
# ============================================================


def kiem_tra_dau_vao(
    n: int,
    danh_sach: List[Tuple[int, int, int, int]],
    goc: int
) -> None:
    """
    Kiểm tra tính hợp lệ của đầu vào.

    Tiền điều kiện : nhận n, danh_sach, goc từ người dùng.
    Hậu điều kiện  : không có lỗi ↔ dữ liệu hợp lệ.
    Ngoại lệ       : ValueError khi vi phạm hợp đồng.
    """
    if not (0 <= n <= 100):
        raise ValueError(f"n={n} phải trong [0, 100].")
    if n == 0:
        if goc != 0:
            raise ValueError("n=0 (cây rỗng) nhưng goc != 0.")
        return

    if len(danh_sach) != n:
        raise ValueError(f"Số bộ ({len(danh_sach)}) không khớp n={n}.")

    ids = [bộ[0] for bộ in danh_sach]
    # Kiểm tra id hợp lệ và duy nhất
    for bộ in danh_sach:
        bid, _, bt, bp = bộ
        if not (1 <= bid <= n):
            raise ValueError(f"id={bid} phải trong [1, {n}].")
        if not (0 <= bt <= n):
            raise ValueError(f"id_trai={bt} của nút {bid} phải trong [0, {n}].")
        if not (0 <= bp <= n):
            raise ValueError(f"id_phai={bp} của nút {bid} phải trong [0, {n}].")
    if len(set(ids)) != n:
        raise ValueError("Có id trùng nhau trong bảng nút.")
    if not (1 <= goc <= n):
        raise ValueError(f"goc={goc} phải trong [1, {n}] khi n>0.")
    if goc not in ids:
        raise ValueError(f"goc={goc} không tồn tại trong bảng nút.")


def tao_cay(
    danh_sach: List[Tuple[int, int, int, int]],
    goc: int
) -> Optional[Nut]:
    """
    Dựng cây nhị phân từ bảng (id, gia_tri, id_trai, id_phai).

    Tiền điều kiện : danh_sach đã qua kiểm tra; goc=0 hoặc id hợp lệ.
    Hậu điều kiện  : trả về Nut gốc của cây, hoặc None nếu goc=0.
    Độ phức tạp    : O(n) thời gian, O(n) bộ nhớ.

    Tham số:
        danh_sach: List[Tuple[int,int,int,int]] — (id, gia_tri, id_trai, id_phai)
        goc      : int — id nút gốc; 0 = cây rỗng

    Trả về:
        Optional[Nut] — gốc cây hoặc None
    """
    if goc == 0 or not danh_sach:
        return None

    # Tạo bảng tra id → Nut
    bang_nut = {}
    for bid, giatri, _, _ in danh_sach:
        bang_nut[bid] = Nut(bid, giatri)

    # Nối con trái và con phải
    for bid, _, bt, bp in danh_sach:
        if bt != 0:
            bang_nut[bid].trai = bang_nut[bt]
        if bp != 0:
            bang_nut[bid].phai = bang_nut[bp]

    return bang_nut[goc]


# ============================================================
# BA HÀM DUYỆT ĐỆ QUY
# ============================================================

def duyet_truoc(g: Optional[Nut]) -> List[int]:
    """
    Duyệt trước (Preorder): Gốc → Trái → Phải.

    Tiền điều kiện : g là nút hợp lệ hoặc None.
    Hậu điều kiện  : trả danh sách giá trị, mỗi nút đúng một lần.
    Bất biến       : mọi nút trong cây con g đều có mặt trong kết quả.
    Độ phức tạp    : O(n) thời gian, O(h) stack — h là chiều cao cây.

    Tham số:
        g: Optional[Nut]

    Trả về:
        List[int]
    """
    if g is None:
        return []
    ket_qua = [g.gia_tri]
    ket_qua += duyet_truoc(g.trai)
    ket_qua += duyet_truoc(g.phai)
    return ket_qua


def duyet_giua(g: Optional[Nut]) -> List[int]:
    """
    Duyệt giữa (Inorder): Trái → Gốc → Phải.

    Tiền điều kiện : g là nút hợp lệ hoặc None.
    Hậu điều kiện  : trả danh sách giá trị, mỗi nút đúng một lần.
    Bất biến       : với BST thì dãy tăng; cây tổng quát thì không đảm bảo.
    Độ phức tạp    : O(n) thời gian, O(h) stack.

    Tham số:
        g: Optional[Nut]

    Trả về:
        List[int]
    """
    if g is None:
        return []
    ket_qua = duyet_giua(g.trai)
    ket_qua += [g.gia_tri]
    ket_qua += duyet_giua(g.phai)
    return ket_qua


def duyet_sau(g: Optional[Nut]) -> List[int]:
    """
    Duyệt sau (Postorder): Trái → Phải → Gốc.

    Tiền điều kiện : g là nút hợp lệ hoặc None.
    Hậu điều kiện  : trả danh sách giá trị, gốc luôn xuất hiện cuối cùng.
    Bất biến       : lá luôn được thăm trước cha của nó.
    Độ phức tạp    : O(n) thời gian, O(h) stack.

    Tham số:
        g: Optional[Nut]

    Trả về:
        List[int]
    """
    if g is None:
        return []
    ket_qua = duyet_sau(g.trai)
    ket_qua += duyet_sau(g.phai)
    ket_qua += [g.gia_tri]
    return ket_qua


# ============================================================
# HÀM CHÍNH — giai_bai
# ============================================================

def giai_bai(
    n: int,
    danh_sach: List[Tuple[int, int, int, int]],
    goc: int
) -> Tuple[List[int], List[int], List[int]]:
    """
    Dựng cây nhị phân rồi trả ba dãy duyệt trước/giữa/sau.

    Tiền điều kiện : 0 ≤ n ≤ 100; danh_sach có n bộ (id,giatri,trai,phai);
                     goc=0 (cây rỗng) hoặc goc ∈ 1..n; không chu trình.
    Hậu điều kiện  : (pre, ino, post) — mỗi dãy dài n giá trị nguyên.
    Ngoại lệ       : ValueError nếu đầu vào vi phạm hợp đồng.
    Độ phức tạp    : O(n) thời gian, O(n) bộ nhớ tổng.

    Tham số:
        n          : int
        danh_sach  : List[Tuple[int,int,int,int]]
        goc        : int

    Trả về:
        Tuple[List[int], List[int], List[int]]
    """
    kiem_tra_dau_vao(n, danh_sach, goc)
    cay = tao_cay(danh_sach, goc)
    pre  = duyet_truoc(cay)
    ino  = duyet_giua(cay)
    post = duyet_sau(cay)
    return pre, ino, post
