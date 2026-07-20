from __future__ import annotations

import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Unity_URP_Render_Optimization_Theory_Lecture.pdf"

PAGE_W, PAGE_H = landscape(A4)
MARGIN_X = 46
TOP_Y = PAGE_H - 42
BOTTOM_Y = 38

FONT_REG = "Malgun"
FONT_BOLD = "Malgun-Bold"

pdfmetrics.registerFont(TTFont(FONT_REG, r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BOLD, r"C:\Windows\Fonts\malgunbd.ttf"))

INK = colors.HexColor("#151922")
MUTED = colors.HexColor("#596174")
LIGHT = colors.HexColor("#F5F7FB")
PANEL = colors.HexColor("#FFFFFF")
BLUE = colors.HexColor("#4F7DFF")
SKY = colors.HexColor("#D9E7FF")
CYAN = colors.HexColor("#2CBCC4")
GREEN = colors.HexColor("#31A67A")
AMBER = colors.HexColor("#F2A33A")
RED = colors.HexColor("#E45858")
PURPLE = colors.HexColor("#7D64D9")
GRID = colors.HexColor("#D7DDEA")


SOURCES = {
    "S1": ("Project Unity version", "ProjectSettings/ProjectVersion.txt", "local project file"),
    "S2": ("Project package manifest", "Packages/manifest.json", "local project file"),
    "S3": (
        "Universal Render Pipeline Asset | Universal RP 17.0",
        "https://docs.unity.cn/Packages/com.unity.render-pipelines.universal%4017.0/manual/universalrp-asset.html",
        "Unity Technologies",
    ),
    "S4": (
        "Choose a rendering path in URP | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/urp/rendering-paths-comparison.html",
        "Unity Technologies",
    ),
    "S5": (
        "Profiler window reference | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/ProfilerWindow.html",
        "Unity Technologies",
    ),
    "S6": (
        "Rendering Profiler module reference | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/ProfilerRendering.html",
        "Unity Technologies",
    ),
    "S7": (
        "Debug a frame | Unity 6.0 Frame Debugger",
        "https://docs.unity.cn/6000.0/Documentation/Manual/FrameDebugger-debug.html",
        "Unity Technologies",
    ),
    "S8": (
        "Profiling tools reference | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/performance-profiling-tools.html",
        "Unity Technologies",
    ),
    "S9": (
        "Scriptable Render Pipeline Batcher",
        "https://docs.unity.cn/Manual/SRPBatcher.html",
        "Unity Technologies",
    ),
    "S10": (
        "Introduction to GPU instancing | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/GPUInstancing.html",
        "Unity Technologies",
    ),
    "S11": (
        "Optimize custom shaders | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/SL-ShaderPerformance.html",
        "Unity Technologies",
    ),
    "S12": (
        "Optimize shadow rendering in URP | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/shadows-optimization.html",
        "Unity Technologies",
    ),
    "S13": (
        "Occlusion culling | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/OcclusionCulling.html",
        "Unity Technologies",
    ),
    "S14": (
        "Level of Detail for meshes | Unity 6.0",
        "https://docs.unity.cn/6000.0/Documentation/Manual/LevelOfDetail.html",
        "Unity Technologies",
    ),
    "S15": (
        "Mesh Renderer component reference | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/class-MeshRenderer.html",
        "Unity Technologies",
    ),
    "S16": (
        "Skinned Mesh Renderer component reference | Unity 6.0",
        "https://docs.unity3d.com/6000.0/Documentation/Manual/class-SkinnedMeshRenderer.html",
        "Unity Technologies",
    ),
    "S17": (
        "Memory Profiler package 1.0",
        "https://docs.unity.cn/Packages/com.unity.memoryprofiler%401.0/manual/index.html",
        "Unity Technologies",
    ),
    "S18": (
        "Profile Analyzer package 1.2",
        "https://docs.unity.cn/Packages/com.unity.performance.profile-analyzer%401.2/manual/index.html",
        "Unity Technologies",
    ),
    "S19": (
        "Performance Testing Extension for Unity Test Framework 3.0",
        "https://docs.unity.cn/Packages/com.unity.test-framework.performance%403.0/manual/index.html",
        "Unity Technologies",
    ),
    "S20": (
        "Pipeline Stages (Direct3D 10)",
        "https://learn.microsoft.com/en-us/windows/win32/direct3d10/d3d10-graphics-programming-guide-pipeline-stages",
        "Microsoft Learn",
    ),
    "S21": (
        "Rendering Pipeline Overview",
        "https://wikis.khronos.org/opengl/Rendering_Pipeline_Overview",
        "Khronos OpenGL Wiki",
    ),
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


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = FONT_REG,
    size: int = 13,
    leading: int = 18,
    color=INK,
) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for para in text.split("\n"):
        if not para:
            y -= leading
            continue
        for line in wrap_line(c, para, width, font, size):
            c.drawString(x, y, line)
            y -= leading
    return y


def bullet_list(
    c: canvas.Canvas,
    items: list[str],
    x: float,
    y: float,
    width: float,
    size: int = 13,
    leading: int = 20,
    bullet_color=BLUE,
    text_color=INK,
) -> float:
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 4, y + 4, 3.2, fill=1, stroke=0)
        y = draw_wrapped(c, item, x + 17, y, width - 17, FONT_REG, size, leading, text_color)
        y -= 3
    return y


def small_label(c, text, x, y, width, fill=LIGHT, stroke=GRID, text_color=INK):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, width, 28, 8, fill=1, stroke=1)
    c.setFillColor(text_color)
    c.setFont(FONT_BOLD, 10)
    c.drawCentredString(x + width / 2, y + 9, text)


