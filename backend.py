from flask import Flask, request, jsonify
import torch
from transformers import AutoModel, AutoTokenizer
from flask_cors import CORS
from fn import convertToVec
from db import execQuery, getQuery, cur, conn
from fn import summarize


model_id = 'SeanLee97/angle-bert-base-uncased-nli-en-v1'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id)


def findClosestPost(vector: str, field: str):
    try:
        sql = "SELECT post_id, title, summary FROM posts ORDER BY " + \
            field + " <-> '" + vector + "' LIMIT 10"
        cur.execute(sql)
        rows = cur.fetchall()
        return (rows)

    except Exception:
        conn.rollback()
        return ([])


def findClosest(vector: str, field: str):
    try:
        sql = "SELECT * FROM main2 ORDER BY " + field + " <-> '" + vector + "' LIMIT 5"
        cur.execute(sql)
        rows = cur.fetchall()
        return (rows)

    except Exception:
        conn.rollback()
        return ([])


def cosineSimilarity(vec1, vec2):
    return torch.nn.functional.cosine_similarity(vec1, vec2)


def addData(sentence, translation, sdg):
    vec = convertToVec(translation)
    embedding = vec.tolist()
    cur.execute("INSERT INTO main (sentence, translation, sdg, embedding) VALUES (%s, %s, %s, %s)",
                (sentence, translation, sdg, embedding[0]))
    conn.commit()


app = Flask(__name__)
CORS(app)

# Sample data
data = {
    "hello": "world",
    "man": [
        "aaa", "bbb", "ccc"
    ]
}

# POST request handler


@app.route("/api/new_post", methods=['POST'])
def api_new_post():
    inputs = request.get_json()
    post_id = inputs['post_id']
    title = inputs['title']
    text = inputs['text']
    summary = summarize(text)
    title_vector = convertToVec(title)
    summary_vector = convertToVec(summary)
    title_vector_string = '[' + ', '.join(map(str, title_vector)) + ']'
    summary_vector_string = '[' + ', '.join(map(str, summary_vector)) + ']'
    execQuery("INSERT INTO posts (post_id, content, summary, embedding, title, title_vector) VALUES (%s, %s, %s, %s, %s, %s)",
              (post_id, text, summary, summary_vector_string, title, title_vector_string))
    return jsonify({'message': 'Data added successfully'})

# SGDS API---------------------


@app.route('/api/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    data.append(new_data)
    return jsonify({'message': 'Data added successfully', 'data': data}), 201


@app.route("/api/vectorize", methods=['POST'])
def api_vectorize():
    inputs = request.get_json()
    vec = convertToVec(inputs['text'])
    return jsonify(vec.tolist())


@app.route("/api/insert", methods=['POST'])
def api_insert():
    inputs = request.get_json()
    addData(inputs['sentence'], inputs['translation'], inputs['sdg'])
    return jsonify({'message': 'Data added successfully'})


@app.route("/api/find-id", methods=['POST'])
def api_find_id():
    try:
        inputs = request.get_json()
        id = inputs['id']
        sql = "SELECT * FROM main2 WHERE id = " + str(id)
        print(sql)
        cur.execute(sql, "")
        rows = cur.fetchall()
        keys = ['id', 'title', 'text', 'summary', 'class',
                'subclass', 'related', 'title_vector', 'summary_vector']

        # convert to json with keys
        rows = [dict(zip(keys, row)) for row in rows]

        return jsonify(rows)
    except Exception:
        conn.rollback()
        return jsonify([])


@app.route("/api/find-post", methods=['POST'])
def api_find_post():
    inputs = request.get_json()
    text = inputs['text']
    field = inputs['field']
    text_vec = convertToVec(text)
    text_vec_string = '[' + ', '.join(map(str, text_vec)) + ']'
    closest = findClosestPost(text_vec_string, field)
    keys = ['post_id', 'title', 'summary']
    closest = [dict(zip(keys, row)) for row in closest]
    return jsonify(closest)


@app.route("/api/find-closest", methods=['POST'])
def api_find_closest():
    inputs = request.get_json()
    text = inputs['text']
    field = inputs['field']
    text_vec = convertToVec(text)
    text_vec_string = '[' + ', '.join(map(str, text_vec)) + ']'
    closest = findClosest(text_vec_string, field)
    keys = ['id', 'title', 'text', 'summary', 'class',
            'subclass', 'related', 'title_vector', 'summary_vector']
    closest = [dict(zip(keys, row)) for row in closest]
    return jsonify(closest)


@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=3012)
