import logging
import os

import bdrk
from bdrk.utils.exceptions import BedrockClientNotFound
from bdrk.utils.vars import Constants
from spanlib.infrastructure.kubernetes.env_var import (
    BEDROCK_ENVIRONMENT_ID,
    BEDROCK_PIPELINE_ID,
    BEDROCK_PIPELINE_RUN_ID,
    BEDROCK_PROJECT_ID,
    BEDROCK_RUN_STEP_NAME,
)
from spanlib.types import PipelineRunStatus

from .base import RunContext

_logger = logging.getLogger(Constants.MAIN_LOG)


class OrchestratedRunContext(RunContext):
    def __init__(self):
        """Initialize the run context, register the necessary variables"""
        self.project_id = os.getenv(BEDROCK_PROJECT_ID)
        self.environment_id = os.getenv(BEDROCK_ENVIRONMENT_ID)
        self.pipeline_id = os.getenv(BEDROCK_PIPELINE_ID)
        self.run_id = os.getenv(BEDROCK_PIPELINE_RUN_ID)
        self.step_name = os.getenv(BEDROCK_RUN_STEP_NAME)

    def __enter__(self):
        """Enter the run context, register it with the bedrock_client"""
        if bdrk.bedrock_client is None:
            raise BedrockClientNotFound
        # First, need to register the run context to block other runs
        bdrk.bedrock_client.init_run_context(self)
        try:
            _logger.info(f"Run started: {self.pipeline_id}-run{self.run_id}")
        except Exception as e:
            # Clean up the run context if the run cannot start
            bdrk.bedrock_client.exit_run_context()
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the run context, unregister it with the bedrock_client"""
        status = PipelineRunStatus.SUCCEEDED if exc_type is None else PipelineRunStatus.FAILED
        _logger.info(f"Run {status}: {self.pipeline_id}-run{self.run_id}")
        # Always exit the context
        bdrk.bedrock_client.exit_run_context()
        _logger.info("Run exitted")
        return True if exc_type is None else False
