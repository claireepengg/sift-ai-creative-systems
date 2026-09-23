# Architecture Notes

This document expands on the system architecture summarized in the main case study.

## System boundaries

Sift's image-generation workflow sat between three kinds of inputs and the user-facing product:

- **Identity references:** face and body photographs
- **Creative reference:** a target scene / composition
- **Product reference:** exact garment photography

A backend job layer assembled those inputs, created a generation configuration, invoked the AI pipeline, stored outputs/intermediates, and saved evaluation metadata back to the database.

## Stage-by-stage flow

### 1. Job assembly

The runner loads the generation job, user AI profile, product metadata, reference imagery, and scene imagery. Private media is exposed to the pipeline through time-limited URLs rather than making the underlying storage public.

### 2. Scene analysis

A multimodal analysis step extracts composition, pose, environment, lighting, camera/framing, and other visual information from the reference scene. Identity-specific attributes are deliberately separated from the scene description so they do not overwrite the target user's characteristics.

### 3. Identity-aware base generation

The base generation stage produces multiple candidates. Rather than selecting a candidate manually, downstream evaluators compare candidates against the user's face references and score anatomical/visual quality.

### 4. Body-proportion gate and correction

The pipeline compares generated body regions with body reference imagery. If key regions are already sufficiently aligned, the stage is skipped. Otherwise a localized correction stage is invoked.

This gate exists because unnecessary image edits can degrade otherwise good outputs.

### 5. Garment replacement

The selected image is edited using the actual product photography as ground truth. The editing instruction explicitly protects face, hair, pose, background, lighting, framing, and body proportions while changing the intended garment region.

### 6. Garment fidelity evaluation

The edited output is compared against product images. Individual garment attributes are returned as structured checks. Failed checks are converted into targeted feedback for a subsequent attempt.

The pipeline keeps the best attempt rather than assuming the last attempt is the best.

### 7. Color normalization

A lightweight image-processing step corrects model-introduced color-temperature shifts before compositing, reducing visible seams between stages.

### 8. Face restoration

A landmark-based computer-vision stage uses facial landmarks, piecewise affine warping, and a feathered face mask to restore identity from the stronger base-generation stage onto the final edited image.

The stage fails gracefully: if face detection or the local CV dependency is unavailable, the generated image remains usable.

### 9. Persistence

The final image and useful intermediates are uploaded to cloud storage. Evaluation values and output references are saved against the job.

### 10. Human QA

Reviewers inspect results in an internal admin tool and set an explicit review state. Approved variants can be promoted as the primary output; rejected or revision-needed jobs remain available for corrective workflows.

## Reliability principles

### Save expensive work

Intermediate outputs allow a later stage to be retried without paying the time/cost of successful earlier stages again.

### Retry only recoverable failures

Transient network/provider errors are retried; non-transient errors surface rather than looping indefinitely.

### Fallback by capability

Where appropriate, the pipeline can move between model variants/providers rather than treating provider failure as total workflow failure.

### Keep human judgment in the loop

Machine evaluation narrows the search space and catches repeatable errors. Human reviewers remain responsible for final aesthetic/product approval.
