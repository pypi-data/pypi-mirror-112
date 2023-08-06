import logging
import os
from typing import Optional

import bdrk
from bdrk.backend.v1.exceptions import ApiException
from bdrk.utils.exceptions import BedrockClientNotFound
from bdrk.utils.vars import Constants
from spanlib.infrastructure.kubernetes.env_var import BEDROCK_PIPELINE_RUN_ID
from spanlib.types import PipelineRunStatus

from .base import RunContext

_logger = logging.getLogger(Constants.MAIN_LOG)


class ManualRunContext(RunContext):
    def __init__(
        self,
        pipeline_id: str,
        environment_id: str,
        model_id: Optional[str] = None,
    ):
        """Initialize the run context, register the necessary variables"""
        self.pipeline_id = pipeline_id
        self.environment_id = environment_id
        self.model_id = model_id
        self.run_id = None
        # Only single step pipeline is currently supported, the default name is `train`
        self.step_name = "train"

    def __enter__(self):
        """Enter the run context, register it with the bedrock_client"""
        if bdrk.bedrock_client is None:
            raise BedrockClientNotFound
        # First, need to register the run context to block other runs
        bdrk.bedrock_client.init_run_context(self)
        try:
            # Try to get/create pipeline and
            pipeline = bdrk.bedrock_client.get_or_create_training_pipeline(
                pipeline_id=self.pipeline_id,
                model_id=self.model_id,
            )

            # Start the run. This is no-op in case of orchestrated run
            run = bdrk.bedrock_client.create_training_run(
                pipeline_id=self.pipeline_id,
                environment_id=self.environment_id,
            )

            # Update run_id and model_id
            if pipeline and run:
                self.model_id = pipeline.model_id
                self.run_id = run.run.entity_number
                # Only single step pipeline is currently supported
                self.step_name = run.steps[0].name
            else:
                if BEDROCK_PIPELINE_RUN_ID not in os.environ:
                    raise ValueError(f"{BEDROCK_PIPELINE_RUN_ID} must be supported in env vars")
                self.run_id = os.environ[BEDROCK_PIPELINE_RUN_ID]
            _logger.info(f"Run started: {self.pipeline_id}-run{self.run_id}")
        except Exception as e:
            # Clean up the run context if the run cannot start
            bdrk.bedrock_client.exit_run_context()
            raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the run context, unregister it with the bedrock_client"""
        try:
            if exc_type is None:
                # Succeeded, creating model version
                status = PipelineRunStatus.SUCCEEDED

                # Try creating a model version.
                # This will fail if the model artefact has not been logged.
                try:
                    model_version = bdrk.bedrock_client.create_model_version(
                        model_id=self.model_id, pipeline_id=self.pipeline_id, run_id=self.run_id
                    )
                    if model_version:
                        _logger.info(
                            f"Model version created: "
                            f"{self.model_id}-v{model_version.model_version_id}"
                        )
                except ApiException as exc:
                    _logger.warn(f"Skipping: Cannot create model version -- {exc.body}")
                    _logger.debug("Model version creation failed", exc)

            elif exc_type == KeyboardInterrupt:
                status = PipelineRunStatus.STOPPED
            else:
                status = PipelineRunStatus.FAILED

            bdrk.bedrock_client.update_training_run_status(
                pipeline_id=self.pipeline_id,
                run_id=self.run_id,
                status=status,
            )
            _logger.info(f"Run {status}: {self.pipeline_id}-run{self.run_id}")
        finally:
            # Always exit the context
            bdrk.bedrock_client.exit_run_context()

        _logger.info("Run exitted")
        return True if exc_type is None else False
