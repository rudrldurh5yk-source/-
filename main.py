import streamlit as st

st.title ('게임인 척하는 미적분')
st.write ('이 쿠키는 칙촉일까 촉촉한 초코칩 쿠키일까')


# -*- coding: utf-8 -*-
"""
🍪 말랑말랑 미적분 쿠키타이쿤
------------------------------------------------
미래엔 미적분1 중간고사 범위(함수의 극한, 함수의 연속, 미분계수와 도함수,
접선의 방정식 등) 문제를 풀면 쿠키가 구워집니다.
제한시간 안에 최대한 많은 쿠키를 모으세요!

* 타이머는 실시간으로 흘러가지 않고, 문제를 제출하거나
  넘길 때(=화면이 다시 그려질 때)마다 남은 시간이 갱신되어 표시됩니다.

실행 방법:
    pip install streamlit
    streamlit run cookie_calculus_game.py
"""

import random
import time
from fractions import Fraction

import streamlit as st


# ============================================================
# 1. 문제 은행 (미래엔 미적분1 중간고사 범위 기반)
# ============================================================
PROBLEMS = [
    # ---------------- 함수의 극한 ----------------
    {"latex": r"\lim_{x \to 2} (3x+4)", "answer": 10,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to -3} (4-x^2)", "answer": -5,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to 1} \left(x^2+\frac{2}{x}\right)", "answer": 3,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to -2} (x^3-3x+7)", "answer": 5,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to 2} (2x-1)(3x+2)", "answer": 24,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to -1} \frac{4x-2}{x^4+2x^2+3}", "answer": -1,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to 3} \frac{x^2-9}{x-3}", "answer": 6,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to 2} \frac{x^2-8x+12}{x-2}", "answer": -4,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to \infty} \frac{4x^2+3x}{2x^2+1}", "answer": 2,
     "desc": "함수의 극한값을 구하시오."},
    {"latex": r"\lim_{x \to \infty} \left(\sqrt{4x^2+x}-2x\right)", "answer": 0.25,
     "desc": "함수의 극한값을 구하시오. (분수 1/4 형태로 입력 가능)"},
    {"latex": r"\lim_{x \to -2} \frac{x^3+4x^2+3x-2}{x^2-4}", "answer": 0.25,
     "desc": "함수의 극한값을 구하시오. (분수 1/4 형태로 입력 가능)"},
    {"latex": r"\lim_{x \to 0}\frac{f(x)}{x}=5 \text{ 일 때, } \lim_{x \to 0}\frac{4x+5f(x)}{3x^2-4x+f(x)}",
     "answer": 29, "desc": "주어진 조건을 이용하여 극한값을 구하시오."},
    {"latex": r"\lim_{x \to \infty}\left(\sqrt{4x^2+ax}-2x\right)=-3 \text{ 일 때, 상수 } a",
     "answer": -12, "desc": "상수 a의 값을 구하시오."},
    {"latex": r"\lim_{x \to 3}\frac{x-3}{\sqrt{x+a}-2}=b \ (b\neq 0) \text{ 일 때, } a+b",
     "answer": 5, "desc": "상수 a, b에 대하여 a+b의 값을 구하시오."},
    {"latex": r"2x+2 \le f(x) \le x^2+3 \text{ 일 때, } \lim_{x \to 1} f(x)",
     "answer": 4, "desc": "함수의 극한의 대소 관계를 이용하여 극한값을 구하시오."},
    {"latex": r"\lim_{x \to -1}(x-1)f(x)=4 \text{ 일 때, } \lim_{x \to -1}(3x^2+2x+1)f(x)",
     "answer": -4, "desc": "주어진 조건을 이용하여 극한값을 구하시오."},
    {"latex": r"\lim_{x \to 1}f(x)=-1,\ \lim_{x \to 1}g(x)=k,\ "
              r"\lim_{x \to 1}\frac{2f(x)-9g(x)}{f(x)g(x)-6}=5 \text{ 일 때, } k",
     "answer": 7, "desc": "상수 k의 값을 구하시오."},

    # ---------------- 함수의 연속 ----------------
    {"latex": r"f(x)=2x^2-6x-1 \text{ 일 때, } f(1)",
     "answer": -5, "desc": "함숫값을 구하시오."},
    {"latex": r"f(x)=\begin{cases}\dfrac{x^2+x+a}{x-3} & (x \neq 3) \\ b & (x=3)\end{cases}"
              r"\text{ 이 모든 실수에서 연속일 때, } b-a",
     "answer": 19, "desc": "상수 a, b에 대하여 b-a의 값을 구하시오."},
    {"latex": r"f(x)=\begin{cases}x^2-3x-6 & (x \le k) \\ x+k & (x>k)\end{cases}"
              r"\text{ 가 모든 실수에서 연속이 되도록 하는 양수 } k",
     "answer": 6, "desc": "양수 k의 값을 구하시오."},

    # ---------------- 미분계수와 도함수 ----------------
    {"latex": r"f(x)=2x^2-x+4 \text{ 의 } x=1 \text{ 에서의 미분계수}",
     "answer": 3, "desc": "미분계수를 구하시오."},
    {"latex": r"\text{곡선 } y=2x^3-5x^2+1 \text{ 위의 점 } (2,-3) \text{ 에서의 접선의 기울기}",
     "answer": 4, "desc": "접선의 기울기를 구하시오."},
    {"latex": r"f(3)=-3,\ f'(3)=4,\ g(3)=2,\ g'(3)=5 \text{ 일 때, } \{f(x)-2g(x)\}'|_{x=3}",
     "answer": -6, "desc": "x=3에서의 미분계수를 구하시오."},
    {"latex": r"f(3)=-3,\ f'(3)=4,\ g(3)=2,\ g'(3)=5 \text{ 일 때, } \{f(x)g(x)\}'|_{x=3}",
     "answer": -7, "desc": "x=3에서의 미분계수를 구하시오."},
    {"latex": r"f(x)=-x^2+5x \text{ 에서 } x \text{ 의 값이 } -2 \text{ 에서 } 1 \text{ 까지 변할 때의 평균변화율}",
     "answer": 6, "desc": "평균변화율을 구하시오."},
    {"latex": r"y=-x^4+4x^2+1 \text{ 을 미분한 도함수의 } x=1 \text{ 에서의 값}",
     "answer": 4, "desc": "도함수의 값을 구하시오."},
    {"latex": r"y=3x^6 \text{ 을 미분하면 } y'=ax^5 \text{ 의 꼴이다. 이때 } a",
     "answer": 18, "desc": "상수 a의 값을 구하시오."},

    # ---------------- 접선의 방정식 (교사용교과서 추가분) ----------------
    {"latex": r"\text{곡선 } y=x^2+4x+3 \text{ 위의 점 } (0,3) \text{ 에서의 접선의 기울기}",
     "answer": 4, "desc": "접선의 기울기를 구하시오."},
    {"latex": r"\text{곡선 } y=x^2+4x+3 \text{ 에 접하고 기울기가 6인 접선의 } y\text{절편}",
     "answer": 2, "desc": "접선의 y절편을 구하시오."},
    {"latex": r"\text{곡선 } y=x^3-x^2-2x-3 \text{ 위의 점 } (1,-5) \text{ 에서의 접선에 수직인 직선의 } y\text{절편}",
     "answer": -6, "desc": "수직인 직선의 y절편을 구하시오."},
    {"latex": r"\text{점 } (1,0) \text{ 에서 곡선 } y=x^3-6x+1 \text{ 에 그은 접선의 기울기}",
     "answer": -3, "desc": "접선의 기울기를 구하시오."},
    {"latex": r"\text{곡선 } y=x^3-6x^2+10x \text{ 의 접선 중 기울기가 최소인 접선과 } x\text{축, }"
              r"y\text{축으로 둘러싸인 도형의 넓이}",
     "answer": 16, "desc": "도형의 넓이를 구하시오."},
    {"latex": r"\text{곡선 } y=x^3+4x^2-14 \text{ 위의 점 } (-3,-5) \text{ 에서의 접선이 이 곡선과 }"
              r"\text{점 } (a,b) \text{ 에서 만날 때 } (a\neq -3),\ b-a",
     "answer": 8, "desc": "b-a의 값을 구하시오."},
    {"latex": r"\text{곡선 } y=x^3-ax^2+3x+4 \text{ 에 접하는 직선 중 기울기가 2인 것이 존재하지 않도록 }"
              r"\text{하는 실수 } a \text{ 의 값의 범위를 만족시키는 정수 } a \text{ 의 개수}",
     "answer": 3, "desc": "정수 a의 개수를 구하시오."},
    {"latex": r"f(1)=3,\ f'(1)=-4,\ g(x)=(x^4+3x^2)f(x) \text{ 일 때, } g'(1)",
     "answer": 14, "desc": "곱의 미분법을 이용하여 g'(1)의 값을 구하시오."},
    {"latex": r"\lim_{x \to 1}\frac{x^{2026}+x^{2025}-2}{x-1}",
     "answer": 4051, "desc": "미분계수의 정의를 이용하여 극한값을 구하시오."},
    {"latex": r"f(x)=x^2-4x \text{ 에서 } x \text{ 의 값이 } 1 \text{ 에서 } 3 \text{ 까지 변할 때의 평균변화율과 }"
              r"x=c \text{ 에서의 미분계수가 같을 때, } c",
     "answer": 2, "desc": "상수 c의 값을 구하시오."},
    {"latex": r"\lim_{x \to 1}\frac{f(x)-4}{x^3-1}=\frac{1}{2} \text{ 일 때, } f(1)f'(1)",
     "answer": 6, "desc": "f(1)f'(1)의 값을 구하시오."},
    {"latex": r"f(x)=x^2+ax+b \text{ 가 } \lim_{x \to 2}\frac{f(x)+1}{x-2}=f'(2)+f(3) "
              r"\text{ 를 만족시킬 때, } ab",
     "answer": -12, "desc": "ab의 값을 구하시오."},
    {"latex": r"\text{곡선 } f(x)=2x^3-3ax \text{ 위의 서로 다른 두 점 } (a,f(a)),\ (1,f(1)) "
              r"\text{ 에서 그은 두 접선이 서로 평행할 때, } a \ (a \neq 1)",
     "answer": -1, "desc": "상수 a의 값을 구하시오."},
    {"latex": r"f(x)=\begin{cases}x^3+ax^2 & (x \le 1) \\ bx+4 & (x>1)\end{cases} "
              r"\text{ 가 } x=1 \text{ 에서 미분가능할 때, } a+b",
     "answer": -15, "desc": "a+b의 값을 구하시오."},
]

