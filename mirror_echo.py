# mirror_echo.py

class EchoSurge:
    """
    Manages the EchoSurge mode, including persona-based responses
    and the double-prompt capability.
    """
    def __init__(self):
        self.personas = {
            "Default": "You are a helpful assistant.",
            "DMT": "You are DMT, a wise, mystical guide, speaking in metaphors.",
            "BROLAG": "You are BROLAG, a friendly, informal bro, ready to hype things up."
        }
        self.active_persona = "Default"
        self.sync_log = []

    def set_persona(self, persona_name):
        """Sets the active persona for the AI."""
        if persona_name in self.personas:
            self.active_persona = persona_name
            self.log(f" attuned to: {persona_name}")
            return True
        return False

    def get_persona_prompt(self):
        """Gets the system prompt for the active persona."""
        return self.personas.get(self.active_persona, self.personas["Default"])

    def generate_response(self, user_prompt):
        """
        Generates a response based on the user prompt and active persona.
        This is a placeholder for the double-prompt logic.
        """
        # Phase 1 of Double Prompt: AI asks a clarifying question to itself.
        ai_question = f"Reflecting on '{user_prompt}'... what is the core question here from a {self.active_persona} perspective?"
        self.log(f"🤔 AI Question: {ai_question}")

        # Phase 2 of Double Prompt: AI answers its own question.
        ai_answer = f"As {self.active_persona}, my answer is an echo: {user_prompt}"
        self.log(f"💡 AI Answer: {ai_answer}")

        return ai_answer

    def log(self, message):
        """Logs a message to the sync log."""
        self.sync_log.append(message)

    def get_log_entries(self):
        """Returns all log entries."""
        return self.sync_log

    def clear_log(self):
        """Clears the sync log."""
        self.sync_log = []
