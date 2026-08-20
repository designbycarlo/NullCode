# gui_coding_agent

A lightweight, open‑source **GUI‑oriented coding assistant** that runs entirely in the terminal.  
It leverages only **free, open‑source models** available via Ollama (e.g., `phi3:mini`, `mistral:7b`, `llama3:8b`) and provides a simple interactive UI for describing coding tasks and receiving generated code suggestions.

## Features

- **Terminal‑style GUI** built with `urwid` (ncurses‑like) for a clean, responsive interface.
- **Model‑agnostic**: works with any Ollama model that supports the `/generate` API.
- **Zero‑install for the UI** – just `pip install -r requirements.txt`.
- **Extensible**: add custom prompts, save generated snippets, or integrate with your own codebase.

## Quick Start

1. **Install Ollama** (if you haven't already): https://ollama.com  
   Pull a free model, e.g.:

   ```bash
   ollama pull phi3:mini
   ```

2. **Clone & install**:

   ```bash
   git clone https://github.com/yourname/gui_coding_agent.git
   cd gui_coding_agent
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the agent**:

   ```bash
   ./run.sh
   ```

   You’ll see a simple full‑screen UI prompting you for a coding task.  
   Type your request (e.g., “Create a Python function that sorts a list”) and hit **Enter**.  
   The agent will call the selected model and display the generated code.

## Configuration

- Edit `config.json` to switch models, adjust temperature, or set a custom system prompt.
- The default configuration uses `phi3:mini` with a temperature of `0.7`.

## License

MIT © 2025 Your Name

---

**Enjoy coding!** 🎉