import json
import numpy as np
import warnings
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, util

# Suppress FutureWarnings related to clean_up_tokenization_spaces
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="`clean_up_tokenization_spaces` was not set."
)

# Load LaBSE model and tokenizer
model_name = 'bert-base-multilingual-cased'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
embedder = SentenceTransformer('sentence-transformers/LaBSE')

def compute_similarity_matrix(names):
    embeddings = embedder.encode(names, convert_to_tensor=True)
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).numpy()
    return similarity_matrix

def find_similar_names(similarity_matrix, names, threshold=0.5):
    similar_pairs = []
    num_names = len(names)
    for i in range(num_names):
        for j in range(i + 1, num_names):
            if similarity_matrix[i][j] >= threshold:
                similar_pairs.append({
                    'name1': names[i],
                    'name2': names[j],
                    'similarity': float(similarity_matrix[i][j])
                })
    return similar_pairs

def save_results_to_json(results, filename='similarity_results.json'):
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)
