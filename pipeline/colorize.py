"""썸네일 배경 흑백 사진 → 컬러 복원 (2026-11-24 · DDColor-tiny, Apache-2.0 · 추가 비용 0원)

  python colorize.py <ep>

격전의 세계사 썸네일은 컬러 배경이 표준(2026-11-19 사용자 지시). 배경으로 고른 사료 사진이 흑백이면
DDColor로 색을 입혀 public/ep/<ep>/thumbcolor/<경로>.jpg 로 저장 → Thumbnail.tsx(ParohoV2Thumb)가
그 파일이 있으면 자동으로 컬러 버전을 쓴다. 원본 사진은 그대로.

- 대상: remotion/Thumbnail.tsx 의 PAROHO_V2["<ep>"] (와 alt) 의 bg — `gray: true` 이거나 `colorize: false` 면 건너뜀
- 이미 컬러인 사진(재연 그림 등)은 건너뜀
- 결과 색이 이상하면(값 범위 검사 실패) 저장하지 않음 → 예전처럼 원본 사용
- ⚠️ AI가 추측한 색이라 실제 군복·깃발 색과 다를 수 있음 → 렌더 뒤 썸네일 PNG를 직접 열어 확인
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / ".cache" / "models"
URL = "https://huggingface.co/edgetools/ddcolor/resolve/main/ddcolor-tiny-fp16.onnx"


def log(*a):
    print("[colorize]", *a, flush=True)


def color_path(bg: str) -> str:
    """ep/<ep>/photos/s061_photo_0.jpg → ep/<ep>/thumbcolor/photos_s061_photo_0.jpg (Thumbnail.tsx와 같은 규칙)"""
    parts = bg.split("/")
    return "/".join(parts[:2] + ["thumbcolor", "_".join(parts[2:]).rsplit(".", 1)[0] + ".jpg"])


def is_gray(img):
    a = np.asarray(img.convert("RGB").resize((96, 96)), dtype=np.int16)
    return float(np.abs(a[..., 0] - a[..., 1]).mean() + np.abs(a[..., 1] - a[..., 2]).mean()) < 6


def targets(ep):
    src = (ROOT / "remotion" / "Thumbnail.tsx").read_text(encoding="utf-8")
    i = src.find(f'"{ep}": {{', src.find("PAROHO_V2"))
    if i < 0:
        return []
    j = src.find("\n  \"", i + 5)  # 다음 에피소드 항목까지
    blk = src[i: j if j > 0 else i + 4000]
    if re.search(r"\bgray:\s*true", blk) or re.search(r"\bcolorize:\s*false", blk):
        log("gray/colorize 설정으로 건너뜀")
        return []
    return list(dict.fromkeys(re.findall(r'\bbg:\s*"([^"]+)"', blk)))


def model():
    p = MODELS / "ddcolor-tiny-fp16.onnx"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        log("모델 받기 (약 130MB)")
        for i in range(4):
            try:
                urllib.request.urlretrieve(URL, p.with_suffix(".part"))
                p.with_suffix(".part").rename(p)
                break
            except Exception as e:  # noqa: BLE001
                log("  재시도", i + 1, e)
                time.sleep(5 * (i + 1))
    import onnxruntime as ort
    return ort.InferenceSession(str(p), providers=["CPUExecutionProvider"])


def colorize(sess, img: Image.Image) -> Image.Image | None:
    import cv2
    bgr = cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR).astype(np.float32) / 255.0
    H, W = bgr.shape[:2]
    orig_l = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab)[:, :, :1]
    small = cv2.resize(bgr, (512, 512))
    l_s = cv2.cvtColor(small, cv2.COLOR_BGR2Lab)[:, :, :1]
    gray_rgb = cv2.cvtColor(np.concatenate([l_s, np.zeros_like(l_s), np.zeros_like(l_s)], -1), cv2.COLOR_LAB2RGB)
    x = gray_rgb.transpose(2, 0, 1)[None].astype(np.float32)
    ab = sess.run(None, {sess.get_inputs()[0].name: x})[0][0].astype(np.float32).transpose(1, 2, 0)
    if not np.isfinite(ab).all():
        return None
    m = float(np.abs(ab).mean())
    if not (1.5 <= m <= 45):  # 색이 거의 없거나 비정상적으로 강하면 실패로 봄
        log(f"  색 범위 이상(평균 |ab| {m:.1f}) → 원본 사용")
        return None
    ab = cv2.resize(ab, (W, H))
    out = cv2.cvtColor(np.concatenate([orig_l, ab], -1), cv2.COLOR_LAB2BGR)
    out = (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def main(ep):
    sess = None
    for bg in targets(ep):
        src = ROOT / "public" / bg
        if not src.exists():
            log("배경 파일 없음:", bg)
            continue
        img = Image.open(src).convert("RGB")
        if not is_gray(img):
            log("이미 컬러:", bg)
            continue
        dst = ROOT / "public" / color_path(bg)
        try:
            sess = sess or model()
            out = colorize(sess, img)
            if out is not None:
                dst.parent.mkdir(parents=True, exist_ok=True)
                out.save(dst, quality=92)
                log("컬러 복원:", bg, "→", color_path(bg))
        except Exception as e:  # noqa: BLE001 — 실패해도 썸네일은 원본으로 렌더
            log("실패(원본 사용):", bg, repr(e)[:200])


if __name__ == "__main__":
    main(sys.argv[1])
