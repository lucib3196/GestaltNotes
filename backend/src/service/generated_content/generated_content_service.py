import asyncio
from collections.abc import Sequence
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from src.core.logger import logger
from src.model import MCQV1, GeneratedMCQ, MCQResponseV1
from src.service.generated_content.exceptions import (
    GeneratedContentBatchSaveError,
    GeneratedContentDeletionError,
    GeneratedContentNotFoundError,
    GeneratedContentPersistenceError,
    GeneratedContentRetrievalError,
    GeneratedContentValidationError,
    UnsupportedSchemaVersionError,
)
from src.utils import convert_uuid, to_serializable

ID = str | UUID


class GeneratedMCQService:
    def __init__(self, session: Session) -> None:
        """Initialize the generated MCQ service with a database session."""
        self._session = session

    # Retrieval
    def retrieve_mcq(self, quiz_id: ID) -> GeneratedMCQ | None:
        """Retrieve a generated MCQ by quiz ID."""
        try:
            query = select(GeneratedMCQ).where(GeneratedMCQ.id == convert_uuid(quiz_id))
            return self._session.exec(query).first()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentRetrievalError(
                f"Failed to retrieve generated MCQ by quiz id '{quiz_id}'."
            ) from e

    async def aretrieve_mcq(self, quiz_id: ID) -> GeneratedMCQ | None:
        return await asyncio.to_thread(self.retrieve_mcq, quiz_id)

    async def retrieve_all_mcq_user(self, user_id: ID) -> Sequence[GeneratedMCQ]:
        """Retrieve all generated MCQs for a user ID."""
        try:
            query = select(GeneratedMCQ).where(
                GeneratedMCQ.user_id == convert_uuid(user_id)
            )
            return self._session.exec(query).all()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentRetrievalError(
                f"Failed to retrieve generated MCQs for user id '{user_id}'."
            ) from e

    async def retrive_all_mcq_user_quiz(
        self, user_id: ID, schema_version: int = 1
    ) -> Sequence[MCQV1]:
        """Retrieve and validate all generated MCQs for a user as schema models."""
        try:
            qs = await self.retrieve_all_mcq_user(user_id)
            return [self._validate_quiz(q.quiz_data, schema_version) for q in qs]

        except GeneratedContentValidationError as e:
            raise e
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentRetrievalError(
                f"Failed to retrieve and validate generated MCQs for user id '{user_id}'."
            ) from e

    async def retrieve_all_mcq_thread(self, thread_id: ID) -> Sequence[GeneratedMCQ]:
        """Retrieve all generated MCQs for a thread ID."""
        try:
            query = select(GeneratedMCQ).where(
                GeneratedMCQ.thread_id == convert_uuid(thread_id)
            )
            return self._session.exec(query).all()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentRetrievalError(
                f"Failed to retrieve generated MCQs for thread id '{thread_id}'."
            ) from e

    async def delete_mcq(self, quiz_id: ID) -> bool:
        """Delete a generated MCQ by quiz ID."""
        try:
            quiz = await self.aretrieve_mcq(quiz_id)
            if not quiz:
                raise GeneratedContentNotFoundError(str(quiz_id))
            self._session.delete(quiz)
            self._session.commit()
            return True
        except GeneratedContentNotFoundError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentDeletionError(
                f"Failed to delete generated MCQ with quiz id '{quiz_id}'."
            ) from e

    # Saving mechanism
    def add_mcq(
        self, quiz: Any, user_id: ID, thread_id: ID, schema_version: int = 1
    ) -> GeneratedMCQ:
        """Validate and save a generated MCQ for a user/thread."""
        try:
            quiz_data = self._validate_quiz(quiz, schema_version)
            if quiz_data.id:
                existing = self.retrieve_mcq(quiz_id=quiz_data.id)

                if existing:
                    logger.debug(
                        f"Question with id already exists {quiz_data.id}",
                    )
                    return existing

            gen_mcq = GeneratedMCQ(
                quiz_data=to_serializable(quiz_data),
                schema_version=schema_version,
                user_id=convert_uuid(user_id),
                thread_id=convert_uuid(thread_id),
                id=quiz_data.id,
            )
            self._session.add(gen_mcq)
            self._session.commit()
            self._session.flush()
            return gen_mcq
        except GeneratedContentValidationError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentPersistenceError(
                f"Failed to save generated MCQ for user id '{user_id}' and thread id '{thread_id}'."
            ) from e

    async def async_add_mcq(
        self, quiz: Any, user_id: ID, thread_id: ID, schema_version: int = 1
    ) -> GeneratedMCQ:
        """Asynchronously validate and save a generated MCQ."""
        return await asyncio.to_thread(
            self.add_mcq, quiz, user_id, thread_id, schema_version
        )

    def batch_add_mcq(
        self, data: Any, user_id: ID, thread_id: ID, schema_version: int = 1
    ) -> list[GeneratedMCQ]:
        """Validate and save a batch of generated MCQs for a user/thread."""
        try:
            quiz_data = self._validate_quiz_payload(data, schema_version)
            questions = quiz_data.payload
            return [
                self.add_mcq(q, user_id, thread_id, schema_version) for q in questions
            ]
        except GeneratedContentValidationError:
            raise
        except GeneratedContentPersistenceError:
            raise
        except SQLAlchemyError as e:
            self._session.rollback()
            raise GeneratedContentBatchSaveError(
                f"Failed to batch save generated MCQs for user id '{user_id}' and thread id '{thread_id}'."
            ) from e

    async def async_batch_add_mcq(
        self, data: Any, user_id: ID, thread_id: ID, schema_version: int = 1
    ) -> list[GeneratedMCQ]:
        """Asynchronously validate and save a batch of generated MCQs."""
        return await asyncio.to_thread(
            self.batch_add_mcq, data, user_id, thread_id, schema_version
        )

    @classmethod
    def _validate_quiz(cls, data: Any, schema_version: int) -> MCQV1:
        """Validate a single MCQ payload against the supported schema version."""
        try:
            if schema_version == 1:
                if isinstance(data, MCQV1):
                    return data
                return MCQV1.model_validate(data)
            raise UnsupportedSchemaVersionError(schema_version)
        except UnsupportedSchemaVersionError:
            raise
        except Exception as e:
            raise GeneratedContentValidationError(
                f"Failed to validate MCQ payload for schema version {schema_version}: {e}"
            ) from e

    @classmethod
    def _validate_quiz_payload(cls, data: Any, schema_version: int) -> MCQResponseV1:
        """Validate an MCQ response payload against the supported schema version."""
        try:
            if schema_version == 1:
                return MCQResponseV1.model_validate(data)
            raise UnsupportedSchemaVersionError(schema_version)
        except UnsupportedSchemaVersionError:
            raise
        except Exception as e:
            raise GeneratedContentValidationError(
                f"Failed to validate MCQ response payload for schema version {schema_version}: {e}"
            ) from e


# Backward-compatible alias
GeneratedContentDb = GeneratedMCQService


if __name__ == "__main__":
    import json
    from pathlib import Path

    from sqlmodel import Session, SQLModel, create_engine

    data = json.loads(Path("src/service/generated_content/test.json").read_text())
    result = GeneratedMCQService._validate_quiz_payload(data, schema_version=1)
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        gen = GeneratedMCQService(session)
        gen.batch_add_mcq(data=data, thread_id=uuid4(), user_id=uuid4())