def card(c, x, y, w, h, title, body, accent=BLUE, source=None):
    c.setFillColor(PANEL)
    c.setStrokeColor(GRID)
    c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 8, w, 8, 4, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(x + 16, y + h - 31, title)
    yy = draw_wrapped(c, body, x + 16, y + h - 55, w - 32, FONT_REG, 11, 15, MUTED)
    if source:
        c.setFillColor(accent)
        c.setFont(FONT_BOLD, 8)
        c.drawRightString(x + w - 14, y + 12, source)
    return yy


def header(c, page, title, sources=None):
    sources = sources or []
    c.setFillColor(LIGHT)
    c.rect(0, PAGE_H - 28, PAGE_W, 28, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(FONT_BOLD, 9)
    c.drawString(MARGIN_X, PAGE_H - 18, "Unity URP Render Optimization Theory")
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 18, "실습 전 이론 강의")
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 24)
    c.drawString(MARGIN_X, TOP_Y - 20, title)
    c.setStrokeColor(GRID)
    c.line(MARGIN_X, TOP_Y - 34, PAGE_W - MARGIN_X, TOP_Y - 34)
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawString(MARGIN_X, 20, f"{page:02d}")
    if sources:
        c.drawRightString(PAGE_W - MARGIN_X, 20, "근거: " + ", ".join(sources))


