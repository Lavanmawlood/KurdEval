"""KurdEval Dashboard — Professional LLM Evaluation Interface."""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ============================================================
# Configuration
# ============================================================
st.set_page_config(
    page_title="KurdEval",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT = Path(__file__).parent.parent
PROMPTS_FILE = PROJECT / "data" / "prompts" / "kurdish_prompts.json"
RESPONSES_FILE = PROJECT / "data" / "responses" / "responses.json"
ANNOTATIONS_FILE = PROJECT / "data" / "annotations" / "annotations.json"

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF4B4B, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: -10px;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
    }
    .model-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background: #FF4B4B;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .annotation-saved {
        color: #00C853;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load Data
# ============================================================
@st.cache_data(ttl=60)
def load_data():
    prompts = []
    responses = []
    annotations = {}
    
    if PROMPTS_FILE.exists():
        prompts = json.loads(PROMPTS_FILE.read_text(encoding="utf-8"))
    
    if RESPONSES_FILE.exists():
        responses = json.loads(RESPONSES_FILE.read_text(encoding="utf-8"))
    
    if ANNOTATIONS_FILE.exists():
        annotations = json.loads(ANNOTATIONS_FILE.read_text(encoding="utf-8"))
    
    return prompts, responses, annotations


prompts, responses, annotations = load_data()

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown("### 🎯 KurdEval")
    st.markdown("*Kurdish LLM Evaluation Framework*")
    st.divider()
    
    st.markdown("### 📊 Stats")
    st.metric("Prompts", len(prompts))
    st.metric("Responses", len(responses))
    st.metric("Annotations", len(annotations))
    
    st.divider()
    
    # Filters
    st.markdown("### ⚙️ Filters")
    
    all_models = sorted(set(r["model"] for r in responses)) if responses else []
    selected_models = st.multiselect(
        "Models",
        all_models,
        default=all_models,
    )
    
    all_prompts = sorted(set(r.get("prompt_id", 0) for r in responses)) if responses else []
    selected_prompts = st.multiselect(
        "Prompts",
        all_prompts,
        default=all_prompts[:5] if len(all_prompts) > 5 else all_prompts,
    )

# ============================================================
# Header
# ============================================================
st.markdown('<h1 class="main-header">🎯 KurdEval</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">A Kurdish LLM Evaluation Framework</p>', unsafe_allow_html=True)
st.divider()

# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Annotate",
    "📊 Analytics",
    "📋 Prompts",
    "ℹ️ About",
])

