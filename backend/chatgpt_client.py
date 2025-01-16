"""
This module provides functionality for interacting with OpenAI's ChatGPT asynchronously,
enabling session-based conversation management and enhanced prompt augmentation.

### Overview
The module implements a `ChatGPTClient` class designed to:
- Manage session-specific conversation histories.
- Augment user prompts with contextual information using the `AugmentPrompt` utility.
- Send asynchronous requests to the OpenAI ChatCompletion API and handle responses.
"""

import os
from openai import AsyncOpenAI


api_key = os.getenv("OPENAI_API_KEY")
aclient = AsyncOpenAI(api_key=api_key)  # Ensure you have: pip install --upgrade openai


from augment_prompt import AugmentPrompt


# --- ChatGPT Client (Asynchronous) ---
class ChatGPTClient:
    """
    A client for interacting with OpenAI's ChatGPT asynchronously.

    This class manages session-based interactions with ChatGPT, including:
    - Maintaining user-specific conversation history.
    - Augmenting prompts with contextual information.
    - Sending requests to OpenAI asynchronously and managing responses.

    Attributes:
        augmentor (AugmentPrompt): A utility to generate augmented prompts.
        user_sessions (dict): Stores session-specific conversation history.
    """

    def __init__(self):
        """
        Initialize the ChatGPTClient with an augmentor and a session manager.
        """
        self.augmentor = AugmentPrompt()
        self.user_sessions = {}

    def update_correspondence(self, session_id, message, is_user, clean):
        """
        Update the conversation history for a given session.

        Depending on the `clean` flag, this method either stores the raw user message
        or an augmented version with additional context.

        Args:
            session_id (str): The unique identifier for the user's session.
            message (str): The message content to be stored.
            is_user (bool): Whether the message is from the user (`True`) or the assistant (`False`).
            clean (bool): Whether to store the raw message (`True`) or an augmented version (`False`).

        Notes:
            - Limits conversation history to the last 5 entries to avoid memory overload.
            - Augments messages with prior book recommendations if `clean` is `False`.
        """
        if session_id not in self.user_sessions:
            # Initialize a minimal conversation context
            self.user_sessions[session_id] = [
                {
                    "role": "user",
                    "content": "Provide context for book recommendations."
                },
                {
                    "role": "assistant",
                    "content": "I'm here to assist with book recommendations. What topic are you interested in?"
                }
            ]

        if clean:
            # Just append the message as-is
            self.user_sessions[session_id].append(
                {
                    "role": "user" if is_user else "assistant",
                    "content": message
                }
            )
            if len(self.user_sessions[session_id]) >= 5:
                # Clipping the data - so that the server will not arrive to a
                # state that it has too much data from a specific client that will
                # cause it to crash
                self.user_sessions[session_id] = self.user_sessions[session_id][-5:]
        else:
            # Optionally augment the prompt with prior "books" data or additional instructions
            prev = ""
            n = len(self.user_sessions[session_id]) - 2
            for index, data in enumerate(self.user_sessions[session_id][2:]):
                if index == 0:
                    prev += f"- {index + 1}) (oldest) query:\n"
                elif index + 1 == n:
                    prev += f"- {index + 1}) (latest) query:\n"
                else:
                    prev += f"- {index + 1}) query:\n"
                if "books" in data:
                    for item in data:
                        prev += f"{item['book']} by {item['author_name']}\n"

            # Attach your custom instructions via the Prompt Augmentor
            self.user_sessions[session_id].append(
                {
                    "role": "user" if is_user else "assistant",
                    "content": f"{prev}\n\n{self.augmentor.generate(message)}"
                }
            )

    async def send_prompt(self, session_id, message):
        """
        Send a user prompt to ChatGPT and retrieve the assistant's response.

        This method:
        - Augments the user's prompt with context if necessary.
        - Sends the prompt to OpenAI's ChatCompletion API asynchronously.
        - Stores the assistant's response in the session history.

        Args:
            session_id (str): The unique identifier for the user's session.
            message (str): The user's prompt or message.

        Returns:
            str: The response generated by ChatGPT.

        Raises:
            Exception: If the OpenAI API request fails.
        """
        # 1) Add augmented message (clean=False)
        self.update_correspondence(session_id, message, is_user=True, clean=False)

        # 2) Call ChatCompletion asynchronously
        response = await aclient.chat.completions.create(
            model="gpt-4o",
            messages=self.user_sessions[session_id],
            temperature=0.1,
            #stream=True  # Enable streaming
        )

        # 3) Remove the last augmented message
        self.user_sessions[session_id].pop()

        # 4) Add user message as-is
        self.update_correspondence(session_id, message, is_user=True, clean=True)

        # 5) Extract and store assistant's reply
        reply = response.choices[0].message.content
        self.update_correspondence(session_id, reply, is_user=False, clean=True)

        return reply