def title_slide(c, page):
    c.setFillColor(colors.HexColor("#EEF4FF"))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.circle(PAGE_W - 110, PAGE_H - 90, 62, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.circle(PAGE_W - 80, PAGE_H - 160, 36, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.circle(PAGE_W - 168, PAGE_H - 150, 30, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 34)
    c.drawString(MARGIN_X, PAGE_H - 135, "Unity URP 렌더 최적화")
    c.drawString(MARGIN_X, PAGE_H - 178, "이론 강의 노트")
    c.setFont(FONT_REG, 17)
    c.setFillColor(MUTED)
    c.drawString(MARGIN_X, PAGE_H - 216, "실습 전에 이해해야 할 렌더링 비용, 프로파일링, URP 설정")
    c.setFillColor(PANEL)
    c.roundRect(MARGIN_X, 112, PAGE_W - MARGIN_X * 2, 128, 14, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 15)
    c.drawString(MARGIN_X + 24, 205, "이 문서의 기준")
    c.setFont(FONT_REG, 12)
    c.setFillColor(MUTED)
    lines = [
        "프로젝트 기준: Unity 6000.3.9f1, Universal Render Pipeline 17.3.0",
        "목표: 개발자 지원 포트폴리오용 렌더 최적화 테스트 필드에 들어가기 전 이론 정리",
        "주의: 특정 회사의 내부 모델 포맷이나 파이프라인은 공개 자료만으로 단정하지 않음",
        "출처: 공식 문서 중심, 모든 외부 문서는 2026-07-20 기준 확인",
    ]
    y = 181
    for line in lines:
        c.drawString(MARGIN_X + 24, y, line)
        y -= 22
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawString(MARGIN_X, 20, f"{page:02d}")


def diagram_pipeline(c, x, y):
    stages = [
        ("C# / Scene", BLUE),
        ("Draw command", CYAN),
        ("Vertex", GREEN),
        ("Rasterize", AMBER),
        ("Fragment", RED),
        ("Depth/Blend", PURPLE),
        ("Frame", BLUE),
    ]
    w = 96
    gap = 12
    for i, (name, col) in enumerate(stages):
        xx = x + i * (w + gap)
        c.setFillColor(col)
        c.roundRect(xx, y, w, 46, 12, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 10)
        c.drawCentredString(xx + w / 2, y + 18, name)
        if i < len(stages) - 1:
            c.setStrokeColor(MUTED)
            c.setLineWidth(1.2)
            c.line(xx + w + 3, y + 23, xx + w + gap - 3, y + 23)
            c.line(xx + w + gap - 8, y + 28, xx + w + gap - 3, y + 23)
            c.line(xx + w + gap - 8, y + 18, xx + w + gap - 3, y + 23)


def diagram_frame_budget(c, x, y):
    budgets = [("60 FPS", 16.67, BLUE), ("30 FPS", 33.33, GREEN), ("24 FPS", 41.67, AMBER)]
    max_ms = 45
    for i, (label, ms, col) in enumerate(budgets):
        yy = y - i * 52
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 12)
        c.drawString(x, yy + 17, label)
        c.setFillColor(LIGHT)
        c.roundRect(x + 86, yy + 8, 420, 22, 11, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(x + 86, yy + 8, 420 * (ms / max_ms), 22, 11, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 11)
        c.drawRightString(x + 548, yy + 14, f"{ms:.2f} ms / frame")


def diagram_profiler_ladder(c, x, y):
    steps = [
        ("Game Stats", "현장 감각", BLUE),
        ("Profiler", "CPU/GPU/Memory", CYAN),
        ("Rendering", "Draw/SetPass/Tri", GREEN),
        ("Frame Debugger", "이 프레임의 사건 순서", AMBER),
        ("Analyzer", "Before/After 비교", PURPLE),
    ]
    for i, (name, desc, col) in enumerate(steps):
        xx = x + i * 138
        c.setFillColor(col)
        c.roundRect(xx, y, 120, 70, 13, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 12)
        c.drawCentredString(xx + 60, y + 41, name)
        c.setFont(FONT_REG, 9)
        c.drawCentredString(xx + 60, y + 22, desc)
        if i < len(steps) - 1:
            c.setStrokeColor(MUTED)
            c.line(xx + 123, y + 35, xx + 134, y + 35)


def diagram_bottleneck_matrix(c, x, y):
    headers = ["증상", "우선 의심", "첫 확인"]
    widths = [180, 190, 250]
    c.setFillColor(BLUE)
    c.roundRect(x, y + 146, sum(widths), 34, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont(FONT_BOLD, 11)
    xx = x
    for h, w in zip(headers, widths):
        c.drawCentredString(xx + w / 2, y + 157, h)
        xx += w
    rows = [
        ("해상도 낮추면 빨라짐", "GPU fill/fragment", "Render Scale, Post, Overdraw"),
        ("Draw/SetPass가 큼", "CPU render setup", "Rendering Profiler, Frame Debugger"),
        ("그림자 켜면 급락", "Shadow pass", "Shadow caster, light count"),
        ("캐릭터 수에 비례", "Skinning/material", "SkinnedMeshRenderer, material count"),
    ]
    row_h = 36
    for r, row in enumerate(rows):
        yy = y + 146 - (r + 1) * row_h
        c.setFillColor(PANEL if r % 2 == 0 else LIGHT)
        c.rect(x, yy, sum(widths), row_h, fill=1, stroke=0)
        c.setStrokeColor(GRID)
        c.line(x, yy, x + sum(widths), yy)
        xx = x
        c.setFillColor(INK)
        c.setFont(FONT_REG, 10)
        for txt, w in zip(row, widths):
            c.drawString(xx + 10, yy + 13, txt)
            xx += w
    c.setStrokeColor(GRID)
    xx = x
    for w in widths:
        c.line(xx, y + 2, xx, y + 180)
        xx += w
    c.line(xx, y + 2, xx, y + 180)


def diagram_field(c, x, y):
    c.setFillColor(LIGHT)
    c.roundRect(x, y, 620, 230, 12, fill=1, stroke=0)
    zones = [
        ("Static Mesh", x + 25, y + 145, 170, 60, BLUE),
        ("Materials", x + 225, y + 145, 170, 60, CYAN),
        ("Lights/Shadow", x + 425, y + 145, 170, 60, AMBER),
        ("Transparency", x + 25, y + 45, 170, 60, PURPLE),
        ("Post Process", x + 225, y + 45, 170, 60, RED),
        ("Character Slot", x + 425, y + 45, 170, 60, GREEN),
    ]
    for name, xx, yy, ww, hh, col in zones:
        c.setFillColor(col)
        c.roundRect(xx, yy, ww, hh, 10, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 12)
        c.drawCentredString(xx + ww / 2, yy + 34, name)
        c.setFont(FONT_REG, 8)
        c.drawCentredString(xx + ww / 2, yy + 17, "측정 조건 분리")
    c.setStrokeColor(INK)
    c.setLineWidth(1.4)
    c.line(x + 55, y + 20, x + 565, y + 210)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 10)
    c.drawString(x + 56, y + 24, "고정 카메라 경로")


def slide_fact_boundary(c, page):
    header(c, page, "0강. 사실과 가정을 분리한다", ["S1", "S2"])
    y = TOP_Y - 72
    c.setFont(FONT_BOLD, 15)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, "강의 시작 전에 먼저 지켜야 할 원칙")
    y -= 34
    items = [
        "프로젝트 사실: 현재 프로젝트는 Unity 6000.3.9f1, URP 17.3.0 기준이다.",
        "프로젝트 사실: 기본 씬은 카메라, 방향성 조명, 볼륨 정도만 있는 초기 상태에 가깝다.",
        "직무 해석: 공고 이미지에는 Unity, 리소스 최적화, 부하/기능 테스트, 스튜디오 운영 유지보수가 보인다.",
        "주의: 특정 기업이 VRM, FBX, 자체 포맷 중 무엇을 쓰는지는 공개 자료만으로 단정하지 않는다.",
        "따라서 포트폴리오는 특정 포맷이 아니라 Unity 3D 캐릭터/라이브 씬 최적화로 설계한다.",
    ]
    bullet_list(c, items, MARGIN_X, y, PAGE_W - 2 * MARGIN_X, 13, 22)
    card(
        c,
        MARGIN_X,
        82,
        PAGE_W - 2 * MARGIN_X,
        82,
        "오늘의 결론",
        "이론 수업의 목표는 '어떤 옵션을 끄면 빨라진다'를 외우는 것이 아니라, 병목을 측정하고 원인을 설명하는 언어를 갖추는 것이다.",
        BLUE,
    )


def slide_frame(c, page):
    header(c, page, "1강. 렌더 최적화는 프레임 예산 관리다", ["S8"])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "게임 화면은 매 프레임 반복해서 계산되고 그려진다.",
            "60 FPS 목표라면 한 프레임에 사용할 수 있는 총 시간은 약 16.67ms다.",
            "CPU, GPU, 스크립트, 애니메이션, 렌더링, 메모리 할당이 모두 이 예산을 나눠 쓴다.",
            "최적화의 첫 질문은 '느린가?'가 아니라 '어느 구간이 예산을 초과하는가?'다.",
        ],
        MARGIN_X,
        y,
        365,
        13,
        22,
    )
    diagram_frame_budget(c, 430, TOP_Y - 92)
    card(
        c,
        430,
        100,
        330,
        88,
        "강의 메모",
        "FPS는 결과값이고, Frame Time은 원인 분석에 더 가까운 숫자다. 포트폴리오에서는 FPS와 ms를 함께 기록한다.",
        CYAN,
    )


