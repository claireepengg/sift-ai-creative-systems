# Sift — AI Creative Systems Case Study

**Claire Peng — Co-founder / Product & AI Systems**

Sift was an iOS fashion discovery product built around personalized generative imagery. I co-founded the product and helped design and build the AI system that turned user references, scene references, and product imagery into personalized fashion visuals.

This case study focuses on the creative-technology problem: how to turn probabilistic generative models into a repeatable production workflow with enough structure, evaluation, and human oversight to support a real product.

> Certain implementation details, prompts, evaluation criteria, and production architecture have been intentionally omitted because Sift remains proprietary.

---

## The challenge

Generating a compelling image once is easy.

Generating personalized fashion imagery reliably enough for a user-facing product is a systems problem.

The workflow had to account for multiple competing constraints at once:

- preserve the user’s visual identity
- preserve the intended scene and composition
- maintain recognizable product characteristics
- recover from inconsistent model outputs
- move generations through a repeatable production process
- surface outputs for human review before they reached the product

The core question became:

**How do you build a creative system around models that are powerful, but inherently variable?**

---

## My role

I worked across product, creative systems, and technical implementation.

My work included:

- designing the end-to-end generative workflow
- testing and comparing multimodal image-generation approaches
- translating visual-quality requirements into system logic
- building production tooling around model outputs
- integrating generation jobs with application data and storage
- designing recovery and retry behavior for unreliable outputs
- creating internal review workflows for image quality control
- iterating on the user experience alongside the underlying AI system

The work sat between product design, creative direction, model experimentation, and software engineering.

---

## System overview

Sift used a multi-stage AI workflow rather than relying on a single generation step.

```text
PERSON REFERENCES
        +
SCENE REFERENCE
        +
PRODUCT REFERENCES
        ↓
┌────────────────────────────┐
│   MULTI-STAGE AI SYSTEM    │
│                            │
│   Generation               │
│   Evaluation               │
│   Corrective processing    │
│   Retry / recovery         │
└────────────────────────────┘
        ↓
HUMAN QUALITY REVIEW
        ↓
PRODUCT EXPERIENCE
```

Different stages of the system were designed around different model strengths. Outputs were evaluated before progressing, and failed or weak generations could be routed through corrective or recovery steps rather than treated as final.

The important design principle was not “find the best model.”

It was:

**Build a system that expects models to fail in different ways, then make those failures manageable.**

---

## Creative quality as a systems problem

A recurring challenge was that “technically successful” generations were often not visually acceptable.

A result could be photorealistic but still fail because:

- the person no longer looked sufficiently like the user
- the product changed in important ways
- proportions drifted
- visual details became inconsistent
- the result looked synthetic or overprocessed
- the image worked in isolation but did not fit the rest of the product experience

Instead of treating quality as a purely subjective final check, I designed the workflow so that visual quality informed what happened next.

Some outputs progressed. Others were corrected, regenerated, or rejected.

That shift — from **generation** to **generation + evaluation + recovery** — was one of the most important parts of making the system usable in production.

---

## Production workflow

Sift’s AI layer was connected to the rest of the product rather than operating as a standalone experiment.

The production system handled:

- user reference inputs
- generation-job state
- model orchestration
- result persistence
- storage and retrieval
- recovery from failed or incomplete runs
- internal review
- delivery into the user-facing application

This meant the system had to work not only when the AI behaved well, but also when it timed out, produced a weak result, returned an incomplete result, or needed another review cycle.

---

## Human-in-the-loop review

We built internal review tooling so generated imagery could be inspected before being treated as production-ready.

The review layer supported a simple but important principle:

**AI output was not automatically product output.**

Human review remained part of the system for:

- visual quality
- identity consistency
- product fidelity
- obvious generation artifacts
- overall suitability for the user experience

This helped separate fast model experimentation from the quality bar of the final product.

<!-- Add screenshot here once ready:
![Sift quality review interface](assets/qc-review.jpg)
-->

---

## From prototype to product

The project evolved from individual model experiments into a repeatable application workflow.

That required thinking beyond prompting:

- What information should each stage receive?
- Which model should handle which kind of task?
- What happens when a stage fails?
- When should the system retry?
- What should be cached or persisted?
- What should be evaluated automatically?
- Where should human judgment stay in the loop?
- How do you improve quality without making the workflow impossibly slow?

Those questions shaped the system more than any single prompt or model choice.

---

## What I learned

### 1. Model orchestration matters more than model loyalty

Different models fail differently. A robust creative workflow benefits from assigning tasks based on model strengths rather than forcing one model to do everything.

### 2. Evaluation is part of generation

A production system needs to decide whether an output is usable, not merely whether an API returned successfully.

### 3. Creative quality needs operational structure

Visual judgment can inform system behavior. The best workflows make room for both machine evaluation and human review.

### 4. Reliability changes the creative possibilities

Once retries, fallbacks, persistence, and review are designed into the system, generative AI becomes much more useful as a real production tool.

### 5. Human taste remains the final constraint

Automation helped us generate, evaluate, and recover faster. But the product still depended on human judgment about what looked believable, appropriate, and worth showing.

---

## Selected tools & technologies

Sift combined generative AI, multimodal models, computer-vision techniques, backend APIs, cloud storage, database-backed job orchestration, and internal review tooling.

Selected technologies used across the project included:

- Python
- Flask
- MySQL
- AWS S3
- multimodal generative image models
- image-processing / computer-vision tooling
- REST APIs
- production job orchestration

Specific prompts, implementation details, internal evaluation criteria, and proprietary pipeline logic are intentionally not published here.

---

## Visuals

This case study is being prepared as a visual walkthrough of the system.

Planned materials include:

1. **Hero example** — user/scene/product references alongside a final Sift output
2. **Workflow progression** — selected intermediate stages without exposing proprietary logic
3. **Product experience** — generated imagery inside the iOS app
4. **Quality review** — internal review tooling used to inspect outputs
5. **Output gallery** — a small selection of final generations

<!-- Recommended hero placement:
![Sift hero](assets/hero.jpg)
-->

---

## About the project

**Sift**  
iOS fashion discovery product  
Co-founded and built by Claire Peng and team

**My focus:** AI creative systems, product, workflow design, model experimentation, technical implementation

---

## Notes on proprietary work

This repository is a portfolio case study, not Sift’s production codebase.

To protect the product and its underlying system, this public version intentionally excludes:

- source code
- production prompts
- model-selection logic
- internal scoring criteria
- system-specific correction methods
- detailed pipeline architecture
- infrastructure configuration
- private datasets and user data

I’m happy to discuss the reasoning behind the system, tradeoffs, and implementation approach in an interview.
