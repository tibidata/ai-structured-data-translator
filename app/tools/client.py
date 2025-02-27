import json
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed

from openai import OpenAI

from .get_prompt import get_prompt


class TranslatorClient:
    """
    A client for translating text using OpenAI's language models.
    """

    def __init__(self):
        """
        Initialize the TranslatorClient with an OpenAI client.
        """
        self.client = OpenAI()

    def __call__(self, input_dict):
        """
        Translate the values of the input dictionary.

        Args:
            input_dict (dict): The dictionary containing text to translate.

        Returns:
            dict: The translated dictionary.
        """
        # Slice the input dictionary into smaller chunks
        dict_list = TranslatorClient.slice_dict(input_dict=input_dict, n=30)
        # Generate translations in parallel
        results = self.generate_parallel(dict_list=dict_list)

        return results

    def generate_parallel(self, dict_list, max_workers=5):
        """
        Generate translations for multiple dictionary chunks in parallel.

        Args:
            dict_list (list): List of dictionary chunks to translate.
            max_workers (int): Maximum number of parallel workers.

        Returns:
            dict: Combined results of all translations.
        """
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit translation tasks for each dictionary chunk
            future_to_prompt = {
                executor.submit(self.__generate, input_data=input_data): input_data
                for input_data in dict_list
            }
            # Collect results as they complete
            for future in as_completed(future_to_prompt):
                results.update(future.result())
        return results

    def __generate(self, **kwargs):
        """
        Generate a translation for a single dictionary chunk.

        Args:
            **kwargs: Keyword arguments containing the input data.

        Returns:
            dict: The translated dictionary chunk.
        """
        # Create a chat completion request to OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o-2024-05-13",
            seed=42,
            temperature=0.0000001,
            messages=[
                {
                    "role": "system",
                    "content": get_prompt(),
                },
                {
                    "role": "user",
                    "content": f"Translate the values of the following json:{kwargs.get('input_data')}",
                },
            ],
        )

        # Extract and return the JSON from the model's response
        return TranslatorClient.extract_json(
            response.choices[0].message.content.replace("'", '"')
        )

    @staticmethod
    def extract_json(generated_text) -> dict:
        """
        Extract a JSON object from the generated text.

        Args:
            generated_text (str): The text containing a JSON object.

        Returns:
            dict: The extracted JSON object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        # Find the start and end of the JSON content
        json_start = generated_text.find("{")
        json_end = generated_text.rfind("}") + 1
        json_content = generated_text[json_start:json_end]

        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON from model output.")

    @staticmethod
    def slice_dict(input_dict, n):
        """
        Slice a dictionary into smaller chunks.

        Args:
            input_dict (dict): The input dictionary to slice.
            n (int): The size of each chunk.

        Returns:
            list: A list of dictionary chunks.
        """
        it = iter(input_dict.items())
        return [
            {k: v for k, v in islice(it, n)}
            for _ in range((len(input_dict) + n - 1) // n)
        ]
