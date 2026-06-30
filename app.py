"""
EdgeCase Recommendation Learning — Interactive Demo (with Knowledge Graph Animation)
"""
import json
import base64
import streamlit as st
import time
from pathlib import Path

st.set_page_config(
    page_title="EdgeCase Recommendation Learning",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu {visibility:hidden;} footer {visibility:hidden;}
    .block-container { padding-top: 1rem !important; padding-bottom: 0 !important; }

    /* ── Keyframes ── */
    @keyframes fadeSlideUp {
        from { opacity:0; transform:translateY(20px); }
        to   { opacity:1; transform:translateY(0);    }
    }
    @keyframes slideInLeft {
        from { opacity:0; transform:translateX(-24px); }
        to   { opacity:1; transform:translateX(0);     }
    }
    @keyframes slideInRight {
        from { opacity:0; transform:translateX(24px); }
        to   { opacity:1; transform:translateX(0);    }
    }
    @keyframes heroPulse {
        0%,100% { background-position:0% 50%; }
        50%      { background-position:100% 50%; }
    }
    @keyframes shimmer {
        0%   { transform:translateX(-100%); }
        100% { transform:translateX(200%); }
    }
    @keyframes scorePop {
        0%   { opacity:0; transform:scale(0.4); }
        65%  { transform:scale(1.18); }
        100% { opacity:1; transform:scale(1); }
    }
    @keyframes wiggle {
        0%,100% { transform:rotate(0deg)  scale(1);   }
        20%      { transform:rotate(-18deg) scale(1.25); }
        40%      { transform:rotate(14deg)  scale(1.2);  }
        60%      { transform:rotate(-10deg) scale(1.15); }
        80%      { transform:rotate(6deg)   scale(1.1);  }
    }
    @keyframes shakeIn {
        0%   { opacity:0; transform:translateX(-12px); }
        25%  { transform:translateX(8px);  }
        45%  { transform:translateX(-6px); }
        65%  { transform:translateX(4px);  }
        80%  { transform:translateX(-2px); }
        100% { opacity:1; transform:translateX(0); }
    }
    @keyframes springIn {
        0%   { opacity:0; transform:scale(0.82) translateY(10px); }
        60%  { transform:scale(1.04) translateY(-2px); }
        100% { opacity:1; transform:scale(1) translateY(0); }
    }
    @keyframes borderPulse {
        0%,100% { box-shadow:0 0 0 0   rgba(79,70,229,0.45); }
        50%      { box-shadow:0 0 0 8px rgba(79,70,229,0);    }
    }
    @keyframes badgeBounce {
        0%,100% { transform:translateY(0);   }
        40%      { transform:translateY(-4px); }
        70%      { transform:translateY(2px);  }
    }
    @keyframes drawLine {
        from { transform:scaleX(0); }
        to   { transform:scaleX(1); }
    }
    @keyframes fadeIn {
        from { opacity:0; }
        to   { opacity:1; }
    }
    @keyframes loadPulse {
        0%,100% { opacity: 1; }
        50%      { opacity: 0.55; }
    }

    /* ── Hero ── */
    .hero {
        position:relative; overflow:hidden;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #4f46e5 100%);
        background-size:200% 200%;
        animation: heroPulse 6s ease infinite;
        padding:30px 40px 28px 40px;
        color:white; text-align:center;
        border-radius:0 0 18px 18px; margin-bottom:22px;
    }
    .hero::after {
        content:''; position:absolute; top:0; left:0; width:40%; height:100%;
        background:linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
        animation: shimmer 3.5s ease 0.8s infinite;
        pointer-events:none;
    }
    .hero h1 { font-size:30px; font-weight:800; margin:0; color:white !important;
               animation:fadeSlideUp 0.6s ease both; }
    .hero p  { font-size:14px; margin:8px 0 0 0; color:rgba(255,255,255,0.9) !important;
               animation:fadeSlideUp 0.6s ease 0.18s both; }

    /* ── Section headings ── */
    .sec-h {
        position:relative;
        font-size:14px; font-weight:800; color:#4f46e5 !important;
        text-transform:uppercase; letter-spacing:1px;
        padding-bottom:6px; margin:18px 0 12px 0;
        animation:fadeIn 0.4s ease both;
    }
    .sec-h::after {
        content:''; position:absolute; bottom:0; left:0; right:0; height:2px;
        background:#4f46e5;
        transform-origin:left;
        animation:drawLine 0.45s ease 0.15s both;
    }

    /* ── Quiz question cards ── */
    .quiz-card {
        background:#f9fafb; border:1px solid #e5e7eb;
        border-left: 4px solid #4f46e5;
        border-radius:10px; padding:14px 18px; margin:0 0 6px 0;
        animation:fadeSlideUp 0.45s ease both;
    }
    .quiz-card .qc-num {
        display:inline-block;
        background:#4f46e5; color:white;
        font-size:11px; font-weight:800;
        border-radius:50%; width:22px; height:22px;
        text-align:center; line-height:22px;
        margin-right:8px;
    }
    .quiz-card .qc-text { font-size:14px; font-weight:600; color:#111827 !important; line-height:1.5; }
    .quiz-card .qc-lo   { font-size:11px; color:#9ca3af !important; font-style:italic; margin-top:6px; }

    /* ── Loading overlay ── */
    @keyframes shimmerBar {
        0%   { background-position: -400px 0; }
        100% { background-position:  400px 0; }
    }
    @keyframes overlayIn {
        from { opacity:0; }
        to   { opacity:1; }
    }
    @keyframes cardPop {
        from { opacity:0; transform:scale(0.92) translateY(16px); }
        to   { opacity:1; transform:scale(1)    translateY(0);    }
    }

    /* ── Result question cards (correct / wrong) ── */
    .rq {
        border-radius:10px; padding:12px 14px; margin:6px 0;
        transition:transform 0.2s ease, box-shadow 0.2s ease;
    }
    .rq-correct { animation:springIn 0.45s cubic-bezier(0.34,1.56,0.64,1) both; }
    .rq-wrong   { animation:shakeIn  0.5s ease both; }
    .rq:hover   { transform:translateX(5px); box-shadow:0 3px 12px rgba(0,0,0,.08); }
    .rq .rq-top  { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
    .rq .rq-lo   { font-size:12px; font-weight:700; color:#111827 !important; }
    .rq .rq-text { font-size:13px; color:#1f2937 !important; line-height:1.4; }
    .rq .rq-badge {
        font-size:12px; font-weight:700;
        display:inline-block;
        animation:badgeBounce 0.5s ease 0.4s both;
    }
    .rq .rq-picked { font-size:11px; color:#6b7280 !important; margin-top:4px; font-style:italic; }

    /* ── Score card ── */
    .score-card {
        background:white; border-radius:16px; padding:28px 24px;
        text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.08);
        margin-bottom:20px;
        animation:springIn 0.55s cubic-bezier(0.34,1.56,0.64,1) both;
    }
    .score-card .sc-num {
        font-size:52px; font-weight:900; line-height:1;
        animation:scorePop 0.55s cubic-bezier(0.34,1.56,0.64,1) 0.2s both;
        display:inline-block;
    }
    .score-card .sc-label { font-size:14px; font-weight:600; margin-top:6px; }

    /* ── Recommendation panel ── */
    .rec-panel {
        background:white;
        border:2px solid #4f46e5;
        border-radius:14px; padding:16px 20px;
        animation:slideInRight 0.5s ease 0.05s both, borderPulse 1.8s ease 0.8s 3;
    }
    .rec-panel .rp-title { font-size:20px; font-weight:800; color:#4f46e5 !important; margin:0 0 14px 0; }
    .rec-panel .rp-sub   { font-size:13px; color:#374151 !important; margin-bottom:16px; }

    /* ── Practice question cards ── */
    .pq {
        border-radius:12px; padding:16px 18px; margin:10px 0;
        border:1.5px solid #fbbf24 !important; background:#fffbeb !important;
        transition:all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
        animation:springIn 0.45s cubic-bezier(0.34,1.56,0.64,1) both;
        cursor: pointer !important;
    }
    .pq:hover { 
        transform:translateY(-5px) scale(1.02) !important; 
        box-shadow:0 14px 32px rgba(217,119,6,0.3) !important; 
        border-color:#d97706 !important; 
        background-color:#fef3c7 !important;
    }
    .pq .pq-tag   { font-size:10px; font-weight:700; text-transform:uppercase;
                    letter-spacing:.6px; color:#92400e !important;
                    background:#fde68a; border-radius:4px; padding:2px 7px;
                    display:inline-block; margin-bottom:8px; }
    .pq .pq-meta  { font-size:11px; color:#6b7280 !important; font-weight:600;
                    text-transform:uppercase; letter-spacing:.4px; margin-bottom:4px; }
    .pq .pq-lo    { font-size:14px; font-weight:800; color:#92400e !important; margin-bottom:8px; }
    .pq .pq-text  { font-size:14px; color:#111827 !important; line-height:1.5; font-weight:600; margin-bottom:10px; }
    .pq .pq-opts  { list-style:none; padding:0; margin:0; }
    .pq .pq-opts li {
        font-size:12.5px; color:#374151 !important; padding:6px 10px; margin:4px 0;
        background:#fff; border:1px solid #e5e7eb; border-radius:7px; line-height:1.4;
        transition:border-color 0.15s ease, background 0.15s ease;
    }
    .pq .pq-opts li:hover { border-color:#d97706; background:#fef9ee; }
    .pq .pq-opts li span.opt-lbl {
        font-weight:700; color:#d97706 !important; margin-right:7px; }
    .pq .pq-lo-desc { font-size:11px; color:#9ca3af !important; font-style:italic; margin-top:8px; }

    /* ── Reasoning box ── */
    .why-box {
        background:#f5f3ff; border-radius:10px; border:1px solid #c4b5fd;
        padding:14px 16px; margin-top:14px;
        animation:fadeSlideUp 0.45s ease 0.25s both;
        transition:box-shadow 0.2s ease, transform 0.2s ease;
    }
    .why-box:hover { box-shadow:0 5px 18px rgba(139,92,246,.18); transform:translateY(-2px); }
    .why-box .wb-title { font-size:13px; font-weight:800; color:#4338ca !important; margin-bottom:8px; }
    .why-box li { font-size:13px; color:#1f2937 !important; margin:4px 0; line-height:1.5;
                  animation:slideInLeft 0.35s ease both; }
    .why-box li:nth-child(1) { animation-delay:0.3s; }
    .why-box li:nth-child(2) { animation-delay:0.42s; }
    .why-box li:nth-child(3) { animation-delay:0.54s; }
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
# Questions from demo_questions.json — all Ch10, matching the demo_graph.html
QUESTIONS = {
    "q10_genome_structure": {
        "lo": "ch10_sec1_obj1", "ch": 10, "num": 1,
        "text": "Which statement accurately describes the layout of a prokaryotic genome compared to a eukaryotic genome?",
        "options": [
            "Prokaryotes store double-stranded DNA in a single circular chromosome, while eukaryotes have multiple linear chromosomes.",
            "Prokaryotes use linear chromosomal structures bound tightly to histones inside a nucleus.",
            "Eukaryotic genomes are composed strictly of single-stranded RNA packets wrapped in structural plasmids.",
            "Both structural classes organize genomes identically into double-membrane nuclear envelopes.",
        ],
        "correct": "Prokaryotes store double-stranded DNA in a single circular chromosome, while eukaryotes have multiple linear chromosomes.",
    },
    "q10_chromosomes_genes": {
        "lo": "ch10_sec1_obj2", "ch": 10, "num": 2,
        "text": "What is the specific functional relationship between chromosomes, genes, and inherited traits?",
        "options": [
            "Chromosomes are cellular proteins that modify organism traits directly without nucleotide guidance.",
            "Genes are specific linear nucleotide sequences located on chromosomes that code for specific proteins, defining specific traits.",
            "Traits serve as the micro-structural building sequences that duplicate to assemble identical sister chromatids.",
            "Genes and chromosomes are independent entities that only align during structural mutations.",
        ],
        "correct": "Genes are specific linear nucleotide sequences located on chromosomes that code for specific proteins, defining specific traits.",
    },
    "q10_compaction": {
        "lo": "ch10_sec1_obj3", "ch": 10, "num": 3,
        "text": "Which protein complex provides the foundational structural core around which eukaryotic genomic DNA wraps during initial compaction?",
        "options": ["Actin fibers", "Histone octamers", "Centromere fibers", "DNA polymerase complexes"],
        "correct": "Histone octamers",
    },
    "q10_interphase_stage": {
        "lo": "ch10_sec2_obj1", "ch": 10, "num": 4,
        "text": "During which functional stage of interphase does semi-conservative replication of genomic DNA take place?",
        "options": ["G1 Phase", "S Phase", "G2 Phase", "G0 Phase"],
        "correct": "S Phase",
    },
    "q10_metaphase": {
        "lo": "ch10_sec2_obj2", "ch": 10, "num": 5,
        "text": "What primary event occurs regarding the layout of chromosomes during the Metaphase stage of mitotic karyokinesis?",
        "options": [
            "Chromosomes undergo complete nuclear de-condensation at opposite terminal cell poles.",
            "Sister chromatids separate dynamically and travel toward independent centrosomes.",
            "Chromosomes line up linearly along the cell's equatorial plate, attached to spindle fibers.",
            "Nuclear envelopes actively reform around clustered chromatid structures.",
        ],
        "correct": "Chromosomes line up linearly along the cell's equatorial plate, attached to spindle fibers.",
    },
}

# LO descriptions match demo_graph.html node labels exactly
LO_DESC = {
    "ch10_sec1_obj1": "Describe the structure of prokaryotic and eukaryotic genomes",
    "ch10_sec1_obj2": "Distinguish between chromosomes, genes, and traits",
    "ch10_sec1_obj3": "Describe the mechanisms of chromosome compaction",
    "ch10_sec2_obj1": "Describe the three stages of interphase",
    "ch10_sec2_obj2": "Discuss the behavior of chromosomes during karyokinesis/mitosis",
}

# Prereq pairs verified in dependency_graph.jsonl and demo_graph.html edges
# ch10_sec2_obj2's direct graph prereqs are other quiz LOs → use transitive ch3/ch4 prereqs
PREREQ_LO_MAP = {
    "ch10_sec1_obj1": ["ch4_sec3_obj1", "ch4_sec3_obj2", "ch3_sec5_obj2", "ch3_sec5_obj1"],
    "ch10_sec1_obj2": ["ch4_sec3_obj4", "ch4_sec3_obj1", "ch3_sec5_obj2", "ch3_sec5_obj1"],
    "ch10_sec1_obj3": ["ch4_sec3_obj4", "ch4_sec3_obj1", "ch3_sec5_obj2", "ch3_sec5_obj1"],
    "ch10_sec2_obj1": ["ch10_sec1_obj1", "ch6_sec4_obj2", "ch6_sec4_obj1"],
    "ch10_sec2_obj2": ["ch10_sec1_obj1", "ch10_sec1_obj3", "ch10_sec1_obj2"],
}

# Prereq questions from ch3, ch4, ch6 — verified against textbook_questions_with_answers.json
PREREQ_QUESTIONS = {
    "ch4_sec3_obj1": {
        "id":      "bio-ch04-rq-008",
        "lo_desc": "Describe the structure and characteristics of prokaryotic and eukaryotic cells",
        "ch": 4, "sec": "4.3",
        "text": "Which of the following organisms is a prokaryote?",
        "options": ["Amoeba", "Influenza A virus", "Charophyte algae", "E. coli"],
    },
    "ch4_sec3_obj4": {
        "id":      "bio-ch04-rq-013",
        "lo_desc": "Summarize the functions of the major cell organelles",
        "ch": 4, "sec": "4.3",
        "text": "Tay-Sachs disease results in destruction of neurons due to a buildup of gangliosides. Which organelle is most likely affected?",
        "options": ["Lysosome", "Endoplasmic reticulum", "Peroxisome", "Mitochondria"],
    },
    "ch3_sec5_obj2": {
        "id":      "bio-ch03-rq-020",
        "lo_desc": "Explain the structure of DNA and its role in encoding the genome",
        "ch": 3, "sec": "3.5",
        "text": "How does the double helix structure of DNA support its role in encoding the genome?",
        "options": [
            "The sugar-phosphate backbone provides a template for DNA replication.",
            "tRNA pairing with the template strand creates proteins directly.",
            "Complementary base pairing creates a very stable structure.",
            "Complementary base pairing allows for easy editing of base sequences.",
        ],
    },
    "ch3_sec5_obj1": {
        "id":      "bio-ch03-rq-019",
        "lo_desc": "Describe the structure of nucleic acids and define the two types",
        "ch": 3, "sec": "3.5",
        "text": "The building blocks of nucleic acids are ________.",
        "options": ["Sugars", "Nitrogenous bases", "Peptides", "Nucleotides"],
    },
    "ch6_sec4_obj1": {
        "id":      "bio-ch06-rq-004",
        "lo_desc": "Explain ATP's role as the cellular energy currency",
        "ch": 6, "sec": "6.4",
        "text": "Energy is stored long-term in the bonds of _____ and used short-term to perform work from a(n) _____.",
        "options": [
            "ATP : glucose",
            "An anabolic molecule : catabolic molecule",
            "Glucose : ATP",
            "A catabolic molecule : anabolic molecule",
        ],
    },
    "ch6_sec4_obj2": {
        "id":      "bio-ch06-rq-011",
        "lo_desc": "Describe how energy is released through ATP hydrolysis",
        "ch": 6, "sec": "6.4",
        "text": "The energy released by the hydrolysis of ATP is ____.",
        "options": [
            "Primarily stored between the alpha and beta phosphates.",
            "Equal to −57 kcal/mol.",
            "Harnessed as heat energy by the cell to perform work.",
            "Providing energy to coupled reactions.",
        ],
    },
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_recommendation(wrong_los: set):
    """Build practice recommendations dynamically using full graph traversal.
    Finds ALL recursive prerequisites that have practice questions.
    """
    prereq_to_wrong = {}
    
    for lo in wrong_los:
        # Find all recursive prerequisites limited to 2 levels deep
        visited = set()
        queue = [(lo, 0)]
        while queue:
            curr, depth = queue.pop(0)
            if depth >= 2:
                continue
            for pre in PREREQ_LO_MAP.get(curr, []):
                if pre not in visited:
                    visited.add(pre)
                    queue.append((pre, depth + 1))
                    
        # Add only valid practice questions
        for pre in visited:
            if pre in PREREQ_QUESTIONS:
                if pre not in prereq_to_wrong:
                    prereq_to_wrong[pre] = []
                prereq_to_wrong[pre].append(lo)

    if not prereq_to_wrong:
        return None

    # Sort the practice questions
    sorted_prereqs = sorted(
        prereq_to_wrong.keys(),
        key=lambda lo: (
            PREREQ_QUESTIONS.get(lo, {}).get("ch", 999),
            PREREQ_QUESTIONS.get(lo, {}).get("sec", "999"),
            lo
        )
    )

    practice = []
    for pre_lo in sorted_prereqs:
        if pre_lo not in PREREQ_QUESTIONS:
            continue
        practice.append({
            "prereq_lo":  pre_lo,
            "needed_for": prereq_to_wrong[pre_lo],
            "q":          PREREQ_QUESTIONS[pre_lo],
            "reason":     prereq_to_wrong[pre_lo][0] # ADDED: Prevents Dashboard KeyError!
        })

    # Dummy reasons to prevent unpacking errors later
    reasons = ["Dynamically generated from full BFS graph traversal."]
    return {"practice": practice, "reasons": reasons}


# ── Session State ──────────────────────────────────────────────────────────────
for key, default in [("phase", "quiz"), ("answers", {}), ("quiz_error", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("<div id='ec-top-anchor'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="hero">
    <h1>EdgeCase Recommendation Learning</h1>
    <p>AI-powered system that identifies learning gaps and recommends exactly what to practice next</p>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
home_tab, graph_tab, dashboard_tab = st.tabs(["🏠  Home", "📊  Knowledge Graph", "👤  Student Dashboard"])

# ══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE GRAPH TAB
# ══════════════════════════════════════════════════════════════════════════════
with graph_tab:
    st.markdown("""
    <div style="padding: 10px 0 16px 0;">
        <span style="font-size:15px; color:#6b7280;">Arrows show prerequisites. A concept at the top must be understood before the ones below it.</span>
    </div>
    """, unsafe_allow_html=True)
    graph_path = Path(__file__).resolve().parent / "demo_graph.html"
    if graph_path.exists():
        graph_html = graph_path.read_text(encoding="utf-8")
        st.components.v1.html(graph_html, height=720, scrolling=False)
    else:

        st.components.v1.html("""
            <script>
                function forceScroll() {
                    var doc = window.parent.document;
                    var containers = [
                        doc.querySelector("[data-testid=\"stAppViewContainer\"]"),
                        doc.querySelector(".main"),
                        doc.documentElement,
                        window.parent
                    ];
                    containers.forEach(function(c) {
                        if (c && c.scrollTo) { c.scrollTo({top: 0, behavior: "instant"}); }
                    });
                }
                forceScroll();
                setTimeout(forceScroll, 100);
                setTimeout(forceScroll, 300);
                setTimeout(forceScroll, 600);
            </script>
        """, height=0)
        st.error(f"demo_graph.html not found at: {graph_path}")

# ══════════════════════════════════════════════════════════════════════════════
# HOME TAB
# ══════════════════════════════════════════════════════════════════════════════
with home_tab:

    # ────────────────────────────────────────────────────────────────────────
    # PHASE 1 — QUIZ
    # ────────────────────────────────────────────────────────────────────────
    if st.session_state.phase == "quiz":

        st.markdown('<div class="sec-h">Biology 2e Questions</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="color:#6b7280; font-size:13px; margin-bottom:18px;">'
            'Answer all 5 questions, then click <strong>Submit Quiz</strong> to see your personalized practice plan.'
            '</p>',
            unsafe_allow_html=True,
        )

        if st.session_state.quiz_error:
            st.error(st.session_state.quiz_error)
            st.session_state.quiz_error = ""

        opt_labels = ["A", "B", "C", "D"]
        for qid, q in QUESTIONS.items():
            delay = (q["num"] - 1) * 0.1
            st.markdown(f"""
            <div class="quiz-card" style="animation-delay:{delay}s;">
                <span class="qc-num">{q['num']}</span>
                <span class="qc-text">{q['text']}</span>
                <div class="qc-lo">LO: {LO_DESC[q['lo']]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.radio(
                label="",
                options=q["options"],
                key=f"ans_{qid}",
                index=None,
                label_visibility="collapsed",
                horizontal=False,
            )
            st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        if st.button("Submit Quiz →", type="primary", use_container_width=True):
            answers = {qid: st.session_state.get(f"ans_{qid}") for qid in QUESTIONS}
            unanswered = [str(q["num"]) for qid, q in QUESTIONS.items() if answers[qid] is None]
            if unanswered:
                st.session_state.quiz_error = (
                    f"Please answer Q{', Q'.join(unanswered)} before submitting."
                )
                st.rerun()
            else:
                st.session_state.answers = answers
                st.session_state.phase = "loading"
                st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    # PHASE 2 — LOADING (full-screen overlay with graph animation on step 3)
    # ────────────────────────────────────────────────────────────────────────
    elif st.session_state.phase == "loading":

        slot = st.empty()

        STEPS = [
            ("📊", "Evaluating quiz responses"),
            ("🔍", "Identifying knowledge gaps"),
            ("🕸️", "Traversing prerequisite knowledge graph"),
            ("✨", "Generating personalized practice questions"),
        ]

        # Short display labels — quiz LOs match demo_graph.html node labels exactly
        LO_SHORT = {
            # Quiz LOs (ch10) — same as demo_graph.html
            "ch10_sec1_obj1": "Prokaryotic/Eukaryotic\nGenome [Ch10.1]",
            "ch10_sec1_obj2": "Chromosomes,\nGenes & Traits [Ch10.1]",
            "ch10_sec1_obj3": "Chromosome\nCompaction [Ch10.1]",
            "ch10_sec2_obj1": "Interphase\nStages [Ch10.2]",
            "ch10_sec2_obj2": "Mitosis\nChromosomes [Ch10.2]",
            # Prereq LOs (ch3, ch4, ch6) — same as demo_graph.html prereq nodes
            "ch4_sec3_obj1": "Eukaryotic Cell\nStructure [Ch4.3]",
            "ch4_sec3_obj4": "Cell Organelle\nFunctions [Ch4.3]",
            "ch3_sec5_obj2": "DNA Structure\n& Role [Ch3.5]",
            "ch3_sec5_obj1": "Nucleic Acid\nStructure [Ch3.5]",
            "ch6_sec4_obj1": "ATP Energy\nCurrency [Ch6.4]",
            "ch6_sec4_obj2": "ATP Hydrolysis\n[Ch6.4]",
        }

        # ── Pre-compute graph data from session answers ──────────────────────
        answers = st.session_state.answers
        correct_lo_set = {QUESTIONS[qid]["lo"] for qid, ans in answers.items() if ans == QUESTIONS[qid]["correct"]}
        wrong_lo_set  = {QUESTIONS[qid]["lo"] for qid, ans in answers.items()
                         if ans != QUESTIONS[qid]["correct"]}
        lo_to_qnum    = {q["lo"]: f"Q{q['num']}" for q in QUESTIONS.values()}

        graph_nodes, graph_edges, edge_id_list = [], [], []
        added_ids = set()

        for lo in sorted(wrong_lo_set):
            label = LO_SHORT.get(lo, lo) + f"\n({lo_to_qnum.get(lo,'')})"
            graph_nodes.append({"id": lo, "label": label, "group": "wrong", "level": 1})
            added_ids.add(lo)

        for lo in sorted(wrong_lo_set):
            for pre in PREREQ_LO_MAP.get(lo, []):
                if pre not in added_ids:
                    graph_nodes.append({"id": pre, "label": LO_SHORT.get(pre, pre),
                                        "group": "prereq", "level": 0})
                    added_ids.add(pre)
                eid = f"e_{pre}_{lo}"
                graph_edges.append({"id": eid, "from": pre, "to": lo})
                edge_id_list.append(eid)

        # If no wrong answers, show all correct nodes
        if not graph_nodes:
            for lo in sorted({q["lo"] for q in QUESTIONS.values()}):
                graph_nodes.append({"id": lo, "label": LO_SHORT.get(lo, lo),
                                    "group": "correct", "level": 1})

        nodes_js  = json.dumps(graph_nodes)
        edges_js  = json.dumps(graph_edges)
        eids_js   = json.dumps(edge_id_list)

        # ── Helpers ───────────────────────────────────────────────────────────
        BACKDROP = (
            'position:fixed;inset:0;background:rgba(10,10,20,0.85);'
            'backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);'
            'z-index:99999;display:flex;align-items:center;justify-content:center;'
            'transition:opacity 0.3s ease;'
        )

        def _ensure_overlay_js() -> str:
            """JS snippet: ensure dark backdrop exists in parent document."""
            return f"""
            if (!parent.document.getElementById('ec-kf')) {{
                var _s = parent.document.createElement('style');
                _s.id = 'ec-kf';
                _s.textContent = '@keyframes ecShimmer{{0%{{background-position:-300px 0}}100%{{background-position:300px 0}}}}';
                parent.document.head.appendChild(_s);
            }}
            var ov = parent.document.getElementById('ec-overlay');
            if (!ov) {{
                ov = parent.document.createElement('div');
                ov.id = 'ec-overlay';
                ov.style.cssText = '{BACKDROP}';
                parent.document.body.appendChild(ov);
            }}
            ov.style.opacity = '1';
            """


        def make_loader_html() -> str:
            rows = ""
            for i, (icon, label) in enumerate(STEPS):
                bg, sym, lc, fw, op = "#e5e7eb", str(i + 1), "#9ca3af", "400", "0.45"
                rows += (
                    f'<div id="step-row-{i}" style="display:flex;align-items:center;gap:14px;padding:10px 0;'
                    f'border-bottom:1px solid #f3f4f6;opacity:{op};transition:all 0.3s;">'
                    f'<div id="step-icon-{i}" style="width:34px;height:34px;border-radius:50%;background:{bg};'
                    f'color:white;flex-shrink:0;display:flex;align-items:center;'
                    f'justify-content:center;font-size:14px;font-weight:700;transition:all 0.3s;">{sym}</div>'
                    f'<span id="step-label-{i}" style="font-size:14px;color:{lc};font-weight:{fw};transition:all 0.3s;">{label}</span>'
                    f'</div>'
                )
            return (
                f'<div style="background:white;border-radius:24px;padding:44px 50px 38px;'
                f'width:480px;max-width:90vw;box-shadow:0 40px 100px rgba(0,0,0,0.55);'
                f'font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;">'
                f'<div style="text-align:center;margin-bottom:28px;">'
                f'<p style="font-size:12px;font-weight:800;letter-spacing:2.5px;color:#6366f1;'
                f'text-transform:uppercase;margin:0 0 10px 0;">EdgeCase Recommendation Learning</p>'
                f'<h2 style="font-size:22px;font-weight:900;margin:0 0 6px 0;'
                f'letter-spacing:-0.3px;">Building your practice plan</h2>'
                f'<p style="font-size:13px;color:#6b7280;margin:0;">Analyzing answers against the knowledge graph...</p>'
                f'</div>{rows}'
                f'<div style="margin-top:24px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
                f'<span style="font-size:11px;color:#6b7280;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;">Progress</span>'
                f'<span id="progress-text" style="font-size:16px;color:#4f46e5;font-weight:900;">0%</span>'
                f'</div>'
                f'<div style="height:13px;background:#e5e7eb;border-radius:7px;overflow:hidden;">'
                f'<div id="progress-bar" style="height:100%;width:0%;border-radius:7px;'
                f'background:linear-gradient(90deg,#6366f1,#a78bfa 50%,#4f46e5);'
                f'background-size:300% 100%;animation:ecShimmer 1.8s linear infinite;'
                f'transition:width 0.1s linear;"></div></div>'
                f'<p id="step-counter" style="text-align:center;font-size:11px;color:#9ca3af;margin:8px 0 0 0;">'
                f'Step 1 of {len(STEPS)}</p></div></div>'
            )

        def inject_animated_loader():
            safe = make_loader_html().replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            script = f"""
            <script>
            (function() {{
                {_ensure_overlay_js()}
                ov.innerHTML = `{safe}`;
                
                var bar = ov.querySelector('#progress-bar');
                var text = ov.querySelector('#progress-text');
                var counter = ov.querySelector('#step-counter');
                
                var startTime = Date.now();
                var duration = 4500;
                
                function updateStep(idx, state) {{
                    var row = ov.querySelector('#step-row-' + idx);
                    var icon = ov.querySelector('#step-icon-' + idx);
                    var label = ov.querySelector('#step-label-' + idx);
                    if(!row) return;
                    if (state === 'done') {{
                        row.style.opacity = '1.0';
                        icon.style.background = '#22c55e';
                        icon.innerHTML = '&#10003;';
                        label.style.color = '#374151';
                        label.style.fontWeight = '500';
                        label.innerText = label.innerText.replace('...', '');
                    }} else if (state === 'active') {{
                        row.style.opacity = '1.0';
                        icon.style.background = '#4f46e5';
                        var icons = ['📊', '🔍', '🎯'];
                        icon.innerHTML = icons[idx];
                        label.style.color = '#1e1b4b';
                        label.style.fontWeight = '700';
                        if(!label.innerText.endsWith('...')) label.innerText += '...';
                        counter.innerText = 'Step ' + (idx + 1) + ' of 3';
                    }}
                }}
                
                function tick() {{
                    var elapsed = Date.now() - startTime;
                    var p = Math.min(1.0, elapsed / duration);
                    var pct = Math.floor(p * 100);
                    
                    if(bar) bar.style.width = pct + '%';
                    if(text) text.innerText = pct + '%';
                    
                    if(pct < 33) {{
                        updateStep(0, 'active');
                    }} else if(pct < 66) {{
                        updateStep(0, 'done');
                        updateStep(1, 'active');
                    }} else if(pct <= 100) {{
                        updateStep(1, 'done');
                        updateStep(2, 'active');
                    }}
                    
                    if(p < 1.0) {{
                        requestAnimationFrame(tick);
                    }}
                }}
                requestAnimationFrame(tick);
            }})();
            </script>
            """
            with slot:
                st.components.v1.html(script, height=0, scrolling=False)


        def inject_graph_step() -> None:
            """Step 3: replace the card with the full live vis.js knowledge graph via overlay iframe."""
            graph_path = Path(__file__).resolve().parent / "demo_graph_anim.html"
            full_html = graph_path.read_text(encoding="utf-8")
            
            ui_overlay = """
            <div style="flex-shrink:0; padding-top:24px; padding-bottom:16px; margin-top:12px; border-bottom:1px solid rgba(0,0,0,0.05); margin-bottom:16px; display:flex; justify-content:space-between; align-items:flex-end;">
                <div>
                    <p style="font-size:11px;font-weight:800;letter-spacing:2px;color:#6366f1;text-transform:uppercase;margin:0 0 4px 0;">EdgeCase Recommendation Learning</p>
                    <h2 style="font-size:18px;font-weight:900;margin:0 0 4px 0;color:#000000;">Traversing Knowledge Graph</h2>
                    <p style="font-size:12px;color:#6b7280;margin:0;">Tracing prerequisite paths for your incorrect answers through the full dependency graph...</p>
                </div>
                <div style="display:flex;gap:12px;align-items:center;background:#f9fafb;padding:8px 12px;border-radius:8px;border:1px solid #f3f4f6;">
                    <div style="display:flex;align-items:center;gap:6px;">
                        <div style="width:13px;height:13px;border-radius:3px;background:#fef3c7;border:2px solid #f59e0b;"></div>
                        <span style="font-size:10px;color:#374151;font-weight:600;">Prerequisite Topic</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:6px;">
                        <div style="width:13px;height:13px;border-radius:3px;background:#dcfce7;border:2px solid #16a34a;"></div>
                        <span style="font-size:10px;color:#374151;font-weight:600;">Correct Ans</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:6px;">
                        <div style="width:13px;height:13px;border-radius:3px;background:#fee2e2;border:2px solid #dc2626;"></div>
                        <span style="font-size:10px;color:#374151;font-weight:600;">Incorrect Ans</span>
                    </div>
                </div>
            </div>
            """
            
            pairs_js = json.dumps([{"from": e["from"], "to": e["to"]} for e in graph_edges])
            correct_js = json.dumps(list(correct_lo_set))
            wrong_js = json.dumps(list(wrong_lo_set))
            
            animation_script = f"""
            <script>
                var animationDone = false;
                function runAnimation() {{
                    if(animationDone) return;
                    animationDone = true;
                    
                    var correctLos = {correct_js};
                    var wrongLos = {wrong_js};
                    var edgePairs = {pairs_js};
                    
                    // BRING ALL NODES TO FRONT so thick edges don't overlap them
                    var allNodes = document.querySelectorAll(".node");
                    allNodes.forEach(function(n) {{
                        if (n.parentNode) {{
                            n.parentNode.appendChild(n);
                        }}
                    }});
                    
                    // Mark correct answers first
                    correctLos.forEach(function(lo) {{
                        var node = document.getElementById(lo);
                        if(node) {{
                            var poly = node.querySelector("polygon, ellipse, path");
                            if(poly) {{
                                poly.setAttribute("fill", "#dcfce7");
                                poly.setAttribute("stroke", "#16a34a");
                                poly.setAttribute("stroke-width", "3");
                            }}
                        }}
                    }});
                    
                    // Mark all wrong answers immediately
                    wrongLos.forEach(function(lo) {{
                        var node = document.getElementById(lo);
                        if(node) {{
                            var poly = node.querySelector("polygon, ellipse, path");
                            if(poly) {{
                                poly.setAttribute("fill", "#fee2e2");
                                poly.setAttribute("stroke", "#dc2626");
                                poly.setAttribute("stroke-width", "4");
                            }}
                        }}
                    }});
                    
                    var startDelay = 600;
                    var stepMs = 900;
                    
                    edgePairs.forEach(function(pair, idx) {{
                        setTimeout(function() {{
                            var edgeId = "edge____" + pair.from + "___" + pair.to;
                            var edgeIdReverse = "edge____" + pair.to + "___" + pair.from;
                            var edge = document.getElementById(edgeId) || document.getElementById(edgeIdReverse);
                            
                            if (edge) {{
                                var path = edge.querySelector("path");
                                var polygon = edge.querySelector("polygon");
                                if(path) {{
                                    path.setAttribute("stroke", "#f59e0b");
                                    path.setAttribute("stroke-width", "4");
                                }}
                                if(polygon) {{
                                    polygon.setAttribute("fill", "#f59e0b");
                                    polygon.setAttribute("stroke", "#f59e0b");
                                }}
                            }}
                            
                            var fromNode = document.getElementById(pair.from);
                            if(fromNode) {{
                                var poly = fromNode.querySelector("polygon, ellipse, path");
                                if(poly && !correctLos.includes(pair.from) && !wrongLos.includes(pair.from)) {{
                                    poly.setAttribute("stroke", "#f59e0b");
                                    poly.setAttribute("stroke-width", "4");
                                }}
                            }}
                        }}, startDelay + idx * stepMs);
                    }});
                }}
                
                var checkInterval = setInterval(function() {{
                    if(typeof isInitialized !== "undefined" && isInitialized) {{
                        clearInterval(checkInterval);
                        setTimeout(runAnimation, 300);
                    }}
                }}, 100);
            </script>
            """
            
            full_html = full_html.replace("</style>", "body, .graph-container { background: transparent !important; border:none !important; box-shadow:none !important; margin:0; padding:0; height:100vh !important; } #reset-btn, #hint { display: none !important; } </style>")
            full_html = full_html.replace("</body>", animation_script + "</body>")
            
            b64_html = base64.b64encode(full_html.encode("utf-8")).decode("utf-8")
            
            with slot:
                st.components.v1.html(f"""
                <script>
                (function() {{
                    {_ensure_overlay_js()}
                    
                    ov.innerHTML = `
                      <div id="ec-graph-card" style="background:rgba(255,255,255,0.85); backdrop-filter:blur(10px); border-radius:24px; padding:24px; width:92vw; max-width:1400px; box-shadow:0 40px 100px rgba(0,0,0,0.6); display:flex; flex-direction:column; position:relative; overflow:hidden;">
                        {ui_overlay}
                        <iframe id="ec-vis-iframe" src="data:text/html;base64,{b64_html}" style="flex-grow:1; width:100%; height:72vh; min-height:600px; border:none; display:block;"></iframe>
                        
                      </div>
                    `;
                }})();
                </script>
                """, height=0, scrolling=False)
        inject_animated_loader()
        time.sleep(4.7)  # Stay long enough for the 3s loader animation to finish cleanly

        # Step 2 — Knowledge Graph animation
        inject_graph_step()
        # We must sleep briefly to ensure Streamlit flushes the component to the browser before rerunning
        import time
        time.sleep(1)
        st.session_state.phase = "anim"
        st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    # PHASE 2.5 — ANIMATION WAIT STATE
    # ────────────────────────────────────────────────────────────────────────
    elif st.session_state.phase == "anim":
        # The visible button is rendered directly in the HTML overlay above.
        # This hidden Streamlit button catches the JS click event to trigger the state change.
        st.markdown("""
        <style>
            div[data-testid="stMain"] div[data-testid="stButton"] {
                opacity: 0 !important;
                position: absolute !important;
                z-index: -100 !important;
                pointer-events: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("HIDDEN_TRIGGER", use_container_width=False):
            st.session_state.phase = "results"
            st.rerun()

    # ────────────────────────────────────────────────────────────────────────
    # PHASE 3 — RESULTS
    # ────────────────────────────────────────────────────────────────────────
    elif st.session_state.phase == "results":
        import streamlit.components.v1 as components
        components.html('''<script>window.parent.document.querySelector(".main").scrollTo(0,0);</script>''', height=0)

        


        answers  = st.session_state.answers
        correct  = {qid for qid, ans in answers.items() if ans == QUESTIONS[qid]["correct"]}
        wrong    = set(answers) - correct
        n_cor    = len(correct)
        n_tot    = len(QUESTIONS)

        # ── Score card ──
        if n_cor == n_tot:
            sc_color = "#16a34a"
            sc_label = "No Knowledge Gaps 🎉"
            sc_sub   = "You answered every question correctly!"
        elif n_cor >= 3:
            sc_color = "#d97706"
            sc_label = f"{n_tot - n_cor} Knowledge Gap{'s' if n_tot - n_cor > 1 else ''} Found"
            sc_sub   = "Review the practice prerequisites below."
        else:
            sc_color = "#dc2626"
            sc_label = f"{n_tot - n_cor} Knowledge Gaps Found"
            sc_sub   = "Several prerequisite topics need attention."

        st.markdown(f"""
        <div class="score-card">
            <div class="sc-num" style="color:{sc_color};">{n_cor}/{n_tot}</div>
            <div class="sc-label" style="color:{sc_color};">{sc_label}</div>
            <div style="font-size:12px; color:#9ca3af; margin-top:4px;">{sc_sub}</div>
        </div>
        """, unsafe_allow_html=True)

        if n_cor == n_tot:
            st.markdown("""
            <div class="rec-panel" style="border-color:#16a34a; background:linear-gradient(135deg,#f0fdf415,#dcfce715);">
                <div class="rp-title" style="color:#16a34a !important;">🎉 All Questions Correct!</div>
                <ul style="padding-left:18px; margin:0;">
                    <li style="font-size:13px; color:#374151; margin:4px 0;">Answered all 5 questions correctly</li>
                    <li style="font-size:13px; color:#374151; margin:4px 0;">No prerequisite gaps found in the dependency graph</li>
                    <li style="font-size:13px; color:#374151; margin:4px 0;">System recommends advancing to Chapter 13</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        else:
            left, right = st.columns([1, 1.3], gap="large")

            # LEFT — question-by-question review
            with left:
                st.markdown("<div class=\"sec-h\">Your Responses</div>", unsafe_allow_html=True)
                for qid, q in QUESTIONS.items():
                    got    = qid in correct
                    bg     = "#f0fdf4" if got else "#fff5f5"
                    border = "#16a34a" if got else "#dc2626"
                    rq_cls = "rq-correct" if got else "rq-wrong"
                    ic_text = "✓ Correct" if got else "✗ Incorrect"
                    st.markdown(f"""
                    <div class="rq {rq_cls}" style="background:{bg}; border-left:4px solid {border}; animation-delay:{(q['num']-1)*0.09}s;">
                        <div class="rq-top">
                            <span class="rq-lo" style="font-weight:bold;">Q{q['num']}</span>
                            <span class="rq-badge" style="color:{border}; font-size:12px; font-weight:bold;">{ic_text}</span>
                        </div>
                        <div class="rq-text">{q['text']}</div>
                        <div style="font-size:11px; color:#6b7280; margin-top:5px; font-style:italic;">LO: {LO_DESC[q['lo']]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # RIGHT — recommendations
            with right:
                wrong_los = {QUESTIONS[qid]["lo"] for qid in wrong}
                rec = get_recommendation(wrong_los)

                if rec is None:
                    st.markdown("""
                    <div class="rec-panel" style="border-color:#d97706; background:#fffbeb;">
                        <div class="rp-title" style="color:#d97706 !important;">⚠️ No Prerequisite Path Found</div>
                        <ul style="padding-left:18px; margin:0;">
                            <li style="font-size:13px; color:#374151; margin:4px 0;">Review the learning objective text directly</li>
                            <li style="font-size:13px; color:#374151; margin:4px 0;">No earlier chapter prerequisites found in the dependency graph</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="sec-h">Prerequisite Practice Questions</div>
                    """, unsafe_allow_html=True)

                    lo_to_qnum = {info["lo"]: f"Q{info['num']}" for info in QUESTIONS.values()}
                    for rank, item in enumerate(rec["practice"], 1):
                        q      = item["q"]
                        needed_raw = [lo_to_qnum.get(lo, lo) for lo in item["needed_for"]]
                        needed = sorted(needed_raw)
                        st.markdown(f"""
                        <div class="pq" style="animation-delay:{rank*0.12}s;">
                            <span class="pq-tag">📌 Prerequisite for: {' · '.join(needed)}</span>
                            <div class="pq-meta">Practice Q{rank} &nbsp;·&nbsp; Ch {q['ch']} · Sec {q['sec']}</div>
                            <div class="pq-text">{q['text']}</div>
                            <div class="pq-lo-desc">LO: {q['lo_desc']}</div>
                        </div>
                        """, unsafe_allow_html=True)



            
        # ── Reset button ──
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("🔄  Take Quiz Again", use_container_width=True):
            for qid in QUESTIONS:
                st.session_state.pop(f"ans_{qid}", None)
            st.session_state.phase   = "quiz"
            st.session_state.answers = {}
            st.session_state.quiz_error = ""
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STUDENT DASHBOARD TAB
# ══════════════════════════════════════════════════════════════════════════════
with dashboard_tab:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:6px 0;margin-bottom:12px;">
        <span style="font-size:32px;">👩🏽‍🎓</span>
        <div>
            <div style="font-size:22px;font-weight:900;">Sarah Jenkins · Biology 101</div>
            <div style="font-size:14px;color:#6b7280;">Student Profile & Historical Assessment Data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected_date = st.radio(
        "Select Historical Assessment:", 
        options=["April 14, 2026 - Unit 2 Test", "May 22, 2026 - Midterm Quiz", "June 30, 2026 - Chapter 10 (Current)"],
        horizontal=True
    )
    st.markdown("<hr style='margin-top:0; margin-bottom:24px;'>", unsafe_allow_html=True)
    
    if "April 14" in selected_date:
        dash_answers = {
            "q10_genome_structure": "Incorrect",
            "q10_chromosomes_genes": QUESTIONS["q10_chromosomes_genes"]["correct"],
            "q10_compaction": "Incorrect",
            "q10_interphase_stage": QUESTIONS["q10_interphase_stage"]["correct"],
            "q10_metaphase": QUESTIONS["q10_metaphase"]["correct"]
        }
    elif "May 22" in selected_date:
        dash_answers = {
            "q10_genome_structure": QUESTIONS["q10_genome_structure"]["correct"],
            "q10_chromosomes_genes": QUESTIONS["q10_chromosomes_genes"]["correct"],
            "q10_compaction": QUESTIONS["q10_compaction"]["correct"],
            "q10_interphase_stage": QUESTIONS["q10_interphase_stage"]["correct"],
            "q10_metaphase": "Incorrect"
        }
    else:
        dash_answers = {
            "q10_genome_structure": QUESTIONS["q10_genome_structure"]["correct"],
            "q10_chromosomes_genes": "Incorrect answer example",
            "q10_compaction": QUESTIONS["q10_compaction"]["correct"],
            "q10_interphase_stage": "Incorrect answer example",
            "q10_metaphase": QUESTIONS["q10_metaphase"]["correct"]
        }
        
    correct = [qid for qid, ans in dash_answers.items() if ans == QUESTIONS[qid]["correct"]]
    wrong = [qid for qid, ans in dash_answers.items() if ans != QUESTIONS[qid]["correct"]]
    score_pct = int(len(correct) / len(QUESTIONS) * 100)
    score_color = "#16a34a" if score_pct >= 80 else "#d97706" if score_pct >= 60 else "#dc2626"
    
    st.markdown(f"""
    <div style="font-size:16px;color:#374151;margin-bottom:18px;font-weight:600;">
        Assessment Score: <strong style="color:{score_color}; font-size:18px;">{score_pct}%</strong> &nbsp;·&nbsp; {len(correct)}/5 correct
    </div>
    """, unsafe_allow_html=True)
    
    dcol1, dcol2 = st.columns([1, 1.3], gap="large")
    with dcol1:
        st.markdown("<div class=\"sec-h\">Previous Responses</div>", unsafe_allow_html=True)
        for qid, q in QUESTIONS.items():
            got = qid in correct
            bg = "#f0fdf4" if got else "#fff5f5"
            br = "#16a34a" if got else "#dc2626"
            ic = "✓ Correct" if got else "✗ Incorrect"
            st.markdown(f"""
<div class="rq" style="background:{bg}; border-left:4px solid {br}; margin-bottom:12px;">
    <div class="rq-top">
        <span class="rq-lo">Question {q['num']}</span>
        <span class="rq-badge" style="color:{br}; font-weight:bold;">{ic}</span>
    </div>
    <div class="rq-text">{q['text']}</div>
    <div style="font-size:11px; color:#6b7280; margin-top:5px; font-style:italic;">LO: {LO_DESC[q['lo']]}</div>
</div>
            """, unsafe_allow_html=True)

    with dcol2:
        wrong_los = {QUESTIONS[qid]["lo"] for qid in wrong}
        if wrong_los:
            rec = get_recommendation(wrong_los)
        else:
            rec = None

        if not rec:
            st.markdown("""
            <div class="rec-panel" style="border-color:#d97706; background:#fffbeb;">
                <div class="rp-title" style="color:#d97706 !important;">⚠️ No Prerequisite Path Found</div>
                <ul style="padding-left:18px; margin:0;">
                    <li style="font-size:13px; color:#374151; margin:4px 0;">Review the learning objective text directly</li>
                    <li style="font-size:13px; color:#374151; margin:4px 0;">No earlier chapter prerequisites found in the dependency graph</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sec-h">Prerequisite Practice Recommendations</div>
            """, unsafe_allow_html=True)

            lo_to_qnum = {info["lo"]: f"Q{info['num']}" for info in QUESTIONS.values()}
            for rank, item in enumerate(rec["practice"], 1):
                q = item["q"]
                needed_raw = [lo_to_qnum.get(lo, lo) for lo in item["needed_for"]]
                needed = sorted(needed_raw)
                st.markdown(f"""
                <div class="pq" style="margin-top:16px;">
                    <span class="pq-tag">📌 Prerequisite for: {' · '.join(needed)}</span>
                    <div class="pq-meta">Practice Q{rank} &nbsp;·&nbsp; Ch {q['ch']}</div>
                    <div class="pq-text">{q['text']}</div>
                    <div class="pq-lo-desc">LO: {q['lo_desc']}</div>
                </div>
                """, unsafe_allow_html=True)



