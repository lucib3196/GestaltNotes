from langgraph.runtime import Runtime

from .context import ExtractionContext, PromptName


def resolve_context_prompts(
    prompt_name: PromptName,
    runtime: Runtime[ExtractionContext],
    *,
    default_prompt: str,
) -> str:
    """Use a nonblank context prompt, falling back to the default."""
    prompt = runtime.context.prompts.get(prompt_name)
    return prompt if prompt and prompt.strip() else default_prompt