def slide_pipeline(c, page):
    header(c, page, "2강. 화면 한 장이 그려지는 큰 흐름", ["S20", "S21"])
    y = TOP_Y - 82
    draw_wrapped(
        c,
        "실시간 3D 렌더링은 대체로 CPU가 장면 상태를 정리하고, 그래픽 API 명령을 만들고, GPU가 정점/래스터화/픽셀 단계에서 이미지를 만들어내는 구조로 이해할 수 있다.",
        MARGIN_X,
        y,
        PAGE_W - 2 * MARGIN_X,
        FONT_REG,
        14,
        23,
    )
    diagram_pipeline(c, MARGIN_X, 330)
    y = 265
    bullet_list(
        c,
        [
            "Vertex 단계: 메시의 정점이 변환되고, 스키닝이나 정점 기반 계산이 들어갈 수 있다.",
            "Rasterization: 삼각형이 화면의 fragment/pixel 후보로 쪼개진다.",
            "Fragment/Pixel 단계: 텍스처 샘플링, 조명, 그림자, 투명도, 후처리 비용이 커지기 쉽다.",
            "Depth/Blend 단계: 깊이 테스트, 스텐실, 블렌딩 같은 per-sample 작업이 일어난다.",
        ],
        MARGIN_X,
        y,
        PAGE_W - 2 * MARGIN_X,
        13,
        21,
    )


def slide_cpu_gpu(c, page):
    header(c, page, "3강. CPU 병목과 GPU 병목을 구분한다", ["S5", "S6", "S11"])
    y = TOP_Y - 72
    card(c, MARGIN_X, y - 120, 360, 120, "CPU 쪽 렌더 병목", "Draw Call 준비, SetPass 전환, 스크립트, 애니메이션, 오브젝트 탐색, 컬링 준비 등이 누적될 때 나타난다.", BLUE, "S5/S6")
    card(c, 430, y - 120, 360, 120, "GPU 쪽 렌더 병목", "해상도, fragment shader, texture bandwidth, render target, shadow map, post process, overdraw 비용이 커질 때 나타난다.", RED, "S11/S12")
    diagram_bottleneck_matrix(c, MARGIN_X + 45, 95)


def slide_draw_calls(c, page):
    header(c, page, "4강. Draw Call, SetPass, Batch", ["S6"])
    y = TOP_Y - 72
    items = [
        "Draw Call은 Unity가 화면에 렌더링하라고 그래픽스 쪽에 보내는 그리기 명령이다.",
        "SetPass는 렌더링에 사용할 shader pass가 바뀐 횟수로, 상태 전환 비용을 이해하는 데 중요하다.",
        "Batch는 Unity가 여러 렌더 작업을 묶어 처리한 단위다.",
        "Rendering Profiler는 Batches, SetPass Calls, Triangles, Vertices, Draw Calls 같은 지표를 보여준다.",
    ]
    bullet_list(c, items, MARGIN_X, y, PAGE_W - 2 * MARGIN_X, 14, 24)
    c.setFillColor(LIGHT)
    c.roundRect(MARGIN_X, 120, PAGE_W - 2 * MARGIN_X, 110, 12, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 15)
    c.drawString(MARGIN_X + 20, 200, "포트폴리오 문장 예시")
    draw_wrapped(
        c,
        "서로 다른 머티리얼을 많이 사용한 구역에서 SetPass Calls가 증가했고, 동일 shader variant와 머티리얼 공유를 적용한 뒤 CPU 렌더 준비 비용을 비교했다.",
        MARGIN_X + 20,
        174,
        PAGE_W - 2 * MARGIN_X - 40,
        FONT_REG,
        13,
        21,
        MUTED,
    )


def slide_batching(c, page):
    header(c, page, "5강. 묶어서 그리는 전략들", ["S3", "S9", "S10"])
    y = TOP_Y - 72
    cards = [
        ("Static Batching", "움직이지 않는 오브젝트를 큰 메시처럼 묶어 CPU 렌더 비용을 줄이는 방향. 메모리 비용과 정적 조건을 고려한다.", BLUE, "S6"),
        ("SRP Batcher", "SRP에서 같은 shader variant를 쓰는 머티리얼의 CPU 렌더 준비 비용을 줄이는 경로. URP/HDRP에서 사용 가능하다.", CYAN, "S9"),
        ("GPU Instancing", "같은 mesh와 material의 복사본을 한 draw call로 렌더링하는 최적화. SRP Batcher와 우선순위/호환 조건을 확인해야 한다.", GREEN, "S10"),
    ]
    for i, (t, b, col, src) in enumerate(cards):
        card(c, MARGIN_X + i * 255, y - 120, 230, 120, t, b, col, src)
    bullet_list(
        c,
        [
            "처음 실습에서는 같은 큐브 100/500/1000개, 같은 머티리얼/다른 머티리얼 조건을 나눠 테스트한다.",
            "캐릭터는 SkinnedMeshRenderer가 많아질 수 있으므로, 단순 인스턴싱만으로 모든 문제가 해결된다고 보면 안 된다.",
            "좋은 포트폴리오는 '어떤 기법을 썼다'보다 '이 조건에서는 이 기법이 더 맞았다'를 보여준다.",
        ],
        MARGIN_X,
        205,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )


