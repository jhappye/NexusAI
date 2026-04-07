"""
NexusAIAPI Repository Factory for creating repository instances.

This factory is specifically designed for NexusAIAPI repositories that handle
service-layer operations with dependency injection patterns.
"""

from sqlalchemy.orm import Session, sessionmaker

from configs import nexusai_config
from core.repositories import NexusAICoreRepositoryFactory, RepositoryImportError
from libs.module_loading import import_string
from repositories.api_workflow_node_execution_repository import NexusAIAPIWorkflowNodeExecutionRepository
from repositories.api_workflow_run_repository import APIWorkflowRunRepository


class NexusAIAPIRepositoryFactory(NexusAICoreRepositoryFactory):
    """
    Factory for creating NexusAIAPI repository instances based on configuration.

    This factory handles the creation of repositories that are specifically designed
    for service-layer operations and use dependency injection with sessionmaker
    for better testability and separation of concerns.
    """

    @classmethod
    def create_api_workflow_node_execution_repository(
        cls, session_maker: sessionmaker[Session]
    ) -> NexusAIAPIWorkflowNodeExecutionRepository:
        """
        Create a NexusAIAPIWorkflowNodeExecutionRepository instance based on configuration.

        This repository is designed for service-layer operations and uses dependency injection
        with a sessionmaker for better testability and separation of concerns. It provides
        database access patterns specifically needed by service classes, handling queries
        that involve database-specific fields and multi-tenancy concerns.

        Args:
            session_maker: SQLAlchemy sessionmaker to inject for database session management.

        Returns:
            Configured NexusAIAPIWorkflowNodeExecutionRepository instance

        Raises:
            RepositoryImportError: If the configured repository cannot be imported or instantiated
        """
        class_path = nexusai_config.API_WORKFLOW_NODE_EXECUTION_REPOSITORY

        try:
            repository_class = import_string(class_path)
            return repository_class(session_maker=session_maker)
        except (ImportError, Exception) as e:
            raise RepositoryImportError(
                f"Failed to create NexusAIAPIWorkflowNodeExecutionRepository from '{class_path}': {e}"
            ) from e

    @classmethod
    def create_api_workflow_run_repository(cls, session_maker: sessionmaker[Session]) -> APIWorkflowRunRepository:
        """
        Create an APIWorkflowRunRepository instance based on configuration.

        This repository is designed for service-layer WorkflowRun operations and uses dependency
        injection with a sessionmaker for better testability and separation of concerns. It provides
        database access patterns specifically needed by service classes for workflow run management,
        including pagination, filtering, and bulk operations.

        Args:
            session_maker: SQLAlchemy sessionmaker to inject for database session management.

        Returns:
            Configured APIWorkflowRunRepository instance

        Raises:
            RepositoryImportError: If the configured repository cannot be imported or instantiated
        """
        class_path = nexusai_config.API_WORKFLOW_RUN_REPOSITORY

        try:
            repository_class = import_string(class_path)
            return repository_class(session_maker=session_maker)
        except (ImportError, Exception) as e:
            raise RepositoryImportError(f"Failed to create APIWorkflowRunRepository from '{class_path}': {e}") from e
