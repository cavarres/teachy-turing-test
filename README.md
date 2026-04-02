# Teachy AI Tests

A collection of interactive evaluations for AI-generated ENEM content, deployed on GitHub Pages.

**[Open the tests](https://cavarres.github.io/teachy-turing-test/)**

## About

Part of a proof of concept for [Teachy](https://www.teachy.com.br/), exploring AI-generated exam questions aligned with Brazil's ENEM (Exame Nacional do Ensino Médio). Results are exported as CSV for use in model training and research.

---

## Test 1 — ENEM Turing Test

Can you tell AI-generated ENEM questions from real ones?

**How it works:**
1. You are shown a series of questions (real and AI-generated, shuffled randomly)
2. For each one, guess: **Original ENEM** or **AI-generated**?
3. Rate your confidence (1–5) and optionally explain your reasoning
4. After each answer you see whether you were right — and for AI questions, the real ENEM questions used as references
5. At the end, export your results as CSV

---

## Test 2 — Question Difficulty Evaluation

Teachers rate the difficulty of ENEM-style questions to build a labeled dataset for difficulty prediction models.

**How it works:**
1. Choose to evaluate **all 28 questions** or a **custom number** (randomly sampled)
2. For each question you see the full prompt, answer options, and the **correct answer highlighted**
3. Rate the difficulty: **Very Easy / Easy / Medium / Hard / Very Hard**
4. Optionally add notes explaining what makes the question easy or hard
5. At the end, export your ratings as CSV

**Question CSV input format** (for adding new questions):
```
id,grade,discipline,topic,question_type,prompt,option_a,option_b,option_c,option_d,option_e,correct_answer,expected_answer,image_path
```
- `question_type`: `multiple_choice` or `open`
- For open questions: leave options and `correct_answer` blank, fill `expected_answer`
- `image_path`: leave blank if no image

**Results CSV output columns:**
```
#, name, question_id, grade, discipline, topic, correct_answer, difficulty, reasoning
```
