# Multi_Agent_Uni_project

​A Local-First Desktop Orchestrator powered by LLMs and Reinforcement Learning.
​MAA is a modular desktop assistant that acts as a central "brain" for your computer. Unlike standard chatbots, it doesn't just talk—it does. It uses a local Large Language Model (via LM Studio) to parse natural language into structured intents, which are then routed to specialized agents for execution.
​Key Features:
- ​Local Intelligence: Powered by LM Studio (OpenAI compatible server). No data leaves your machine.
- ​Intent Orchestrator: A specialized "Router" that translates messy human speech (e.g., "find me some python vids") into precise JSON commands.
- ​YouTube Bandit Agent:
​Reinforcement Learning: Uses a Multi-Armed Bandit algorithm to rank videos.
- ​Thompson Sampling: Balances Exploration (trying new topics) vs. Exploitation (showing what you love) using Beta Distributions.
- ​Dynamic Learning: The system learns from your clicks and updates its internal arms.json database in real-time.
​- Note Automation Agent:
​"Double Brain" Workflow: Uses one LLM to understand the command and a second LLM to structure the note content (bullet points, summaries).
​GUI Automation: Uses PyAutoGUI to physically control Windows Sticky Notes, typing out the formatted note for you.
​Kivy Interface: A clean, touch-friendly, cross-platform UI.
​Architecture
​The system follows a strict Decoupled Architecture:
