"""
AI service for transcription and content generation using OpenAI API.
"""
import json
from typing import Dict, Any, Optional
import openai
from openai import OpenAI

from app.core.config import settings
from app.core.prompts import (
    BLOG_POST_PROMPT,
    OUTLINE_PROMPT,
    SOCIAL_POSTS_PROMPT,
    SYSTEM_MESSAGE,
    format_prompt,
)


class AIService:
    """
    Service for AI-powered transcription and content generation.

    Uses OpenAI's Whisper for transcription and GPT-4 for content generation.
    """

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper.

        Args:
            audio_file_path: Path to audio file on disk

        Returns:
            Transcription text

        Raises:
            Exception: If transcription fails
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=settings.OPENAI_TRANSCRIPTION_MODEL,
                    file=audio_file,
                    response_format="text",
                )

            return transcript

        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    async def generate_blog_post(self, transcription: str) -> Dict[str, Any]:
        """
        Generate a blog post from transcription using GPT-4.

        Args:
            transcription: Audio transcription text

        Returns:
            Dictionary containing blog post structure

        Raises:
            Exception: If generation fails
        """
        try:
            prompt = format_prompt(BLOG_POST_PROMPT, transcription)

            response = self.client.chat.completions.create(
                model=settings.OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2500,
            )

            content = response.choices[0].message.content

            # Parse JSON response
            try:
                blog_post = json.loads(content)
                return blog_post
            except json.JSONDecodeError:
                # If response is not JSON, create a simple structure
                return {
                    "title": "Generated Blog Post",
                    "content": content,
                    "word_count": len(content.split()),
                }

        except Exception as e:
            raise Exception(f"Blog post generation failed: {str(e)}")

    async def generate_outline(self, transcription: str) -> Dict[str, Any]:
        """
        Generate an outline from transcription using GPT-4.

        Args:
            transcription: Audio transcription text

        Returns:
            Dictionary containing outline structure

        Raises:
            Exception: If generation fails
        """
        try:
            prompt = format_prompt(OUTLINE_PROMPT, transcription)

            response = self.client.chat.completions.create(
                model=settings.OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=1500,
            )

            content = response.choices[0].message.content

            # Parse JSON response
            try:
                outline = json.loads(content)
                return outline
            except json.JSONDecodeError:
                # If response is not JSON, create a simple structure
                lines = content.split("\n")
                return {
                    "title": "Content Outline",
                    "overview": lines[0] if lines else "",
                    "sections": [{"topic": line, "key_points": []} for line in lines[1:] if line.strip()],
                }

        except Exception as e:
            raise Exception(f"Outline generation failed: {str(e)}")

    async def generate_social_posts(self, transcription: str) -> list:
        """
        Generate social media posts from transcription using GPT-4.

        Args:
            transcription: Audio transcription text

        Returns:
            List of social media post dictionaries

        Raises:
            Exception: If generation fails
        """
        try:
            prompt = format_prompt(SOCIAL_POSTS_PROMPT, transcription)

            response = self.client.chat.completions.create(
                model=settings.OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                max_tokens=2000,
            )

            content = response.choices[0].message.content

            # Parse JSON response
            try:
                result = json.loads(content)
                return result.get("posts", [])
            except json.JSONDecodeError:
                # If response is not JSON, create simple posts from lines
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                return [
                    {
                        "platform": "general",
                        "type": "insight",
                        "content": line,
                        "hashtags": [],
                    }
                    for line in lines[:10]
                ]

        except Exception as e:
            raise Exception(f"Social posts generation failed: {str(e)}")


# Global AI service instance
ai_service = AIService()