def slide_urp_asset(c, page):
    header(c, page, "6강. URP Asset은 렌더링 품질의 조종판이다", ["S3"])
    y = TOP_Y - 168
    labels = [
        ("Rendering", "Depth Texture, Opaque Texture, Store Actions", BLUE),
        ("Quality", "HDR, MSAA, Render Scale, Upscaling", CYAN),
        ("Lighting", "Main Light, Additional Lights", AMBER),
        ("Shadows", "Distance, Resolution, Cascade, Soft Shadow", PURPLE),
        ("Post", "Bloom, SSAO, Tonemapping 등", RED),
    ]
    for i, (a, b, col) in enumerate(labels):
        card(c, MARGIN_X + (i % 3) * 252, y - (i // 3) * 116, 230, 90, a, b, col, "S3")
    card(
        c,
        525,
        88,
        265,
        112,
        "현재 프로젝트 힌트",
        "이미 PC_RPAsset과 Mobile_RPAsset이 있으므로, 이론 이후 PC/Mobile 비교 실험으로 바로 이어갈 수 있다.",
        GREEN,
        "S2/S3",
    )


def slide_urp_levers(c, page):
    header(c, page, "7강. 가장 먼저 실험할 URP 레버", ["S3", "S11"])
    y = TOP_Y - 72
    rows = [
        ("Render Scale", "렌더 타깃 해상도를 조절한다. 낮추면 GPU 비용이 줄 수 있지만 선명도가 희생된다."),
        ("HDR", "넓은 밝기 범위와 Bloom 표현에 유리하지만 낮은 사양에서는 계산을 줄이기 위해 끌 수 있다."),
        ("MSAA", "기하 경계의 계단 현상을 줄이지만 샘플 수가 늘수록 비용이 증가한다."),
        ("Depth/Opaque Texture", "효과 구현에 필요할 수 있지만 추가 텍스처 생성/복사 비용을 만든다."),
        ("Store Actions", "특히 모바일/tile-based GPU에서 메모리 대역폭 비용과 연결될 수 있다."),
    ]
    for i, (name, desc) in enumerate(rows):
        yy = y - i * 66
        c.setFillColor(LIGHT if i % 2 == 0 else colors.white)
        c.roundRect(MARGIN_X, yy - 40, PAGE_W - 2 * MARGIN_X, 50, 10, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.setFont(FONT_BOLD, 13)
        c.drawString(MARGIN_X + 18, yy - 10, name)
        draw_wrapped(c, desc, MARGIN_X + 175, yy - 10, PAGE_W - 2 * MARGIN_X - 195, FONT_REG, 12, 18, MUTED)


def slide_render_paths(c, page):
    header(c, page, "8강. Forward, Forward+, Deferred", ["S4"])
    y = TOP_Y - 72
    card(c, MARGIN_X, y - 128, 230, 128, "Forward", "기본 경로. 조명이 많지 않거나 모바일/저사양 플랫폼에서 우선 고려할 수 있다.", BLUE, "S4")
    card(c, MARGIN_X + 255, y - 128, 230, 128, "Forward+", "많은 조명이 필요하지만 Deferred가 느린 플랫폼 등에서 검토한다.", CYAN, "S4")
    card(c, MARGIN_X + 510, y - 128, 230, 128, "Deferred", "조명 수 처리에 강점이 있지만 G-buffer 등 추가 렌더 타깃 비용을 고려해야 한다.", PURPLE, "S4")
    bullet_list(
        c,
        [
            "URP 문서는 프로젝트 유형과 목표 하드웨어에 따라 렌더링 경로를 고르라고 설명한다.",
            "Forward 계열은 MSAA 지원 측면에서 유리한 경우가 있고, Deferred는 모바일에서 추가 pass 비용이 커질 수 있다.",
            "처음 포트폴리오는 경로 전환보다 URP Asset 옵션과 조명/그림자 비용을 먼저 측정하는 편이 안전하다.",
        ],
        MARGIN_X,
        245,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )


def slide_tools(c, page):
    header(c, page, "9강. 프로파일링 도구 사다리", ["S5", "S6", "S7", "S8", "S17", "S18"])
    diagram_profiler_ladder(c, MARGIN_X, TOP_Y - 150)
    bullet_list(
        c,
        [
            "Profiler: CPU, GPU, Rendering, Memory 등 모듈별로 프레임 데이터를 확인한다.",
            "Rendering Profiler: Batches, SetPass, Draw Calls, Triangles, Vertices, RenderTexture, Shadow Casters 같은 렌더 지표를 확인한다.",
            "Frame Debugger: 한 프레임을 멈추고 어떤 렌더 이벤트가 어떤 순서로 실행되는지 확인한다.",
            "Profile Analyzer: 여러 프레임 데이터를 집계하고 두 데이터 세트를 나란히 비교한다.",
            "Memory Profiler: 스냅샷을 캡처해서 native/managed 메모리, 할당, 누수 의심 지점을 본다.",
        ],
        MARGIN_X,
        300,
        PAGE_W - 2 * MARGIN_X,
        12,
        20,
    )


def slide_measure_protocol(c, page):
    header(c, page, "10강. 측정 규칙이 없으면 최적화도 없다", ["S5", "S19"])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "같은 씬, 같은 카메라 경로, 같은 해상도, 같은 품질 설정에서 비교한다.",
            "처음 몇 초는 워밍업으로 버리고, 일정 시간의 평균/중앙값/최저 구간을 기록한다.",
            "Editor Play Mode 수치는 참고용이다. 가능하면 목표 플랫폼 빌드에서도 측정한다.",
            "VSync, 해상도, 품질 레벨, Development Build 여부를 로그에 남긴다.",
            "자동화 단계에서는 Performance Testing Extension으로 반복 측정 기반을 만들 수 있다.",
        ],
        MARGIN_X,
        y,
        460,
        13,
        22,
    )
    c.setFillColor(LIGHT)
    c.roundRect(555, 114, 230, 310, 12, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 15)
    c.drawString(578, 382, "기록 템플릿")
    draw_wrapped(
        c,
        "Case: Shadow Distance\nScene: Benchmark_Field\nQuality: Mobile_RPAsset\nResolution: 1920x1080\nDuration: 60s\nAvg FPS:\nCPU Main ms:\nGPU ms:\nDraw Calls:\nSetPass:\nNote:",
        578,
        352,
        180,
        FONT_REG,
        11,
        18,
        MUTED,
    )


def slide_mesh(c, page):
    header(c, page, "11강. 메시 비용: 삼각형, 정점, LOD, 컬링", ["S6", "S13", "S14"])
    y = TOP_Y - 72
    card(c, MARGIN_X, y - 115, 235, 115, "Triangles / Vertices", "Rendering Profiler에서 프레임 동안 처리된 삼각형과 정점 수를 확인한다.", BLUE, "S6")
    card(c, MARGIN_X + 260, y - 115, 235, 115, "LOD", "먼 오브젝트에 낮은 디테일 메시를 사용해 GPU 작업을 줄이는 기법이다.", GREEN, "S14")
    card(c, MARGIN_X + 520, y - 115, 235, 115, "Occlusion Culling", "다른 오브젝트에 완전히 가려진 Renderer의 불필요한 렌더 계산을 줄인다.", PURPLE, "S13")
    bullet_list(
        c,
        [
            "벤치마크 필드에는 '보이는 오브젝트 수'와 '가려지는 오브젝트 수'를 분리한 구역이 필요하다.",
            "LOD는 멀리 있는 메시의 삼각형 수를 낮추는 전략이므로 고정 카메라 거리 조건이 중요하다.",
            "Occlusion Culling은 CPU 런타임 계산과 메모리 데이터가 필요하므로, 실내/복도형 구조처럼 가림이 명확한 씬에서 효과를 확인한다.",
        ],
        MARGIN_X,
        245,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )


def slide_material_shader(c, page):
    header(c, page, "12강. 머티리얼과 셰이더 비용", ["S9", "S11", "S15"])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "Mesh Renderer와 Skinned Mesh Renderer는 Materials 목록을 가진다. 머티리얼 수와 sub-mesh 구조는 렌더 이벤트 수에 영향을 줄 수 있다.",
            "SRP Batcher는 같은 shader variant를 쓰는 머티리얼들의 CPU 렌더 준비 비용을 낮추는 데 도움이 된다.",
            "커스텀 셰이더는 텍스처 대역폭, 버퍼 대역폭, ALU 연산, fragment shader 반복 계산을 확인해야 한다.",
            "fragment shader에서 매 픽셀 계산하는 값을 vertex shader나 C#으로 옮길 수 있는지 검토한다.",
        ],
        MARGIN_X,
        y,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )
    c.setStrokeColor(GRID)
    c.setFillColor(LIGHT)
    c.roundRect(MARGIN_X, 96, PAGE_W - 2 * MARGIN_X, 92, 12, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(MARGIN_X + 18, 158, "처음 만들 테스트")
    draw_wrapped(
        c,
        "동일 mesh 300개를 같은 Lit material로 배치한 구역과, 서로 다른 material 300개로 배치한 구역을 나누고 Rendering Profiler / Frame Debugger로 SetPass와 draw event 차이를 확인한다.",
        MARGIN_X + 18,
        133,
        PAGE_W - 2 * MARGIN_X - 36,
        FONT_REG,
        12,
        19,
        MUTED,
    )


def slide_transparency(c, page):
    header(c, page, "13강. 투명 렌더링과 Overdraw", ["S3", "S11", "S21"])
    y = TOP_Y - 72
    card(c, MARGIN_X, y - 120, 345, 120, "Opaque", "깊이 테스트와 렌더 순서 최적화가 비교적 잘 맞는다. 불투명 오브젝트는 먼저 정리하기 좋다.", BLUE)
    card(c, 445, y - 120, 345, 120, "Transparent", "블렌딩과 정렬이 필요하고, 가려진 픽셀도 여러 번 계산될 수 있어 overdraw 비용을 만든다.", RED)
    bullet_list(
        c,
        [
            "캐릭터 머리카락, 장식, 이펙트, 유리/물 같은 표현은 투명 렌더링 비용을 만들 수 있다.",
            "Opaque Texture는 투명 셰이더의 굴절/열기/유리 효과에 사용할 수 있지만, 장면 스냅샷 생성 비용을 고려해야 한다.",
            "투명 구역 실습에서는 카메라에 겹쳐 보이는 알파 오브젝트 수를 늘려 Frame Debugger와 GPU 시간을 비교한다.",
        ],
        MARGIN_X,
        235,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )


def slide_lighting(c, page):
    header(c, page, "14강. 조명과 그림자는 가장 비싼 품질 옵션 중 하나다", ["S12"])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "그림자 렌더링 시간은 shadow caster 수, shadow receiver 수, shadow-casting light 수, cascade count, shadow resolution, soft shadow 설정의 영향을 받는다.",
            "Point Light 그림자는 여섯 방향의 shadow map이 필요하므로 모바일에서는 특히 비용을 조심해야 한다.",
            "멀리 있는 조명의 그림자를 끄거나, 카메라 거리 조건으로 실시간 조명을 비활성화하는 전략을 검토할 수 있다.",
            "정적 오브젝트는 baked shadow / Shadowmask / Light Probe 조합을 비교할 수 있다.",
        ],
        MARGIN_X,
        y,
        470,
        13,
        22,
    )
    c.setFillColor(LIGHT)
    c.roundRect(560, 110, 230, 310, 12, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.circle(675, 350, 30, fill=1, stroke=0)
    c.setStrokeColor(AMBER)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        c.line(675, 350, 675 + math.cos(rad) * 70, 350 + math.sin(rad) * 70)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 13)
    c.drawCentredString(675, 255, "Light/Shadow 실험")
    draw_wrapped(c, "Shadow Distance, Cascade Count, Resolution, Soft Shadow, Additional Light Shadow를 하나씩 바꿔 비교한다.", 590, 225, 170, FONT_REG, 11, 18, MUTED)


