"""AgentCore CLI entrypoint (staged into build/runtime/ by scripts/deploy.py)."""
from ict_pipeline.runtime import app, invoke  # noqa: F401

if __name__ == "__main__":
    app.run()
