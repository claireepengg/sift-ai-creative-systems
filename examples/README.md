# Code examples

These files are simplified, redacted examples based on systems I implemented while building Sift.

They are included to show the engineering work behind the product without publishing Sift's production code or proprietary AI workflow.

### `generation_runner.py`
Shows the overall lifecycle of a generation job: loading inputs, running the pipeline, saving a result, and updating job status.

### `job_queue.py`
Shows the database pattern used to atomically claim queued work and prevent multiple workers from processing the same job.

### `quality_review.py`
Shows the review-state pattern behind Sift's internal quality-control tooling.

Production names, table structures, prompts, providers, model-routing logic, evaluation logic, and infrastructure configuration have been removed.
