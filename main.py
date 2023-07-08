from fastapi import FastAPI
from api.endpoints import chat_completions, completions
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

app.include_router(completions.router, prefix="/openai/deployments/{deployment_id}/completions)", tags=["completion"])
app.include_router(chat_completions.router, prefix="/openai/deployments/{deployment_id}/chat/completions", tags=["chat_completion"])