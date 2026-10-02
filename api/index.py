"""
Vercel Python serverless entrypoint.

Mangum adapts the FastAPI ASGI app to the AWS Lambda handler interface
that Vercel's Python runtime expects.

The sys.path insertion below guarantees that `backend.*` is importable
regardless of which working directory Vercel uses when invoking this
file — the repo root is always added to the module search path first.

All application logic lives in backend/. Do not add logic here.
"""

import os
import sys

# Ensure the repository root (the directory that contains backend/) is
# always the first entry on sys.path so that `from backend.xxx import`
# works correctly when Vercel invokes this file from the api/ subdirectory.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from mangum import Mangum          # noqa: E402
from backend.main import app       # noqa: E402, F401

handler = Mangum(app, lifespan="off")
