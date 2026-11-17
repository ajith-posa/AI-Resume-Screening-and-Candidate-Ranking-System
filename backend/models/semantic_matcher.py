from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embedding(self, text):

        return self.model.encode(
            text,
            convert_to_numpy=True
        )

    def calculate_similarity(
        self,
        text1,
        text2
    ):

        embedding1 = self.generate_embedding(text1)
        embedding2 = self.generate_embedding(text2)

        score = cosine_similarity(
            [embedding1],
            [embedding2]
        )[0][0]

        return float(score)