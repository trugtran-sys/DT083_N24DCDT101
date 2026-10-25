# -*- coding: utf-8 -*-
"""
chup_ket_qua.py — Chạy 1 lệnh để chụp toàn bộ kết quả ra file .txt
DT083: Biểu diễn cây nhị phân và ba thứ tự duyệt
Sinh viên: Trần Tiến Trung — N24DCDT101

Cách dùng:
    py chup_ket_qua.py

Kết quả được lưu vào:
    docs/anh_ket_qua/A01_A08_demo_output.txt
    docs/anh_ket_qua/A09_test_output.txt
(Sau đó chụp màn hình terminal từ 2 file này để có ảnh minh chứng A01–A09)
"""

import sys, os, subprocess, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs", "anh_ket_qua")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def run_and_save(script_path: str, label: str, out_file: str):
    """Chạy script và lưu output ra file."""
    print(f"\n{'='*60}")
    print(f"Đang chạy: {label}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=BASE_DIR
    )
    output = result.stdout
    if result.stderr:
        output += "\n[STDERR]\n" + result.stderr

    # In ra terminal
    print(output)

    # Lưu ra file
    header = (
        f"DT083 — Biểu diễn cây nhị phân và ba thứ tự duyệt\n"
        f"Sinh viên: Trần Tiến Trung — N24DCDT101 — D24CQDT01-N\n"
        f"Thời gian chạy: {TIMESTAMP}\n"
        f"Script: {os.path.basename(script_path)}\n"
        f"{'='*62}\n\n"
    )
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(header + output)

    print(f"✓ Đã lưu ra: {out_file}")
    return result.returncode == 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 62)
    print("CHUP TOAN BO KET QUA --- DT083 --- N24DCDT101")
    print("Tran Tien Trung -- Bieu dien cay nhi phan va 3 duyet")
    print("=" * 62)

    results = []

    # 1. Chạy demo.py → A01–A09
    demo_script = os.path.join(BASE_DIR, "demo.py")
    demo_out    = os.path.join(OUTPUT_DIR, f"A01_A09_demo_output.txt")
    ok1 = run_and_save(demo_script, "demo.py (A01–A09)", demo_out)
    results.append(("demo.py", ok1))

    # 2. Chạy bộ test → A01–A16 (≥12 ca)
    test_script = os.path.join(BASE_DIR, "test", "test_cay_nhi_phan.py")
    test_out    = os.path.join(OUTPUT_DIR, f"A09_test_output.txt")
    ok2 = run_and_save(test_script, "test_cay_nhi_phan.py (≥12 ca)", test_out)
    results.append(("test_cay_nhi_phan.py", ok2))

    # Tổng kết
    print("\n" + "="*60)
    print("TỔNG KẾT CHẠY:")
    all_ok = True
    for name, ok in results:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"  {status} — {name}")
        if not ok:
            all_ok = False

    print()
    print("Các file kết quả (dùng để chụp ảnh minh chứng):")
    print(f"  {demo_out}")
    print(f"  {test_out}")
    print()
    print("Hướng dẫn chụp ảnh:")
    print("  1. Mở terminal, cd vào thư mục dự án")
    print("  2. Chạy: py chup_ket_qua.py")
    print("  3. Chụp màn hình terminal (hoặc copy từ file .txt)")
    print("  4. Đặt ảnh vào docs/anh_ket_qua/ với tên A01.png, A02.png, ...")
    print("="*60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
