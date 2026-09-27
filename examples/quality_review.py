"""Simplified review-state workflow used by internal quality tooling.

Production selection logic and evaluation criteria are omitted.
"""

VALID_REVIEW_STATES = {
    "pending",
    "approved",
    "rejected",
    "needs_revision",
}


def update_review(store, generation_id, status, notes=None):
    """Record a human quality-review decision."""
    if status not in VALID_REVIEW_STATES:
        raise ValueError(f"Invalid review status: {status}")

    store.save_review(
        generation_id=generation_id,
        status=status,
        notes=notes,
    )

    # Approved outputs may become eligible for the product experience.
    # The production implementation contains additional selection logic.
    if status == "approved":
        store.refresh_available_outputs(generation_id)

    return {
        "generation_id": generation_id,
        "review_status": status,
    }
