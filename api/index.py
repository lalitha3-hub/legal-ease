# Vercel Python runtime entrypoint.
# Mangum wraps the FastAPI ASGI app as an AWS-Lambda-compatible handler,
# which is what Vercel's @vercel/python builder expects.
# All routes, middleware, and business logic stay in backend/ — do NOT
# add any logic here.

from mangum import Mangum

from backend.main import app  # noqa: F401

handler = Mangum(app, lifespan="off")
