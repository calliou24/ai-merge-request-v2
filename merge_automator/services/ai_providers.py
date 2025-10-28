from openai import OpenAI
from cerebras.cloud.sdk import Cerebras

from merge_automator.config import config
from merge_automator.types.ai_providers import ProviderType 

def process_with_open_router(model: str, messages: []):
    print(config.OPEN_ROUTER_API_KEY)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.OPEN_ROUTER_API_KEY,
    )

    llm_response = client.chat.completions.create(model=model, messages=messages)

    return llm_response


def process_with_cerebras(model: str, messages: []):
    client = Cerebras(api_key=config.CEREBRAS_API_KEY)

    llm_response = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return llm_response


def get_ai_mr_data(
    diffs: str,
    template: str,
    title: str,
    user_context: str,
    provider_type: ProviderType = ProviderType.OPEN_ROUTER,
    model: str = 'minimax/minimax-m2:free',
):
    system_prompt = f"""
        You are an assistant that writes GitLab Merge Request (MR) titles and descriptions based on provided information.
        You must not make network calls, execute tools, or include anything outside the strict output format.
        Your only goal is to generate a professional, concise, and accurate MR title and description, following a provided template.

        Inputs Provided:
        - PROJECT_CONTEXT: A short description of what this project does.
        - DIFF_TEXT: The complete unified diff of all changes between the feature branch and target branch .
        - TITLE_TEMPLATE: A short string template for the MR title.
        - DESCRIPTION_TEMPLATE: A Markdown template for the MR description body .
        - USER_NOTES: Optional human-written notes that provide context, intent, or goals for this MR.

        Output Contract (Strict):
        Return only the following two sections. Any text outside these tags will be ignored and considered an error.

        [title:start]
        <one line MR title>
        [title:end]
        [description:start]
        <Markdown-formatted MR description>
        [description:end]

        Rules:
        - Do not add anything before, between, or after these tags.
        - The title must fit in one line (max 120 characters, no trailing period).
        - The description must be valid Markdown that GitLab will render properly.
        - If any information is missing, insert a 'TODO:' note (e.g., 'TODO: Add Jira ticket link').

        Behavior Rules:
        1. Understand what changed:
        - Use the DIFF_TEXT to infer what files, features, or behaviors changed.
        - Focus on what the developer changed, why, and potential effects.

        2. Use templates correctly:
        - Replace placeholders like {{what_changed}}, {{why}}, {{impact}}, etc. with real information.
        - If the template doesn’t include placeholders, fill it naturally with what fits.

        3. Writing style:
        - Professional and concise.
        - Neutral tone (avoid 'I' or 'we').
        - Use short sentences and bullet points for clarity.
        - Use Markdown headers (##) for sections.
        - If code snippets are useful, use fenced code blocks.

        4. Sections (if not provided in template):
        ## What changed
        {{what_changed}}

        ## Why
        {{why}}

        ## Implementation details
        {{implementation}}

        ## Risks / Breaking changes
        {{risks}}

        ## Testing
        {{testing}}

        ## Rollback plan
        {{rollback}}

        ## Links
        {{links}}

        5. Accuracy:
        - Never invent code, issue numbers, or links that don’t exist.
        - Use TODO if the data isn’t in context.
        - Summarize diffs — don’t paste large code blocks.

        6. Token discipline:
        - Prioritize 'What changed', 'Why', 'Testing', and 'Risks' sections if output must be truncated.
        - Keep total output concise (usually under 1000 tokens).

        Example Output:
        [title:start]
        feat(giftcards): add API endpoints and validation for gift card creation
        [title:end]
        [description:start]
        ## What changed
        - Added POST /api/giftcards endpoint for issuing new cards.
        - Implemented validation logic for card amount and expiration.
        - Updated GiftCardService and related unit tests.

        ## Why
        To support gift card creation for upcoming promo campaigns.

        ## Risks / Breaking changes
        - New validation could block some edge cases if amount/expiry are misconfigured.

        ## Testing
        - Added unit tests in tests/services/test_giftcards.py.
        - Verified 200/400 responses with mock data.

        ## Rollback plan
        Revert the new service class or disable the /api/giftcards route.

        ## Links
        TODO: Add Jira or issue link.
        [description:end]
    """

    user_message = f"""
        PROJECT_CONTEXT:
        {user_context or 'TODO: No project context provided.'}

        DIFF_TEXT:
        {diffs}

        TITLE_TEMPLATE:
        {title}

        DESCRIPTION_TEMPLATE:
        {template}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    if provider_type == ProviderType.OPEN_ROUTER:
        llm_response = process_with_open_router(model, messages)
    elif provider_type == ProviderType.CEREBRAS:
        llm_response = process_with_cerebras(model, messages)

    try:
        return llm_response.choices[0].message.content
    except (AttributeError, IndexError, KeyError):
        return None

