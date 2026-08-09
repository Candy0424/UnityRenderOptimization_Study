from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

import create_extosc_lecture_pdf as base


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Unity_extOSC_Practical_Lecture.pdf"
base.OUT = OUT

PAGE_W = base.PAGE_W
PAGE_H = base.PAGE_H
MARGIN_X = base.MARGIN_X
TOP_Y = base.TOP_Y

FONT_REG = base.FONT_REG
FONT_BOLD = base.FONT_BOLD
FONT_CODE = base.FONT_CODE

INK = base.INK
MUTED = base.MUTED
SOFT = base.SOFT
PANEL = base.PANEL
GRID = base.GRID
BLUE = base.BLUE
CYAN = base.CYAN
GREEN = base.GREEN
AMBER = base.AMBER
RED = base.RED
VIOLET = base.VIOLET
DARK = base.DARK
LAV = base.LAV
MINT = base.MINT
CREAM = base.CREAM
ROSE = base.ROSE

SOURCES = {
    "S1": ("OpenSoundControl Specification 1.0", "OpenSoundControl.org / Matt Wright", "https://opensoundcontrol.stanford.edu/spec-1_0.html"),
    "S2": ("extOSC GitHub README", "Iam1337 / dr. ext", "https://github.com/Iam1337/extOSC"),
    "S3": ("OpenUPM extOSC package page", "OpenUPM", "https://openupm.com/packages/com.iam1337.extosc/"),
    "S4": ("Unity Manual - Install a UPM package from a Git URL", "Unity Technologies", "https://docs.unity3d.com/Manual/upm-ui-giturl.html"),
    "S5": ("Unity Manual - Create samples for your package", "Unity Technologies", "https://docs.unity3d.com/Manual/cus-samples.html"),
    "S6": ("VMC Protocol specification", "VirtualMotionCaptureProtocol", "https://protocol.vmc.info/english.html"),
    "S7": ("OBS Remote Control Guide", "OBS Project", "https://obsproject.com/kb/remote-control-guide"),
    "L1": ("Project manifest and lock file", "Local project", "Packages/manifest.json, Packages/packages-lock.json"),
    "L2": ("Installed extOSC package manifest", "Local package cache", "Library/PackageCache/com.iam1337.extosc@b7c2bfa81633/package.json"),
    "L3": ("Installed extOSC examples", "Local package cache", "Examples~/01-13"),
    "L4": ("Installed extOSC runtime source", "Local package cache", "OSCReceiver.cs, OSCTransmitter.cs, OSCMessage.cs, OSCValue.cs, OSCUtilities.cs"),
    "L5": ("Installed extOSC editor/UI source and icons", "Local package cache", "OSCMenuOptions.cs, Resources/extOSC/*.png"),
    "L6": ("Installed URP runtime source", "Local package cache", "UniversalRenderPipelineAsset.cs, Bloom.cs, VolumeProfile.cs"),
}


class PracticalDeck(base.Deck):
    def new_page(self, title: str, section: str = "", sources: list[str] | None = None):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.section = section

        c = self.c
        c.setFillColor(colors.white)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(SOFT)
        c.rect(0, PAGE_H - 74, PAGE_W, 74, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.rect(0, PAGE_H - 74, 9, 74, fill=1, stroke=0)

        c.setFont(FONT_BOLD, 18)
        c.setFillColor(INK)
        c.drawString(MARGIN_X, PAGE_H - 42, title)
        if section:
            c.setFont(FONT_BOLD, 8.5)
            c.setFillColor(BLUE)
            c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 44, section)

        c.setStrokeColor(GRID)
        c.setLineWidth(0.8)
        c.line(MARGIN_X, PAGE_H - 77, PAGE_W - MARGIN_X, PAGE_H - 77)

        c.setFont(FONT_REG, 8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN_X, 20, "Unity extOSC Practical Lecture - hands-on project course")
        c.drawCentredString(PAGE_W / 2, 20, f"{self.page}")
        base.draw_small_source_row(c, sources or [])


def txt(c, text, x, y, w, size=10.5, leading=14, color=INK, font=FONT_REG):
    return base.draw_wrapped(c, text, x, y, w, size=size, leading=leading, color=color, font=font)


def bullets(c, items, x, y, w, size=10.2, accent=BLUE, leading=14):
    return base.draw_bullets(c, items, x, y, w, size=size, leading=leading, bullet_color=accent)


def mini_card(c, title, body, x, y, w, h, accent=BLUE, fill=PANEL):
    base.card(c, title, body, x, y, w, h, fill=fill, accent=accent, body_size=9.7)


def source_footer(deck, sources):
    base.draw_small_source_row(deck.c, sources)


def section_bar(c, label, x, y, w, accent=BLUE):
    c.setFillColor(accent)
    c.roundRect(x, y - 18, w, 22, 7, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.white)
    c.drawCentredString(x + w / 2, y - 11, label)


def draw_scene_blueprint(c, x, y, w, h):
    base.draw_round_rect(c, x, y - h, w, h, colors.white, stroke=GRID, radius=8)
    c.setFont(FONT_BOLD, 11)
    c.setFillColor(INK)
    c.drawString(x + 18, y - 24, "Scene hierarchy blueprint")
    rows = [
        ("OSC_System", "OSCReceiver, OSCTransmitter, DebugHUD"),
        ("Stage_Root", "Light, Camera, Volume, props"),
        ("ControlPanel_Canvas", "Slider, Button, Pad, status text"),
        ("Controllers", "LightController, CameraController, URPController, PresetController"),
    ]
    base.draw_table(c, x + 18, y - 48, w - 36, [("GameObject", "Attach / purpose")] + rows, [0.32, 0.68], row_h=33)


def draw_packet_board(c, x, y, w, h):
    base.draw_round_rect(c, x, y - h, w, h, colors.white, stroke=GRID, radius=8)
    c.setFont(FONT_BOLD, 11)
    c.setFillColor(INK)
    c.drawString(x + 18, y - 24, "One packet, one job")
    base.draw_flow(
        c,
        x + 18,
        y - 42,
        w - 36,
        120,
        [
            ("Address", "/stage/light/key/intensity"),
            ("Type", "float"),
            ("Value", "0.75"),
            ("Apply", "Light.intensity"),
        ],
        [BLUE, VIOLET, GREEN, AMBER],
    )
    txt(
        c,
        "비유: 주소는 택배 송장, 타입은 상자 라벨, 값은 물건입니다. 실전에서는 주소표를 먼저 만들고 코드가 그 주소표를 따라가게 합니다.",
        x + 18,
        y - h + 54,
        w - 36,
        size=9.5,
        leading=13,
        color=MUTED,
    )


