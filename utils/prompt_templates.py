def build_prompt(role, context, task, output_format):
    """
    Build a structured AI prompt.
    """

    prompt = f"""
ROLE:
{role}

CONTEXT:
{context}

TASK:
{task}

OUTPUT FORMAT:
{output_format}

IMPORTANT:
Do not invent facts.
Clearly identify assumptions.
"""

    return prompt.strip()
