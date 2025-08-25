"""
Data models for the CBT Journal app.

This module defines the JournalEntry dataclass, which represents
a single journaling record. Entries capture:
- event description
- automatic thoughts
- primary/secondary/tertiary emotions and intensity
- recognized cognitive distortion
- reframed thought
- (optional) AI-generated reflection
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class JournalEntry:
    """
    A data structure representing one CBT journal entry.

    Attributes:
        date (str): Date of the entry (format YYYY-MM-DD).
        event (str): Description of what happened.
        thought (str): The automatic thought about the event.
        emotion_primary (str): The primary emotion selected by the user.
        emotion_secondary (Optional[str]): The secondary emotion, if selected.
        emotion_tertiary (Optional[str]): The tertiary emotion, if selected.
        emotion_intensity (int): Intensity rating (1–7 scale).
        cbt_distortion (str): Cognitive distortion label chosen by the user.
        reframing (str): Balanced reframe or alternative thought.
        ai_reflection (Optional[str]): Optional AI-generated reflection text.
    """

    date: str
    event: str
    thought: str
    emotion_primary: str
    emotion_secondary: Optional[str] = None
    emotion_tertiary: Optional[str] = None
    emotion_intensity: int = 1
    cbt_distortion: str = ""
    reframing: str = ""
    ai_reflection: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the journal entry into a dictionary.

        Returns:
            dict: A dictionary representation of the entry,
                  suitable for JSON serialization.
        """
        return self.__dict__

    @staticmethod
    def from_dict(data: dict) -> "JournalEntry":
        """
        Create a JournalEntry object from a dictionary.

        Args:
            data (dict): Dictionary containing the entry fields.

        Returns:
            JournalEntry: An instantiated JournalEntry object.
        """
        return JournalEntry(**data)
