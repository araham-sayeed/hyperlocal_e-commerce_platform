"""Azure Blob and file storage (Level 3). Level 1: return placeholder URLs."""

from uuid import uuid4


def placeholder_image_url(filename: str) -> str:
    return f"https://example.blob.core.windows.net/dev/{uuid4().hex}/{filename}"
