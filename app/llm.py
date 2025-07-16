import os

import torch
from groq import Groq
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def generate_mash_options(theme: str, platform: str, api_key: str = None) -> list[str]:
    match platform:
        case "groq":
            """
            Generates MASH categories based on a given theme using the Groq API.
            """
            if not api_key:
                api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable not set.")

            client = Groq(api_key=api_key)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate 4 diverse and creative categories for a MASH game based on the theme: {theme}.  Return only the categories, one per line, without any introductory or concluding remarks.  For example, if the theme is 'Superheroes', return: Strength\nAgility\nSuper Power\nWeakness",
                    }
                ],
                model="llama3-8b-8192",  # Smaller model for faster inference
                temperature=0.7,
                max_tokens=100,
            )

            options_str = chat_completion.choices[0].message.content.strip()

        case "huggingface":
            torch.random.manual_seed(0)
            model_path = "microsoft/Phi-4-mini-instruct"  # Smaller model for faster inference
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                device_map="auto",
                torch_dtype="auto",
                trust_remote_code=True,
            )
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {
                    "role": "user",
                    "content": "Generate 4 diverse and creative categories for a MASH game based on the theme: Superheroes. Return only the categories, one per line, without any introductory or concluding remarks. For example, if the theme is 'Superheroes', return: Strength\nAgility\nSuper Power\nWeakness",
                },
                {
                    "role": "assistant",
                    "content": "Strength\nAgility\nSuper Power\nWeakness",
                },
                {
                    "role": "user",
                    "content": f"Now generate exactly 4 diverse and creative categories for a MASH game based on the theme: {theme}. Return only the categories, one per line, without any introductory or concluding remarks. For example, if the theme is 'Food', return: Flavour\nTexture\nNutrition\nCuisine",
                },
            ]
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
            )
            generation_args = {
                "max_new_tokens": 100,
                "return_full_text": False,
                "temperature": 0.0,
                "do_sample": False,
            }
            output = pipe(messages, **generation_args, use_auth_token=api_key)
            print(output[0]["generated_text"])

            options_str = output[0]["generated_text"]

    return [option.strip() for option in options_str.split("\n") if option.strip()]


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    theme = "general health"
    platform = "huggingface"

    if platform == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        model = "llama3-8b-8192"
    elif platform == "huggingface":
        api_key = os.environ.get("HF_TOKEN")
        if not api_key:
            raise ValueError("HF_TOKEN environment variable not set.")
        model = "microsoft/Phi-4-mini-instruct"
    options = generate_mash_options(theme, platform, api_key)

    print(f"Generated MASH options for theme '{theme}':")
    for option in options:
        print(f"- {option}")
