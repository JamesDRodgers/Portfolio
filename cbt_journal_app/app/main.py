"""
Main entry point for the CBT Journal app.

This script initializes and launches the Gradio UI for the application.
It imports the UI factory (`create_ui`) from `app.interfaces.gradio_ui`
and runs it with `share=True` so that a public link is available
for sharing.

Usage:
    python -m app.main

This will start the Gradio app and display both a local URL and a
public `.gradio.live` URL for access.
"""

from app.interfaces.gradio_ui import create_ui

if __name__ == "__main__":
    app = create_ui()
    app.launch(share=True)
