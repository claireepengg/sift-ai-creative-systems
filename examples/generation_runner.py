"""Simplified example of Sift's generation-job orchestration.

The production system contains additional model, image-processing, evaluation,
and recovery stages that are intentionally omitted here.
"""


def run_generation(job_id, store, pipeline):
    """Execute one generation job and persist its final state."""
    store.update_job_status(job_id, "running")

    try:
        job = store.get_job(job_id)

        inputs = store.load_generation_inputs(
            user_id=job.user_id,
            product_id=job.product_id,
            scene_id=job.scene_id,
        )

        result = pipeline.run(inputs)

        output_id = store.save_generation_result(
            job_id=job_id,
            output=result.output,
        )

        store.update_job_status(job_id, "completed")
        return output_id

    except Exception as exc:
        store.update_job_status(
            job_id,
            "failed",
            error_message=str(exc),
        )
        raise