def slide_texture_memory(c, page):
    header(c, page, "15강. 텍스처와 메모리는 성능의 바닥 체력이다", ["S6", "S11", "S17"])
    y = TOP_Y - 72
    card(c, MARGIN_X, y - 115, 235, 115, "Texture Bandwidth", "셰이더가 텍스처를 많이 읽고 쓰면 GPU 대역폭 한계에 가까워질 수 있다.", BLUE, "S11")
    card(c, MARGIN_X + 260, y - 115, 235, 115, "Mipmaps", "Unity는 텍스처 읽기 최적화 전략 중 하나로 mipmap 사용을 제시한다.", CYAN, "S11")
    card(c, MARGIN_X + 520, y - 115, 235, 115, "Memory Snapshot", "Memory Profiler는 메모리 스냅샷을 캡처하고 비교해 native/managed 할당을 본다.", GREEN, "S17")
    bullet_list(
        c,
        [
            "Rendering Profiler는 사용 텍스처와 RenderTexture 관련 메모리 지표도 제공한다.",
            "Render Scale, HDR Precision, MSAA, Opaque/Depth Texture는 렌더 타깃 크기와 대역폭 비용에 연결된다.",
            "캐릭터 포트폴리오에서는 텍스처 해상도, 압축, 머티리얼 슬롯 수, normal/emission 사용 여부를 함께 기록한다.",
        ],
        MARGIN_X,
        245,
        PAGE_W - 2 * MARGIN_X,
        13,
        22,
    )


