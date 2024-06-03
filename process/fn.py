import torch
from transformers import AutoModel, AutoTokenizer
from openai import OpenAI

# OpenAI Cred
client = OpenAI(api_key="API KEY")

# Agnel Setup
model_id = 'SeanLee97/angle-bert-base-uncased-nli-en-v1'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)


def translate(s: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are a translator that translate from spanish to english"},
            {"role": "user", "content": s}
        ]
    )
    return (completion.choices[0].message.content)


def summarize(s: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              "role": "system",
              "content": "You are a summarizer that summarize the text. \
                Limit to under 200 words."},
            {"role": "user", "content": s}
        ]
    )

    return (completion.choices[0].message.content)


def convertToVec(inputs: str):
    tok = tokenizer([inputs], return_tensors='pt')
    for k, v in tok.items():
        tok[k] = v
    hidden_state = model(**tok).last_hidden_state
    vec = (hidden_state[:, 0] + torch.mean(hidden_state, dim=1)) / 2.0
    vectorValue = vec.tolist()
    return vectorValue[0]


# calculate cosine similarity without using torch
def cosineSimilarity(vec1, vec2):
    dot = sum(a*b for a, b in zip(vec1, vec2))
    norm1 = sum(a*a for a in vec1) ** 0.5
    norm2 = sum(b*b for b in vec2) ** 0.5
    result = dot / (norm1*norm2)
    # 6 digit decimal
    result = round(result, 6)
    return result
