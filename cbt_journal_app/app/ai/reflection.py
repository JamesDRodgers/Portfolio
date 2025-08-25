"""
AI reflection utilities for the CBT Journal app.

This version strengthens the prompt with:
- Clear guardrails (non-clinical, trauma-informed, LGBTQ+ affirming, no diagnoses).
- Deeper explanations of cognitive distortions & emotional meaning.
- Evidence-for/against review, *three* alternative reframes, and a tiny next-step.
- Crisis language guidelines if intensity is very high or risk language appears.

Output is structured, concise, and compassionate.
"""

from openai import OpenAI
from app.data_models.journal import JournalEntry

def generate_reflection(entry: JournalEntry, api_key: str, model: str = "gpt-4o-mini") -> str:
    """
    Generate an AI-based reflection for a journal entry using a structured,
    safety-aware prompt that returns practical and compassionate feedback.

    Args:
        entry (JournalEntry): User entry with event, thought, emotions, distortion, reframe, intensity (1–7).
        api_key (str): OpenAI API key.
        model (str, optional): Chat model. Defaults to "gpt-4o-mini".

    Returns:
        str: The formatted reflection. On failure, returns a message prefixed with "[AI Error]".
    """
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.6,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a compassionate, CBT-informed helper. "
                        "Use supportive, non-judgmental, inclusive language. "
                        "Be LGBTQ+ affirming and trauma-informed. "
                        "Do NOT diagnose, pathologize, or give medical/legal advice. "
                        "If entry suggests risk (self-harm/others-harm) or intensity is very high, "
                        "encourage seeking immediate human support and crisis resources in a gentle way. "
                        "Avoid moralizing language and 'shoulds'. "
                        "Keep the tone warm and clear; keep sections concise."
                    ),
                },
                {
                    "role": "user",
                    "content": build_prompt(entry),
                },
            ],
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        return f"[AI Error] {str(e)}"


def build_prompt(entry: JournalEntry) -> str:
    """
    Build a structured prompt from a JournalEntry that elicits
    deeper insight, safeguards, and practical next steps.

    Args:
        entry (JournalEntry): The journal entry to transform.

    Returns:
        str: A formatted prompt with explicit sections and constraints for the model.
    """
    emotions_path = entry.emotion_primary
    if entry.emotion_secondary:
        emotions_path += f" → {entry.emotion_secondary}"
    if entry.emotion_tertiary:
        emotions_path += f" → {entry.emotion_tertiary}"

    # Gentle guardrail hints for detection
    risk_hint = (
        "Note: If you notice language that suggests self-harm, hopelessness, "
        "or danger to self/others, include the 'Gentle Safety Note' section."
    )

    # Clear, structured output request
    return f"""
I am practicing cognitive behavioral therapy. Here is my journal entry:

• Date: {entry.date}
• Event: {entry.event}
• Automatic Thought: {entry.thought}
• Emotion(s): {emotions_path}
• Intensity: {entry.emotion_intensity}/7
• Identified Distortion: {entry.cbt_distortion}
• My Current Reframe: {entry.reframing}

Please respond with the following SECTIONS (use these exact headings). Keep total length about 180–300 words, concise but caring.

1) Warm Reflection
- 2–3 sentences validating the experience. Use inclusive, non-clinical language.

2) Distortion Deep-Dive
- Name the distortion in plain words and briefly explain how it typically shows up.
- Map that explanation to THIS entry with 1–2 concrete, specific links to the thought/event.

3) Emotion Check
- What might this emotion be trying to signal or protect?
- Normalize the reported intensity ({entry.emotion_intensity}/7) in one sentence.
- Offer ONE quick grounding or regulation step (e.g., paced breathing, brief movement, or self-talk).

4) Evidence Scan
- Two short bullets of evidence that SUPPORT the automatic thought.
- Two short bullets of evidence that CHALLENGE the automatic thought.

5) Balanced Reframe Options
- Provide THREE alternative reframes (numbered). Each should be kind, realistic, and specific to THIS situation.
- Begin each with phrases like “It’s possible that…”, “Another way to see this is…”, or “A fairer take might be…”.

6) Tiny Next Step
- Offer one next step that takes < 2 minutes and is within the user’s control.

7) Gentle Safety Note (only if warranted)
- {risk_hint}
- If intensity seems ≥ 6/7 or risk language is present, write one brief, compassionate sentence encouraging reaching out to a trusted person or local resources. Do NOT include hotline numbers; suggest contacting local emergency services or a trusted clinician if in immediate danger.

Constraints & Style:
- No medical or diagnostic claims. No moralizing. No “should” statements directed at the user.
- Be concrete and practical. Keep a warm, invitational tone.
- Avoid filler like “as an AI”. Do not repeat the headings’ instructions; just produce the sections.
""".strip()
