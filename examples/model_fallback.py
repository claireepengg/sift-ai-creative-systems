"""Sanitized representative excerpt — not production Sift source.

A small version of the retry/fallback pattern used around external multimodal
image services.
"""

import time


TRANSIENT_HINTS = (
    "timeout",
    "connection",
    "service unavailable",
    "502",
    "503",
)


def is_transient(exc: Exception) -> bool:
    text = f"{type(exc).__name__}: {exc}".lower()
    return any(hint in text for hint in TRANSIENT_HINTS)


def generate_with_fallback(client, models, contents, attempts_per_model=3):
    last_error = None

    for model in models:
        for attempt in range(attempts_per_model):
            try:
                return client.generate(model=model, contents=contents)
            except Exception as exc:
                last_error = exc
                if not is_transient(exc):
                    raise
                if attempt < attempts_per_model - 1:
                    time.sleep(2 ** attempt)

    raise RuntimeError("All configured image models failed") from last_error
