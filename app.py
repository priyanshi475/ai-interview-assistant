import streamlit as st
import speech_recognition as sr
import threading
import time
import re

st.set_page_config(page_title="AI Interview Pro", page_icon="🎯", layout="centered")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#080810;color:#e8e8f0}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding-top:2rem;max-width:780px}

.hero{text-align:center;padding:2.5rem 0 1.5rem;position:relative}
.hero::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:500px;height:300px;background:radial-gradient(ellipse,rgba(99,102,241,.15) 0%,transparent 70%);pointer-events:none}
.hero-badge{display:inline-block;background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.35);color:#a5b4fc;font-size:.72rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;padding:.35rem 1rem;border-radius:999px;margin-bottom:1.2rem}
.hero h1{font-family:'Syne',sans-serif;font-size:2.8rem;font-weight:800;background:linear-gradient(135deg,#e8e8f0 0%,#a5b4fc 50%,#818cf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.15;margin:0 0 .6rem}
.hero p{color:#6b7280;font-size:1rem;margin:0}

.card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:1.8rem 2rem;margin:1.2rem 0;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.5),transparent)}

.q-card{background:linear-gradient(135deg,rgba(99,102,241,.08),rgba(129,140,248,.04));border:1px solid rgba(99,102,241,.25);border-radius:16px;padding:1.8rem 2rem;margin:1rem 0}
.q-num{font-family:'Syne',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#818cf8;margin-bottom:.6rem}
.q-text{font-size:1.3rem;font-weight:500;color:#e8e8f0;line-height:1.45;margin:0}
.q-hint{font-size:.82rem;color:#4b5563;margin-top:.8rem;font-style:italic}

.pill{display:inline-flex;align-items:center;gap:.5rem;padding:.45rem 1rem;border-radius:999px;font-size:.82rem;font-weight:500;margin:.5rem 0}
.pill-red{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);color:#fca5a5}
.pill-yellow{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.3);color:#fcd34d}
.pill-green{background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.3);color:#86efac}
.dot{width:8px;height:8px;border-radius:50%;background:currentColor;animation:pulse 1.2s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}

.ans-box{background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.06);border-left:3px solid #818cf8;border-radius:0 12px 12px 0;padding:1rem 1.2rem;margin:.8rem 0;color:#c4c4d4;font-size:.95rem;line-height:1.6}
.ans-label{font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#4b5563;margin-bottom:.4rem}

.prog-wrap{margin:1.2rem 0}
.prog-row{display:flex;justify-content:space-between;font-size:.78rem;color:#4b5563;margin-bottom:.4rem}
.prog-track{background:rgba(255,255,255,.06);border-radius:999px;height:4px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#6366f1,#a5b4fc);border-radius:999px}

.fb-header{text-align:center;padding:1.5rem 0 1rem}
.fb-header h2{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:700;color:#e8e8f0;margin-bottom:.3rem}
.score-ring{display:inline-flex;flex-direction:column;align-items:center;justify-content:center;width:110px;height:110px;border-radius:50%;border:3px solid #6366f1;background:rgba(99,102,241,.1);margin:1rem 0;box-shadow:0 0 30px rgba(99,102,241,.3)}
.score-num{font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:#a5b4fc;line-height:1}
.score-lbl{font-size:.7rem;color:#6b7280;letter-spacing:.08em}
.sec-title{font-family:'Syne',sans-serif;font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.15em;color:#6366f1;margin:1.5rem 0 .7rem}
.chip-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.5rem}
.chip-g{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.25);color:#86efac;padding:.35rem .85rem;border-radius:999px;font-size:.82rem}
.chip-a{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);color:#fcd34d;padding:.35rem .85rem;border-radius:999px;font-size:.82rem}
.qfb-card{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:1rem 1.2rem;margin-bottom:.8rem}
.badge{font-size:.72rem;font-weight:600;padding:.2rem .6rem;border-radius:6px;text-transform:uppercase;letter-spacing:.08em}
.b-ex{background:rgba(34,197,94,.15);color:#86efac}
.b-go{background:rgba(99,102,241,.15);color:#a5b4fc}
.b-av{background:rgba(245,158,11,.15);color:#fcd34d}
.b-nw{background:rgba(239,68,68,.15);color:#fca5a5}
.rec-box{background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(129,140,248,.05));border:1px solid rgba(99,102,241,.3);border-radius:12px;padding:1.2rem;margin-top:1rem;text-align:center}
.rec-box strong{font-family:'Syne',sans-serif;font-size:1rem}
.rec-box p{font-size:.88rem;color:#9ca3af;margin-top:.4rem}

.stButton>button{background:linear-gradient(135deg,#6366f1,#818cf8)!important;color:#fff!important;border:none!important;border-radius:10px!important;padding:.65rem 2rem!important;font-family:'DM Sans',sans-serif!important;font-weight:500!important;font-size:.95rem!important;box-shadow:0 4px 20px rgba(99,102,241,.3)!important;width:100%}
.stTextArea textarea{background:rgba(255,255,255,.04)!important;border:1px solid rgba(255,255,255,.1)!important;border-radius:10px!important;color:#e8e8f0!important;font-size:.95rem!important}
</style>
""", unsafe_allow_html=True)

# ── Questions ──────────────────────────────────────────────────────────────────
QUESTIONS = [
    {"q": "Tell me about yourself.",
     "hint": "Cover your background, key skills, and what drives you professionally."},
    {"q": "What are your greatest strengths?",
     "hint": "Pick 2-3 strengths and back each with a concrete example."},
    {"q": "What is your biggest weakness?",
     "hint": "Be honest, then show how you are actively working to improve it."},
    {"q": "Why should we hire you?",
     "hint": "Connect your unique skills directly to what this role needs."},
    {"q": "Where do you see yourself in 5 years?",
     "hint": "Show ambition that aligns with the company's growth direction."},
]

# ── Module-level mic result (shared across reruns) ─────────────────────────────
_MIC = {"result": None, "error": None, "done": False}

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {
    "page": "start",          # start | interview | results
    "q_index": 0,
    "answers": [],
    "stage": "ask",           # ask | listening | done_q
    "text_mode": False,
    "mic_active": False,
    "error_msg": "",
    "feedback": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ────────────────────────────────────────────────────────────────────
def speak(text):
    try:
        import pyttsx3
        e = pyttsx3.init()
        e.setProperty('rate', 155)
        e.say(text)
        e.runAndWait()
        e.stop()
    except Exception:
        pass

def _mic_worker():
    global _MIC
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.8
    r.non_speaking_duration = 0.8
    try:
        with sr.Microphone() as src:
            r.adjust_for_ambient_noise(src, duration=0.5)
            audio = r.listen(src, timeout=10, phrase_time_limit=30)
    except OSError:
        _MIC = {"result": None, "error": "mic",     "done": True}; return
    except sr.WaitTimeoutError:
        _MIC = {"result": None, "error": "timeout", "done": True}; return
    except Exception as ex:
        _MIC = {"result": None, "error": str(ex),   "done": True}; return
    try:
        _MIC = {"result": r.recognize_google(audio, language="en-IN"), "error": None, "done": True}
    except sr.UnknownValueError:
        _MIC = {"result": None, "error": "unclear", "done": True}
    except sr.RequestError:
        _MIC = {"result": None, "error": "network", "done": True}

def start_mic():
    global _MIC
    _MIC = {"result": None, "error": None, "done": False}
    threading.Thread(target=_mic_worker, daemon=True).start()

def badge(r):
    cls = {"Excellent":"b-ex","Good":"b-go","Average":"b-av","Needs Work":"b-nw"}.get(r,"b-av")
    return f'<span class="badge {cls}">{r}</span>'

def prog(cur, tot):
    pct = int(cur/tot*100)
    return f'<div class="prog-wrap"><div class="prog-row"><span>Progress</span><span>Question {cur} of {tot}</span></div><div class="prog-track"><div class="prog-fill" style="width:{pct}%"></div></div></div>'

# ── FREE Local Feedback ────────────────────────────────────────────────────────
def make_feedback(answers):
    GOOD_KW = [
        ["experience","skill","background","worked","studied","passionate","achieved","developed","graduated","specialize","expertise"],
        ["strength","good at","excel","skilled","ability","capable","example","instance","helped","improved","led","delivered"],
        ["weakness","working on","improving","learning","challenge","overcome","course","practice","feedback","better","growth"],
        ["value","contribute","unique","offer","experience","benefit","team","result","achieve","fit"],
        ["goal","grow","lead","senior","manage","develop","learn","contribute","advance","career","vision","aspire"],
    ]
    FILLERS   = ["um","uh","like","basically","literally","you know","kind of","sort of","i mean"]
    CONFIDENT = ["i will","i can","i have","i am","i believe","definitely","certainly","confident"]
    WEAK      = ["i don't know","not sure","i guess","i think maybe","no idea"]

    qfb, scores = [], []
    for i, ans in enumerate(answers):
        al   = ans.lower()
        wc   = len(al.split())
        sc   = len([s for s in re.split(r'[.!?]+', ans) if s.strip()])
        kws  = sum(1 for k in (GOOD_KW[i] if i < len(GOOD_KW) else []) if k in al)
        conf = sum(1 for c in CONFIDENT if c in al)
        fill = sum(al.count(f) for f in FILLERS)
        weak = sum(1 for w in WEAK if w in al)

        s = 0
        if wc >= 80: s += 3
        elif wc >= 50: s += 2
        elif wc >= 25: s += 1
        s += min(kws, 3)
        s += min(conf, 2)
        if sc >= 3: s += 1
        s -= min(fill // 2, 2)
        s -= weak * 2
        s = max(0, min(s, 9))
        scores.append(s)

        rating = "Excellent" if s>=7 else "Good" if s>=5 else "Average" if s>=3 else "Needs Work"

        tips = []
        if wc < 25:    tips.append("Very short — aim for 50+ words.")
        elif wc < 50:  tips.append("Add a concrete example to elaborate.")
        if kws == 0:   tips.append("Include more relevant keywords for this question.")
        if fill >= 3:  tips.append(f"Reduce filler words — detected {fill} times.")
        if weak > 0:   tips.append("Avoid uncertain phrases — speak with confidence.")
        if conf == 0:  tips.append("Use confident language: 'I have', 'I can', 'I believe'.")
        if sc < 3:     tips.append("Structure: situation → action → result.")
        if not tips:   tips.append("Great answer — confident, detailed, and well-structured!")

        qfb.append({
            "question": QUESTIONS[i]["q"],
            "rating":   rating,
            "feedback": " ".join(tips[:2]),
            "answer":   ans,
        })

    overall = max(1, min(10, round(sum(scores)/len(scores)/9*10))) if scores else 1

    tw = sum(len(a.split()) for a in answers)
    tf = sum(sum(a.lower().count(f) for f in FILLERS) for a in answers)
    tc = sum(sum(1 for c in CONFIDENT if c in a.lower()) for a in answers)
    tk = sum(sum(1 for k in (GOOD_KW[i] if i<len(GOOD_KW) else []) if k in answers[i].lower()) for i in range(len(answers)))

    strengths, improvements = [], []
    if tw >= 200:  strengths.append("Detailed and thorough responses")
    if tc >= 4:    strengths.append("Confident and assertive language")
    if tk >= 8:    strengths.append("Strong relevant keywords")
    if all(len(a.split())>30 for a in answers): strengths.append("Consistent answer length")
    if tw < 150:   improvements.append("Give longer, more detailed answers")
    if tf >= 4:    improvements.append("Reduce filler words (um, uh, like…)")
    if tc < 2:     improvements.append("Use more confident language")
    if tk < 5:     improvements.append("Include more role-relevant keywords")
    if any(len(a.split())<20 for a in answers): improvements.append("Avoid very short answers")

    if not strengths:    strengths    = ["Attempted all questions", "Showed willingness to engage"]
    if not improvements: improvements = ["Keep practising for fluency", "Record yourself to spot filler words"]

    if overall >= 8:   rec, reason = "Hire",    "Strong performance with confident, detailed answers."
    elif overall >= 6: rec, reason = "Consider","Solid foundation — a few areas need polishing."
    else:              rec, reason = "Pass",    "Answers need more depth and confidence — keep practising!"

    avg_w   = tw // len(answers)
    summary = (
        f"You answered all {len(answers)} questions, averaging {avg_w} words per answer. "
        f"{'Great confidence and keyword usage overall.' if overall>=7 else 'Focus on more structured, detailed answers.'} "
        f"{'Filler words minimal — nice work!' if tf<3 else f'Filler words used {tf} times — work on reducing these.'}"
    )
    return {"overall_score":overall,"overall_summary":summary,
            "strengths":strengths[:3],"improvements":improvements[:3],
            "question_feedback":qfb,"recommendation":rec,"recommendation_reason":reason}

# ══════════════════════════════════════════════════════════════════════════════
# HERO (always shown)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ 100% Free — No API Key Needed</div>
  <h1>AI Interview<br>Simulator</h1>
  <p>Practice. Get feedback. Get hired.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: START
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "start":
    st.markdown("""
    <div class="card">
      <p style="color:#9ca3af;font-size:.95rem;margin:0 0 .5rem">
        Answer <strong style="color:#e8e8f0">5 common interview questions</strong> by voice or
        text and get <strong style="color:#e8e8f0">detailed instant feedback</strong> — 100% free, no internet needed for feedback.
      </p>
      <p style="color:#6b7280;font-size:.85rem;margin:0">
        🎙️ Microphone recommended &nbsp;|&nbsp; ⌨️ Typing also works
      </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀  Start Interview", key="start_btn"):
        st.session_state.page       = "interview"
        st.session_state.q_index    = 0
        st.session_state.answers    = []
        st.session_state.stage      = "ask"
        st.session_state.text_mode  = False
        st.session_state.mic_active = False
        st.session_state.error_msg  = ""
        st.session_state.feedback   = None
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "interview":
    qi = st.session_state.q_index

    # ── All 5 questions answered → show results NOW (same render pass) ──
    if qi >= len(QUESTIONS):
        # Calculate feedback right here, show results immediately
        if st.session_state.feedback is None:
            if len(st.session_state.answers) == 0:
                st.error("No answers recorded. Please restart.")
                if st.button("Restart"):
                    st.session_state.page = "start"
                    st.rerun()
            else:
                st.session_state.feedback = make_feedback(st.session_state.answers)
        
        fb = st.session_state.feedback
        score     = fb["overall_score"]
        rec       = fb["recommendation"]
        rec_color = {"Hire":"#86efac","Consider":"#fcd34d","Pass":"#fca5a5"}.get(rec,"#a5b4fc")

        st.markdown(f"""
        <div class="fb-header">
          <h2>Interview Complete 🎯</h2>
          <p style="color:#6b7280;font-size:.9rem">{fb['overall_summary']}</p>
          <div class="score-ring">
            <span class="score-num">{score}</span>
            <span class="score-lbl">/ 10</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rec-box">
          <strong style="color:{rec_color}">Verdict: {rec}</strong>
          <p>{fb['recommendation_reason']}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-title">✅ Strengths</div>', unsafe_allow_html=True)
        st.markdown('<div class="chip-row">'+"".join(f'<span class="chip-g">✓ {s}</span>' for s in fb["strengths"])+'</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-title">🔧 Areas to Improve</div>', unsafe_allow_html=True)
        st.markdown('<div class="chip-row">'+"".join(f'<span class="chip-a">→ {i}</span>' for i in fb["improvements"])+'</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-title">📋 Question-by-Question Review</div>', unsafe_allow_html=True)
        for i, item in enumerate(fb["question_feedback"]):
            st.markdown(f"""
            <div class="qfb-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:.5rem">
                <span style="font-weight:500;color:#e8e8f0;font-size:.92rem">Q{i+1}: {item['question']}</span>
                {badge(item['rating'])}
              </div>
              <div class="ans-label">Your Answer</div>
              <div style="color:#9ca3af;font-size:.85rem;margin-bottom:.5rem;font-style:italic">"{item['answer']}"</div>
              <div style="color:#c4c4d4;font-size:.85rem">{item['feedback']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄  Start New Interview", key="restart_btn"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()

    else:
        # ── Active question ──
        q_obj = QUESTIONS[qi]
        st.markdown(prog(qi+1, len(QUESTIONS)), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="q-card">
          <div class="q-num">Question {qi+1} of {len(QUESTIONS)}</div>
          <p class="q-text">{q_obj['q']}</p>
          <p class="q-hint">💡 {q_obj['hint']}</p>
        </div>""", unsafe_allow_html=True)

        # ── ASK: speak then move to listening ──
        if st.session_state.stage == "ask":
            speak(q_obj['q'])
            st.session_state.stage = "listening"
            st.rerun()

        # ── LISTENING ──
        elif st.session_state.stage == "listening":

            if not st.session_state.text_mode:
                if st.session_state.mic_active:
                    # Recording in progress
                    st.markdown('<div class="pill pill-red"><div class="dot"></div>🎤 Recording… speak now, then stop talking</div>', unsafe_allow_html=True)
                    st.info("The page will update automatically when you finish speaking.")

                    if _MIC["done"]:
                        st.session_state.mic_active = False
                        if _MIC["result"]:
                            st.session_state.answers.append(_MIC["result"])
                            st.session_state.stage     = "done_q"
                            st.session_state.error_msg = ""
                        else:
                            err = _MIC["error"]
                            st.session_state.error_msg = {
                                "timeout": "No speech detected — try again or type.",
                                "unclear": "Could not understand — speak clearly or type.",
                                "network": "No internet for speech — please type your answer.",
                                "mic":     "Microphone not found — please type your answer.",
                            }.get(err, f"Error: {err}. Please type your answer.")
                            if err in ("network", "mic"):
                                st.session_state.text_mode = True
                        st.rerun()
                    else:
                        time.sleep(1)
                        st.rerun()

                else:
                    # Idle — show buttons
                    if st.session_state.error_msg:
                        st.markdown(f'<div class="pill pill-yellow">⚠️ {st.session_state.error_msg}</div>', unsafe_allow_html=True)

                    c1, c2 = st.columns([2, 1])
                    with c1:
                        if st.button("🎤  Record My Answer", key=f"rec_{qi}"):
                            st.session_state.mic_active = True
                            st.session_state.error_msg  = ""
                            start_mic()
                            st.rerun()
                    with c2:
                        if st.button("⌨️  Type Instead", key=f"typ_{qi}"):
                            st.session_state.text_mode  = True
                            st.session_state.error_msg  = ""
                            st.rerun()

            else:
                # TEXT MODE
                st.markdown('<div class="pill pill-yellow"><div class="dot"></div>Type your answer below</div>', unsafe_allow_html=True)
                typed = st.text_area("Your Answer", height=130, placeholder="Type here…", key=f"txt_{qi}")
                c1, c2 = st.columns([2, 1])
                with c1:
                    if st.button("✅  Submit Answer", key=f"sub_{qi}"):
                        a = typed.strip()
                        if not a:
                            st.warning("Please type something first.")
                        else:
                            st.session_state.answers.append(a)
                            st.session_state.stage     = "done_q"
                            st.session_state.error_msg = ""
                            st.session_state.text_mode = False
                            st.rerun()
                with c2:
                    if st.button("🎤  Try Mic Again", key=f"mic2_{qi}"):
                        st.session_state.text_mode  = False
                        st.session_state.error_msg  = ""
                        st.rerun()

        # ── DONE_Q: show answer, advance ──
        elif st.session_state.stage == "done_q":
            ans = st.session_state.answers[-1]
            st.markdown(f'<div class="ans-label">Your Answer</div><div class="ans-box">{ans}</div>', unsafe_allow_html=True)
            st.markdown('<div class="pill pill-green">✓ Recorded — moving to next question…</div>', unsafe_allow_html=True)
            time.sleep(1.5)
            st.session_state.q_index  += 1
            st.session_state.stage     = "ask"
            st.session_state.text_mode = False
            st.session_state.error_msg = ""
            st.rerun()
