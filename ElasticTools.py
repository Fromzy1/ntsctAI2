import os
#import elasticsearch as Elasticsearch
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import OpenAIClient as OpenAI

class Tools():
    def __init__(self, es_url="http://10.10.10.50:9200", index_name="omnis.dns"):
       
        #Load credentials and settings from environment variables
        self.es_url = os.getenv("ELASTICSEARCH_URL")
        self.username = os.getenv("ELASTICSEARCH_USERNAME")
        self.password = os.getenv("ELASTICSEARCH_PASSWORD")
        self.ca_cert = os.getenv("ELASTICSEARCH_CA_CERT")

        # Initialize Elasticsearch with SSL/TLS and authentication
        self.es = Elasticsearch(
            self.es_url,
            basic_auth=(self.username, self.password),
            ca_certs=self.ca_cert,
            verify_certs=True,
            request_timeout=60
        )
        self.index_name = index_name

    def __getattr__(self, name):
        """
        Delegate attribute access to the underlying Elasticsearch instance.
        """
        if hasattr(self.es, name):
            return getattr(self.es, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def get_indices(self, name="omnis"):
        try:
            # Retrieves a list of all indices
            indices = self.es.cat.indices(format="json")
            print(type(indices))
            # Extracts and returns only the index names
            if name=="omnis" :
                return [index_info['index'] for index_info in indices if index_info['index'].startswith("omnis")]
            else :
                return [index_info['index'] for index_info in indices]
        except Exception as e:
            print(f"Error retrieving indices: {e}")
            return []
            
    def get_indices_dict(self, name="kafka"):
        # Use dict to give access to index by their names
        try:
            indices = self.es.cat.indices(format="json")
            filtered_indices = [index_info['index'] for index_info in indices if index_info['index'].startswith(name)]
            # Convert list to dictionary
            return {index_name: index_name for index_name in filtered_indices}
        except Exception as e:
            print(f"Error retrieving indices: {e}")
            return {}
            
    def get_index_schema(self, index_name=None):
        # Get the schema of the index
        try:
            # Default to self.index_name if no index is specified
            index_name = index_name or self.index_name
            # Retrieves the mapping for the specified index
            mapping = self.es.indices.get_mapping(index=index_name)
            # Returns the schema (mapping) of the index
            return mapping.get(index_name, {}).get('mappings', {})
        except Exception as e:
            print(f"Error retrieving schema for index '{index_name}': {e}")
            return {}
            
    def load_es_index_fields(self, index_name):
        # Load available fields from ES for index_name
        mapping = self.es.indices.get_mapping(index=index_name)
        fields = list(mapping[index_name]['mappings']['properties'].keys())
        available_fields = ", ".join(fields)
        #print(f"Available fields : {available_fields} \n\n")
        #print(f"Fields : {fields}")
        return fields

    def search_results(self, index_name=None, es_query=None):
        # Return result of a search query
        return self.es.search(index=index_name, body=es_query)
    
    def get_embedding(self, text):
        # Use OpenAI to get embeddings
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(
            model="text-embedding-ada-002",  # You can choose other models as well
            input=text
        )
        return response.data[0].embedding

    def find_closest_match(self, suggested_metric):
        suggested_embedding = self.get_embedding(suggested_metric)

        closest_match = None
        highest_similarity = -1

        for field in self.db_fields:
            field_embedding = self.get_embedding(field)
            similarity = 1 - cosine(suggested_embedding, field_embedding)
            print(f"field: {field} (similarity: {similarity:.2f})")

            if similarity > highest_similarity:
                highest_similarity = similarity
                closest_match = field

        return closest_match, highest_similarity