# DT083 — Biểu diễn cây nhị phân và ba thứ tự duyệt

**Sinh viên**: Trần Tiến Trung — **MSSV**: N24DCDT101 — **Lớp**: D24CQDT01-N  
**Môn**: INT13185 — Cấu trúc dữ liệu và giải thuật — Nhóm 03  
**Giảng viên**: Hồ Nhựt Minh  
**Giáo trình**: Chương 7, mục 7.2; 7.3.1 — trang in 162–165; trang PDF 174–177

---

## Cấu trúc thư mục

```
DT083_N24DCDT101/
├── src/
│   └── cay_nhi_phan.py     # Cài đặt chính: Nut, tao_cay, 3 hàm duyệt
├── test/
│   └── test_cay_nhi_phan.py # ≥16 ca kiểm thử (A01–A16)
├── docs/
│   └── anh_ket_qua/        # Ảnh minh chứng A01–A11 (sinh viên tự chụp)
│       └── README.md
├── demo.py                  # Demo A01–A09 với lần vết tay
├── chup_ket_qua.py          # 1 lệnh chạy toàn bộ, lưu output
└── README.md
```

---

## Ngôn ngữ và phiên bản

- **Python 3.x** (chạy bằng `py tenfile.py` trên Windows)
- Chỉ dùng thư viện chuẩn (`sys`, `os`, `unittest`, `subprocess`)

---

## Lệnh chạy

```powershell
# Tại thư mục DT083_N24DCDT101\

# Chạy demo (A01–A09 với lần vết tay):
py demo.py

# Chạy bộ kiểm thử (≥12 ca, A01–A16):
py test\test_cay_nhi_phan.py

# Chụp toàn bộ kết quả ra file (1 lệnh duy nhất):
py chup_ket_qua.py
```

---

## Hợp đồng Input / Output

| Tham số     | Kiểu                                | Ràng buộc                               |
|-------------|-------------------------------------|-----------------------------------------|
| `n`         | `int`                               | 0 ≤ n ≤ 100                             |
| `danh_sach` | `List[Tuple[int,int,int,int]]`      | `(id, gia_tri, id_trai, id_phai)`, id ∈ 1..n, con ∈ 0..n |
| `goc`       | `int`                               | 0 (cây rỗng) hoặc 1..n                 |
| **Output**  | `Tuple[List[int],List[int],List[int]]` | (preorder, inorder, postorder)       |

---

## Ví dụ chạy

### Ví dụ 1 (trên phiếu)

```
Input : n=3, goc=1, nut=[(1,2,2,3),(2,1,0,0),(3,3,0,0)]
Cây   :       2 (id=1)
             / \
         1(id2)  3(id3)

truoc = [2, 1, 3]
giua  = [1, 2, 3]
sau   = [1, 3, 2]
```

### Ví dụ 2 (trên phiếu)

```
Input : n=3, goc=1, nut=[(1,5,0,2),(2,6,0,3),(3,7,0,0)]
Cây   :  5(id1) → 6(id2) → 7(id3)  [dây phải]

truoc = [5, 6, 7]
giua  = [5, 6, 7]
sau   = [7, 6, 5]
```

---

## Bộ kiểm thử (A01–A16, ≥12 ca)

| ID  | Đối tượng | Input tóm tắt | Kỳ vọng (tính tay) | Mục tiêu |
|-----|-----------|---------------|---------------------|----------|
| A01 | giai_bai  | Ví dụ 1 phiếu, n=3 | pre=[2,1,3] ino=[1,2,3] post=[1,3,2] | Cơ bản 3 thứ tự |
| A02 | giai_bai  | Ví dụ 2 phiếu, n=3 dây phải | pre=ino=[5,6,7] post=[7,6,5] | Cây dây phải |
| A03 | giai_bai  | n=0, cây rỗng | pre=ino=post=[] | Ca biên rỗng |
| A04 | giai_bai  | n=1, val=8 | pre=ino=post=[8] | Ca biên 1 nút |
| A05 | giai_bai  | Gốc=2,trái=1,phải=3 | ino=[1,2,3] không phải BST | Kiểm bất biến |
| A06 | giai_bai  | Gốc=1,trái=9,phải=2 | ino=[9,1,2] không tăng | Cây tổng quát ≠ BST |
| A07 | giai_bai  | Dây trái 3→2→1 | pre=[3,2,1] ino=post=[1,2,3] | Ca biên dây trái |
| A08 | kiem_tra  | id_trai=5 > n=2 | ValueError | Input sai |
| A08b| kiem_tra  | n=-1 | ValueError | Input sai (n âm) |
| A08c| kiem_tra  | goc=99, n=1 | ValueError | goc không tồn tại |
| A09 | giai_bai  | n=5, cây 2 mức | len=5 mọi dãy | Bất biến độ dài |
| A10 | duyet_*   | Cây dựng tay | pre=[2,1,3] ino=[1,2,3] post=[1,3,2] | Hàm con độc lập |
| A11 | giai_bai  | Cây đầy 7 nút | pre=[1,2,4,5,3,6,7] ino=[4,2,5,1,6,3,7] post=[4,5,2,6,7,3,1] | Cây cân bằng |
| A12 | giai_bai  | Gốc=100,trái=5,phải=50 | ino=[5,100,50] không tăng | Không phải BST |
| A13 | giai_bai  | Dây phải 5 nút | pre=ino=[1..5] post=[5..1] | Cây suy biến phải |
| A14 | giai_bai  | 3 nút cùng val=5 | pre=ino=post=[5,5,5] | Giá trị trùng |
| A15 | duyet_sau | Nhiều cấu hình | gốc luôn cuối postorder | Bất biến postorder |
| A16 | duyet_truoc| n=4 | gốc(val=99) luôn đầu preorder | Bất biến preorder |

---

## GitHub 

```powershell
git init
git add .
git commit -m "DT083: Hoan thanh cay nhi phan va ba thu tu duyet"
git branch -M main
git remote add origin https://github.com/TEN_TAI_KHOAN/DT083_N24DCDT101.git
git push -u origin main
git rev-parse HEAD  
```

Clone kiểm tra:
```powershell
git clone https://github.com/TEN_TAI_KHOAN/DT083_N24DCDT101.git kiem_tra_N24DCDT101
cd kiem_tra_N24DCDT101
git rev-parse HEAD
py demo.py
py test\test_cay_nhi_phan.py
```

---

## Chụp ảnh minh chứng (A01–A11)

Chạy **1 lệnh duy nhất**:
```powershell
py chup_ket_qua.py
```

Kết quả được lưu vào `docs/anh_ket_qua/`. Sau đó chụp màn hình terminal để có ảnh A01–A11 chèn vào báo cáo Word.

---

*Ngày hoàn tất: 25/10/2026*  
*SHA C: d131fb65e8be2e096f4953d45738500a6a366968*  
*SHA S: 09f3f3b2ebb9165ad401385fd5f540fe7b3d44c1*
