from openai import OpenAI
import os

class Client:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def __getattr__(self, name):
        """
        Delegate attribute access to the underlying Elasticsearch instance.
        """
        if hasattr(self.es, name):
            return getattr(self.es, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def generate_non_streaming_response(self, prompt, model="gpt-4o-mini", system_prompt=""):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content
    def generate_embeddings(self, text, model="text-embedding-ada-002"):
        """
        Generate embeddings for a given text using OpenAI's embedding API.

        :param text: The text to generate embeddings for.
        :param model: The embedding model to use (default is "text-embedding-ada-002").
        :return: A list of floats representing the embedding vector.
        """
        response = self.client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding
        