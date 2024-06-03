import torch

def cosineSimilarity(vec1, vec2): 
    return torch.nn.functional.cosine_similarity(vec1, vec2) 

vec1 = torch.tensor([[1.3, 2.3, 3.3]])
vec2 = torch.tensor([[4.0, 5.1, 6.2]])

cos = cosineSimilarity(vec1, vec2)
print(cos.item())

