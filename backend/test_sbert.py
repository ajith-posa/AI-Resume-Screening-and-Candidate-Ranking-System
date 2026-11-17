from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence1 = "Python machine learning developer"
sentence2 = "Developer experienced in Python and machine learning"

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)

print("Embedding 1 shape:", embedding1.shape)
print("Embedding 2 shape:", embedding2.shape)

print("SBERT working successfully!")