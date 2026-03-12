# Hệ thống Crawl Dữ Liệu Intraday Chứng Khoán

Đây là hệ thống Python dùng để crawl dữ liệu khớp lệnh intraday từ thư viện vnstock theo chu kỳ thời gian được cấu hình.

**Hệ thống tự động**

- Crawl dữ liệu cho nhiều mã cổ phiếu
- Lưu dữ liệu theo từng mã
- Ghi log hoạt động
- Tự động merge dữ liệu cuối ngày
- Loại bỏ dữ liệu trùng lặp
- Hệ thống được thiết kế để chạy ổn định trong thời gian dài.

## Cài đặt

```
pip install vnstock pandas schedule
```

## Cấu hình hệ thống

Tất cả thông số nằm trong file: `config.py`

| Tham số                  | Ý nghĩa                            |
| ------------------------ | ---------------------------------- |
| `CRAWL_INTERVAL_MINUTES` | Khoảng cách giữa các lần crawl     |
| `MERGE_TIME`             | Thời điểm merge dữ liệu trong ngày |
| `MAX_WORKERS`            | Số thread crawl song song          |
| `RETRY`                  | Số lần retry khi API lỗi           |
| `PAGE_SIZE`              | Số record intraday yêu cầu         |

## Danh sách mã cổ phiếu

Điều chỉnh danh sách mã cổ phiếu cần crawl trong file `symbols.txt`. Các mã cách nhau bằng dấu phẩy (,).

## Chạy hệ thống

Chạy crawler bằng lệnh:

```
python scheduler.py
```

Hệ thống tự động merge các file vào thời điểm được cấu hình trong file `config.py`. Ngoài ra có thể merge thủ công:

```
python merge.py
```


## Output

Output được lưu trong folder `data/`:

- Kết quả mỗi lần crawl lưu trong file: `SYMBOL-DDMMYYYY-HHMM.csv`. Mỗi lần crawl được 1,500 dòng.

- Kết quả sau khi merge lưu trong file: `SYMBOL_FULL.csv`. Các dòng trùng lặp sẽ được tự động loại bỏ.

## Logging

Log được lưu trong thư mục: `logs/`

Hệ thống sử dụng log rotate theo ngày. 