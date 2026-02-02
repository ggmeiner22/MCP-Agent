import os
from fastmcp import FastMCP

mcp = FastMCP("conditional-llm-mcp")


@mcp.tool()
def hello_llm(message: str) -> str:
    """Respond using OpenAI or Gemini, depending on which API key is configured."""
    openai_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    # Prefer OpenAI if both keys exist (you can flip this if you want)
    if openai_key:
        from openai import OpenAI

        client = OpenAI(api_key=openai_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}],
        )
        return resp.choices[0].message.content or ""

    if google_key:
        from google import genai

        client = genai.Client(api_key=google_key)
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=message,
        )
        return resp.text or ""

    return "No LLM API key found. Set OPENAI_API_KEY or GOOGLE_API_KEY."


if __name__ == "__main__":
    mcp.run()
