"""
AI prompt templates for content generation.

These prompts are carefully crafted to produce high-quality,
platform-specific content from audio transcriptions.
"""

# =============================================================================
# Blog Post Generation
# =============================================================================
BLOG_POST_PROMPT = """You are an expert content writer specializing in converting audio transcriptions into engaging blog posts.

TASK:
Transform the following audio transcription into a well-structured, SEO-optimized blog post.

REQUIREMENTS:
1. **Title**: Create a compelling, click-worthy title (50-60 characters)
2. **Introduction**: Write an engaging hook that summarizes the main topic (100-150 words)
3. **Body**: Organize content into clear sections with H2/H3 headers
   - Use the natural flow of the conversation
   - Extract key insights and actionable advice
   - Include relevant examples mentioned in the audio
   - Aim for 800-1500 words total
4. **Conclusion**: Summarize key takeaways and include a call-to-action
5. **Tone**: Professional but conversational, easy to read
6. **SEO**: Naturally incorporate relevant keywords based on the topic

FORMAT YOUR RESPONSE AS JSON:
{
  "title": "Blog post title here",
  "meta_description": "SEO meta description (150-160 chars)",
  "introduction": "Introduction paragraph(s)",
  "body_sections": [
    {
      "heading": "Section heading",
      "content": "Section content with multiple paragraphs if needed"
    }
  ],
  "conclusion": "Conclusion paragraph(s)",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "word_count": 1200
}

TRANSCRIPTION:
{transcription}

Generate the blog post now:"""


# =============================================================================
# Outline Generation
# =============================================================================
OUTLINE_PROMPT = """You are an expert at creating structured outlines from audio content.

TASK:
Create a comprehensive, scannable outline from the following audio transcription.

REQUIREMENTS:
1. **Main Topics**: Identify 5-10 main topics discussed
2. **Structure**: Use hierarchical bullet points
3. **Timestamps**: If timestamps are available in the transcription, include them
4. **Key Points**: Extract the most important points under each topic
5. **Actionable Items**: Highlight any action items, tips, or recommendations
6. **Quotes**: Include 2-3 memorable quotes if present

FORMAT YOUR RESPONSE AS JSON:
{
  "title": "Brief title summarizing the content",
  "overview": "One-sentence overview of the content",
  "sections": [
    {
      "topic": "Main topic name",
      "timestamp": "00:05:23" (if available, else null),
      "key_points": [
        "First key point",
        "Second key point"
      ],
      "notable_quote": "Any memorable quote from this section" (optional)
    }
  ],
  "action_items": [
    "Actionable takeaway 1",
    "Actionable takeaway 2"
  ],
  "resources_mentioned": [
    "Any books, tools, websites mentioned"
  ]
}

TRANSCRIPTION:
{transcription}

Generate the outline now:"""


# =============================================================================
# Social Media Posts Generation
# =============================================================================
SOCIAL_POSTS_PROMPT = """You are a social media expert specializing in content repurposing.

TASK:
Create 5-10 engaging social media posts from the following audio transcription.

REQUIREMENTS:
1. **Variety**: Mix of post types:
   - Quote posts (with attribution if speaker is known)
   - Key insight posts
   - Question posts (to drive engagement)
   - Listicle posts (3-5 points)
   - Teaser posts (to drive traffic to full content)

2. **LinkedIn Posts** (3-4 posts):
   - Professional tone
   - 150-200 characters for short posts, up to 300 for longer
   - Include relevant professional hashtags (2-3 max)
   - Can be multi-paragraph for thought leadership

3. **Twitter/X Posts** (3-4 posts):
   - Concise and punchy
   - Under 280 characters
   - 1-2 relevant hashtags
   - Thread-starter style when appropriate

4. **Instagram/General** (2-3 posts):
   - Engaging and visual-friendly
   - Can suggest image ideas in brackets
   - Emoji usage encouraged
   - Hashtags at end (3-5 max)

FORMAT YOUR RESPONSE AS JSON:
{
  "posts": [
    {
      "platform": "linkedin",
      "type": "insight",
      "content": "Post content here with natural hashtag integration",
      "hashtags": ["#hashtag1", "#hashtag2"],
      "notes": "Optional: suggest when to post or image ideas"
    }
  ]
}

TRANSCRIPTION:
{transcription}

Generate the social media posts now:"""


# =============================================================================
# Summary Generation (for quick preview)
# =============================================================================
SUMMARY_PROMPT = """Provide a concise 2-3 sentence summary of the following audio transcription.

Focus on:
- Main topic discussed
- Key insights or conclusions
- Target audience or purpose

TRANSCRIPTION:
{transcription}

SUMMARY:"""


# =============================================================================
# Helper function to format prompts
# =============================================================================
def format_prompt(template: str, transcription: str) -> str:
    """
    Format a prompt template with the transcription.

    Args:
        template: Prompt template string with {transcription} placeholder
        transcription: The audio transcription text

    Returns:
        Formatted prompt string
    """
    return template.format(transcription=transcription)


# =============================================================================
# System message for GPT (used across all prompts)
# =============================================================================
SYSTEM_MESSAGE = """You are an AI assistant specialized in content repurposing.
You excel at transforming audio transcriptions into various written formats while
maintaining the original meaning, tone, and key insights. You always provide
well-structured, engaging content optimized for the target platform."""