def slide_character(c, page):
    header(c, page, "16강. 캐릭터 렌더링은 정적 메시와 다르다", ["S16"])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "Skinned Mesh Renderer는 뼈대와 bind pose를 가진 deformable mesh, blend shape, cloth simulation 등을 렌더링한다.",
            "Bone influence 수가 많을수록 움직임 품질은 좋아질 수 있지만 계산 자원이 더 필요할 수 있다.",
            "Update When Offscreen은 보이지 않는 동안에도 bounds를 매 프레임 계산하게 하므로, 기본적으로 성능 이유로 꺼져 있다.",
            "BlendShapes는 표정/입 모양 같은 값에 쓰이며, 캐릭터 수가 늘 때 비용을 따로 관찰해야 한다.",
            "캐릭터 테스트는 '모델 포맷'이 아니라 SkinnedMeshRenderer, material count, blend shape, shadow caster 수를 중심으로 설계한다.",
        ],
        MARGIN_X,
        y,
        510,
        13,
        22,
    )
    c.setFillColor(LIGHT)
    c.roundRect(600, 115, 180, 300, 12, fill=1, stroke=0)
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    c.circle(690, 352, 22, fill=0, stroke=1)
    c.line(690, 330, 690, 260)
    c.line(690, 300, 652, 282)
    c.line(690, 300, 728, 282)
    c.line(690, 260, 662, 210)
    c.line(690, 260, 718, 210)
    c.setStrokeColor(GREEN)
    c.rect(638, 190, 104, 192, fill=0, stroke=1)
    c.setFillColor(INK)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(690, 160, "Bounds / Bones / BlendShapes")


def slide_not_vrm(c, page):
    header(c, page, "17강. 특정 포맷을 단정하지 않는 설계", [])
    y = TOP_Y - 72
    bullet_list(
        c,
        [
            "VTuber/아바타 분야에는 VRM, FBX, glTF, 자체 변환 포맷 등 여러 가능성이 있다.",
            "공개 공고 이미지만으로 특정 기업이 어떤 포맷을 쓴다고 단정할 수 없다.",
            "지원 포트폴리오는 포맷 이름보다 Unity에서 캐릭터 렌더링 비용을 분석하고 개선하는 능력을 보여줘야 한다.",
            "그래서 테스트 필드는 'Character Slot'을 비워두고, 어떤 캐릭터 에셋도 나중에 넣을 수 있게 만든다.",
        ],
        MARGIN_X,
        y,
        PAGE_W - 2 * MARGIN_X,
        14,
        24,
    )
    card(
        c,
        MARGIN_X,
        102,
        PAGE_W - 2 * MARGIN_X,
        98,
        "지원서에 쓸 표현",
        "Unity 기반 3D 캐릭터 라이브 씬을 대상으로, 캐릭터 렌더러/머티리얼/조명/URP 품질 설정의 비용을 측정하고 PC/Mobile 프로파일에 맞춰 최적화하는 테스트 환경을 구축했습니다.",
        BLUE,
    )


def slide_benchmark_field(c, page):
    header(c, page, "18강. 이론을 실험장으로 바꾸면 Benchmark Field가 된다", ["S3", "S6", "S12"])
    diagram_field(c, MARGIN_X + 55, 220)
    bullet_list(
        c,
        [
            "Static Mesh 구역: 오브젝트 수와 배칭 전략을 테스트한다.",
            "Materials 구역: 같은 shader/material과 서로 다른 material 조건을 비교한다.",
            "Lights/Shadow 구역: shadow distance, cascade, resolution, additional light shadow를 비교한다.",
            "Transparency/Post 구역: overdraw, Opaque Texture, Bloom/SSAO 등 화면 공간 비용을 확인한다.",
            "Character Slot: 포맷과 무관하게 SkinnedMeshRenderer 기반 캐릭터 비용을 나중에 측정한다.",
        ],
        MARGIN_X,
        172,
        PAGE_W - 2 * MARGIN_X,
        12,
        19,
    )


