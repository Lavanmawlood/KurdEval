# 🎯 Kurdish LLM Evaluator

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

> **A professional evaluation framework for comparing Large Language Models on Kurdish language tasks — bridging AI and low-resource language research.**

---

## 🎯 Problem Statement

Kurdish is spoken by **30+ million people** worldwide, yet it remains a **low-resource language** in AI research. Major LLMs consistently underperform on Kurdish compared to high-resource languages like English or Spanish.

**This project provides:**

- 🔬 A **reproducible evaluation framework** for Kurdish LLM tasks
- 📊 A **comparative analysis** of multiple LLMs
- 🎯 **Human annotation** of responses with structured scoring
- 📈 A **professional dashboard** for visualizing results

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌐 **Multi-Model Comparison** | Evaluate GPT-OSS 120B, 20B side-by-side |
| 📝 **Structured Prompts** | 11 prompts across 6 categories |
| 📊 **Automated Metrics** | Response time, token usage, response length |
| ⭐ **Human Annotation** | Interactive scoring (1-5) with notes |
| 🎨 **Professional Dashboard** | Streamlit-powered interface |

---

## 📊 Sample Results

| Model | Avg Time | Avg Tokens | Avg Length |
|-------|----------|------------|------------|
| **gpt-oss-120b** | 1.34s | 592 | 656 chars |
| **gpt-oss-20b** | 0.86s | 583 | 438 chars |

> **Finding:** The smaller 20B model is ~40% faster but produces shorter responses.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12+ |
| LLM Provider | Groq (LPU inference) |
| Models | GPT-OSS 120B, GPT-OSS 20B |
| Dashboard | Streamlit |
| Data | JSON, Pandas |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Lavanmawlood/kurdish-llm-evaluator.git
cd kurdish-llm-evaluator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key
```bash
export GROQ_API_KEY="your_api_key_here"
```

### 4. Launch the Dashboard
```bash
streamlit run src/dashboard.py
```

---

## 📁 Project Structure

```
kurdish-llm-evaluator/
├── src/
│   ├── evaluators/       # Evaluation logic
│   ├── models/           # LLM connectors
│   ├── utils/            # Helpers
│   └── dashboard.py      # Streamlit dashboard
├── data/
│   ├── prompts/          # Kurdish test prompts
│   ├── responses/        # Model responses
│   └── annotations/      # Human annotations
├── tests/
├── screenshots/
├── requirements.txt
└── README.md
```

---

## 🎯 Why This Project?

### For AI Trainers
- Demonstrates **evaluation methodology** for LLMs
- Shows **human annotation** workflow
- Proves **low-resource language** expertise

### For AI Companies
- Shows ability to **design evaluation frameworks**
- Demonstrates **multi-model comparison** at scale
- Proves **data quality** focus

### For the Kurdish Community
- Provides a **baseline** for Kurdish LLM performance
- Creates **open data** for future research

---



---



---

## 🔬 Key Findings

### Evaluation Setup

We evaluated **3 state-of-the-art LLMs** on **the same 5 Kurdish (Sorani) prompts** across 5 categories:

| Prompt ID | Category | Prompt |
|-----------|----------|--------|
| 1 | General | کوردستان لە کوێیە؟ |
| 4 | Instruction | بە کوردی فێرم بکە چۆن چای ئامادە بکەم |
| 7 | Creative | چیرۆکێکی کورت بە کوردی بۆم بنووسە |
| 10 | Linguistic | زمانی کوردی چەند زاراوەی هەیە؟ |
| 13 | Reasoning | بۆچی خەون دەبینین؟ |

### 📊 Performance Summary

| Model | Avg Response Time | Avg Length | Kurdish Quality |
|-------|-------------------|------------|-----------------|
| **Gemini 3.x Flash** | 36.83s | 399 chars | ⭐⭐⭐⭐ **Excellent** |
| **GPT-OSS 120B** | 2.24s | 841 chars | ⭐⭐ Poor |
| **GPT-OSS 20B** | 1.31s | 670 chars | ⭐ Very Poor |

### 🎯 Sample Comparison (Same Prompt)

**Prompt:** `چیرۆکێکی کورت بە کوردی بۆم بنووسە.`

#### ✨ Gemini 3.x Flash
> *"تەمێکی تەنک داوێنی چیاکەی داپۆشیبوو. پاییز بە هێواشی زێڕی زەردی بەسەر دارگوێزەکاندا دەڕشت و کزەبای ئێوارە، دەنگێکی کزی وەک شیوەن لەناو کۆڵانە تەسک و بەردینەکانی گوندەکەدا دەزرنگاندەوە."*

**✅ Literary quality. Natural Kurdish. Proper grammar.**

#### 🤖 GPT-OSS 120B
> *"لە گوندێکی بچووکی سەروەی هەولێر، کە سەرچاوەی ئاسمان بە سەوزی دارەکان دەستەی دەستەی دەستبەجێی هەیە..."*

**❌ Repetitive phrase "دەستەی دەستەی دەستبەجێی". Incoherent meaning.**

#### 🤖 GPT-OSS 20B
**❌ Severe repetition. Fails to form grammatical sentences.**

### 🔍 Key Observations

1. **Speed vs Quality Trade-off** — GPT-OSS models respond **~5x faster** than Gemini, but this comes at the cost of severe output degradation.
2. **Repetition Failure** — GPT-OSS models frequently loop on meaningless words.
3. **Vocabulary Mixing** — GPT-OSS injects Arabic/Turkish words when Kurdish equivalents exist.
4. **Only Gemini produces literary-quality Kurdish** suitable for native readers.

### 📌 Conclusion

> **Current LLMs still fail at Kurdish.** Even in 2026, producing fluent, natural Kurdish remains a challenge for most models. This demonstrates a critical need for:
> - Kurdish-specific training data
> - Kurdish evaluation benchmarks
> - Investment in low-resource language AI

---

## 🚀 Roadmap

- [ ] Add more models (Llama 3.3, Qwen 3.5, Claude)
- [ ] Expand prompt set to 100+
- [ ] Multi-annotator support
- [ ] Kurdish-specific benchmarks
- [ ] Academic paper submission

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Lavan Mawlood**

- GitHub: [@Lavanmawlood](https://github.com/Lavanmawlood)

---

⭐ **If you find this useful, please star the repo!**
