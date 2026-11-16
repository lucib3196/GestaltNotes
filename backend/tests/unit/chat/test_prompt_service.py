import pytest
import pytest_asyncio
from authorization import AccessDeniedError

from backend.accounts.models import User
from backend.chat.model import Prompt, PromptBase, PromptUpdate
from backend.chat.service.prompt_service import (
    PaginationOptions,
    PromptAccessGate,
    PromptService,
)


@pytest.fixture
def service(db_session) -> PromptService:
    return PromptService(db_session, access=PromptAccessGate())


@pytest_asyncio.fixture
async def user(make_user) -> User:
    return await make_user(first_name="Owner")


@pytest.fixture
def prompt_data() -> PromptBase:
    return PromptBase(
        title="Study guide",
        description="Summarize lecture notes",
        content="Turn these notes into a study guide.",
    )


@pytest.mark.asyncio
async def test_create_prompt_saves_all_fields_and_owner(
    service, user, prompt_data, db_session
):
    created = await service.create(prompt_data, user)
    prompt_id = created.id
    db_session.expunge_all()

    stored = db_session.get(Prompt, prompt_id)

    assert stored is not None
    assert stored.user_id == user.id
    assert stored.model_dump(include={"title", "description", "content"}) == (
        prompt_data.model_dump()
    )


@pytest.mark.asyncio
async def test_owner_can_retrieve_saved_prompt(service, user, prompt_data, db_session):
    created = await service.create(prompt_data, user)
    prompt_id = created.id
    db_session.expunge_all()

    retrieved = await service.get_prompt_by_id(prompt_id, user)

    assert retrieved.id == prompt_id
    assert retrieved.content == prompt_data.content


@pytest.mark.asyncio
async def test_update_prompt_persists_changed_fields(
    service, user, prompt_data, db_session
):
    created = await service.create(prompt_data, user)
    update = PromptUpdate(
        title="Updated guide",
        description="Create review questions",
        content="Generate questions from these notes.",
    )

    await service.update_prompt(created.id, update, user)
    prompt_id = created.id
    db_session.expunge_all()
    stored = await service.get_prompt_by_id(prompt_id, user)

    assert stored.model_dump(include={"title", "description", "content"}) == (
        update.model_dump()
    )
    assert stored.user_id == user.id


@pytest.mark.asyncio
async def test_list_prompts_returns_only_current_users_prompts(
    service, user, prompt_data, make_user
):
    other_user = await make_user()
    owned = await service.create(prompt_data, user)
    await service.create(prompt_data, other_user)

    prompts = await service.list_user_prompts(user)

    assert [prompt.id for prompt in prompts] == [owned.id]
    assert prompts[0].content == prompt_data.content


@pytest.mark.asyncio
async def test_list_prompt_summaries_returns_description_without_content(
    service, user, prompt_data, make_user
):
    owned = await service.create(prompt_data, user)
    await service.create(prompt_data, await make_user())

    summaries = await service.list_user_prompts_by_title(user)

    assert [summary.model_dump() for summary in summaries] == [
        {
            "id": owned.id,
            "title": prompt_data.title,
            "description": prompt_data.description,
        }
    ]


@pytest.mark.asyncio
async def test_list_prompts_applies_sort_offset_and_limit(service, user):
    created = [
        await service.create(PromptBase(title=title, content="Content"), user)
        for title in ("First", "Second", "Third")
    ]

    prompts = await service.list_user_prompts(
        user, PaginationOptions(sort="created", order="asc", offset=1, limit=1)
    )

    assert [prompt.id for prompt in prompts] == [created[1].id]


@pytest.mark.asyncio
async def test_another_user_cannot_access_owners_prompt(
    service, user, prompt_data, make_user
):
    created = await service.create(prompt_data, user)
    other_user = await make_user()

    with pytest.raises(AccessDeniedError):
        await service.get_prompt_by_id(created.id, other_user)