def draw_lesson_pattern(c, x, y, w, h, do_text, check_text, result_text, accent=BLUE):
    base.draw_round_rect(c, x, y - h, w, h, colors.white, stroke=GRID, radius=8)
    col_w = (w - 54) / 3
    blocks = [
        ("1. 만들기", do_text, accent, LAV),
        ("2. 확인", check_text, GREEN, MINT),
        ("3. 남기기", result_text, AMBER, CREAM),
    ]
    for i, (title, body, col, fill) in enumerate(blocks):
        bx = x + 18 + i * (col_w + 9)
        base.draw_round_rect(c, bx, y - 32 - 112, col_w, 112, fill, stroke=GRID, radius=7)
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(col)
        c.drawString(bx + 12, y - 53, title)
        txt(c, body, bx + 12, y - 74, col_w - 24, size=9.2, leading=12.5, color=INK)


def lab_title(deck, title, subtitle, goal, output, sources, accent=BLUE):
    deck.new_page(title, "실전 Lab", sources)
    c = deck.c
    c.setFont(FONT_BOLD, 24)
    c.setFillColor(accent)
    c.drawString(MARGIN_X, TOP_Y - 80, subtitle)
    txt(c, goal, MARGIN_X, TOP_Y - 120, PAGE_W - MARGIN_X * 2, size=12, leading=17, color=MUTED)
    draw_lesson_pattern(
        c,
        MARGIN_X,
        TOP_Y - 178,
        PAGE_W - MARGIN_X * 2,
        170,
        "씬/오브젝트/스크립트를 직접 만듭니다.",
        "OSC Console, Unity Console, Game View, Profiler 중 필요한 도구로 통과 기준을 봅니다.",
        output,
        accent=accent,
    )


def code_box_fit(c, code: str, x, y, w, h, title="C# example"):
    raw_lines = [line.replace("\t", "    ") for line in code.strip("\n").split("\n")]

    for size, leading in [(7.8, 9.6), (7.2, 8.9), (6.6, 8.2)]:
        wrapped = []
        for line in raw_lines:
            parts = base.wrap_text(line, FONT_CODE, size, w - 28)
            wrapped.extend(parts or [""])
        if len(wrapped) <= int((h - 42) / leading):
            break

    base.draw_round_rect(c, x, y - h, w, h, colors.HexColor("#1F2733"), stroke=colors.HexColor("#323C4A"), radius=7)
    c.setFont(FONT_BOLD, 9)
    c.setFillColor(colors.HexColor("#B6C4D8"))
    c.drawString(x + 14, y - 18, title)
    c.setFont(FONT_CODE, size)
    c.setFillColor(colors.HexColor("#EDF4FF"))
    cy = y - 35
    for line in wrapped:
        if cy < y - h + 13:
            c.drawString(x + 14, cy, "...")
            break
        c.drawString(x + 14, cy, line)
        cy -= leading


def code_page(deck, title, intro, code, notes, sources, accent=BLUE):
    deck.new_page(title, "실습 코드", sources)
    c = deck.c
    txt(c, intro, MARGIN_X, TOP_Y - 62, PAGE_W - MARGIN_X * 2, size=10.8, leading=14.5, color=MUTED)
    code_box_fit(c, code, MARGIN_X, TOP_Y - 106, 520, 388, title="C# example")
    c.setFont(FONT_BOLD, 12)
    c.setFillColor(accent)
    c.drawString(MARGIN_X + 544, TOP_Y - 106, "읽는 법")
    bullets(c, notes, MARGIN_X + 544, TOP_Y - 132, PAGE_W - MARGIN_X * 2 - 544, size=10.0, leading=14, accent=accent)


def table_page(deck, title, intro, rows, widths, sources, accent=BLUE, row_h=36):
    deck.new_page(title, "실습 표", sources)
    c = deck.c
    txt(c, intro, MARGIN_X, TOP_Y - 62, PAGE_W - MARGIN_X * 2, size=11, leading=15, color=MUTED)
    base.draw_table(c, MARGIN_X, TOP_Y - 112, PAGE_W - MARGIN_X * 2, rows, widths, row_h=row_h)


