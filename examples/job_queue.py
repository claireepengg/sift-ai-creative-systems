"""Simplified database-backed job queue.

The production database schema and connection configuration are omitted.
"""


class JobQueue:
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory

    def claim_next(self):
        """Atomically claim the oldest pending job."""
        with self.connection_factory() as connection:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT id
                  FROM jobs
                 WHERE status = 'pending'
                 ORDER BY created_at ASC
                 LIMIT 1
                 FOR UPDATE SKIP LOCKED
                """
            )

            row = cursor.fetchone()
            if row is None:
                connection.commit()
                return None

            cursor.execute(
                """
                UPDATE jobs
                   SET status = 'running',
                       updated_at = CURRENT_TIMESTAMP
                 WHERE id = %s
                """,
                (row["id"],),
            )

            connection.commit()
            return row["id"]

    def update_status(self, job_id, status, error_message=None):
        with self.connection_factory() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE jobs
                   SET status = %s,
                       error_message = %s,
                       updated_at = CURRENT_TIMESTAMP
                 WHERE id = %s
                """,
                (status, error_message, job_id),
            )

            connection.commit()
