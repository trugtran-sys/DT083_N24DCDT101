# -*- coding: utf-8 -*-
"""
test_cay_nhi_phan.py — Bộ kiểm thử DT083
Sinh viên: Trần Tiến Trung — N24DCDT101 — D24CQDT01-N

Chạy: py test\test_cay_nhi_phan.py
≥ 12 ca độc lập với ID A01–A12+.
"""

import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from cay_nhi_phan import (
    giai_bai, kiem_tra_dau_vao, tao_cay,
    duyet_truoc, duyet_giua, duyet_sau, Nut
)

# ──────────────────────────────────────────────────────────────
# Hàm helper: tạo cây trực tiếp từ Nut để test hàm con riêng
# ──────────────────────────────────────────────────────────────
def make_tree_manual():
    """
    Tạo tay cây:       2 (id1)
                      / \\
                 1(id2)  3(id3)
    Dùng để test các hàm duyệt độc lập với tao_cay().
    """
    root = Nut(1, 2)
    root.trai = Nut(2, 1)
    root.phai = Nut(3, 3)
    return root


# ──────────────────────────────────────────────────────────────
# CA KIỂM THỬ
# ──────────────────────────────────────────────────────────────

class TestCayNhiPhan(unittest.TestCase):

    # ── A01: Ví dụ 1 trên phiếu ──────────────────────────────
    def test_A01_vi_du_1_phieu(self):
        """
        A01 — Ví dụ 1 trên phiếu.
        Input : n=3, goc=1, nut=[(1,2,2,3),(2,1,0,0),(3,3,0,0)]
        Kỳ vọng (tính tay): pre=[2,1,3], ino=[1,2,3], post=[1,3,2]
        Mục tiêu: kiểm tra đúng 3 thứ tự duyệt cơ bản.
        """
        pre, ino, post = giai_bai(
            3, [(1,2,2,3),(2,1,0,0),(3,3,0,0)], goc=1
        )
        self.assertEqual(pre,  [2, 1, 3], "A01 preorder sai")
        self.assertEqual(ino,  [1, 2, 3], "A01 inorder sai")
        self.assertEqual(post, [1, 3, 2], "A01 postorder sai")

    # ── A02: Ví dụ 2 trên phiếu (cây dây phải) ───────────────
    def test_A02_vi_du_2_phieu(self):
        """
        A02 — Ví dụ 2 trên phiếu.
        Input : n=3, goc=1, nut=[(1,5,0,2),(2,6,0,3),(3,7,0,0)]
        Kỳ vọng: pre=[5,6,7], ino=[5,6,7], post=[7,6,5]
        Mục tiêu: cây dây phải — pre và ino trùng, post đảo ngược.
        """
        pre, ino, post = giai_bai(
            3, [(1,5,0,2),(2,6,0,3),(3,7,0,0)], goc=1
        )
        self.assertEqual(pre,  [5, 6, 7], "A02 preorder sai")
        self.assertEqual(ino,  [5, 6, 7], "A02 inorder sai")
        self.assertEqual(post, [7, 6, 5], "A02 postorder sai")

    # ── A03: Ca tự thiết kế — cây rỗng ───────────────────────
    def test_A03_cay_rong(self):
        """
        A03 — Cây rỗng.
        Input : n=0, goc=0
        Kỳ vọng: pre=[], ino=[], post=[]
        Mục tiêu: ca biên — không có nút nào để duyệt.
        """
        pre, ino, post = giai_bai(0, [], goc=0)
        self.assertEqual(pre,  [], "A03 preorder sai")
        self.assertEqual(ino,  [], "A03 inorder sai")
        self.assertEqual(post, [], "A03 postorder sai")

    # ── A04: Ca tự thiết kế — một nút ────────────────────────
    def test_A04_mot_nut(self):
        """
        A04 — Một nút duy nhất val=8.
        Input : n=1, goc=1, nut=[(1,8,0,0)]
        Kỳ vọng: pre=[8], ino=[8], post=[8]
        Mục tiêu: một nút → gốc là lá, cả 3 thứ tự đều bằng [val].
        """
        pre, ino, post = giai_bai(1, [(1,8,0,0)], goc=1)
        self.assertEqual(pre,  [8], "A04 preorder sai")
        self.assertEqual(ino,  [8], "A04 inorder sai")
        self.assertEqual(post, [8], "A04 postorder sai")

    # ── A05: Ca biên — Gốc 2, trái 1, phải 3 ────────────────
    def test_A05_goc2_trai1_phai3(self):
        """
        A05 — Gốc val=2, trái val=1, phải val=3.
        Kỳ vọng: ino=[1,2,3] (tăng nhưng không phải BST).
        Mục tiêu: inorder=[1,2,3] nhưng cây được xây theo id không theo giá trị.
        """
        pre, ino, post = giai_bai(
            3, [(1,2,2,3),(2,1,0,0),(3,3,0,0)], goc=1
        )
        self.assertEqual(ino, [1, 2, 3])
        # Bất biến: độ dài từng dãy = số nút
        self.assertEqual(len(pre), 3)
        self.assertEqual(len(post), 3)

    # ── A06: Ca biên — inorder KHÔNG tăng với cây tổng quát ──
    def test_A06_inorder_khong_tang(self):
        """
        A06 — Gốc val=1, trái val=9, phải val=2.
        Kỳ vọng: ino=[9,1,2] — KHÔNG tăng.
        Mục tiêu: minh chứng duyệt giữa không đảm bảo tăng với cây tổng quát.
        """
        pre, ino, post = giai_bai(
            3, [(1,1,2,3),(2,9,0,0),(3,2,0,0)], goc=1
        )
        self.assertEqual(pre,  [1, 9, 2])
        self.assertEqual(ino,  [9, 1, 2])
        self.assertEqual(post, [9, 2, 1])
        # Bất biến: ino không tăng
        self.assertFalse(ino == sorted(ino), "A06: ino không được tăng")

    # ── A07: Ca biên — Dây trái 3→2→1 ───────────────────────
    def test_A07_day_trai(self):
        """
        A07 — Dây trái: 3(gốc)→2→1.
        Input : nut=[(1,3,2,0),(2,2,3,0),(3,1,0,0)], goc=1
        Kỳ vọng: pre=[3,2,1], ino=[1,2,3], post=[1,2,3]
        Mục tiêu: dây trái — pre=giảm, ino=post=tăng.
        """
        pre, ino, post = giai_bai(
            3, [(1,3,2,0),(2,2,3,0),(3,1,0,0)], goc=1
        )
        self.assertEqual(pre,  [3, 2, 1])
        self.assertEqual(ino,  [1, 2, 3])
        self.assertEqual(post, [1, 2, 3])

    # ── A08: Input sai — id_trai ngoài phạm vi ───────────────
    def test_A08_input_sai_id_trai_qua_lon(self):
        """
        A08a — id_trai=5 với n=2: vượt phạm vi [0,2].
        Kỳ vọng: ValueError.
        Mục tiêu: kiểm tra hàm validator từ chối đúng.
        """
        with self.assertRaises(ValueError):
            giai_bai(2, [(1,10,5,0),(2,20,0,0)], goc=1)

    def test_A08b_input_sai_n_am(self):
        """
        A08b — n=-1: âm.
        Kỳ vọng: ValueError.
        """
        with self.assertRaises(ValueError):
            giai_bai(-1, [], 0)

    def test_A08c_input_sai_goc_khong_ton_tai(self):
        """
        A08c — goc=99 không có trong bảng nút n=1.
        Kỳ vọng: ValueError.
        """
        with self.assertRaises(ValueError):
            giai_bai(1, [(1,5,0,0)], goc=99)

    # ── A09: Bất biến — độ dài dãy = n ───────────────────────
    def test_A09_bat_bien_do_dai_bang_n(self):
        """
        A09 — Bất biến: len(pre)=len(ino)=len(post)=n mọi cây hợp lệ.
        Mục tiêu: mỗi nút xuất hiện đúng một lần trong mỗi dãy.
        """
        # Cây 5 nút: gốc=1, có hai mức
        n = 5
        ds = [(1,10,2,3),(2,20,4,5),(3,30,0,0),(4,40,0,0),(5,50,0,0)]
        pre, ino, post = giai_bai(n, ds, goc=1)
        self.assertEqual(len(pre),  n)
        self.assertEqual(len(ino),  n)
        self.assertEqual(len(post), n)
        # Bất biến: tập giá trị bằng nhau trong cả 3 dãy
        self.assertEqual(sorted(pre), sorted(ino))
        self.assertEqual(sorted(ino), sorted(post))

    # ── A10: Hàm con — duyet_truoc, duyet_giua, duyet_sau ────
    def test_A10_ham_con_tren_cay_thu_cong(self):
        """
        A10 — Kiểm hàm con (duyet_truoc/giua/sau) độc lập với tao_cay.
        Dựng cây tay: gốc val=2, trái val=1, phải val=3.
        Kỳ vọng: pre=[2,1,3], ino=[1,2,3], post=[1,3,2].
        Mục tiêu: xác nhận logic hàm duyệt tách biệt với tao_cay.
        """
        root = make_tree_manual()
        self.assertEqual(duyet_truoc(root), [2, 1, 3])
        self.assertEqual(duyet_giua(root),  [1, 2, 3])
        self.assertEqual(duyet_sau(root),   [1, 3, 2])

    # ── A11: Cây 7 nút — cây đầy mức 3 ─────────────────────
    def test_A11_cay_day_7_nut(self):
        """
        A11 — Cây nhị phân đầy 7 nút (3 mức).
        Cấu trúc: gốc=1(val=1), con=[2(val=2),3(val=3)],
                  con[2]=[4(val=4),5(val=5)], con[3]=[6(val=6),7(val=7)]
        Kỳ vọng (tính tay):
          pre  = [1,2,4,5,3,6,7]
          ino  = [4,2,5,1,6,3,7]
          post = [4,5,2,6,7,3,1]
        Mục tiêu: cây cân bằng đầy đủ — kiểm thứ tự 3 mức.
        """
        n = 7
        ds = [(1,1,2,3),(2,2,4,5),(3,3,6,7),
              (4,4,0,0),(5,5,0,0),(6,6,0,0),(7,7,0,0)]
        pre, ino, post = giai_bai(n, ds, goc=1)
        self.assertEqual(pre,  [1,2,4,5,3,6,7])
        self.assertEqual(ino,  [4,2,5,1,6,3,7])
        self.assertEqual(post, [4,5,2,6,7,3,1])

    # ── A12: Cây không phải BST — inorder không tăng ─────────
    def test_A12_khong_phai_BST(self):
        """
        A12 — Cây tổng quát không phải BST.
        Cấu trúc: gốc val=100, trái val=5, phải val=50
        Kỳ vọng: ino=[5,100,50] — KHÔNG tăng → không phải BST.
        Mục tiêu: xác nhận chương trình không giả định BST.
        """
        pre, ino, post = giai_bai(
            3, [(1,100,2,3),(2,5,0,0),(3,50,0,0)], goc=1
        )
        self.assertEqual(pre,  [100, 5, 50])
        self.assertEqual(ino,  [5, 100, 50])
        self.assertEqual(post, [5, 50, 100])
        # Xác nhận ino không tăng → không phải BST
        self.assertNotEqual(ino, sorted(ino))

    # ── A13: Dây phải dài hơn (5 nút) ───────────────────────
    def test_A13_day_phai_5_nut(self):
        """
        A13 — Dây phải 5 nút: 1→2→3→4→5.
        Kỳ vọng: pre=ino=[1,2,3,4,5]; post=[5,4,3,2,1].
        Mục tiêu: cây suy biến phải — chiều cao h=n-1=4.
        """
        ds = [(1,1,0,2),(2,2,0,3),(3,3,0,4),(4,4,0,5),(5,5,0,0)]
        pre, ino, post = giai_bai(5, ds, goc=1)
        self.assertEqual(pre,  [1,2,3,4,5])
        self.assertEqual(ino,  [1,2,3,4,5])
        self.assertEqual(post, [5,4,3,2,1])

    # ── A14: Cây với nút trùng giá trị ───────────────────────
    def test_A14_nut_trung_gia_tri(self):
        """
        A14 — Hai nút cùng giá trị val=5.
        Cấu trúc: gốc val=5, trái val=5, phải val=5
        Kỳ vọng: pre=[5,5,5], ino=[5,5,5], post=[5,5,5].
        Mục tiêu: xử lý đúng khi có giá trị trùng (không lẫn id).
        """
        pre, ino, post = giai_bai(
            3, [(1,5,2,3),(2,5,0,0),(3,5,0,0)], goc=1
        )
        self.assertEqual(pre,  [5, 5, 5])
        self.assertEqual(ino,  [5, 5, 5])
        self.assertEqual(post, [5, 5, 5])

    # ── A15: Bất biến gốc cuối trong postorder ───────────────
    def test_A15_bat_bien_goc_cuoi_postorder(self):
        """
        A15 — Bất biến: gốc luôn là phần tử CUỐI trong postorder.
        Dùng nhiều cấu hình: xác nhận gốc luôn ở cuối.
        Mục tiêu: kiểm bất biến tổng quát của Postorder.
        """
        cases = [
            (3, [(1,2,2,3),(2,1,0,0),(3,3,0,0)], 1, 2),   # gốc val=2
            (3, [(1,5,0,2),(2,6,0,3),(3,7,0,0)], 1, 5),   # gốc val=5
            (1, [(1,42,0,0)], 1, 42),                       # một nút val=42
        ]
        for n, ds, goc_id, goc_val in cases:
            pre, ino, post = giai_bai(n, ds, goc=goc_id)
            self.assertEqual(post[-1], goc_val,
                f"A15: gốc (val={goc_val}) phải là phần tử cuối postorder")

    # ── A16: Bất biến gốc đầu trong preorder ─────────────────
    def test_A16_bat_bien_goc_dau_preorder(self):
        """
        A16 — Bất biến: gốc luôn là phần tử ĐẦU trong preorder.
        Mục tiêu: kiểm bất biến tổng quát của Preorder.
        """
        n = 4
        ds = [(1,99,2,3),(2,10,4,0),(3,20,0,0),(4,5,0,0)]
        pre, ino, post = giai_bai(n, ds, goc=1)
        # Gốc id=1 có val=99
        self.assertEqual(pre[0], 99, "A16: gốc phải là phần tử đầu preorder")


# ──────────────────────────────────────────────────────────────
# CHẠY VÀ THỐNG KÊ
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    # Chạy unittest với output chi tiết
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromTestCase(TestCayNhiPhan)
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print()
    print("=" * 62)
    print("TONG KET BO KIEM THU DT083")
    print(f"  So ca kiem : {result.testsRun}")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"  Dat (PASS) : {passed}")
    print(f"  Loi (FAIL) : {len(result.failures)}")
    print(f"  Ngoai le   : {len(result.errors)}")
    print("=" * 62)
    sys.exit(0 if result.wasSuccessful() else 1)