def slide_roadmap(c, page):
    header(c, page, "19강. 첫 실습 전 로드맵", ["S5", "S6", "S18"])
    steps = [
        ("1", "폴더/문서", "Assets/_Project와 Docs 구조를 만든다."),
        ("2", "Benchmark_Field", "Primitive만으로 테스트 구역을 만든다."),
        ("3", "HUD", "FPS, frame time, quality, render scale을 표시한다."),
        ("4", "수동 측정", "Profiler와 Frame Debugger로 첫 baseline을 기록한다."),
        ("5", "비교", "PC_RPAsset과 Mobile_RPAsset 차이를 문서화한다."),
        ("6", "확장", "Profile Analyzer, Memory Profiler, 캐릭터 에셋으로 확장한다."),
    ]
    x = MARGIN_X
    y = TOP_Y - 86
    for i, (num, title, desc) in enumerate(steps):
        yy = y - i * 58
        c.setFillColor(BLUE if i < 3 else CYAN)
        c.circle(x + 16, yy, 16, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 11)
        c.drawCentredString(x + 16, yy - 4, num)
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 14)
        c.drawString(x + 46, yy + 4, title)
        draw_wrapped(c, desc, x + 180, yy + 4, 520, FONT_REG, 12, 18, MUTED)


def slide_glossary(c, page):
    header(c, page, "20강. 최소 용어 사전", ["S3", "S6", "S9", "S16"])
    terms = [
        ("Frame Time", "한 프레임을 완성하는 데 걸린 시간. 60 FPS 기준 약 16.67ms 이하가 목표."),
        ("Draw Call", "Unity가 화면에 그리라고 보내는 렌더 명령."),
        ("SetPass", "렌더링에 사용할 shader pass가 바뀐 횟수."),
        ("Batch", "Unity가 렌더 작업을 묶어 처리한 단위."),
        ("SRP Batcher", "SRP에서 같은 shader variant 렌더 준비 비용을 줄이는 경로."),
        ("Render Scale", "게임 렌더 타깃 해상도를 조절하는 URP 품질 설정."),
        ("Shadow Cascade", "원거리/근거리 그림자 품질을 나눠 관리하는 그림자 방식."),
        ("Skinned Mesh", "뼈대/블렌드셰이프 등으로 변형되는 캐릭터 메시."),
    ]
    x = MARGIN_X
    y = TOP_Y - 64
    for i, (term, desc) in enumerate(terms):
        col = BLUE if i % 2 == 0 else CYAN
        yy = y - i * 45
        c.setFillColor(col)
        c.roundRect(x, yy - 18, 145, 30, 8, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(FONT_BOLD, 11)
        c.drawCentredString(x + 72, yy - 7, term)
        draw_wrapped(c, desc, x + 166, yy + 1, PAGE_W - 2 * MARGIN_X - 166, FONT_REG, 11, 16, INK)


def slide_checklist(c, page):
    header(c, page, "21강. 실습 전에 외워야 할 질문", [])
    questions = [
        "지금 병목은 CPU인가 GPU인가?",
        "측정은 Editor인가 Build인가, 목표 하드웨어인가?",
        "FPS 말고 frame time ms를 기록했는가?",
        "Draw Calls, SetPass, Batches, Triangles, Vertices 중 무엇이 변했는가?",
        "URP 옵션 하나만 바꾸고 비교했는가?",
        "품질 손실과 성능 개선을 둘 다 설명할 수 있는가?",
        "캐릭터 비용을 모델 포맷이 아니라 SkinnedMeshRenderer/Material/BlendShape/Bone 기준으로 봤는가?",
    ]
    y = TOP_Y - 72
    for i, q in enumerate(questions):
        yy = y - i * 48
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.4)
        c.roundRect(MARGIN_X, yy - 20, 26, 26, 5, fill=0, stroke=1)
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 13)
        c.drawString(MARGIN_X + 42, yy - 11, q)
    card(
        c,
        MARGIN_X,
        66,
        PAGE_W - 2 * MARGIN_X,
        62,
        "다음 수업 예고",
        "이론을 끝낸 뒤 첫 실습은 Benchmark_Field 씬과 성능 HUD를 만드는 것이다.",
        GREEN,
    )


def slide_references(c, page, part=1):
    header(c, page, "참고문헌 및 이미지 출처" if part == 1 else "참고문헌 계속", [])
    ids = list(SOURCES.keys())
    subset = ids[:11] if part == 1 else ids[11:]
    y = TOP_Y - 58
    draw_wrapped(
        c,
        "확인일: 2026-07-20. 본 PDF의 도식은 외부 이미지를 복제하지 않고 강의용으로 직접 제작한 벡터 도식이며, 도식 아래의 근거 태그는 아래 문헌을 의미한다.",
        MARGIN_X,
        y,
        PAGE_W - 2 * MARGIN_X,
        FONT_REG,
        10,
        16,
        MUTED,
    )
    y -= 48
    for sid in subset:
        title, url, org = SOURCES[sid]
        c.setFillColor(BLUE)
        c.setFont(FONT_BOLD, 10)
        c.drawString(MARGIN_X, y, f"[{sid}]")
        c.setFillColor(INK)
        c.setFont(FONT_BOLD, 10)
        c.drawString(MARGIN_X + 42, y, title)
        y -= 15
        y = draw_wrapped(c, f"{org} - {url}", MARGIN_X + 42, y, PAGE_W - 2 * MARGIN_X - 42, FONT_REG, 8, 12, MUTED)
        y -= 6


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))

    slides = [
        title_slide,
        slide_fact_boundary,
        slide_frame,
        slide_pipeline,
        slide_cpu_gpu,
        slide_draw_calls,
        slide_batching,
        slide_urp_asset,
        slide_urp_levers,
        slide_render_paths,
        slide_tools,
        slide_measure_protocol,
        slide_mesh,
        slide_material_shader,
        slide_transparency,
        slide_lighting,
        slide_texture_memory,
        slide_character,
        slide_not_vrm,
        slide_benchmark_field,
        slide_roadmap,
        slide_glossary,
        slide_checklist,
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
