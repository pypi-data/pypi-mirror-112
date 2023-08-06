from contextlib import AbstractContextManager
from typing import Optional


class RunContext(AbstractContextManager):
    project_id: str
    environment_id: str
    pipeline_id: str
    run_id: int
    step_name: str
    model_id: Optional[str] = None