def build(deck):
    c = deck.c

    deck.new_page("Unity extOSC 실전 강의자료", "Practical OSC Course", ["S1", "S2", "L1", "L2"])
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, 0, PAGE_W, 12, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(0, 12, PAGE_W * 0.58, 8, fill=1, stroke=0)
    c.setFont(FONT_BOLD, 31)
    c.setFillColor(colors.white)
    c.drawString(58, PAGE_H - 118, "Unity extOSC")
    c.setFont(FONT_BOLD, 23)
    c.drawString(58, PAGE_H - 158, "실전 프로젝트 강의")
    txt(
        c,
        "Hello OSC부터 URP 렌더 제어, 운영자 패널, 프리셋 Bundle, 디버그 대시보드까지 직접 만드는 수업용 자료입니다.",
        60,
        PAGE_H - 204,
        610,
        size=12,
        leading=17,
        color=colors.HexColor("#D8E2F2"),
    )
    base.draw_icon_row(
        c,
        [
            (base.icon("OSC_transmitter_light.png"), "Send", BLUE),
            (base.icon("OSC_receiver_light.png"), "Receive", CYAN),
            (base.icon("OSC_message_light.png"), "Message", GREEN),
            (base.icon("OSC_bundle_light.png"), "Bundle", VIOLET),
        ],
        72,
        PAGE_H - 330,
        gap=55,
        label_color=colors.HexColor("#DDE6F4"),
    )
    c.setFont(FONT_REG, 9)
    c.setFillColor(colors.HexColor("#AEBBD0"))
    c.drawString(58, 58, "Target output: OSC-driven Live Stage Control prototype")
    c.drawRightString(PAGE_W - 58, 58, "Built from installed extOSC 1.21.0 package")

    deck.new_page("이 자료가 이전 자료와 다른 점", "0. 사용법", ["S2", "L2", "L3", "L4"])
    mini_card(c, "이론 먼저가 아님", "각 장은 바로 Unity에서 클릭하거나 코드를 붙이는 실습으로 시작합니다.", MARGIN_X, TOP_Y - 64, 248, 96, BLUE, LAV)
    mini_card(c, "결과물이 남음", "각 Lab 끝에는 캡처, 주소표, README 문장, 테스트 표 같은 제출물이 생깁니다.", MARGIN_X + 272, TOP_Y - 64, 248, 96, GREEN, MINT)
    mini_card(c, "포트폴리오 관점", "단순 송수신이 아니라 렌더/카메라/조명/운영 UI를 연결합니다.", MARGIN_X + 544, TOP_Y - 64, 248, 96, AMBER, CREAM)
    base.callout(
        c,
        "수업 진행 방식",
        "페이지마다 '목표 -> 만들기 -> 코드 -> 확인 -> 흔한 실수 -> 포트폴리오 기록' 순서로 봅니다. 모르는 개념은 실습이 끝난 뒤 되돌아와 확인하는 방식이 더 빠릅니다.",
        MARGIN_X,
        TOP_Y - 205,
        PAGE_W - MARGIN_X * 2,
        90,
        fill=colors.HexColor("#F8FAFD"),
        accent=VIOLET,
    )
    draw_packet_board(c, MARGIN_X, TOP_Y - 330, PAGE_W - MARGIN_X * 2, 170)

    deck.new_page("최종 결과물", "0. 사용법", ["L1", "L2", "L4", "L6"])
    txt(
        c,
        "이 수업의 목표는 '외부 OSC 신호로 Unity 라이브 스테이지를 제어하는 작은 운영 시스템'을 만드는 것입니다. 완성 후에는 데모 영상, README, 주소 계약서, 성능 비교 표까지 포트폴리오로 남깁니다.",
        MARGIN_X,
        TOP_Y - 62,
        PAGE_W - MARGIN_X * 2,
        size=11.2,
        leading=16,
        color=MUTED,
    )
    base.draw_flow(
        c,
        MARGIN_X,
        TOP_Y - 118,
        PAGE_W - MARGIN_X * 2,
        150,
        [
            ("Control", "Unity UI or external OSC app"),
            ("extOSC", "Receiver, Transmitter, Console"),
            ("Stage", "Light, Camera, Volume, URP"),
            ("Portfolio", "video, README, benchmark"),
        ],
        [VIOLET, BLUE, GREEN, AMBER],
    )
    mini_card(c, "씬 1", "OSC_Basics: Hello 메시지 송수신과 Console 확인", MARGIN_X, TOP_Y - 310, 180, 82, BLUE, LAV)
    mini_card(c, "씬 2", "LiveStage: 조명/카메라/이펙트/프리셋 제어", MARGIN_X + 204, TOP_Y - 310, 180, 82, GREEN, MINT)
    mini_card(c, "씬 3", "RenderLab: renderScale과 Bloom 값을 OSC로 조절", MARGIN_X + 408, TOP_Y - 310, 180, 82, AMBER, CREAM)
    mini_card(c, "씬 4", "DebugPanel: Ping, last message, error count 표시", MARGIN_X + 612, TOP_Y - 310, 180, 82, RED, ROSE)

    deck.new_page("준비물 체크", "1. 준비", ["S4", "S5", "L1", "L2"])
    draw_scene_blueprint(c, MARGIN_X, TOP_Y - 58, 455, 240)
    base.callout(
        c,
        "실습 전 체크리스트",
        "1. Package Manager에서 extOSC가 보이는지 확인\n2. Samples 중 Getting Started, Scripting, UI, Mapping, Ping을 Import\n3. Tools > extOSC > OSC Console 메뉴가 보이는지 확인\n4. 빈 Scene을 하나 만들고 OSC_System 오브젝트를 생성\n5. 테스트 포트는 우선 7001 하나로 통일",
        MARGIN_X + 480,
        TOP_Y - 58,
        PAGE_W - MARGIN_X * 2 - 480,
        240,
        fill=CREAM,
        accent=AMBER,
    )
    base.callout(
        c,
        "비유",
        "실습 전 준비는 촬영장 세팅입니다. 카메라, 조명, 무전기, 콘솔 위치가 잡혀야 감독의 큐 사인이 의미가 생깁니다.",
        MARGIN_X,
        TOP_Y - 330,
        PAGE_W - MARGIN_X * 2,
        80,
        fill=LAV,
        accent=VIOLET,
    )

    table_page(
        deck,
        "수업 전체 로드맵",
        "아래 순서대로 진행하면 각 실습이 다음 실습의 기반이 됩니다. 막히면 이전 Lab의 통과 기준으로 돌아가세요.",
        [
            ("Lab", "만드는 것", "통과 기준", "포트폴리오 증거"),
            ("0", "설치/샘플/씬 구조", "extOSC Console과 샘플 확인", "환경 캡처"),
            ("1", "Hello OSC Loopback", "문자열 메시지 송수신", "Console 로그"),
            ("2", "주소 계약서", "주소/타입/범위 표 완성", "README 표"),
            ("3", "Light Controller", "OSC slider로 조명 변화", "GIF/영상"),
            ("4", "Camera Controller", "FOV/위치 오프셋 제어", "연출 전환 영상"),
            ("5", "URP Render Controller", "renderScale/Bloom 값 변경", "Profiler 비교"),
            ("6", "Preset Bundle", "한 명령으로 무대 상태 전환", "시연 영상"),
            ("7", "Debug Dashboard", "Ping/마지막 메시지 표시", "운영 UI 캡처"),
        ],
        [0.08, 0.28, 0.34, 0.30],
        ["L2", "L3", "L4", "L6"],
        row_h=34,
    )

    lab_title(
        deck,
        "Lab 0 - 패키지와 샘플을 실제 수업 도구로 만들기",
        "목표: extOSC가 설치되어 있다는 사실을 실습 환경으로 바꾸기",
        "패키지가 설치된 것과 수업을 시작할 수 있는 것은 다릅니다. Lab 0에서는 설치 확인, 샘플 Import, 실습 씬 구조, 포트 규칙을 한 번에 정리합니다.",
        "환경 캡처 3장: Package Manager extOSC 화면, Tools > extOSC 메뉴, OSC_System hierarchy",
        ["S4", "S5", "L1", "L2", "L3"],
        accent=BLUE,
    )

    table_page(
        deck,
        "Lab 0 작업 순서",
        "Unity 안에서 그대로 따라 하는 체크리스트입니다.",
        [
            ("순서", "Unity에서 할 일", "확인할 것"),
            ("1", "Window > Package Manager 열기", "extOSC 패키지 표시"),
            ("2", "Samples에서 Getting Started, Scripting, UI, Mapping, Ping Import", "Assets/Samples 또는 Imported sample 확인"),
            ("3", "Tools > extOSC > OSC Console 열기", "빈 콘솔 창 표시"),
            ("4", "새 Scene 생성: OSC_Practical_Lab", "Hierarchy에 OSC_System 생성"),
            ("5", "OSC_System에 Receiver, Transmitter 추가", "Receiver LocalPort 7001, Transmitter RemotePort 7001"),
            ("6", "Scene 저장", "Assets/Scenes/OSC_Practical_Lab.unity"),
        ],
        [0.10, 0.47, 0.43],
        ["S4", "S5", "L3", "L5"],
        row_h=42,
    )

    lab_title(
        deck,
        "Lab 1 - Hello OSC Loopback",
        "목표: 같은 컴퓨터 안에서 OSC 메시지가 실제로 왕복하는지 확인",
        "localhost `127.0.0.1`과 port `7001`만 써서 가장 작은 OSC 송수신을 만듭니다. 이 실습이 통과돼야 이후 조명/카메라/렌더 제어가 의미를 가집니다.",
        "OSC Console 로그와 Unity Console 로그",
        ["S1", "S2", "L4", "L3"],
        accent=CYAN,
    )

    code_page(
        deck,
        "Lab 1 코드 - 송신기",
        "버튼 없이 Play 시작 시 한 번 보내는 코드입니다. extOSC README의 기본 송신 구조를 실습용 주소로 바꾼 형태입니다.",
        """
using extOSC;
using UnityEngine;

public class Lab01SendHello : MonoBehaviour
{
    public OSCTransmitter transmitter;

    private void Start()
    {
        var message = new OSCMessage("/lab/hello");
        message.AddValue(OSCValue.String("Hello extOSC"));
        transmitter.Send(message);
    }
}
""",
        [
            "`/lab/hello`는 이 수업에서 첫 번째로 약속하는 주소입니다.",
            "Transmitter의 RemoteHost는 `127.0.0.1`, RemotePort는 `7001`로 둡니다.",
            "외부 앱 없이 자기 자신에게 보내는 loopback 구조라 네트워크 변수를 최소화합니다.",
        ],
        ["S1", "S2", "L4", "L3"],
        accent=CYAN,
    )

    code_page(
        deck,
        "Lab 1 코드 - 수신기",
        "Receiver는 주소와 콜백을 묶습니다. 메시지가 들어오면 주소 비교 후 콜백이 실행됩니다.",
        """
using extOSC;
using UnityEngine;

public class Lab01ReceiveHello : MonoBehaviour
{
    public OSCReceiver receiver;

    private void Start()
    {
        receiver.Bind("/lab/hello", OnHello);
    }

    private void OnHello(OSCMessage message)
    {
        if (message.ToString(out var text))
            Debug.Log($"OSC Hello: {text}");
    }
}
""",
        [
            "Receiver의 LocalPort는 `7001`입니다.",
            "`message.ToString(out var text)`는 extOSC 확장 메서드입니다.",
            "Unity Console에 `OSC Hello: Hello extOSC`가 보이면 통과입니다.",
        ],
        ["S2", "L4", "L3"],
        accent=CYAN,
    )

    table_page(
        deck,
        "Lab 1 통과 기준과 막히는 지점",
        "Hello OSC에서 자주 막히는 부분을 먼저 잡아두면 이후 실습에서 시간을 많이 아낍니다.",
        [
            ("증상", "가장 먼저 볼 것", "해결"),
            ("아무 로그도 없음", "Receiver LocalPort와 Transmitter RemotePort", "둘 다 7001인지 확인"),
            ("Socket Error", "다른 앱이 같은 포트를 쓰는지", "포트 변경 또는 해당 앱 종료"),
            ("OSC Console에는 보임, Unity Console에는 없음", "Bind 주소 오타", "`/lab/hello` 완전 일치 확인"),
            ("값이 안 읽힘", "타입 불일치", "송신 String, 수신 ToString인지 확인"),
        ],
        [0.24, 0.38, 0.38],
        ["L4"],
        accent=RED,
        row_h=44,
    )

    lab_title(
        deck,
        "Lab 2 - 주소 계약서 만들기",
        "목표: 코드보다 먼저 OSC 주소표를 설계하기",
        "실전에서는 주소가 API입니다. 주소표 없이 코드를 쓰면 나중에 UI, 외부 앱, README, 테스트가 서로 다른 말을 하게 됩니다.",
        "README에 붙일 Address Contract Table",
        ["S1", "L4"],
        accent=VIOLET,
    )

    table_page(
        deck,
        "포트폴리오용 주소 계약서",
        "첫 버전은 아래 정도면 충분합니다. 모든 주소는 나중에 외부 패널이나 테스트 앱에서 그대로 사용할 수 있어야 합니다.",
        [
            ("Address", "Type", "Range", "Unity target"),
            ("/stage/light/key/intensity", "float", "0-8", "Key Light.intensity"),
            ("/stage/light/key/color", "float,float,float", "0-1 RGB", "Key Light.color"),
            ("/camera/main/fov", "float", "25-70", "Camera.fieldOfView"),
            ("/camera/main/offset", "float,float", "-3 to 3", "Camera rig local position"),
            ("/render/scale", "float", "0.5-1.0", "URP Asset renderScale"),
            ("/render/bloom/intensity", "float", "0-10", "VolumeProfile Bloom.intensity"),
            ("/stage/preset/load", "string", "preset id", "Preset controller"),
            ("/system/ping", "impulse", "none", "Connection monitor"),
        ],
        [0.34, 0.18, 0.18, 0.30],
        ["S1", "L4", "L6"],
        row_h=32,
    )

    code_page(
        deck,
        "Lab 2 코드 - 주소 상수",
        "주소 문자열은 여기저기 직접 쓰지 말고 한 곳에 모읍니다. 오타를 줄이고 README 표와 코드가 같은 이름을 쓰게 만드는 작은 습관입니다.",
        """
public static class OscAddress
{
    public const string KeyLightIntensity = "/stage/light/key/intensity";
    public const string KeyLightColor = "/stage/light/key/color";
    public const string CameraFov = "/camera/main/fov";
    public const string CameraOffset = "/camera/main/offset";
    public const string RenderScale = "/render/scale";
    public const string BloomIntensity = "/render/bloom/intensity";
    public const string StagePresetLoad = "/stage/preset/load";
    public const string SystemPing = "/system/ping";
}
""",
        [
            "이 파일은 `Assets/Scripts/OscAddress.cs`로 두면 됩니다.",
            "주소를 바꿀 때 코드 전체 검색이 아니라 이 파일과 README 표만 보면 됩니다.",
            "마스크 주소를 쓰기 전에는 정확한 주소로 먼저 통과시키세요.",
        ],
        ["L4"],
        accent=VIOLET,
    )

    lab_title(
        deck,
        "Lab 3 - 조명 제어",
        "목표: OSC float 값 하나로 실제 렌더 결과를 바꾸기",
        "조명은 가장 즉각적으로 보이는 실습 대상입니다. `/stage/light/key/intensity`로 Light intensity를 바꾸고, 색상까지 확장합니다.",
        "조명 밝기 Before/After 캡처와 10초 데모 영상",
        ["S2", "L4"],
        accent=GREEN,
    )

    code_page(
        deck,
        "Lab 3 코드 - Light Controller",
        "float 하나를 받아 Light intensity에 반영합니다. 외부 입력은 항상 clamp해서 안전한 범위 안에 넣습니다.",
        """
using extOSC;
using UnityEngine;

public class Lab03LightController : MonoBehaviour
{
    public OSCReceiver receiver;
    public Light keyLight;

    private void Start()
    {
        receiver.Bind(OscAddress.KeyLightIntensity, OnIntensity);
        receiver.Bind(OscAddress.KeyLightColor, OnColor);
    }

    private void OnIntensity(OSCMessage message)
    {
        if (!message.ToFloat(out var value)) return;
        keyLight.intensity = Mathf.Clamp(value, 0f, 8f);
    }

    private void OnColor(OSCMessage message)
    {
        if (message.Values.Count < 3) return;
        var r = Mathf.Clamp01(message.Values[0].FloatValue);
        var g = Mathf.Clamp01(message.Values[1].FloatValue);
        var b = Mathf.Clamp01(message.Values[2].FloatValue);
        keyLight.color = new Color(r, g, b);
    }
}
""",
        [
            "실전에서는 intensity와 color를 분리해 주소를 설계합니다.",
            "색상은 float 3개를 RGB로 해석합니다. 타입 검사 코드를 더 엄격히 붙이면 더 좋습니다.",
            "조명 변화는 Game View에서 바로 확인되므로 첫 포트폴리오 데모에 적합합니다.",
        ],
        ["S2", "L4"],
        accent=GREEN,
    )

    table_page(
        deck,
        "Lab 3 테스트 시나리오",
        "조명 제어는 감각으로만 보지 말고 테스트 값과 기대 결과를 표로 남깁니다.",
        [
            ("보낼 메시지", "기대 결과", "캡처"),
            ("/stage/light/key/intensity 0", "Key Light가 꺼진 것처럼 어두워짐", "Before"),
            ("/stage/light/key/intensity 4", "중간 밝기", "Mid"),
            ("/stage/light/key/intensity 8", "최대 밝기", "After"),
            ("/stage/light/key/color 1 0.6 0.3", "따뜻한 색 조명", "Color A"),
            ("/stage/light/key/color 0.4 0.7 1", "차가운 색 조명", "Color B"),
        ],
        [0.38, 0.42, 0.20],
        ["L4"],
        row_h=40,
    )

    lab_title(
        deck,
        "Lab 4 - 카메라 제어",
        "목표: OSC 값으로 방송 연출 파라미터를 바꾸기",
        "라이브 콘텐츠 개발자는 렌더 품질뿐 아니라 장면 전환과 카메라 연출도 다룹니다. FOV와 오프셋을 OSC로 조절합니다.",
        "FOV 변화 영상과 카메라 오프셋 테스트 캡처",
        ["S2", "L4"],
        accent=AMBER,
    )

    code_page(
        deck,
        "Lab 4 코드 - Camera Controller",
        "기본 Camera만으로도 실습할 수 있게 구성했습니다. Cinemachine을 쓰는 경우에는 같은 값을 Virtual Camera 쪽으로 연결하면 됩니다.",
        """
using extOSC;
using UnityEngine;

public class Lab04CameraController : MonoBehaviour
{
    public OSCReceiver receiver;
    public Camera targetCamera;
    public Transform cameraRig;

    private void Start()
    {
        receiver.Bind(OscAddress.CameraFov, OnFov);
        receiver.Bind(OscAddress.CameraOffset, OnOffset);
    }

    private void OnFov(OSCMessage message)
    {
        if (!message.ToFloat(out var value)) return;
        targetCamera.fieldOfView = Mathf.Clamp(value, 25f, 70f);
    }

    private void OnOffset(OSCMessage message)
    {
        if (message.Values.Count < 2) return;
        var x = Mathf.Clamp(message.Values[0].FloatValue, -3f, 3f);
        var y = Mathf.Clamp(message.Values[1].FloatValue, -2f, 2f);
        cameraRig.localPosition = new Vector3(x, y, cameraRig.localPosition.z);
    }
}
""",
        [
            "Camera와 cameraRig를 분리하면 회전/위치/줌 역할을 나누기 쉽습니다.",
            "오프셋은 Pad UI와 궁합이 좋습니다.",
            "갑작스러운 점프가 싫다면 이후 단계에서 Mathf.Lerp 또는 SmoothDamp를 추가합니다.",
        ],
        ["L4"],
        accent=AMBER,
    )

    code_page(
        deck,
        "Lab 4 확장 - 부드러운 값 적용",
        "외부 OSC 값은 즉시 바꾸는 것보다 target 값을 저장하고 Update에서 보간하면 방송 화면이 덜 거칠어집니다.",
        """
public class SmoothFloat
{
    public float current;
    public float target;
    public float speed = 8f;

    public float Tick(float deltaTime)
    {
        current = Mathf.Lerp(current, target, 1f - Mathf.Exp(-speed * deltaTime));
        return current;
    }
}

// Usage idea:
// OnFov message: fov.target = Mathf.Clamp(value, 25f, 70f);
// Update: targetCamera.fieldOfView = fov.Tick(Time.deltaTime);
""",
        [
            "OSC는 값 전달, 보간은 Unity 쪽 연출 책임으로 나눕니다.",
            "빠른 반응이 중요한 버튼은 즉시 적용하고, 카메라/조명은 보간하는 편이 자연스럽습니다.",
            "포트폴리오 설명에서 '운영 입력과 화면 적용을 분리했다'고 말할 수 있습니다.",
        ],
        ["L4"],
        accent=AMBER,
    )

    lab_title(
        deck,
        "Lab 5 - URP 렌더 제어",
        "목표: OSC로 렌더 품질과 비용을 비교하는 실험 패널 만들기",
        "URP renderScale과 Bloom intensity를 OSC로 바꾸고, Profiler에서 프레임 비용 변화를 기록합니다. 렌더 최적화 포트폴리오와 가장 직접적으로 연결되는 실습입니다.",
        "renderScale 1.0/0.8/0.67 비교 표와 Game View 캡처",
        ["L6", "L4"],
        accent=RED,
    )

    code_page(
        deck,
        "Lab 5 코드 - Render Scale Controller",
        "로컬 URP 17.3.0 소스에서 `UniversalRenderPipelineAsset.renderScale`은 get/set 가능한 프로퍼티로 확인됩니다. 실습에서는 별도 URP Asset을 참조해 값을 바꿉니다.",
        """
using extOSC;
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class Lab05RenderScaleController : MonoBehaviour
{
    public OSCReceiver receiver;
    public UniversalRenderPipelineAsset urpAsset;

    private void Start()
    {
        receiver.Bind(OscAddress.RenderScale, OnRenderScale);
    }

    private void OnRenderScale(OSCMessage message)
    {
        if (urpAsset == null) return;
        if (!message.ToFloat(out var value)) return;

        urpAsset.renderScale = Mathf.Clamp(value, 0.5f, 1.0f);
    }
}
""",
        [
            "주의: 프로젝트 공용 URP Asset을 런타임에서 바꾸면 전체 카메라 렌더링에 영향을 줄 수 있습니다.",
            "포트폴리오 실험용 URP Asset을 따로 복제해 사용하는 편이 안전합니다.",
            "renderScale은 품질/성능 비교용으로 좋지만 UI는 네이티브 해상도로 렌더된다는 Unity UI 설명도 함께 기억하세요.",
        ],
        ["L6", "L4"],
        accent=RED,
    )

    code_page(
        deck,
        "Lab 5 코드 - Bloom Controller",
        "URP Bloom은 VolumeProfile 안의 VolumeComponent입니다. 로컬 URP 소스의 예제도 VolumeProfile에서 component를 가져와 runtime에 값을 바꾸는 흐름을 보여줍니다.",
        """
using extOSC;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class Lab05BloomController : MonoBehaviour
{
    public OSCReceiver receiver;
    public VolumeProfile volumeProfile;
    private Bloom bloom;

    private void Start()
    {
        if (volumeProfile != null)
            volumeProfile.TryGet(out bloom);

        receiver.Bind(OscAddress.BloomIntensity, OnBloom);
    }

    private void OnBloom(OSCMessage message)
    {
        if (bloom == null) return;
        if (!message.ToFloat(out var value)) return;

        bloom.intensity.overrideState = true;
        bloom.intensity.value = Mathf.Clamp(value, 0f, 10f);
    }
}
""",
        [
            "VolumeProfile에 Bloom override가 없으면 `TryGet`은 false가 됩니다.",
            "실습 전 Global Volume에 Bloom을 추가하고 intensity Override 체크를 켭니다.",
            "런타임 수정용 Profile은 원본을 복제해 쓰면 에셋 오염을 줄일 수 있습니다.",
        ],
        ["L6", "L4"],
        accent=RED,
    )

    table_page(
        deck,
        "Lab 5 측정표",
        "수치는 네 노트북/씬 기준으로 직접 채워 넣는 칸입니다. 중요한 것은 '설정 변경 -> 화면 변화 -> 비용 변화'를 같은 표에 묶는 것입니다.",
        [
            ("Test", "Message", "Visual result", "CPU/GPU ms", "Note"),
            ("A", "/render/scale 1.0", "Native render target", "", "baseline"),
            ("B", "/render/scale 0.8", "약간 부드러워짐", "", "quality/perf compare"),
            ("C", "/render/scale 0.67", "픽셀 확대감 증가", "", "low scale test"),
            ("D", "/render/bloom/intensity 0", "Bloom off", "", "post cost compare"),
            ("E", "/render/bloom/intensity 5", "Bloom visible", "", "post cost compare"),
        ],
        [0.08, 0.28, 0.28, 0.18, 0.18],
        ["L6"],
        row_h=40,
    )

    lab_title(
        deck,
        "Lab 6 - 프리셋과 Bundle",
        "목표: 한 번의 명령으로 여러 무대 상태를 바꾸기",
        "실제 운영에서는 조명 하나만 바꾸기보다 '무대 A', '토크 모드', '클라이맥스 효과'처럼 여러 값을 묶어 전환합니다. 이때 주소 계약과 Bundle 개념이 같이 필요합니다.",
        "프리셋 3개와 전환 영상",
        ["S1", "S2", "L4"],
        accent=VIOLET,
    )

    code_page(
        deck,
        "Lab 6 코드 - Preset Receiver",
        "`/stage/preset/load`로 문자열 id를 받아 여러 컨트롤러에 값을 넘기는 구조입니다. 직접 값을 바꾸지 말고 전용 controller에 위임하면 유지보수가 쉽습니다.",
        """
using extOSC;
using UnityEngine;

[System.Serializable]
public class StagePreset
{
    public string id;
    public float keyIntensity;
    public float cameraFov;
    public float renderScale;
}

public class Lab06PresetReceiver : MonoBehaviour
{
    public OSCReceiver receiver;
    public StagePreset[] presets;
    public Lab03LightController lightController;
    public Lab04CameraController cameraController;
    public Lab05RenderScaleController renderController;

    private void Start()
    {
        receiver.Bind(OscAddress.StagePresetLoad, OnLoadPreset);
    }

    private void OnLoadPreset(OSCMessage message)
    {
        if (!message.ToString(out var id)) return;

        foreach (var preset in presets)
        {
            if (preset.id != id) continue;
            Debug.Log($"Load preset: {id}");
            // In production, call explicit Apply methods on each controller.
            return;
        }
    }
}
""",
        [
            "여기서는 구조를 보여주기 위해 Apply 호출부를 주석으로 남겼습니다.",
            "실제 구현에서는 각 Controller에 `ApplyIntensity`, `ApplyFov`, `ApplyRenderScale` 메서드를 만드세요.",
            "프리셋 데이터는 ScriptableObject로 옮기면 포트폴리오 완성도가 올라갑니다.",
        ],
        ["L4"],
        accent=VIOLET,
    )

    code_page(
        deck,
        "Lab 6 코드 - Bundle 송신",
        "여러 메시지를 한 타이밍에 보내고 싶을 때 Bundle을 씁니다. OSC 스펙은 Packet 내용이 Message 또는 Bundle이라고 정의합니다.",
        """
using extOSC;
using UnityEngine;

public class Lab06PresetSender : MonoBehaviour
{
    public OSCTransmitter transmitter;

    public void SendTalkPreset()
    {
        var bundle = new OSCBundle();
        bundle.AddPacket(OSCMessage.Create(
            OscAddress.KeyLightIntensity, OSCValue.Float(3.0f)));
        bundle.AddPacket(OSCMessage.Create(
            OscAddress.CameraFov, OSCValue.Float(42f)));
        bundle.AddPacket(OSCMessage.Create(
            OscAddress.RenderScale, OSCValue.Float(0.8f)));

        transmitter.Send(bundle);
    }
}
""",
        [
            "Bundle은 '여러 메시지를 한 봉투에 담기'입니다.",
            "수신 쪽이 Bundle을 풀어 각 메시지를 처리하는 흐름은 extOSC Receiver 내부 처리와도 연결됩니다.",
            "한 프레임에 많은 값을 보내는 경우 UseBundle과 빈도 제한을 같이 고려합니다.",
        ],
        ["S1", "S2", "L4"],
        accent=VIOLET,
    )

    lab_title(
        deck,
        "Lab 7 - 운영자 디버그 패널",
        "목표: 만든 기능이 방송 중에도 상태를 설명하게 만들기",
        "실무형 도구는 동작만 하면 끝이 아닙니다. 마지막 메시지, 연결 상태, 현재 프리셋, 경고를 표시해야 운영자가 믿고 쓸 수 있습니다.",
        "DebugPanel Game View 캡처",
        ["S2", "L4", "L5"],
        accent=BLUE,
    )

    code_page(
        deck,
        "Lab 7 코드 - 마지막 메시지 표시",
        "주소 마스크 `*`를 사용해 모든 메시지를 받아 UI 텍스트에 마지막 메시지 정보를 남깁니다.",
        """
using extOSC;
using UnityEngine;
using UnityEngine.UI;

public class Lab07OscDebugHud : MonoBehaviour
{
    public OSCReceiver receiver;
    public Text lastMessageText;
    public int receivedCount;

    private void Start()
    {
        receiver.Bind("*", OnAnyMessage);
    }

    private void OnAnyMessage(OSCMessage message)
    {
        receivedCount++;
        lastMessageText.text =
            $"#{receivedCount} {message.Address} values:{message.Values.Count}";
    }
}
""",
        [
            "`*` 마스크는 모든 주소를 받으므로 디버그 전용으로 쓰는 편이 안전합니다.",
            "운영 UI에는 마지막 주소, 값 개수, 시간, 연결 상태를 표시하세요.",
            "UI Text 대신 TMP를 써도 구조는 같습니다.",
        ],
        ["S2", "L4", "L5"],
        accent=BLUE,
    )

    table_page(
        deck,
        "Lab 7 운영 표시 항목",
        "이 항목을 넣으면 단순 예제에서 운영 도구로 한 단계 올라갑니다.",
        [
            ("항목", "표시 내용", "왜 필요한가"),
            ("Connection", "Ping OK / Timeout", "외부 앱 연결 상태 파악"),
            ("Last Address", "마지막 수신 OSC 주소", "주소 오타 추적"),
            ("Last Value", "값 개수와 대표 값", "타입 불일치 추적"),
            ("Current Preset", "현재 무대 프리셋 id", "운영 상태 공유"),
            ("Message Rate", "최근 1초 수신 개수", "메시지 폭주 감지"),
            ("Warnings", "type mismatch, missing component", "실패 원인 표시"),
        ],
        [0.20, 0.34, 0.46],
        ["L4", "L5"],
        row_h=38,
    )

    lab_title(
        deck,
        "Lab 8 - Avatar/VMC 응용 준비",
        "목표: OSC 기반 아바타 제어를 단정하지 않고 안전하게 설계하기",
        "VMC Protocol은 OSC over UDP/IP를 쓰지만, extOSC는 VMC 전용 라이브러리가 아니라 일반 OSC 송수신 도구입니다. 따라서 주소와 타입 규약을 별도로 맞춰야 합니다.",
        "VMC 수신 로그 캡처와 해석 표",
        ["S6", "L4"],
        accent=GREEN,
    )

    code_page(
        deck,
        "Lab 8 코드 - 표정 라우터 Mock",
        "실제 VRM 런타임 API에 붙이기 전, Animator 파라미터로 표정 weight 라우팅 구조를 먼저 검증합니다.",
        """
using extOSC;
using UnityEngine;

public class Lab08ExpressionRouter : MonoBehaviour
{
    public OSCReceiver receiver;
    public Animator animator;

    private void Start()
    {
        receiver.Bind("/avatar/expression/*/weight", OnExpression);
    }

    private void OnExpression(OSCMessage message)
    {
        if (!message.ToFloat(out var weight)) return;

        var parts = message.Address.Split('/');
        if (parts.Length < 4) return;

        var expression = parts[3];
        animator.SetFloat(expression, Mathf.Clamp01(weight));
    }
}
""",
        [
            "이 코드는 VMC 구현이 아니라 주소 라우팅 연습입니다.",
            "실제 VRM Expression 적용은 사용하는 VRM 런타임 API에 맞게 바꿔야 합니다.",
            "마스크 주소를 쓸 때는 허용 expression 목록을 두고 검증하면 더 안전합니다.",
        ],
        ["S6", "L4"],
        accent=GREEN,
    )

    deck.new_page("실전 성능 규칙", "성능/안정성", ["L3", "L4"])
    mini_card(c, "보내는 빈도 제한", "슬라이더를 매 프레임 보내기보다 20-30Hz 또는 값 변경 시 전송을 우선합니다.", MARGIN_X, TOP_Y - 64, 245, 96, BLUE, LAV)
    mini_card(c, "값 검증", "타입, 범위, 대상 컴포넌트 null 여부를 검사하고 실패 원인을 HUD에 남깁니다.", MARGIN_X + 270, TOP_Y - 64, 245, 96, GREEN, MINT)
    mini_card(c, "Bundle 사용", "동시에 바뀌는 상태는 Bundle 또는 프리셋 명령으로 묶어 관리합니다.", MARGIN_X + 540, TOP_Y - 64, 245, 96, VIOLET, colors.HexColor("#F5F3FF"))
    base.callout(
        c,
        "Drown Detection을 보는 관점",
        "extOSC changelog와 Receiver 소스에는 수신 처리 과부하를 감지하는 흐름이 있습니다. 경고가 보이면 OSC가 잘못됐다는 뜻보다 'Unity 메인 스레드에서 처리할 양을 줄여야 한다'는 신호로 봅니다.",
        MARGIN_X,
        TOP_Y - 205,
        PAGE_W - MARGIN_X * 2,
        92,
        fill=ROSE,
        accent=RED,
    )
    table_page(
        deck,
        "문제 해결 루틴",
        "실습 중 막히면 아래 순서로만 확인하세요. 이 순서가 제일 빠릅니다.",
        [
            ("단계", "질문", "도구"),
            ("1", "패키지가 설치됐나?", "Package Manager, manifest.json"),
            ("2", "송신 포트와 수신 포트가 같은가?", "Transmitter/Receiver Inspector"),
            ("3", "주소가 완전히 같은가?", "OSC Console, Address Contract"),
            ("4", "값 타입이 맞는가?", "ToFloat/ToString, Match Pattern"),
            ("5", "Unity 대상이 null이 아닌가?", "Inspector reference, Debug.LogWarning"),
            ("6", "메시지가 너무 많은가?", "Profiler, Message Rate HUD"),
        ],
        [0.10, 0.55, 0.35],
        ["L4", "L5"],
        row_h=38,
    )

    table_page(
        deck,
        "7일 실전 제작 플랜",
        "하루에 하나씩 끝내면 결과물이 남는 일정입니다. 깊게 파는 것보다 매일 통과 기준을 남기는 쪽이 좋습니다.",
        [
            ("Day", "작업", "끝났다는 기준"),
            ("1", "Lab 0-1: 설치, 샘플, Hello OSC", "Hello 로그 캡처"),
            ("2", "Lab 2: 주소 계약서와 OscAddress.cs", "README 주소표 1차"),
            ("3", "Lab 3: 조명 제어", "밝기/색상 영상"),
            ("4", "Lab 4: 카메라 제어", "FOV/오프셋 영상"),
            ("5", "Lab 5: URP 렌더 제어", "Profiler 비교 표"),
            ("6", "Lab 6-7: 프리셋과 디버그 패널", "운영 UI 캡처"),
            ("7", "문서/영상 정리", "1분 데모 영상과 README 완성"),
        ],
        [0.10, 0.48, 0.42],
        ["L1", "L2", "L4", "L6"],
        accent=AMBER,
        row_h=36,
    )

    table_page(
        deck,
        "포트폴리오 제출물 체크리스트",
        "이 표를 README 마지막에 그대로 넣고 체크해도 됩니다.",
        [
            ("구분", "필수 산출물", "왜 중요한가"),
            ("Demo", "1분 데모 영상", "기능을 한 번에 보여줌"),
            ("Docs", "OSC Address Contract", "협업 가능한 설계 증명"),
            ("Code", "Controller scripts", "구현 역량 증명"),
            ("Debug", "OSC Console/HUD 캡처", "문제 해결 역량 증명"),
            ("Performance", "renderScale/Bloom 비교 표", "렌더 최적화 연결"),
            ("Caution", "VMC/OBS는 제안 구조로 명시", "근거와 추정을 구분"),
        ],
        [0.18, 0.38, 0.44],
        ["S1", "S2", "S6", "S7", "L4", "L6"],
        accent=GREEN,
        row_h=38,
    )

    deck.new_page("마지막 수업 정리", "마무리", ["S1", "S2", "L4", "L6"])
    txt(
        c,
        "이번 실전 강의의 핵심은 extOSC 자체를 많이 아는 것이 아니라, OSC 메시지를 Unity 안의 실제 렌더/연출 시스템으로 안전하게 연결하는 것입니다.",
        MARGIN_X,
        TOP_Y - 62,
        PAGE_W - MARGIN_X * 2,
        size=12,
        leading=17,
        color=MUTED,
    )
    mini_card(c, "1. 주소는 API", "주소표를 먼저 만들고 모든 코드와 UI가 그 표를 따르게 합니다.", MARGIN_X, TOP_Y - 130, 245, 100, BLUE, LAV)
    mini_card(c, "2. 값은 검증", "타입, 범위, null, 실패 로그를 기본으로 넣습니다.", MARGIN_X + 270, TOP_Y - 130, 245, 100, GREEN, MINT)
    mini_card(c, "3. 결과는 측정", "렌더 스케일과 Bloom은 화면 캡처와 Profiler 수치를 함께 남깁니다.", MARGIN_X + 540, TOP_Y - 130, 245, 100, RED, ROSE)
    base.callout(
        c,
        "면접에서 한 문장으로 말하기",
        "extOSC를 이용해 OSC 주소 계약서를 설계하고, 외부 제어 신호를 Unity의 조명/카메라/URP 렌더 파라미터에 연결했으며, Debug HUD와 Profiler 측정으로 운영성과 성능을 함께 검증했습니다.",
        MARGIN_X,
        TOP_Y - 275,
        PAGE_W - MARGIN_X * 2,
        92,
        fill=CREAM,
        accent=AMBER,
    )

    deck.new_page("출처와 근거 구분", "Sources", ["S1", "S2", "L1", "L2", "L6"])
    txt(
        c,
        "이 자료는 공식 문서와 현재 프로젝트의 로컬 패키지 파일을 근거로 작성했습니다. 실습 구조와 포트폴리오 과제는 사용자의 목표에 맞춘 설계 제안이며, 특정 기업의 실제 내부 기술 스택을 단정하지 않습니다.",
        MARGIN_X,
        TOP_Y - 62,
        PAGE_W - MARGIN_X * 2,
        size=11.2,
        leading=16,
        color=MUTED,
    )
    mini_card(c, "확인된 사실", "OSC 스펙, extOSC README/manifest/source, Unity Package Manager/Samples 문서, VMC/OBS 공식 안내, 로컬 URP API", MARGIN_X, TOP_Y - 150, 360, 116, GREEN, MINT)
    mini_card(c, "실습 설계", "조명/카메라/URP/프리셋/디버그 패널을 연결하는 포트폴리오 구성은 이 프로젝트 목표에 맞춘 수업 설계입니다.", MARGIN_X + 390, TOP_Y - 150, 360, 116, AMBER, CREAM)
    base.callout(
        c,
        "로컬 기준",
        "이 프로젝트의 extOSC는 Git UPM dependency로 설치되어 있고, lock 파일 기준 hash는 b7c2bfa81633cbcbc8cc4312e15cb5fbd0ed7d1d입니다.",
        MARGIN_X,
        TOP_Y - 310,
        PAGE_W - MARGIN_X * 2,
        80,
        fill=colors.HexColor("#F8FAFD"),
        accent=BLUE,
    )

    deck.new_page("출처 목록 1", "Sources", ["S1", "S2", "S3", "S4", "S5"])
    y = TOP_Y - 62
    for key in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
        title, owner, url = SOURCES[key]
        base.draw_label(c, key, MARGIN_X, y + 2, BLUE if key != "S7" else RED)
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 38, y, title)
        c.setFont(FONT_REG, 8.8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN_X + 38, y - 15, owner)
        txt(c, url, MARGIN_X + 38, y - 30, PAGE_W - MARGIN_X * 2 - 38, font=FONT_CODE, size=8.2, leading=11, color=BLUE)
        y -= 66

    deck.new_page("출처 목록 2", "Sources", ["L1", "L2", "L3", "L4", "L5", "L6"])
    y = TOP_Y - 62
    for key in ["L1", "L2", "L3", "L4", "L5", "L6"]:
        title, owner, url = SOURCES[key]
        base.draw_label(c, key, MARGIN_X, y + 2, GREEN)
        c.setFont(FONT_BOLD, 10)
        c.setFillColor(INK)
        c.drawString(MARGIN_X + 38, y, title)
        c.setFont(FONT_REG, 8.8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN_X + 38, y - 15, owner)
        txt(c, url, MARGIN_X + 38, y - 30, PAGE_W - MARGIN_X * 2 - 38, font=FONT_CODE, size=8.2, leading=11, color=BLUE)
        y -= 62


if __name__ == "__main__":
    deck = PracticalDeck()
    build(deck)
    deck.save()
    print(OUT)
