import scipy
import sys
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

train_verified, train_fake = [], []

with open('train-verified.txt') as f:
  train_verified = [line.rstrip() for line in f]

train_delimiter = len(train_verified)

with open('train-false.txt') as f:
  train_fake = [line.rstrip() for line in f]

corpus = train_verified + train_fake

corpus_embeddings = embedder.encode(corpus)

test_verified, test_fake = [], []

with open('test-verified.txt') as f:
  test_verified = [line.rstrip() for line in f]

test_delimiter = len(test_verified)

with open('test-false.txt') as f:
  test_fake = [line.rstrip() for line in f]

queries = test_verified + test_fake

query_embeddings = embedder.encode(queries)

right = 0
wrong = 0
for query, query_embedding in zip(queries, query_embeddings):
  distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, 'cosine')[0]
  score = min(distances)
  if score < 0.05:
    index = list(distances).index(score)
    similar = corpus[index]
    label = None
    if index < train_delimiter:
      label = 'TRUE'
    else:
      label = 'FALSE'
    index = queries.index(query)
    expected_label = None
    if index < test_delimiter:
      expected_label = 'TRUE'
    else:
      expected_label = 'FALSE'
    if label == expected_label:
      right += 1
    else:
      wrong += 1
total = right + wrong
print("Accuracy: " + str(right / total))
while True:
  question = input("Enter your query: ")
  queries = [question]
  query_embeddings = embedder.encode(queries)
  for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, 'cosine')[0]
    score = min(distances)
    index = list(distances).index(score)
    similar = corpus[index]
    label = None
    if index < train_delimiter:
      label = 'TRUE'
    else:
      label = 'FALSE'
    print("Query '" + query + "' is similar to '" + similar + "', which is " + label)
