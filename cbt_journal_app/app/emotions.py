"""
Emotion wheel utilities for the CBT Journal app.

This module loads and interacts with the Feeling Wheel JSON file.
The wheel organizes emotions into a hierarchy:

- Primary emotions (e.g., Joy, Anger, Fear)
- Secondary emotions (specific categories under each primary)
- Tertiary emotions (fine-grained descriptors)

It also supports validating emotion paths (primary → secondary → tertiary).
"""

import json
from pathlib import Path
from typing import List, Dict
from app.config import FEELING_WHEEL_PATH

class EmotionWheel:
    """
    A utility class for working with the Feeling Wheel data.

    Attributes:
        emotions (dict): Parsed JSON object containing emotion hierarchy
                         with primary, secondary, and tertiary levels.
    """

    def __init__(self, path: Path = FEELING_WHEEL_PATH):
        """
        Initialize the EmotionWheel.

        Args:
            path (Path): Path to the Feeling Wheel JSON file.
                         Defaults to the configured FEELING_WHEEL_PATH.
        """
        self.emotions = self._load_emotions(path)

    def _load_emotions(self, path: Path) -> Dict:
        """
        Load emotions JSON from file.

        Args:
            path (Path): Path to the Feeling Wheel JSON.

        Returns:
            dict: Parsed JSON structure of emotions.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
        """
        if not path.exists():
            raise FileNotFoundError(f"Feeling wheel JSON not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_primary_emotions(self) -> List[str]:
        """
        Retrieve all primary emotions.

        Returns:
            List[str]: List of primary emotion names (e.g., Joy, Sadness).
        """
        return [item["primary_emotion"] for item in self.emotions["emotions"]]

    def get_secondary_emotions(self, primary: str) -> List[str]:
        """
        Retrieve secondary emotions for a given primary emotion.

        Args:
            primary (str): The primary emotion name.

        Returns:
            List[str]: List of secondary emotions, or [] if not found.
        """
        for item in self.emotions["emotions"]:
            if item["primary_emotion"] == primary:
                return [s["secondary_emotion"] for s in item["secondary_emotions"]]
        return []

    def get_tertiary_emotions(self, primary: str, secondary: str) -> List[str]:
        """
        Retrieve tertiary emotions for a given (primary, secondary) pair.

        Args:
            primary (str): The primary emotion name.
            secondary (str): The secondary emotion name.

        Returns:
            List[str]: List of tertiary emotions, or [] if not found.
        """
        for item in self.emotions["emotions"]:
            if item["primary_emotion"] == primary:
                for s in item["secondary_emotions"]:
                    if s["secondary_emotion"] == secondary:
                        return s["tertiary_emotions"]
        return []

    def validate_emotion_path(self, primary: str, secondary: str, tertiary: str) -> bool:
        """
        Validate whether a primary → secondary → tertiary path exists.

        Args:
            primary (str): The primary emotion name.
            secondary (str): The secondary emotion name.
            tertiary (str): The tertiary emotion name.

        Returns:
            bool: True if the path exists in the Feeling Wheel, else False.
        """
        return tertiary in self.get_tertiary_emotions(primary, secondary)

    def emotion_path_exists(self, primary: str, secondary: str, tertiary: str) -> bool:
        """
        Alias for validate_emotion_path, provided for readability.

        Args:
            primary (str): The primary emotion name.
            secondary (str): The secondary emotion name.
            tertiary (str): The tertiary emotion name.

        Returns:
            bool: True if the emotion path exists, else False.
        """
        return self.validate_emotion_path(primary, secondary, tertiary)
