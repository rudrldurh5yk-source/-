import streamlit as st

st.title ('미적분 중간고사 범위 게임')
st.write ('hello streamlit')


# -*- coding: utf-8 -*-
"""
🍪 미적분 쿠키타이쿤
------------------------------------------------
미래엔 미적분1 중간고사 범위(함수의 극한, 함수의 연속, 미분계수와 도함수)
문제를 풀면 쿠키가 구워집니다. 제한시간 안에 최대한 많은 쿠키를 모으세요!

실행 방법:
    pip install streamlit
    (선택, 자동 타이머 갱신용) pip install streamlit-autorefresh
    streamlit run cookie_calculus_game.py
"""

import random
import time
from fractions import Fraction

import streamlit as st

# streamlit-autorefresh 가 설치되어 있으면 타이머가 1초마다 자동 갱신됩니다.
# 설치되어 있지 않아도 게임은 정상 동작하며(정답 제출/버튼 클릭 시 타이머 갱신),
# 더 부드러운 카운트다운을 원하면 pip install streamlit-autorefresh 를 해주세요.
try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False


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
]

TIME_OPTIONS = {"30초 (스피드런)": 30, "60초 (기본)": 60, "90초 (여유)": 90, "120초 (마라톤)": 120}


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


def cookie_row(n: int) -> str:
    """쿠키 개수를 이모지 문자열로. 너무 많으면 개수 표기로 축약."""
    if n <= 60:
        return "🍪" * n if n > 0 else "아직 없어요"
    return f"🍪 x {n}"


# ============================================================
# 3. 화면 구성
# ============================================================
st.set_page_config(page_title="미적분 쿠키타이쿤", page_icon="🍪", layout="centered")
init_state()

st.title("🍪 미적분 쿠키타이쿤")
st.caption("함수의 극한 · 함수의 연속 · 미분계수와 도함수 — 문제를 풀 때마다 쿠키가 구워집니다!")

# ---------------- 게임 시작 전 ----------------
if not st.session_state.started and not st.session_state.finished:
    st.subheader("게임 설정")
    time_label = st.radio("제한 시간을 선택하세요", list(TIME_OPTIONS.keys()), index=1, horizontal=True)
    st.write(f"최고 기록: **{st.session_state.best_score}개** 🍪")
    st.markdown(
        "**규칙**\n"
        "- 랜덤으로 나오는 미적분 문제를 풀고 정답을 입력하세요.\n"
        "- 정답을 맞히면 쿠키가 1개 구워지고, 다음 문제로 넘어갑니다.\n"
        "- 오답이면 쿠키는 늘지 않지만, 같은 문제를 계속 도전할 수 있어요.\n"
        "- 제한 시간 안에 최대한 많은 쿠키를 모으세요!"
    )
    if st.button("🔥 오븐 예열하고 시작하기", type="primary", use_container_width=True):
        start_game(TIME_OPTIONS[time_label])
        st.rerun()

# ---------------- 게임 진행 중 ----------------
elif st.session_state.started:
    elapsed = time.time() - st.session_state.start_time
    remaining = st.session_state.time_limit - elapsed

    if HAS_AUTOREFRESH and remaining > 0:
        st_autorefresh(interval=1000, key="timer_refresh")

    if remaining <= 0:
        end_game()
        st.rerun()

    # 상태 표시
    col1, col2 = st.columns(2)
    col1.metric("⏱️ 남은 시간", f"{max(0, int(remaining))}초")
    col2.metric("🍪 구운 쿠키", f"{st.session_state.cookies}개")
    st.progress(min(1.0, max(0.0, remaining / st.session_state.time_limit)))

    st.divider()

    problem = PROBLEMS[st.session_state.current]
    st.markdown(f"**문제** — {problem['desc']}")
    st.latex(problem["latex"])

    if st.session_state.feedback:
        if st.session_state.feedback_type == "success":
            st.success(st.session_state.feedback)
        elif st.session_state.feedback_type == "error":
            st.error(st.session_state.feedback)

    with st.form(key=f"answer_form_{st.session_state.answer_box_key}", clear_on_submit=True):
        user_answer = st.text_input("정답을 입력하세요 (예: 10, -5, 1/4)")
        submitted = st.form_submit_button("✅ 정답 제출")

    if submitted:
        if is_correct(user_answer, problem["answer"]):
            st.session_state.cookies += 1
            st.session_state.feedback = "정답입니다! 쿠키가 하나 구워졌어요 🍪"
            st.session_state.feedback_type = "success"
            pick_new_question()
            st.session_state.answer_box_key += 1
            st.balloons()
        else:
            st.session_state.wrong_tries += 1
            st.session_state.feedback = "아쉬워요, 오븐 온도가 안 맞았나 봐요. 다시 계산해보세요!"
            st.session_state.feedback_type = "error"
            st.session_state.answer_box_key += 1
        st.rerun()

    skip_col, refresh_col = st.columns(2)
    with skip_col:
        if st.button("🙈 이 문제 포기하고 다음 문제"):
            pick_new_question()
            st.session_state.feedback = ""
            st.session_state.feedback_type = None
            st.rerun()
    with refresh_col:
        if not HAS_AUTOREFRESH:
            if st.button("🔄 타이머 갱신"):
                st.rerun()

    if not HAS_AUTOREFRESH:
        st.caption("💡 `pip install streamlit-autorefresh` 를 설치하면 타이머가 자동으로 갱신됩니다.")

# ---------------- 게임 종료 ----------------
else:
    st.subheader("🎉 게임 종료!")
    st.markdown(f"## 총 **{st.session_state.cookies}개**의 쿠키를 구웠어요! 🍪")
    st.write(cookie_row(st.session_state.cookies))

    if st.session_state.cookies >= st.session_state.best_score and st.session_state.cookies > 0:
        st.success("🏆 최고 기록 갱신!")

    st.write(f"이번 판 틀린 횟수: {st.session_state.wrong_tries}회")
    st.write(f"최고 기록: **{st.session_state.best_score}개**")

    if st.button("🔁 다시 도전하기", type="primary", use_container_width=True):
        st.session_state.started = False
        st.session_state.finished = False
        st.rerun()