# ============================================================
# TAB 1: ANNOTATION
# ============================================================
with tab1:
    st.markdown("### 📝 Response Annotation")
    st.markdown("Score each response from 1 (poor) to 5 (excellent).")
    
    if not responses:
        st.warning("No responses yet. Run `src/run_evaluation.py` first.")
    else:
        # Filter responses
        filtered = [
            r for r in responses
            if r["model"] in selected_models
            and r.get("prompt_id") in selected_prompts
        ]
        
        # Group by prompt
        by_prompt = {}
        for r in filtered:
            pid = r.get("prompt_id")
            if pid not in by_prompt:
                by_prompt[pid] = []
            by_prompt[pid].append(r)
        
        for pid in sorted(by_prompt.keys()):
            items = by_prompt[pid]
            prompt_text = items[0].get("prompt", "Unknown")
            
            with st.expander(f"📝 Prompt {pid}: {prompt_text[:80]}...", expanded=(pid == sorted(by_prompt.keys())[0])):
                st.info(prompt_text)
                
                cols = st.columns(len(items)) if len(items) > 1 else [st.container()]
                
                for col, item in zip(cols, items):
                    with col:
                        model_short = item["model"].split("/")[-1]
                        
                        st.markdown(f"**🤖 {model_short}**")
                        st.caption(f"⏱️ {item['time_seconds']}s | 🎫 {item['tokens_used']} tokens")
                        
                        # Response box
                        st.markdown("**Response:**")
                        st.markdown(
                            f"<div style='background:#f8f9fa; padding:15px; border-radius:8px; "
                            f"min-height:200px; max-height:400px; overflow-y:auto;'>"
                            f"{item['response'][:2000]}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        
                        st.markdown("**Your score:**")
                        
                        key = f"{pid}_{item['model']}"
                        current = annotations.get(key, {})
                        
                        score = st.slider(
                            "Score",
                            1, 5,
                            current.get("score", 3),
                            key=f"score_{key}",
                            label_visibility="collapsed",
                        )
                        
                        note = st.text_input(
                            "Notes",
                            current.get("note", ""),
                            key=f"note_{key}",
                            placeholder="Optional notes...",
                        )
                        
                        if st.button("💾 Save", key=f"save_{key}"):
                            annotations[key] = {
                                "prompt_id": pid,
                                "model": item["model"],
                                "score": score,
                                "note": note,
                                "saved_at": datetime.now().isoformat(),
                            }
                            ANNOTATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
                            ANNOTATIONS_FILE.write_text(
                                json.dumps(annotations, indent=2, ensure_ascii=False),
                                encoding="utf-8",
                            )
                            st.success(f"✅ Saved!")

# ============================================================
# TAB 2: ANALYTICS
# ============================================================
with tab2:
    st.markdown("### 📊 Model Comparison")
    
    if not responses:
        st.warning("No responses yet.")
    else:
        # Stats per model
        models = sorted(set(r["model"] for r in responses))
        
        cols = st.columns(len(models))
        
        for col, model in zip(cols, models):
            with col:
                model_responses = [r for r in responses if r["model"] == model]
                avg_time = sum(r["time_seconds"] for r in model_responses) / len(model_responses)
                avg_tokens = sum(r["tokens_used"] for r in model_responses) / len(model_responses)
                
                # Score
                model_scores = [a["score"] for a in annotations.values() if a["model"] == model]
                avg_score = sum(model_scores) / len(model_scores) if model_scores else 0
                
                st.markdown(f"#### 🤖 {model.split('/')[-1]}")
                st.metric("Avg Time", f"{avg_time:.2f}s")
                st.metric("Avg Tokens", f"{avg_tokens:.0f}")
                st.metric("Avg Score", f"{avg_score:.1f} ⭐" if model_scores else "—")
        
        st.divider()
        
        # DataFrame
        st.markdown("### 📋 Detailed Table")
        
        df_data = []
        for r in responses:
            key = f"{r.get('prompt_id')}_{r['model']}"
            ann = annotations.get(key, {})
            df_data.append({
                "Prompt ID": r.get("prompt_id"),
                "Model": r["model"].split("/")[-1],
                "Time (s)": r["time_seconds"],
                "Tokens": r["tokens_used"],
                "Length": len(r["response"]),
                "Score": ann.get("score", "—"),
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)

# ============================================================
# TAB 3: PROMPTS
# ============================================================
with tab3:
    st.markdown("### 📋 Kurdish Test Prompts")
    
    for p in prompts:
        with st.container():
            st.markdown(f"**{p['id']}. [{p.get('category', 'general')}]** {p['prompt']}")
            st.divider()

# ============================================================
# TAB 4: ABOUT
# ============================================================
with tab4:
    st.markdown("### ℹ️ About KurdEval")
    
    st.markdown("""
    **KurdEval** is an open-source evaluation framework for comparing Large Language Models (LLMs) on **Kurdish language tasks**.
    
    #### 🎯 Purpose
    - Bridge the gap between AI and low-resource languages
    - Provide a reproducible benchmark for Kurdish LLMs
    - Enable multi-model comparison
    
    #### 🛠️ Tech Stack
    - **LLM Provider:** Groq (LPU inference)
    - **Models:** GPT-OSS 120B, GPT-OSS 20B
    - **Dashboard:** Streamlit
    
    #### 📊 Methodology
    1. **11 prompts** across 6 categories
    2. Each prompt sent to **multiple models**
    3. **Human annotation** on a 1-5 scale
    4. **Comparative analysis** of results
    
    #### 🔗 Links
    - GitHub: [Lavanmawlood/KurdEval](https://github.com/Lavanmawlood/KurdEval)
    """)

# ============================================================
# Footer
# ============================================================
st.divider()
st.markdown(
    "<p style='text-align:center; color:#999; font-size:0.8rem;'>"
    "KurdEval — A Kurdish LLM Evaluation Framework | MIT License"
    "</p>",
    unsafe_allow_html=True,
)
