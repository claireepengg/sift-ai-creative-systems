"""Sanitized representative excerpt — not production Sift source.

Shows the orchestration pattern: assemble a job, reuse saved intermediates,
run the creative pipeline, and persist both output and evaluation metadata.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationJob:
    job_id: int
    user_id: int
    scene_url: str
    product_urls: list[str]
    face_refs: list[str]
    body_refs: list[str]
    garment_type: str
    resume_from: Optional[str] = None
    saved_base_image: Optional[str] = None
    saved_edit_image: Optional[str] = None


def run_job(job: GenerationJob):
    mark_status(job.job_id, "running")

    try:
        # Expensive earlier stages can be reused when a later stage fails.
        base = (
            load_saved(job.saved_base_image)
            if job.resume_from in {"body", "garment", "face"}
            else generate_identity_scene(job)
        )

        identity_score = evaluate_identity(base, job.face_refs)

        body = (
            base
            if body_matches_reference(base, job.body_refs)
            else correct_body_proportions(base, job.body_refs)
        )

        edited, garment_eval = replace_and_validate_garment(
            base_image=body,
            product_images=job.product_urls,
            garment_type=job.garment_type,
        )

        final = restore_identity_face(
            identity_source=base,
            edited_image=edited,
        )

        output_key = persist_image(final, job)
        persist_result(
            job_id=job.job_id,
            output_key=output_key,
            identity_score=identity_score,
            garment_passed=garment_eval.passed,
        )
        mark_status(job.job_id, "completed")

    except Exception as exc:
        mark_status(job.job_id, "failed", error=str(exc))
        raise


# Stub functions intentionally omitted: this is a portfolio excerpt, not the
# production repository.
