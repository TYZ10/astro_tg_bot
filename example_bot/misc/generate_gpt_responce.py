import logging
from openai import AsyncOpenAI


async def generate_gpt_txt(client: AsyncOpenAI, prompt) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(e)