# 제한시간 옵션 (초 단위)
TIME_OPTIONS = {
    "30초 (스피드런)": 30,
    "60초 (기본)": 60,
    "90초 (여유)": 90,
    "120초 (넉넉)": 120,
    "5분 (300초)": 300,
    "7분 (420초)": 420,
    "10분 (600초)": 600,
}


# ============================================================
# 2. 유틸 함수
# ============================================================
def parse_number(text: str):
    """'1/4', '0.25', '-12' 등의 입력을 float 으로 변환. 실패 시 None."""
    if text is None:
        return None
    text = text.strip().replace(" ", "")
    if not text:
        return None
    try:
        if "/" in text:
            return float(Fraction(text))
        return float(text)
    except Exception:
        return None


def is_correct(user_text: str, answer: float) -> bool:
    val = parse_number(user_text)
    if val is None:
        return False
    return abs(val - answer) < 0.01


def format_time(seconds: float) -> str:
    """초를 mm:ss 형식으로 변환."""
    seconds = max(0, int(seconds))
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def pick_new_question():
    """이전 문제와 다른 문제를 랜덤으로 뽑는다."""
    if len(PROBLEMS) == 1:
        st.session_state.current = 0
        return
    choices = [i for i in range(len(PROBLEMS)) if i != st.session_state.get("current")]
    st.session_state.current = random.choice(choices)


