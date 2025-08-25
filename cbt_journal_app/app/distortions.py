"""
Cognitive Distortions module for the CBT Journal app.

This module defines a dictionary of common cognitive distortions
used in Cognitive Behavioral Therapy (CBT). It also provides
helper functions to retrieve all distortions, just the names,
or detailed descriptions for use in the UI.

Reference distortions include patterns such as:
- All-or-Nothing Thinking
- Overgeneralization
- Catastrophizing
- Emotional Reasoning
and others.
"""

from typing import Dict, List, Tuple

#: Dictionary of CBT distortions.
#: Keys are distortion names, values are short descriptions.
CBT_DISTORTIONS: Dict[str, str] = {
    "All-or-Nothing Thinking": "Viewing situations in black-and-white terms, with no middle ground.",
    "Overgeneralization": "Seeing a single negative event as a never-ending pattern of defeat.",
    "Mental Filter": "Dwelling on a single negative detail and ignoring the positive.",
    "Disqualifying the Positive": "Rejecting positive experiences by insisting they 'don't count.'",
    "Jumping to Conclusions": "Assuming the worst without supporting evidence.",
    "Catastrophizing": "Expecting the worst possible outcome.",
    "Emotional Reasoning": "Assuming that negative emotions reflect reality.",
    "Should Statements": "Using 'should' or 'must' statements that create guilt or frustration.",
    "Labeling": "Identifying yourself or others with negative labels.",
    "Personalization": "Taking responsibility for things outside your control.",
    "Blaming": "Holding others fully responsible for your emotions or outcomes.",
    "Control Fallacies": "Believing you are either helpless or responsible for everyone.",
    "Fallacy of Fairness": "Believing everything must be fair by your standards.",
    "Heaven's Reward Fallacy": "Expecting that sacrifice will be rewarded, feeling angry when it isn't."
}

def get_all_distortions() -> List[Tuple[str, str]]:
    """
    Get all cognitive distortions with their descriptions.

    Returns:
        List[Tuple[str, str]]: A list of (name, description) pairs
        for all distortions in the dictionary.
    """
    return list(CBT_DISTORTIONS.items())

def get_distortion_names() -> List[str]:
    """
    Get the names of all cognitive distortions.

    Returns:
        List[str]: A list of distortion names (keys).
    """
    return list(CBT_DISTORTIONS.keys())

def get_distortion_description(name: str) -> str:
    """
    Get the description for a given distortion.

    Args:
        name (str): The distortion name.

    Returns:
        str: The description of the distortion, or
        "No description available." if not found.
    """
    return CBT_DISTORTIONS.get(name, "No description available.")
