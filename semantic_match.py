from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import streamlit as st


@st.cache_resource
def load_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

model = load_model()

def semantic_similarity(skill1, skill2):

    emb1 = model.encode(skill1)
    emb2 = model.encode(skill2)

    similarity = cos_sim(
        emb1,
        emb2
    )

    return float(similarity)