#!/usr/bin/env python3
"""
Terminal‑style GUI coding agent

A minimal interactive coding assistant that runs in a terminal UI
using the urwid library and free Ollama models (phi3:mini, mistral:7b, etc.).
"""

import json
import os
import sys
import urllib.request
from typing import Dict

import urwid as urid

# ----------------------------------------------------------------------
# Load configuration
# ----------------------------------------------------------------------
CONFIG_PATH = "config.json"
if not os.path.exists(CONFIG_PATH):
    sys.exit(f"Config file {CONFIG_PATH} not found.")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG: Dict = json.load(f)

# ----------------------------------------------------------------------
# Ollama client helpers
# ----------------------------------------------------------------------
OLLAMA_HOST = "http://localhost:11434"
MODEL = CONFIG.get("model", "phi3:mini")
TEMPERATURE = CONFIG.get("temperature", 0.7)
MAX_TOKENS = CONFIG.get("max_tokens", 512)


def call_ollama(prompt: str) -> str:
    """
    Send a prompt to Ollama and return the generated text.
    """
    payload = {
        "model": MODEL,
        "prompt": f"### System\nYou are a helpful coding assistant. Output only runnable code.\n\n### User\n{prompt}\n### Assistant:",
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_HOST + "/api/generate", data=body, method="POST"
    )
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=60) as resp:
            resp_data = json.load(resp)
        return resp_data.get("response", "").strip()
    except Exception as exc:
        return f"[Error contacting Ollama: {exc}]"


# ----------------------------------------------------------------------
# UI definition
# ----------------------------------------------------------------------
class CodingAgentApp(urid.Widget):
    """Main UI widget."""

    def __init__(self):
        # Input field
        self.edit = urid.Edit("Enter your coding request (e.g. 'Write a Python function to sort a list'):")
        # Submit button
        self.button = urid.Button("Submit")
        urid.connect_signal(self.button, "clicked", self.on_submit)

        # Output field (read‑only)
        self.output = urid.MultilineEdit(
            "", editable=False, wrap="hard", line_wrap=False, multiline=True
        )
        self.output.set_edit_text("Generated code will appear here...\n")

        # Layout: vertical stack
        pile = urid.Pile([self.edit, self.button, self.output])
        super().__init__(urid.FixedText(""), align="center", valign="top", fmt="%(layer)s")

    def on_submit(self, _button):
        """Callback when the Submit button is pressed."""
        user_prompt = self.edit.edit_text.strip()
        if not user_prompt:
            return  # ignore empty submissions

        # Disable UI while we wait for the model
        self.edit.set_enabled(False)
        self.button.set_enabled(False)
        # simple stdout feedback
        print("Generating code...")
        # Flush to ensure immediate display before potentially long model response
        sys.stdout.flush()

        # Call Ollama
        generated = call_ollama(user_prompt)
        if not generated:
            generated = "[No response]"

        # Show the result
        self.output.set_edit_text(generated + "\n")
        # Optionally clear the input field for the next request
        self.edit.edit_text = ""
        # Re‑enable UI
        self.edit.set_enabled(True)
        self.button.set_enabled(True)


def main():
    """Start the urwid main loop."""
    app = CodingAgentApp()
    loop = urid.MainLoop(app)  # pressing 'q' or escape will quit
    loop.run()


if __name__ == "__main__":
    main()