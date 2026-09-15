# ============================================================
# KURDISH LLM EVALUATOR — Dashboard
# ============================================================

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="Kurdish LLM Evaluator",
    page_icon="🎯",
    layout="wide"
)

PROJECT = Path("/content/kurdish-llm-eval")
RESPONSES_FILE = PROJECT / "data" / "responses.json"
ANNOTATIONS_FILE = PROJECT / "data" / "annotations.json"

# Load responses
responses = json.loads(RESPONSES_FILE.read_text(encoding="utf-8"))

# Load annotations if exist
if ANNOTATIONS_FILE.exists():
    annotations = json.loads(ANNOTATIONS_FILE.read_text(encoding="utf-8"))
else:
    annotations = {}

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("🎯 Kurdish LLM Evaluator")
st.markdown("**هەڵسەنگاندنی مۆدێلەکانی AI بە زمانی کوردی**")

# ------------------------------------------------------------
# Statistics
# ------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 کۆی وەڵام", len(responses))

with col2:
    prompts_count = len(set(r["prompt_id"] for r in responses))
    st.metric("📝 پرسیار", prompts_count)

with col3:
    models_count = len(set(r["model"] for r in responses))
    st.metric("🤖 مۆدێل", models_count)

with col4:
    st.metric("✅ هەڵسەنگێنراو", len(annotations))

st.divider()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
st.sidebar.header("⚙️ ڕێکخستنەکان")

# Model filter
all_models = sorted(set(r["model"] for r in responses))
selected_models = st.sidebar.multiselect(
    "مۆدێلەکان",
    all_models,
    default=all_models
)

# Prompt filter
all_prompts = sorted(set(r["prompt_id"] for r in responses))
selected_prompts = st.sidebar.multiselect(
    "پرسیارەکان",
    all_prompts,
    default=all_prompts
)

# Show only non-annotated
show_only_new = st.sidebar.checkbox("تەنها ئەوانەی هەڵسەنگێنەنراو", value=False)

# ------------------------------------------------------------
# Filter responses
# ------------------------------------------------------------
filtered = [
    r for r in responses
    if r["model"] in selected_models and r["prompt_id"] in selected_prompts
]

# ------------------------------------------------------------
# Main tabs
# ------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📝 هەڵسەنگاندن", "📊 ئامار", "📋 لیستی پرسیارەکان"])

# ============================================================
# TAB 1: Annotation
# ============================================================
with tab1:
    st.header("📝 هەڵسەنگاندنی وەڵامەکان")
    
    # Group by prompt
    by_prompt = {}
    for r in filtered:
        pid = r["prompt_id"]
        if pid not in by_prompt:
            by_prompt[pid] = []
        by_prompt[pid].append(r)
    
    for pid in sorted(by_prompt.keys()):
        items = by_prompt[pid]
        prompt = items[0]["prompt"]
        
        st.subheader(f"📝 پرسیاری {pid}")
        st.info(prompt)
        
        # Show responses side by side
        cols = st.columns(len(items))
        
        for col, item in zip(cols, items):
            with col:
                model_short = item["model"].split("/")[-1]
                st.markdown(f"### 🤖 {model_short}")
                st.caption(f"⏱️ {item['time_seconds']}s | 🎫 {item['tokens_used']} تۆکن")
                
                st.markdown(item["response"])
                
                # Annotation
                key = f"{pid}_{item['model']}"
                current = annotations.get(key, {})
                
                score = st.slider(
                    "⭐ نمرە",
                    1, 5,
                    current.get("score", 3),
                    key=f"score_{key}"
                )
                
                note = st.text_input(
                    "📝 تێبینی",
                    current.get("note", ""),
                    key=f"note_{key}"
                )
                
                if st.button(f"💾 پاشەکەوت", key=f"btn_{key}"):
                    annotations[key] = {
                        "prompt_id": pid,
                        "model": item["model"],
                        "score": score,
                        "note": note,
                        "saved_at": datetime.now().isoformat(),
                    }
                    ANNOTATIONS_FILE.write_text(
                        json.dumps(annotations, indent=2, ensure_ascii=False),
                        encoding="utf-8"
                    )
                    st.success("✅ پاشەکەوت کرا!")
        
        st.divider()

# ============================================================
# TAB 2: Statistics
# ============================================================
with tab2:
    st.header("📊 ئاماری بەراوردکاری")
    
    # Average time per model
    st.subheader("⏱️ خێرایی")
    for model in selected_models:
        model_items = [r for r in responses if r["model"] == model]
        avg_time = sum(r["time_seconds"] for r in model_items) / len(model_items)
        st.write(f"**{model}**: {avg_time:.2f}s")
    
    # Average length
    st.subheader("📏 درێژی وەڵام")
    for model in selected_models:
        model_items = [r for r in responses if r["model"] == model]
        avg_len = sum(len(r["response"]) for r in model_items) / len(model_items)
        st.write(f"**{model}**: {avg_len:.0f} پیت")
    
    # Annotations summary
    st.subheader("⭐ نمرەکان")
    if annotations:
        for model in selected_models:
            model_scores = [
                a["score"] for a in annotations.values()
                if a["model"] == model
            ]
            if model_scores:
                avg_score = sum(model_scores) / len(model_scores)
                st.write(f"**{model}**: {avg_score:.2f} / 5 ({len(model_scores)} هەڵسەنگاندن)")
    else:
        st.info("هێشتا هیچ هەڵسەنگاندنێک نییە")

# ============================================================
# TAB 3: Prompts List
# ============================================================
with tab3:
    st.header("📋 لیستی پرسیارەکان")
    
    prompts_list = sorted(set(r["prompt"] for r in responses))
    for i, prompt in enumerate(prompts_list, 1):
        st.write(f"**{i}.** {prompt}")
