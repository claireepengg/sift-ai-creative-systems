"""Sanitized representative excerpt — not production Sift source.

Shows the human-review state machine and promotion of the strongest approved
variant after a review decision changes.
"""

VALID_REVIEW_STATES = {"pending", "approved", "rejected", "needs_revision"}


def review_generation(db, job_id: int, status: str, notes: str | None = None):
    if status not in VALID_REVIEW_STATES:
        raise ValueError(f"Invalid review state: {status}")

    db.update_job_review(job_id, status=status, notes=notes)

    moodboard_id = db.moodboard_for_job(job_id)
    if moodboard_id is None:
        return

    approved = db.approved_variants(moodboard_id)

    # Clear the old primary before promoting the strongest approved option.
    db.clear_primary_variant(moodboard_id)

    if approved:
        best = max(approved, key=lambda item: item.likeness_score)
        db.promote_primary(best.variant_id)

    if status == "approved":
        enqueue_search_embedding_refresh(moodboard_id)
