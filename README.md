# Sift

**Personalized fashion discovery powered by generative AI**

**Role:** Co-founder / Product & Engineering  
**Platform:** iOS  
**Built with:** Python, Flask, MySQL, AWS S3, generative image models, multimodal models, computer vision

---

## Overview

Sift was an iOS fashion discovery app that generated personalized fashion imagery for users.

Instead of viewing clothing only on models or product pages, users could see fashion items represented on a version of themselves and save the looks they liked.

I built Sift’s end-to-end AI generation workflow and the supporting database and backend systems that powered it.

<!-- Add hero image here:
![Sift](assets/hero.jpg)
-->

---

## What I worked on

My work on Sift included:

- designing the image-generation workflow
- integrating multiple generative and multimodal models
- developing Python services for image processing and generation
- building API endpoints connecting the AI pipeline to the iOS product
- managing asynchronous generation jobs and result storage
- implementing image-quality checks and retry logic
- building internal tools for reviewing generated images
- testing different approaches to improve likeness, product accuracy, and visual consistency
- iterating on the product based on user testing

---

## Generative image pipeline

The image system took several inputs:

- user reference photographs
- a scene or pose reference
- product imagery

These were processed through a multi-stage generation workflow before the resulting image was returned to the application.

```text
User references
       +
Scene reference
       +
Product images
       ↓
Image generation
       ↓
Image evaluation / refinement
       ↓
Quality review
       ↓
Sift
```

Different models and image-processing techniques were used for different parts of the workflow.

Implementation details and production prompts are omitted from this public repository.

<!-- Add workflow visual here:
![Generation workflow](assets/workflow.jpg)
-->

---

## Image quality

One of the main technical challenges was maintaining consistency across several dimensions at once.

Generated images needed to preserve:

- the user's likeness
- body proportions
- the composition of the reference image
- recognizable characteristics of the clothing
- realistic lighting and image texture

I tested and iterated on different model combinations, prompts, image-processing methods, and evaluation steps to improve these results.

<!-- Add output examples here:
![Generation examples](assets/outputs.jpg)
-->

---

## Production system

The generation workflow was connected to Sift's backend rather than running as a standalone prototype.

I built or worked on systems for:

- generation-job management
- API communication
- database integration
- cloud image storage
- generation status tracking
- retries and error handling
- saving and serving completed images

This allowed generation requests to move from the mobile application through the AI pipeline and back into the user experience.

---

## Internal tools

I also built internal tooling for managing and reviewing generated imagery.

The admin interface supported tasks including:

- reviewing generations
- approving or rejecting images
- managing product imagery
- inspecting generation jobs
- selecting images for the application
- monitoring content and generation quality

<!-- Add admin screenshot here:
![Sift admin tools](assets/qc-review.jpg)
-->

---

## Product

The final generated images appeared directly inside the Sift iOS experience, where users could browse and save personalized fashion looks.

<!-- Add app screenshot here:
![Sift iOS app](assets/app.jpg)
-->

---

## Selected technologies

`Python` · `Flask` · `MySQL` · `AWS S3` · `REST APIs` · `Generative AI` · `Multimodal models` · `Computer vision`

---

## Repository note

This repository is a case study of my work on Sift rather than the production source code.

Production code, prompts, internal evaluation criteria, infrastructure configuration, and proprietary implementation details are not included.