def init_state():
    defaults = {
        "started": False,
        "finished": False,
        "cookies": 0,
        "wrong_tries": 0,
        "start_time": None,
        "time_limit": 60,
        "current": None,
        "feedback": "",
        "feedback_type": None,  # "success" / "error" / None
        "best_score": 0,
        "answer_box_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def start_game(time_limit: int):
    st.session_state.started = True
    st.session_state.finished = False
    st.session_state.cookies = 0
    st.session_state.wrong_tries = 0
    st.session_state.start_time = time.time()
    st.session_state.time_limit = time_limit
    st.session_state.feedback = ""
    st.session_state.feedback_type = None
    st.session_state.current = None
    pick_new_question()


def end_game():
    st.session_state.started = False
    st.session_state.finished = True
    if st.session_state.cookies > st.session_state.best_score:
        st.session_state.best_score = st.session_state.cookies


# ============================================================
# 3. 귀여운 디자인 (CSS)
# ============================================================
CUTE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gaegu:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', 'Gaegu', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #fff9f0 0%, #ffefe0 45%, #ffe6d5 100%);
}

h1, h2, h3 {
    color: #a9642b !important;
}

/* 버튼을 몽글몽글하게 */
div.stButton > button {
    border-radius: 999px;
    border: 2px solid #f3b88a;
    background: linear-gradient(180deg, #fff2e2, #ffdfc0);
    color: #9a5b22;
    font-weight: 700;
    font-family: 'Jua', sans-serif;
    padding: 0.55em 1.3em;
    box-shadow: 0 3px 0 #e8a765;
    transition: all 0.15s ease-in-out;
}
div.stButton > button:hover {
    background: linear-gradient(180deg, #ffe4c4, #ffd19a);
    transform: translateY(-2px);
    box-shadow: 0 5px 0 #e8a765;
}
div.stButton > button:active {
    transform: translateY(1px);
    box-shadow: 0 1px 0 #e8a765;
}

/* 입력창 몽글몽글 */
.stTextInput > div > div > input {
    border-radius: 14px;
    border: 2px solid #ffcfa0;
    padding: 10px 14px;
    font-size: 16px;
}

/* 라디오 버튼 라벨 살짝 귀엽게 */
.stRadio > label, .stRadio div[role="radiogroup"] label {
    font-family: 'Jua', sans-serif;
}

.cute-title {
    text-align: center;
    font-size: 44px;
    margin-bottom: 0px;
}
.cute-title .bounce {
    display: inline-block;
    animation: bounce 1.6s infinite;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.cute-sub {
    text-align: center;
    color: #b9895a;
    font-size: 16px;
    margin-top: -6px;
    margin-bottom: 18px;
}

/* 스탯 카드 */
.stat-card {
    background: #fff3e4;
    border: 2px solid #ffd9ad;
    border-radius: 20px;
    padding: 10px 6px 12px 6px;
    text-align: center;
    box-shadow: 0 3px 0 #f3c384;
}
.stat-emoji { font-size: 26px; }
.stat-label { font-size: 13px; color: #a9743f; font-weight: 700; margin-top: 2px; }
.stat-value { font-size: 24px; color: #7a4a1a; font-weight: 800; }

/* 피드백 말풍선 */
.cute-feedback {
    border-radius: 18px;
    padding: 12px 18px;
    margin-bottom: 12px;
    font-weight: 700;
    font-size: 16px;
}
.cute-feedback.success {
    background: #eafbe7;
    border: 2px solid #9fdb9a;
    color: #3d7a37;
}
.cute-feedback.error {
    background: #fff0f0;
    border: 2px solid #f4a9a9;
    color: #a1453f;
}

/* 쿠키 항아리 */
.cookie-jar-box {
    border: 3px dashed #e3a45f;
    border-radius: 26px;
    background: linear-gradient(180deg, #fffaf0 0%, #ffe9c7 100%);
    padding: 16px;
    min-height: 160px;
    max-height: 420px;
    overflow-y: auto;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    gap: 6px;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.05);
}
.cookie-jar-box .cookie {
    font-size: 27px;
    line-height: 1;
    display: inline-block;
    filter: drop-shadow(0 2px 1px rgba(0,0,0,0.2));
}
.cookie-jar-box .sparkle {
    font-size: 15px;
    align-self: center;
    opacity: 0.8;
}
.cookie-jar-box .cookie.newest {
    animation: cookiePop 0.5s ease-out;
}
@keyframes cookiePop {
    0%   { transform: scale(0) rotate(-30deg); opacity: 0; }
    60%  { transform: scale(1.35) rotate(8deg); opacity: 1; }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}
.cookie-jar-empty {
    width: 100%;
    text-align: center;
    color: #c08a4e;
    font-size: 15px;
    padding: 20px 8px;
}
.cookie-count-badge {
    width: 100%;
    text-align: center;
    font-weight: 700;
    color: #8a5a20;
    margin-top: 8px;
}
</style>
"""


def render_cookie_jar(n: int):
    """쿠키 개수만큼 이모지를 쌓아서 보여준다. 마지막 쿠키에는 팝 애니메이션."""
    if n <= 0:
        st.markdown(
            '<div class="cookie-jar-box"><div class="cookie-jar-empty">'
            "🫙 아직 비어있어요! 문제를 풀어서 냠냠 쿠키를 채워보세요 🍪"
            "</div></div>",
            unsafe_allow_html=True,
        )
        return

    MAX_RENDER = 300
    render_count = min(n, MAX_RENDER)
    pieces = []
    for i in range(render_count):
        cls = "cookie newest" if i == render_count - 1 else "cookie"
        pieces.append(f'<span class="{cls}">🍪</span>')
        if (i + 1) % 6 == 0:
            pieces.append('<span class="sparkle">✨</span>')
    st.markdown(f'<div class="cookie-jar-box">{"".join(pieces)}</div>', unsafe_allow_html=True)
    if n > MAX_RENDER:
        st.markdown(
            f'<div class="cookie-count-badge">+{n - MAX_RENDER}개 더 있어요! (총 {n}개) 🍪</div>',
            unsafe_allow_html=True,
        )


def stat_card(emoji: str, label: str, value: str) -> str:
    return f"""
    <div class="stat-card">
        <div class="stat-emoji">{emoji}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
    </div>
    """


def cute_feedback(message: str, kind: str):
    icon = "🎉" if kind == "success" else "😵‍💫"
    st.markdown(
        f'<div class="cute-feedback {kind}">{icon} {message}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# 4. 화면 구성
# ============================================================
st.set_page_config(page_title="말랑말랑 쿠키타이쿤", page_icon="🍪", layout="wide")
st.markdown(CUTE_CSS, unsafe_allow_html=True)
init_state()

st.markdown(
    '<div class="cute-title">🍪<span class="bounce">🧁</span>말랑말랑 미적분 쿠키타이쿤</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="cute-sub">함수의 극한 · 함수의 연속 · 미분계수와 접선 — '
    "문제를 풀 때마다 쿠키가 뿅! 하고 구워져요</div>",
    unsafe_allow_html=True,
)

# ---------------- 게임 시작 전: 시간 선택 화면 ----------------
if not st.session_state.started and not st.session_state.finished:
    st.subheader("⏰ 제한 시간을 선택해주세요")
    time_label = st.radio(
        "제한 시간을 골라주세요",
        list(TIME_OPTIONS.keys()),
        index=1,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.write(f"🏆 최고 기록: **{st.session_state.best_score}개** 🍪")
    st.markdown(
        "**놀이 방법**\n"
        "- 랜덤으로 나오는 말랑말랑 미적분 문제를 풀고 정답을 입력해요.\n"
        "- 정답을 맞히면 쿠키가 1개 뿅! 하고 구워지고, 옆 쿠키 항아리에 차곡차곡 쌓여요.\n"
        "- 틀려도 괜찮아요! 같은 문제를 계속 다시 풀어볼 수 있어요.\n"
        "- 남은 시간은 문제를 제출하거나 넘길 때마다 위쪽에 갱신되어 표시돼요.\n"
        "- 제한 시간 안에 최대한 많은 쿠키를 모아보세요! 🧁"
    )
    if st.button("🔥 오븐 예열하고 시작하기!", type="primary", use_container_width=True):
        start_game(TIME_OPTIONS[time_label])
        st.rerun()

# ---------------- 게임 진행 중 ----------------
elif st.session_state.started:
    elapsed = time.time() - st.session_state.start_time
    remaining = st.session_state.time_limit - elapsed

    if remaining <= 0:
        end_game()
        st.rerun()

    left_col, right_col = st.columns([2, 1])

    with left_col:
        # 남은 시간 / 구운 쿠키 표시 (문제가 넘어갈 때만 갱신됨)
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(stat_card("⏰", "남은 시간", format_time(remaining)), unsafe_allow_html=True)
        with sc2:
            st.markdown(stat_card("🍪", "구운 쿠키", f"{st.session_state.cookies}개"), unsafe_allow_html=True)

        st.divider()

        problem = PROBLEMS[st.session_state.current]
        st.markdown(f"**🧮 문제** — {problem['desc']}")
        st.latex(problem["latex"])

        if st.session_state.feedback:
            cute_feedback(st.session_state.feedback, st.session_state.feedback_type)

        with st.form(key=f"answer_form_{st.session_state.answer_box_key}", clear_on_submit=True):
            user_answer = st.text_input("정답을 입력하세요 (예: 10, -5, 1/4)")
            submitted = st.form_submit_button("✅ 정답 제출")

        if submitted:
            if is_correct(user_answer, problem["answer"]):
                st.session_state.cookies += 1
                st.session_state.feedback = "정답이에요! 쿠키가 뿅 하고 구워졌어요 🍪"
                st.session_state.feedback_type = "success"
                pick_new_question()
                st.session_state.answer_box_key += 1
            else:
                st.session_state.wrong_tries += 1
                st.session_state.feedback = "앗, 오븐 온도가 살짝 안 맞았나 봐요! 다시 계산해볼까요?"
                st.session_state.feedback_type = "error"
                st.session_state.answer_box_key += 1
            st.rerun()

        if st.button("🙈 이 문제는 다음에! 넘어가기"):
            pick_new_question()
            st.session_state.feedback = ""
            st.session_state.feedback_type = None
            st.rerun()

    with right_col:
        st.markdown("### 🫙 쿠키 항아리")
        render_cookie_jar(st.session_state.cookies)

# ---------------- 게임 종료 ----------------
else:
    st.subheader("🎉 게임 끝! 오늘의 결과는요...")
    st.markdown(f"## 총 **{st.session_state.cookies}개**의 쿠키를 구웠어요! 🍪🎊")
    render_cookie_jar(st.session_state.cookies)

    if st.session_state.cookies >= st.session_state.best_score and st.session_state.cookies > 0:
        st.success("🏆 최고 기록 갱신! 대단해요!")

    st.write(f"이번 판 틀린 횟수: {st.session_state.wrong_tries}회")
    st.write(f"최고 기록: **{st.session_state.best_score}개** 🍪")

    if st.button("🔁 다시 도전하기!", type="primary", use_container_width=True):
        st.session_state.started = False
        st.session_state.finished = False
        st.rerun()
