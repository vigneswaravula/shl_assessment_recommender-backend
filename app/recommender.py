# app/recommender.py

import json
import os
from sentence_transformers import SentenceTransformer, util

# Load your pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_assessments():
    json_path = os.path.join(os.path.dirname(__file__), "data", "assessments.json")
    with open(json_path, "r") as f:
        return json.load(f)

assessments = load_assessments()

def get_assessment_embeddings(assessments):
    texts = [a["name"] + " " + a["type"] for a in assessments]  # Removed duration
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

assessment_embeddings = get_assessment_embeddings(assessments)

def recommend_assessments(query, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, assessment_embeddings)[0]
    top_results = cos_scores.topk(k=top_k)

    recommendations = []
    for idx in top_results.indices:
        assessment = assessments[idx]
        recommendations.append({
            "name": assessment["name"],
            "type": assessment["type"],
            "remote_support": assessment["remote_support"],
            "adaptive_support": assessment["adaptive_support"],
            "url": assessment["url"]
        })

    return recommendations
