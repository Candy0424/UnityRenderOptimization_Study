from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Unity_URP_Core_Lecture_Revised.pdf"
TMP = ROOT / "tmp" / "pdfs" / "urp_revised_assets"

PAGE_W, PAGE_H = landscape(A4)
MARGIN_X = 46
TOP_Y = PAGE_H - 42

FONT_REG = "Malgun"
FONT_BOLD = "Malgun-Bold"

pdfmetrics.registerFont(TTFont(FONT_REG, r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\malgunbd.ttf"))

INK = colors.HexColor("#161A24")
MUTED = colors.HexColor("#5E687A")
LIGHT = colors.HexColor("#F3F6FB")
PANEL = colors.HexColor("#FFFFFF")
GRID = colors.HexColor("#D8DFEA")
BLUE = colors.HexColor("#4F7DFF")
CYAN = colors.HexColor("#2DBBC5")
GREEN = colors.HexColor("#2FA779")
AMBER = colors.HexColor("#F2A23A")
RED = colors.HexColor("#E45858")
PURPLE = colors.HexColor("#7D64D9")
DARK = colors.HexColor("#242936")

URP_PACKAGE = ROOT / "Library" / "PackageCache" / "com.unity.render-pipelines.universal@7327e77c1cc2"

RAW_IMAGES = {
    "urp_icon": ROOT / "Assets" / "TutorialInfo" / "Icons" / "URP.png",
    "coins_base": URP_PACKAGE / "Samples~" / "URPPackageSamples" / "Shaders" / "Lit" / "Textures" / "Coins_Base.png",
    "coins_normal": URP_PACKAGE / "Samples~" / "URPPackageSamples" / "Shaders" / "Lit" / "Textures" / "Coins_Normal.png",
    "coins_metallic": URP_PACKAGE / "Samples~" / "URPPackageSamples" / "Shaders" / "Lit" / "Textures" / "Coins_Metallic.png",
    "coins_emission": URP_PACKAGE / "Samples~" / "URPPackageSamples" / "Shaders" / "Lit" / "Textures" / "Coins_Emission.png",
    "lens_ring": URP_PACKAGE / "Samples~" / "URPPackageSamples" / "LensFlares" / "Textures" / "Ring.png",
}

SOURCES = {
    "S1": ("Project Unity version", "ProjectSettings/ProjectVersion.txt", "local project file"),
    "S2": ("Project package manifest", "Packages/manifest.json", "local project file"),
    "S3": (
        "Universal Render Pipeline Asset | Universal RP 17.0.0",
        "https://docs.unity.cn/Packages/com.unity.render-pipelines.universal%4017.0/manual/universalrp-asset.html",
        "Unity Technologies",
    ),
    "S4": (
        "Universal Renderer | Universal RP 17.0.0",
        "https://docs.unity.cn/Packages/com.unity.render-pipelines.universal%4017.0/manual/urp-universal-renderer.html",
        "Unity Technologies",
    ),
    "S5": (
        "Choose a rendering path in URP | Unity 6",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/urp/rendering-paths-comparison.html",
        "Unity Technologies",
    ),
    "S6": (
        "URP Renderer Feature | Universal RP 16.0.3",
        "https://docs.unity.cn/Packages/com.unity.render-pipelines.universal%4016.0/manual/urp-renderer-feature.html",
        "Unity Technologies",
    ),
    "S7": (
        "Render graph system in URP | Unity 6",
        "https://docs.unity3d.com/kr/current/Manual/urp/render-graph.html",
        "Unity Technologies",
    ),
    "S8": (
        "Multiple cameras in URP | Unity 6",
        "https://docs.unity3d.com/kr/6000.0/Manual/urp/cameras-multiple.html",
        "Unity Technologies",
    ),
    "S9": (
        "Volumes in URP | Unity 6",
        "https://docs.unity3d.com/kr/6000.0/Manual/urp/volumes-landing-page.html",
        "Unity Technologies",
    ),
    "S10": (
        "Optimize shadow rendering in URP | Unity 6",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/shadows-optimization.html",
        "Unity Technologies",
    ),
    "S11": (
        "Scriptable Render Pipeline Batcher",
        "https://docs.unity.cn/Manual/SRPBatcher.html",
        "Unity Technologies",
    ),
    "S12": (
        "Shading models in URP | Unity 6",
        "https://docs.unity3d.com/jp/current/Manual/urp/shading-model.html",
        "Unity Technologies",
    ),
    "S13": (
        "Frame Debugger | Unity 6",
        "https://docs.unity.cn/6000.0/Documentation/Manual/FrameDebugger-debug.html",
        "Unity Technologies",
    ),
    "I1": (
        "URP template icon",
        "Assets/TutorialInfo/Icons/URP.png",
        "local Unity template asset",
    ),
    "I2": (
        "URP Package Samples - Lit material textures",
        "Library/PackageCache/com.unity.render-pipelines.universal@7327e77c1cc2/Samples~/URPPackageSamples/Shaders/Lit/Textures",
        "Unity URP package sample assets",
    ),
    "I3": (
        "URP Package Samples - Lens flare Ring texture",
        "Library/PackageCache/com.unity.render-pipelines.universal@7327e77c1cc2/Samples~/URPPackageSamples/LensFlares/Textures/Ring.png",
        "Unity URP package sample asset",
    ),
}


def prepare_images() -> dict[str, Path]:
    TMP.mkdir(parents=True, exist_ok=True)
    prepared: dict[str, Path] = {}
    for name, path in RAW_IMAGES.items():
        if not path.exists():
            continue
        img = Image.open(path).convert("RGBA")
        if name == "lens_ring":
            bg = Image.new("RGBA", img.size, (18, 22, 32, 255))
        elif name in {"coins_emission", "coins_metallic"}:
            bg = Image.new("RGBA", img.size, (58, 62, 70, 255))
        else:
            bg = Image.new("RGBA", img.size, (245, 247, 251, 255))
        bg.alpha_composite(img)
        img = bg.convert("RGB")
        img = ImageOps.contain(img, (900, 900))
        out = TMP / f"{name}.jpg"
        img.save(out, quality=92)
        prepared[name] = out
    return prepared


def find_value(path: Path, key: str, default: str = "-") -> str:
    if not path.exists():
        return default
    pattern = re.compile(rf"\b{re.escape(key)}:\s*(.+)$")
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = pattern.search(line)
        if match:
            return match.group(1).strip()
    return default


def bool_text(v: str) -> str:
    return "On" if v.strip() == "1" else "Off"


PROJECT_VALUES = {
    "pc": {
        "Render Scale": find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_RenderScale"),
        "HDR": bool_text(find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_SupportsHDR")),
        "MSAA": find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_MSAA"),
        "Main Shadow": find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_MainLightShadowmapResolution"),
        "Add Light Shadow": bool_text(find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_AdditionalLightShadowsSupported")),
        "Shadow Distance": find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_ShadowDistance"),
        "Cascade Count": find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_ShadowCascadeCount"),
        "SRP Batcher": bool_text(find_value(ROOT / "Assets" / "Settings" / "PC_RPAsset.asset", "m_UseSRPBatcher")),
        "Transparent Shadow": bool_text(find_value(ROOT / "Assets" / "Settings" / "PC_Renderer.asset", "m_ShadowTransparentReceive")),
        "SSAO Feature": "Present",
    },
    "mobile": {
        "Render Scale": find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_RenderScale"),
        "HDR": bool_text(find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_SupportsHDR")),
        "MSAA": find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_MSAA"),
        "Main Shadow": find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_MainLightShadowmapResolution"),
        "Add Light Shadow": bool_text(find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_AdditionalLightShadowsSupported")),
        "Shadow Distance": find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_ShadowDistance"),
        "Cascade Count": find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_ShadowCascadeCount"),
        "SRP Batcher": bool_text(find_value(ROOT / "Assets" / "Settings" / "Mobile_RPAsset.asset", "m_UseSRPBatcher")),
        "Transparent Shadow": bool_text(find_value(ROOT / "Assets" / "Settings" / "Mobile_Renderer.asset", "m_ShadowTransparentReceive")),
        "SSAO Feature": "None",
    },
}


def wrap_line(c: canvas.Canvas, text: str, max_width: float, font: str, size: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    cur = ""
    for word in words:
        candidate = word if not cur else f"{cur} {word}"
        if c.stringWidth(candidate, font, size) <= max_width:
            cur = candidate
            continue
        if cur:
            lines.append(cur)
            cur = ""
        if c.stringWidth(word, font, size) <= max_width:
            cur = word
        else:
            piece = ""
            for ch in word:
                candidate = piece + ch
                if c.stringWidth(candidate, font, size) <= max_width:
                    piece = candidate
                else:
                    if piece:
                        lines.append(piece)
                    piece = ch
            cur = piece
    if cur:
        lines.append(cur)
    return lines


def text(
    c: canvas.Canvas,
    body: str,
    x: float,
    y: float,
    width: float,
    font: str = FONT_REG,
    size: int = 12,
    leading: int = 18,
    color=INK,
) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for para in body.split("\n"):
        if not para:
            y -= leading
            continue
        for line in wrap_line(c, para, width, font, size):
            c.drawString(x, y, line)
            y -= leading
    return y


def header(c: canvas.Canvas, page: int, title: str, sources: list[str] | None = None):
    sources = sources or []
    c.setFillColor(LIGHT)
    c.rect(0, PAGE_H - 30, PAGE_W, 30, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(FONT_BOLD, 9)
    c.drawString(MARGIN_X, PAGE_H - 19, "Unity URP Core Lecture - Revised")
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 19, "이미지, 비유, 실제 예시 중심")
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 23)
    c.drawString(MARGIN_X, TOP_Y - 21, title)
    c.setStrokeColor(GRID)
    c.line(MARGIN_X, TOP_Y - 35, PAGE_W - MARGIN_X, TOP_Y - 35)
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawString(MARGIN_X, 20, f"{page:02d}")
    if sources:
        c.drawRightString(PAGE_W - MARGIN_X, 20, "근거: " + ", ".join(sources))


def bullet(c, items: list[str], x: float, y: float, width: float, size: int = 12, leading: int = 19) -> float:
    for item in items:
        c.setFillColor(BLUE)
        c.circle(x + 5, y + 4, 3.1, fill=1, stroke=0)
        y = text(c, item, x + 18, y, width - 18, FONT_REG, size, leading, INK)
        y -= 4
    return y


def card(c, x, y, w, h, title, body, accent=BLUE, source=None):
    c.setFillColor(PANEL)
    c.setStrokeColor(GRID)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 8, w, 8, 4, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 13)
    c.drawString(x + 14, y + h - 29, title)
    text(c, body, x + 14, y + h - 51, w - 28, FONT_REG, 10.5, 15, MUTED)
    if source:
        c.setFillColor(accent)
        c.setFont(FONT_BOLD, 8)
        c.drawRightString(x + w - 12, y + 12, source)


def analogy(c, x, y, w, body):
    card(c, x, y, w, 78, "비유", body, AMBER)


def example(c, x, y, w, body):
    card(c, x, y, w, 78, "실제 예시", body, GREEN)


def image_box(c, img_path: Path, x, y, w, h, caption="", source=""):
    c.setFillColor(PANEL)
    c.setStrokeColor(GRID)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    if img_path.exists():
        img = Image.open(img_path)
        iw, ih = img.size
        scale = min((w - 24) / iw, (h - 44) / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(ImageReader(str(img_path)), x + (w - dw) / 2, y + 28 + (h - 48 - dh) / 2, dw, dh)
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawString(x + 12, y + 12, caption)
    if source:
        c.drawRightString(x + w - 12, y + 12, source)


def inspector(c, x, y, w, h, title, rows, accent=BLUE):
    c.setFillColor(colors.HexColor("#2B303A"))
    c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#3A414E"))
    c.roundRect(x + 8, y + h - 36, w - 16, 28, 6, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 11)
    c.drawString(x + 20, y + h - 26, title)
    yy = y + h - 56
    for label, value in rows:
        c.setFillColor(colors.HexColor("#464E5C"))
        c.roundRect(x + 12, yy - 5, w - 24, 24, 5, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#CBD3E0"))
        c.setFont(FONT_REG, 8.5)
        c.drawString(x + 22, yy + 3, label)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 8.5)
        c.drawRightString(x + w - 22, yy + 3, str(value))
        yy -= 28
    c.setFillColor(accent)
    c.roundRect(x + 12, y + 10, w - 24, 8, 4, fill=1, stroke=0)


def draw_urp_stack(c, x, y):
    labels = [
        ("Project Settings", "어떤 파이프라인을 쓸지 선택", BLUE),
        ("URP Asset", "품질 정책과 전역 옵션", CYAN),
        ("Renderer Asset", "프레임을 그리는 순서표", GREEN),
        ("Camera", "어디를 어떤 출력으로 볼지", AMBER),
        ("Scene Objects", "메시, 머티리얼, 조명", PURPLE),
        ("GPU Frame", "최종 화면", RED),
    ]
    for i, (a, b, col) in enumerate(labels):
        xx = x + i * 116
        c.setFillColor(col)
        c.roundRect(xx, y, 98, 55, 10, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 9.2)
        c.drawCentredString(xx + 49, y + 32, a)
        c.setFont(FONT_REG, 6.8)
        c.drawCentredString(xx + 49, y + 17, b)
        if i < len(labels) - 1:
            c.setStrokeColor(MUTED)
            c.line(xx + 101, y + 28, xx + 113, y + 28)


def draw_resolution(c, x, y):
    c.setFillColor(BLUE)
    c.roundRect(x, y + 56, 230, 128, 8, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.roundRect(x + 26, y + 78, 184, 82, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(x + 115, y + 111, "Render Scale 0.8")
    c.setFont(FONT_REG, 9)
    c.drawCentredString(x + 115, y + 94, "1920x1080 -> 1536x864")
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 12)
    c.drawString(x, y + 25, "비유: 큰 사진을 작게 찍은 뒤 확대한다")
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 10)
    c.drawString(x, y + 8, "GPU는 픽셀 일을 덜 하지만, 선명도는 조금 희생된다.")


def draw_edges(c, x, y):
    c.setStrokeColor(RED)
    c.setLineWidth(7)
    c.line(x + 20, y + 30, x + 96, y + 106)
    c.setStrokeColor(BLUE)
    c.setLineWidth(7)
    c.line(x + 142, y + 30, x + 218, y + 106)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 11)
    c.drawCentredString(x + 58, y + 8, "MSAA Off")
    c.drawCentredString(x + 180, y + 8, "MSAA On")
    c.setFillColor(LIGHT)
    for i in range(7):
        c.rect(x + 15 + i * 12, y + 20 + i * 12, 12, 12, fill=1, stroke=0)


def draw_feature_chain(c, x, y):
    stages = [
        ("Opaque", BLUE),
        ("SSAO", CYAN),
        ("Screen Shadow", PURPLE),
        ("Transparent", RED),
        ("Post", GREEN),
        ("Final", AMBER),
    ]
    for i, (name, col) in enumerate(stages):
        xx = x + i * 104
        c.setFillColor(col)
        c.roundRect(xx, y, 88, 42, 9, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 8.2)
        c.drawCentredString(xx + 44, y + 17, name)
        if i < len(stages) - 1:
            c.setStrokeColor(MUTED)
            c.line(xx + 91, y + 21, xx + 101, y + 21)


def draw_path_table(c, x, y):
    rows = [
        ("Forward", "손님마다 바로 요리", "조명이 적고 구조가 단순할 때"),
        ("Forward+", "조명 목록을 먼저 정리", "조명이 많지만 Forward 계열이 필요할 때"),
        ("Deferred", "재료를 창고에 먼저 분류", "불투명 오브젝트와 조명이 많을 때"),
    ]
    widths = [120, 190, 285]
    c.setFillColor(BLUE)
    c.roundRect(x, y + 112, sum(widths), 32, 7, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 10)
    for i, h in enumerate(["경로", "비유", "언제 생각할까"]):
        c.drawCentredString(x + sum(widths[:i]) + widths[i] / 2, y + 123, h)
    for r, row in enumerate(rows):
        yy = y + 112 - (r + 1) * 36
        c.setFillColor(PANEL if r % 2 == 0 else LIGHT)
        c.rect(x, yy, sum(widths), 36, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont(FONT_REG, 9)
        xx = x
        for txt, w in zip(row, widths):
            c.drawString(xx + 9, yy + 13, txt)
            xx += w
    c.setStrokeColor(GRID)
    c.rect(x, y + 4, sum(widths), 140, fill=0, stroke=1)


def draw_camera_stack(c, x, y):
    c.setFillColor(BLUE)
    c.roundRect(x, y + 120, 210, 54, 12, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(x + 105, y + 143, "Base Camera")
    overlays = [("Overlay UI", CYAN), ("Overlay Props", GREEN), ("Overlay FX", PURPLE)]
    for i, (label, col) in enumerate(overlays):
        yy = y + 60 - i * 55
        c.setFillColor(col)
        c.roundRect(x + 28, yy, 154, 42, 10, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 10)
        c.drawCentredString(x + 105, yy + 17, label)
        c.setStrokeColor(MUTED)
        c.line(x + 105, yy + 44, x + 105, yy + 56)


def draw_depth_opaque(c, x, y):
    for i in range(12):
        c.setFillColor(colors.Color(i / 16, i / 16, i / 16))
        c.rect(x + i * 12, y + 88, 12, 72, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#DDE8FF"))
    c.roundRect(x + 190, y + 88, 145, 72, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#8EB4FF"))
    c.circle(x + 240, y + 124, 23, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setFillAlpha(0.42)
    c.roundRect(x + 210, y + 100, 104, 48, 8, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 10)
    c.drawString(x, y + 62, "Depth Texture")
    c.drawString(x + 190, y + 62, "Opaque Texture")
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 9)
    c.drawString(x, y + 45, "좌석 배치도처럼 앞뒤 관계를 알려준다.")
    c.drawString(x + 190, y + 45, "투명 효과가 참고할 무대 사진이다.")


def title_slide(c, page, images):
    c.setFillColor(colors.HexColor("#EEF4FF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 34)
    c.drawString(MARGIN_X, PAGE_H - 134, "Unity URP 핵심 강의")
    c.setFont(FONT_BOLD, 22)
    c.drawString(MARGIN_X, PAGE_H - 173, "이미지, 비유, 실제 예시 보강판")
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 14)
    c.drawString(MARGIN_X, PAGE_H - 207, "URP를 옵션 목록이 아니라 렌더링 스튜디오 구조로 이해하기")
    if "urp_icon" in images:
        image_box(c, images["urp_icon"], PAGE_W - 260, PAGE_H - 250, 178, 125, "Unity URP template icon", "I1")
    card(
        c,
        MARGIN_X,
        108,
        PAGE_W - MARGIN_X * 2,
        130,
        "이번 수정본의 원칙",
        "Unity에서 직접 볼 수 있는 현재 프로젝트 설정값을 Inspector 스타일 이미지로 재구성하고, URP 패키지 샘플 이미지를 함께 사용했다. 각 기능은 비유와 실제 예시를 붙여 실습 전에 머릿속 그림이 생기도록 구성했다.",
        BLUE,
        "S1/S2/I1/I2",
    )
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawString(MARGIN_X, 20, f"{page:02d}")


def slide_source_note(c, page):
    header(c, page, "0강. 이 문서의 이미지 사용 방식", ["S1", "S2", "I1", "I2"])
    bullet(c, [
        "온라인 Unity 문서의 스크린샷을 그대로 복제하지 않고, 현재 프로젝트의 Unity Asset 값을 기반으로 Inspector 스타일 화면을 직접 재구성했다.",
        "URP 패키지에 포함된 샘플 텍스처는 실제 이미지로 사용했다. 예: Coins_Base, Coins_Normal, Coins_Metallic, LensFlares/Ring.",
        "각 페이지의 하단 근거 태그는 Unity 공식 문서, 로컬 프로젝트 파일, 로컬 Unity 패키지 샘플 위치를 가리킨다.",
        "특정 회사의 내부 렌더 파이프라인이나 모델 포맷은 공개 자료 없이 단정하지 않는다.",
    ], MARGIN_X, TOP_Y - 78, PAGE_W - 2 * MARGIN_X, 13, 22)
    analogy(c, MARGIN_X, 112, 350, "스크린샷은 칠판 사진이고, Inspector 스타일 도식은 선생님이 칠판 내용을 다시 정리한 필기다.")
    example(c, 432, 112, 360, "`PC_RPAsset.asset`의 Render Scale 1.0과 `Mobile_RPAsset.asset`의 0.8을 실제 비교값으로 사용한다.")


def slide_big_picture(c, page, images):
    header(c, page, "1강. URP는 렌더링 스튜디오다", ["S3", "S4"])
    draw_urp_stack(c, MARGIN_X, TOP_Y - 140)
    analogy(c, MARGIN_X, 250, 350, "URP Asset은 촬영감독의 품질 지시서, Renderer Asset은 촬영 순서표, Camera는 실제 카메라, Volume은 색보정 룸이다.")
    example(c, 432, 250, 360, "라이브 무대 씬에서 PC는 그림자와 SSAO를 켜고, Mobile은 Render Scale과 그림자 수를 줄이는 식으로 같은 씬을 다르게 촬영한다.")
    if "urp_icon" in images:
        image_box(c, images["urp_icon"], 610, 96, 180, 124, "Unity URP template icon", "I1")


def slide_urp_asset(c, page):
    header(c, page, "2강. URP Asset은 품질 지시서다", ["S3", "S1"])
    inspector(c, MARGIN_X, 160, 250, 235, "PC_RPAsset Inspector", [
        ("Render Scale", PROJECT_VALUES["pc"]["Render Scale"]),
        ("HDR", PROJECT_VALUES["pc"]["HDR"]),
        ("MSAA", PROJECT_VALUES["pc"]["MSAA"]),
        ("Main Shadow", PROJECT_VALUES["pc"]["Main Shadow"]),
        ("Additional Shadow", PROJECT_VALUES["pc"]["Add Light Shadow"]),
        ("Cascade Count", PROJECT_VALUES["pc"]["Cascade Count"]),
    ], BLUE)
    inspector(c, 320, 160, 250, 235, "Mobile_RPAsset Inspector", [
        ("Render Scale", PROJECT_VALUES["mobile"]["Render Scale"]),
        ("HDR", PROJECT_VALUES["mobile"]["HDR"]),
        ("MSAA", PROJECT_VALUES["mobile"]["MSAA"]),
        ("Main Shadow", PROJECT_VALUES["mobile"]["Main Shadow"]),
        ("Additional Shadow", PROJECT_VALUES["mobile"]["Add Light Shadow"]),
        ("Cascade Count", PROJECT_VALUES["mobile"]["Cascade Count"]),
    ], CYAN)
    card(c, 598, 292, 195, 104, "핵심", "URP Asset은 Rendering, Quality, Lighting, Shadows, Post-processing 같은 전역 설정을 묶는다.", GREEN, "S3")
    analogy(c, 598, 190, 195, "촬영감독이 '오늘은 고화질', '오늘은 모바일 절약 모드'라고 지시하는 문서다.")
    example(c, 598, 88, 195, "이 프로젝트는 PC와 Mobile Asset이 이미 있어 비교 실습 출발점이 좋다.")


def slide_render_scale(c, page):
    header(c, page, "3강. Render Scale은 해상도 수도꼭지다", ["S3", "S1"])
    draw_resolution(c, MARGIN_X, 170)
    bullet(c, [
        "Unity 문서는 Render Scale이 기기 해상도가 아니라 렌더 타깃 해상도를 조절한다고 설명한다.",
        "현재 프로젝트: PC는 1.0, Mobile은 0.8이다.",
        "1920x1080 기준 0.8은 내부 렌더링을 약 1536x864로 줄이는 느낌이다.",
        "UI는 네이티브 해상도에 남을 수 있으므로, 3D 장면 선명도와 UI 선명도를 구분해서 본다.",
    ], 344, TOP_Y - 78, 450, 12.5, 21)
    example(c, 344, 92, 450, "Benchmark_Field에서 Render Scale 1.0, 0.8, 0.67을 바꿔 GPU ms와 화면 선명도를 함께 기록한다.")


def slide_hdr_msaa(c, page):
    header(c, page, "4강. HDR과 MSAA는 렌즈와 가장자리 보정이다", ["S3"])
    card(c, MARGIN_X, 298, 330, 106, "HDR", "밝은 조명과 Bloom을 더 넓은 밝기 범위로 표현한다. 낮은 사양에서는 계산을 줄이기 위해 끌 수 있다.", BLUE, "S3")
    card(c, MARGIN_X, 170, 330, 106, "MSAA", "기하 경계의 계단 현상을 줄인다. 샘플 수가 늘수록 더 부드럽지만 비용이 늘어난다.", CYAN, "S3")
    draw_edges(c, 450, 190)
    analogy(c, 432, 300, 360, "HDR은 카메라의 다이내믹 레인지, MSAA는 날카로운 계단을 사포로 살짝 다듬는 작업에 가깝다.")
    example(c, 432, 92, 360, "캐릭터 외곽선이 떨리면 MSAA를 검토하고, 무대 조명이 과하게 날아가면 HDR과 Bloom 관계를 확인한다.")


def slide_renderer_asset(c, page):
    header(c, page, "5강. Renderer Asset은 촬영 순서표다", ["S4", "S1"])
    inspector(c, MARGIN_X, 170, 255, 220, "PC_Renderer", [
        ("Transparent Shadow", PROJECT_VALUES["pc"]["Transparent Shadow"]),
        ("Renderer Feature", PROJECT_VALUES["pc"]["SSAO Feature"]),
        ("Role", "Quality/PC"),
        ("Think", "extra passes allowed"),
    ], BLUE)
    inspector(c, 320, 170, 255, 220, "Mobile_Renderer", [
        ("Transparent Shadow", PROJECT_VALUES["mobile"]["Transparent Shadow"]),
        ("Renderer Feature", PROJECT_VALUES["mobile"]["SSAO Feature"]),
        ("Role", "Performance/Mobile"),
        ("Think", "minimum passes"),
    ], CYAN)
    draw_feature_chain(c, MARGIN_X, 104)
    analogy(c, 600, 292, 192, "Renderer는 주방의 조리 순서표다. 어떤 재료를 먼저 익히고, 어떤 소스를 나중에 바를지 정한다.")
    example(c, 600, 190, 192, "PC_Renderer에는 SSAO가 보이고, Mobile_Renderer는 더 가볍게 구성되어 있다.")


def slide_paths(c, page):
    header(c, page, "6강. Forward, Forward+, Deferred는 계산 방식이다", ["S4", "S5"])
    draw_path_table(c, MARGIN_X, 235)
    bullet(c, [
        "Universal Renderer는 Forward, Forward+, Deferred 렌더링 경로를 구현한다.",
        "Forward와 Forward+는 MSAA를 사용할 수 있지만, Deferred는 G-buffer 비용과 제약을 고려한다.",
        "투명 오브젝트는 Deferred에서도 Forward pass로 처리될 수 있으므로 캐릭터 머리카락/이펙트가 많으면 따로 측정한다.",
    ], MARGIN_X, 186, PAGE_W - 2 * MARGIN_X, 12, 20)
    example(c, MARGIN_X, 82, PAGE_W - 2 * MARGIN_X, "라이브 무대에 조명이 많으면 Forward+나 Deferred를 비교할 수 있지만, 모바일과 투명 파츠가 많다면 Forward 기반 최적화를 먼저 실험한다.")


def slide_renderer_feature(c, page):
    header(c, page, "7강. Renderer Feature는 카메라 앞 특수 장비다", ["S6", "S4"])
    cards = [
        ("Render Objects", "특정 레이어를 다른 시점에 그리거나 material/depth/stencil override를 적용한다.", BLUE),
        ("SSAO", "화면 공간에서 접힌 부분과 가까운 표면을 어둡게 만들어 입체감을 준다.", CYAN),
        ("Screen Space Shadows", "주 방향광 그림자를 화면 공간에서 처리한다. 추가 렌더 타깃 비용을 본다.", PURPLE),
        ("Full Screen Pass", "전체 화면 효과와 커스텀 포스트 프로세싱을 넣는 확장 지점이다.", GREEN),
    ]
    for i, (t, b, col) in enumerate(cards):
        card(c, MARGIN_X + (i % 2) * 380, TOP_Y - 160 - (i // 2) * 136, 350, 102, t, b, col, "S6")
    analogy(c, MARGIN_X, 82, 350, "기본 카메라 앞에 ND 필터, 확산 필터, 특수 렌즈를 추가로 끼우는 느낌이다.")
    example(c, 432, 82, 360, "PC 품질에서는 SSAO를 켜서 접힌 부분을 살리고, Mobile에서는 꺼서 GPU 비용을 낮춘다.")


def slide_render_graph(c, page):
    header(c, page, "8강. Render Graph는 작업지시서와 임시 창고다", ["S7"])
    c.setFillColor(LIGHT)
    c.roundRect(520, 114, 240, 260, 16, fill=1, stroke=0)
    for i, (label, col) in enumerate([("Shadow Pass", BLUE), ("Depth Texture", CYAN), ("Opaque Pass", GREEN), ("Post Pass", PURPLE), ("Final Frame", RED)]):
        yy = 326 - i * 48
        c.setFillColor(col)
        c.roundRect(560, yy, 160, 32, 8, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 10)
        c.drawCentredString(640, yy + 12, label)
        if i < 4:
            c.setStrokeColor(MUTED)
            c.line(640, yy, 640, yy - 16)
    bullet(c, [
        "Unity 6의 URP 17에는 Render Graph 시스템이 도입되었다.",
        "Render Graph는 렌더 패스와 리소스의 관계를 더 명시적으로 관리한다.",
        "초급 단계에서는 코드를 바로 작성하기보다 Frame Debugger에서 패스 흐름을 읽는 습관이 먼저다.",
    ], MARGIN_X, TOP_Y - 78, 430, 13, 22)
    analogy(c, MARGIN_X, 164, 410, "택배 작업표처럼 '어떤 상자를 언제 만들고, 언제 버리고, 어디로 넘길지'를 정리한다.")
    example(c, MARGIN_X, 72, 410, "Depth Texture를 쓰는 효과가 있으면 Render Graph에서 깊이 리소스가 어느 pass에서 만들어지고 소비되는지 추적한다.")


def slide_camera(c, page):
    header(c, page, "9강. Camera Stack은 영상 편집 트랙이다", ["S8"])
    draw_camera_stack(c, 574, 170)
    bullet(c, [
        "URP에는 Base Camera와 Overlay Camera 렌더 타입이 있다.",
        "Base Camera는 화면이나 Render Texture 같은 렌더 타깃에 직접 그린다.",
        "Overlay Camera는 Base Camera 출력 위에 쌓인다.",
        "Unity 문서는 활성 카메라는 아무것도 렌더링하지 않아도 전체 렌더링 루프를 거칠 수 있다고 설명한다.",
    ], MARGIN_X, TOP_Y - 78, 470, 13, 22)
    analogy(c, MARGIN_X, 154, 430, "Base는 배경 영상 트랙, Overlay는 자막/효과/소품 트랙이다. 트랙이 늘면 편집기도 할 일이 늘어난다.")
    example(c, MARGIN_X, 62, 430, "무대와 캐릭터는 Base Camera, UI와 특정 소품은 Overlay Camera로 나눠 Culling Mask 비용을 측정한다.")


def slide_volume(c, page):
    header(c, page, "10강. Volume은 공간별 색보정 룸이다", ["S9"])
    c.setFillColor(LIGHT)
    c.roundRect(498, 142, 285, 220, 16, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.circle(590, 260, 58, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.circle(690, 260, 58, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(590, 260, "Stage")
    c.drawCentredString(690, 260, "Backstage")
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(640, 174, "Priority / Weight / Blend")
    bullet(c, [
        "Volume은 포스트 프로세싱 효과를 씬 전체 또는 특정 공간에 적용하는 시스템이다.",
        "Volume Profile에는 Bloom, Color Adjustments, Depth of Field 같은 override가 들어간다.",
        "Global Volume은 전체 룩을, Local Volume은 특정 구역의 색감과 효과를 바꾸는 데 쓴다.",
    ], MARGIN_X, TOP_Y - 78, 420, 13, 22)
    analogy(c, MARGIN_X, 154, 400, "무대 조명실에서 장면마다 색온도, 안개, 하이라이트를 바꾸는 프리셋이다.")
    example(c, MARGIN_X, 62, 400, "캐릭터 클로즈업 구역에만 Bloom을 강하게 주고, 일반 이동 구역에서는 Bloom을 낮춰 비용을 비교한다.")


def slide_post_image(c, page, images):
    header(c, page, "11강. Post-processing은 화면 전체 필터다", ["S9", "I3"])
    if "lens_ring" in images:
        image_box(c, images["lens_ring"], 545, 118, 230, 230, "Unity URP Package Samples - Lens flare Ring", "I3")
    bullet(c, [
        "Post-processing은 이미 그려진 화면을 다시 가공한다.",
        "Bloom, 색보정, Vignette, Depth of Field 같은 효과는 화면 전체나 큰 영역을 다루므로 GPU 비용을 확인한다.",
        "렌즈 플레어나 Bloom 같은 효과는 무대감이 좋아지지만, 모바일에서는 켜고 끄는 기준이 필요하다.",
    ], MARGIN_X, TOP_Y - 78, 460, 13, 22)
    analogy(c, MARGIN_X, 164, 420, "촬영 후 편집실에서 색보정과 빛 번짐을 얹는 작업이다. 예쁘지만 모든 프레임마다 편집비가 든다.")
    example(c, MARGIN_X, 72, 420, "Bloom On/Off, 렌더 스케일 1.0/0.8 조건을 조합해 GPU ms와 화면 분위기를 함께 기록한다.")


def slide_shader_images(c, page, images):
    header(c, page, "12강. Lit Shader의 텍스처는 역할이 다르다", ["S12", "I2"])
    names = [
        ("coins_base", "Base Map", "색칠"),
        ("coins_normal", "Normal Map", "가짜 요철"),
        ("coins_metallic", "Metallic", "금속 마스크"),
        ("coins_emission", "Emission", "스스로 빛"),
    ]
    for i, (key, title, caption) in enumerate(names):
        x = MARGIN_X + i * 188
        if key in images:
            image_box(c, images[key], x, 218, 166, 166, f"{title} - {caption}", "I2")
        else:
            card(c, x, 218, 166, 166, title, caption, BLUE, "I2")
    analogy(c, MARGIN_X, 116, 350, "Base는 페인트, Normal은 얇은 요철 스티커, Metallic은 금속 여부 스텐실, Emission은 자체 발광 네온이다.")
    example(c, 432, 116, 360, "캐릭터 머티리얼이 많다면 Base/Normal/Emission 사용 여부와 해상도를 표로 기록해 메모리와 GPU 비용을 함께 본다.")


def slide_shader_choice(c, page):
    header(c, page, "13강. Lit, Simple Lit, Unlit은 조명 계산의 양이 다르다", ["S12"])
    card(c, MARGIN_X, 278, 220, 108, "Lit", "PBR 기반 표현. 금속, 거칠기, 조명 반응이 중요할 때.", BLUE, "S12")
    card(c, 300, 278, 220, 108, "Simple Lit", "더 단순한 조명 모델. 모바일이나 단순 스타일에 검토.", CYAN, "S12")
    card(c, 552, 278, 220, 108, "Unlit", "조명 영향을 받지 않는다. UI, 이펙트, 스타일 렌더에 유용.", GREEN, "S12")
    analogy(c, MARGIN_X, 162, 350, "Lit은 풀 조명 촬영, Simple Lit은 조명 장비를 줄인 촬영, Unlit은 이미 색이 칠해진 스티커를 붙이는 느낌이다.")
    example(c, 432, 162, 360, "멀리 있는 배경 소품은 Simple Lit/Unlit을 검토하고, 캐릭터 얼굴과 의상 중심부는 Lit을 유지하는 식으로 품질 구역을 나눈다.")


def slide_lighting_shadows(c, page):
    header(c, page, "14강. 조명과 그림자는 무대 조명 예산이다", ["S3", "S10", "S1"])
    inspector(c, MARGIN_X, 152, 250, 240, "PC Shadow Settings", [
        ("Main Shadow", PROJECT_VALUES["pc"]["Main Shadow"]),
        ("Additional Shadow", PROJECT_VALUES["pc"]["Add Light Shadow"]),
        ("Shadow Distance", PROJECT_VALUES["pc"]["Shadow Distance"]),
        ("Cascade Count", PROJECT_VALUES["pc"]["Cascade Count"]),
    ], BLUE)
    inspector(c, 320, 152, 250, 240, "Mobile Shadow Settings", [
        ("Main Shadow", PROJECT_VALUES["mobile"]["Main Shadow"]),
        ("Additional Shadow", PROJECT_VALUES["mobile"]["Add Light Shadow"]),
        ("Shadow Distance", PROJECT_VALUES["mobile"]["Shadow Distance"]),
        ("Cascade Count", PROJECT_VALUES["mobile"]["Cascade Count"]),
    ], CYAN)
    card(c, 598, 304, 195, 92, "공식 근거", "그림자 비용은 caster, receiver, shadow-casting light, cascade, resolution, soft shadow의 영향을 받는다.", BLUE, "S10")
    analogy(c, 598, 194, 195, "무대 조명이 많을수록 조명감독도 그림자 스태프도 바빠진다.")
    example(c, 598, 88, 195, "Mobile은 Additional Light Shadow Off, Cascade 1로 시작한다.")


def slide_depth_opaque(c, page):
    header(c, page, "15강. Depth와 Opaque는 보조 자료다", ["S3", "S4"])
    draw_depth_opaque(c, 432, 170)
    bullet(c, [
        "Depth Texture는 깊이 기반 효과가 앞뒤 관계를 알 수 있게 만든다.",
        "Opaque Texture는 투명 셰이더가 불투명 장면 결과를 참고하게 만든다.",
        "Unity 문서는 Opaque Texture를 Built-in의 GrabPass와 비슷한 장면 스냅샷으로 설명한다.",
        "필요한 기능이 없다면 켜진 이유부터 확인한다.",
    ], MARGIN_X, TOP_Y - 78, 350, 13, 22)
    analogy(c, MARGIN_X, 116, 350, "Depth는 좌석 배치도, Opaque는 막이 오르기 직전 무대 사진이다.")
    example(c, 432, 82, 360, "열기 왜곡, 유리, 물 굴절 효과가 없다면 Opaque Texture가 필요한지 먼저 점검한다.")


def slide_srp_batcher(c, page):
    header(c, page, "16강. SRP Batcher는 같은 양식 서류를 묶어 처리한다", ["S3", "S11", "S1"])
    c.setFillColor(LIGHT)
    c.roundRect(430, 162, 320, 210, 16, fill=1, stroke=0)
    for i in range(4):
        c.setFillColor(BLUE if i < 3 else RED)
        c.roundRect(465 + i * 62, 285, 50, 44, 8, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 8)
        c.drawCentredString(490 + i * 62, 303, "Mat")
    c.setFillColor(GREEN)
    c.roundRect(498, 205, 190, 44, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 10)
    c.drawCentredString(593, 222, "Same shader variant batch")
    bullet(c, [
        "SRP Batcher는 같은 Shader Variant를 사용하는 머티리얼들의 CPU 렌더 준비 비용을 줄이는 경로다.",
        "현재 PC/Mobile URP Asset 모두 SRP Batcher가 On이다.",
        "GPU 일을 줄이는 기능이 아니라 CPU 쪽 렌더 준비 루프를 빠르게 하는 기능이라는 점을 구분한다.",
    ], MARGIN_X, TOP_Y - 78, 350, 13, 22)
    analogy(c, MARGIN_X, 116, 350, "같은 양식의 서류는 담당자가 한 번에 훑고 도장을 찍을 수 있다.")
    example(c, 432, 82, 360, "Material 300개를 같은 shader variant와 서로 다른 shader variant로 나눠 SetPass와 CPU Render Thread를 비교한다.")


def slide_debug(c, page):
    header(c, page, "17강. Frame Debugger는 CCTV 타임라인이다", ["S13"])
    c.setFillColor(DARK)
    c.roundRect(474, 132, 286, 245, 14, fill=1, stroke=0)
    events = ["Render Shadows", "Depth Prepass", "Draw Opaques", "SSAO", "Draw Transparents", "Post Process"]
    yy = 342
    for i, e in enumerate(events):
        c.setFillColor(colors.HexColor("#3A414E") if i % 2 == 0 else colors.HexColor("#313744"))
        c.roundRect(494, yy, 246, 26, 5, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_REG, 9)
        c.drawString(506, yy + 9, e)
        yy -= 32
    bullet(c, [
        "Frame Debugger는 한 프레임의 render event를 순서대로 보여준다.",
        "URP 공부에서는 결과 화면보다 패스 순서를 읽는 습관이 중요하다.",
        "Rendering Debugger와 함께 보면 조명, 머티리얼, 디버그 뷰를 더 쉽게 확인할 수 있다.",
    ], MARGIN_X, TOP_Y - 78, 380, 13, 22)
    analogy(c, MARGIN_X, 134, 380, "CCTV 타임라인처럼 '방금 프레임에서 누가 먼저 들어오고, 누가 나중에 나갔는지'를 보여준다.")
    example(c, MARGIN_X, 42, 380, "SSAO를 끈 뒤 Frame Debugger에서 SSAO 관련 이벤트가 사라졌는지 확인한다.")


def slide_how_to_find(c, page):
    header(c, page, "18강. Unity에서 어디를 열어야 하나", ["S1", "S2"])
    rows = [
        ("URP Asset", "Assets/Settings/PC_RPAsset.asset 또는 Mobile_RPAsset.asset"),
        ("Renderer Asset", "Assets/Settings/PC_Renderer.asset 또는 Mobile_Renderer.asset"),
        ("Volume Profile", "Assets/Settings/SampleSceneProfile.asset"),
        ("Frame Debugger", "Window > Analysis > Frame Debugger"),
        ("Rendering Debugger", "Window > Analysis > Rendering Debugger"),
    ]
    y = TOP_Y - 78
    for i, (a, b) in enumerate(rows):
        yy = y - i * 54
        c.setFillColor(LIGHT if i % 2 == 0 else PANEL)
        c.roundRect(MARGIN_X, yy - 38, PAGE_W - 2 * MARGIN_X, 46, 9, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.setFont(FONT_BOLD, 12)
        c.drawString(MARGIN_X + 18, yy - 12, a)
        c.setFillColor(INK)
        c.setFont(FONT_REG, 11)
        c.drawString(MARGIN_X + 180, yy - 12, b)
    example(c, MARGIN_X, 70, PAGE_W - 2 * MARGIN_X, "첫 실습은 PC_RPAsset과 Mobile_RPAsset을 열어 Render Scale, Shadow Resolution, Cascade Count 차이를 표로 옮기는 것이다.")


def slide_project_exercise(c, page):
    header(c, page, "19강. 이 프로젝트의 첫 URP 과제", ["S1", "S3", "S4"])
    bullet(c, [
        "PC_RPAsset과 Mobile_RPAsset의 차이를 `Docs/URP_Profile_Compare.md`에 표로 작성한다.",
        "PC_Renderer와 Mobile_Renderer의 Renderer Feature 차이를 기록한다.",
        "Benchmark_Field 씬에서 Render Scale, Additional Light Shadow, Cascade Count를 하나씩 바꾼다.",
        "각 변경마다 FPS, GPU ms, Draw Calls, SetPass, 화면 품질 메모를 기록한다.",
    ], MARGIN_X, TOP_Y - 78, 490, 13, 22)
    inspector(c, 580, 158, 205, 220, "첫 비교표 항목", [
        ("Render Scale", "1.0 vs 0.8"),
        ("Main Shadow", "2048 vs 1024"),
        ("Add Shadow", "On vs Off"),
        ("Cascade", "4 vs 1"),
        ("SSAO", "PC only"),
    ], GREEN)
    analogy(c, MARGIN_X, 92, 490, "최적화는 요리 레시피를 바꾸는 일과 같다. 소금, 불 세기, 조리 시간을 한 번에 다 바꾸면 무엇이 맛을 바꿨는지 모른다.")


def slide_review(c, page):
    header(c, page, "20강. 오늘 기억할 한 장", [])
    cards = [
        ("URP Asset", "품질 정책", BLUE),
        ("Renderer Asset", "그리는 순서표", CYAN),
        ("Renderer Feature", "추가 필터/장비", GREEN),
        ("Camera Stack", "영상 편집 트랙", AMBER),
        ("Volume", "공간별 색보정 룸", PURPLE),
        ("Frame Debugger", "프레임 CCTV", RED),
    ]
    for i, (a, b, col) in enumerate(cards):
        card(c, MARGIN_X + (i % 3) * 252, TOP_Y - 150 - (i // 3) * 130, 228, 96, a, b, col)
    example(c, MARGIN_X, 76, PAGE_W - 2 * MARGIN_X, "URP를 잘 다룬다는 것은 '어떤 옵션이 좋다'를 외우는 것이 아니라, 장면의 목표와 비용에 맞춰 어떤 렌더링 구조를 선택했는지 설명하는 것이다.")


def slide_references(c, page, part):
    header(c, page, "참고문헌 및 이미지 출처" if part == 1 else "참고문헌 계속", [])
    ids = list(SOURCES.keys())
    subset = ids[:9] if part == 1 else ids[9:]
    y = TOP_Y - 58
    text(c, "확인일: 2026-07-21. 본 PDF의 Inspector 화면은 현재 프로젝트의 Unity Asset 값을 바탕으로 재구성한 도식이며, 실제 이미지로 사용한 자료는 로컬 Unity URP 패키지 샘플 이미지다.", MARGIN_X, y, PAGE_W - 2 * MARGIN_X, FONT_REG, 10, 16, MUTED)
    y -= 50
    for sid in subset:
        title, url, org = SOURCES[sid]
        c.setFillColor(BLUE)
        c.setFont(FONT_BOLD, 9)
        c.drawString(MARGIN_X, y, f"[{sid}]")
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 9)
        c.drawString(MARGIN_X + 42, y, title)
        y -= 14
        y = text(c, f"{org} - {url}", MARGIN_X + 42, y, PAGE_W - 2 * MARGIN_X - 42, FONT_REG, 7.8, 11, MUTED)
        y -= 5


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    images = prepare_images()
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    slides = [
        lambda c, p: title_slide(c, p, images),
        slide_source_note,
        lambda c, p: slide_big_picture(c, p, images),
        slide_urp_asset,
        slide_render_scale,
        slide_hdr_msaa,
        slide_renderer_asset,
        slide_paths,
        slide_renderer_feature,
        slide_render_graph,
        slide_camera,
        slide_volume,
        lambda c, p: slide_post_image(c, p, images),
        lambda c, p: slide_shader_images(c, p, images),
        slide_shader_choice,
        slide_lighting_shadows,
        slide_depth_opaque,
        slide_srp_batcher,
        slide_debug,
        slide_how_to_find,
        slide_project_exercise,
        slide_review,
    ]
    page = 1
    for slide in slides:
        slide(c, page)
        c.showPage()
        page += 1
    slide_references(c, page, 1)
    c.showPage()
    page += 1
    slide_references(c, page, 2)
    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build_pdf()
