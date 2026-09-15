# -*- coding: utf-8 -*-
"""从阿里云 OSS 照片头部 EXIF 提取拍摄日期，生成 dates.js 供前端灯箱显示。

用法：
  1) 修改下方 BUCKET_NAME / ENDPOINT / PREFIX 为你的 Bucket 信息
  2) 设置环境变量 OSS_ACCESS_KEY_ID / OSS_ACCESS_KEY_SECRET（建议只读子账号）
  3) 执行 python make_dates.py，生成 dates.js

说明：对象名与本地文件名无需对应——直接对每个对象发 Range 请求只拉文件头部
     （EXIF 就在 JPEG 头部 APP1 段），解析失败者再用更大范围重试。
"""
import io
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import oss2
from PIL import Image

# ===== 按自己的 Bucket 修改这三项 =====
BUCKET_NAME = "best-images"
ENDPOINT = "https://oss-cn-beijing.aliyuncs.com"
PREFIX = "images/"

HEAD = 256 * 1024        # 首次尝试的头部字节数
RETRY = 1024 * 1024      # 解析失败时的重试字节数
DATES_JS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dates.js")


def get_bucket():
    ak = os.environ.get("OSS_ACCESS_KEY_ID")
    sk = os.environ.get("OSS_ACCESS_KEY_SECRET")
    if not (ak and sk):
        sys.exit("请先设置环境变量 OSS_ACCESS_KEY_ID / OSS_ACCESS_KEY_SECRET（建议使用只读子账号）")
    return oss2.Bucket(oss2.Auth(ak, sk), ENDPOINT, BUCKET_NAME)


def list_objects(bucket):
    out = []
    for obj in oss2.ObjectIterator(bucket, prefix=PREFIX):
        if obj.key == PREFIX or obj.key.endswith("/"):
            continue  # 跳过目录占位对象
        out.append(obj.key)
    return out


def exif_date(data):
    """从 JPEG 头部字节里解析拍摄日期，返回 'YYYY-MM-DD' 或 None。"""
    try:
        im = Image.open(io.BytesIO(data))
        exif = im.getexif()
        dt = exif.get(306)                       # DateTime（修改时间）
        try:
            dt = exif.get_ifd(0x8769).get(36867) or dt   # DateTimeOriginal 优先
        except Exception:
            pass
        if not dt:
            return None
        m = re.match(r"(\d{4})[:\-](\d{2})[:\-](\d{2})", str(dt))
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None
    except Exception:
        return None


def fetch_date(bucket, key):
    for n in (HEAD, RETRY):
        try:
            res = bucket.get_object(key, byte_range=(0, n - 1))
            d = exif_date(res.read())
            if d:
                return d
        except oss2.exceptions.RangeNotSatisfiable:
            return None
        except Exception:
            continue
    return None


def main():
    bucket = get_bucket()
    keys = list_objects(bucket)
    print(f"共 {len(keys)} 个对象，开始提取 EXIF 拍摄日期 ...")

    dates = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        for key, d in zip(keys, pool.map(lambda k: fetch_date(bucket, k), keys)):
            if d:
                dates[key.split("/")[-1]] = d

    lines = ",\n".join(f'"{k}": "{d}"' for k, d in sorted(dates.items()))
    with open(DATES_JS, "w", encoding="utf-8") as f:
        f.write(f"window.photoDates = {{\n{lines}\n\n}};\n")
    print(f"完成：{len(dates)}/{len(keys)} 张有拍摄日期，已生成 dates.js")
    miss = [k for k in keys if k.split("/")[-1] not in dates]
    if miss:
        print(f"无日期（前端自动隐藏日期角标）共 {len(miss)} 个，例如：{miss[:5]}")


if __name__ == "__main__":
    main()
