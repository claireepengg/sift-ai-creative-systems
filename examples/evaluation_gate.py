"""Sanitized representative excerpt — not production Sift source.

Illustrates how subjective visual failure modes were converted into explicit,
structured evaluation signals and then fed back into generation retries.
"""

from dataclasses import dataclass


GARMENT_CHECKS = (
    "color",
    "pattern",
    "fabric",
    "neckline",
    "straps_or_sleeves",
    "fit",
    "hem",
    "details",
)


@dataclass
class GarmentEvaluation:
    passed: bool
    failed_checks: list[str]
    reason: str
    score: int


def evaluate_garment(multimodal_model, output_image, product_images) -> GarmentEvaluation:
    """Compare generated clothing directly with product photography."""

    schema = {
        "passed": "boolean",
        "failures": "list[str]",
        "reason": "string",
        "scores": {name: "boolean" for name in GARMENT_CHECKS},
    }

    result = multimodal_model.compare(
        output=output_image,
        references=product_images,
        requested_schema=schema,
        instruction=(
            "Treat product images as the only ground truth. "
            "Evaluate each visible garment attribute independently."
        ),
    )

    score = sum(bool(result["scores"].get(name)) for name in GARMENT_CHECKS)
    return GarmentEvaluation(
        passed=bool(result["passed"]),
        failed_checks=list(result["failures"]),
        reason=result["reason"],
        score=score,
    )


def generate_with_feedback(generator, evaluator, base_image, product_images, max_attempts=5):
    best = None

    for attempt in range(max_attempts):
        feedback = None if best is None else {
            "failed_checks": best[1].failed_checks,
            "reason": best[1].reason,
        }

        candidate = generator.edit(
            base_image=base_image,
            product_images=product_images,
            correction_feedback=feedback,
        )
        evaluation = evaluator(candidate, product_images)

        if best is None or evaluation.score > best[1].score:
            best = (candidate, evaluation)

        if evaluation.passed:
            return candidate, evaluation

    return best
