import csv

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from konlpy.tag import Okt
import importlib
import graph

importlib.reload(graph) 

class BooleanModel:
    def __init__(self, documents):
        self.index = {}
        self.documents = documents
        self.build_index()

    def build_index(self):
        for doc_id, document in enumerate(self.documents):
            for word in document['article'].split():
                if word in self.index:
                    self.index[word].add(doc_id)
                else:
                    self.index[word] = {doc_id}

    def search(self, query):
        query_words = query.split()
        result = None
        for word in query_words:
            if word in self.index:
                if result is None:
                    result = self.index[word]
                else:
                    result = result.intersection(self.index[word])
            else:
                result = set()
                break
        return result

def save_articles_to_csv(documents, output_file):
    with open(output_file, mode='w', newline='', encoding='cp949') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Article'])
        for doc in documents:
            writer.writerow([doc['title'], doc['article']])

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', '', text)
    return ' '.join(word_tokenize(text))

def extract_keywords(article_text, num_clusters=5, num_keywords=5):
    okt = Okt()
    preprocessed_text = preprocess_text(article_text)
    words = okt.pos(preprocessed_text, stem=True)
    nouns = [word for word, pos in words if pos == 'Noun' and len(word) > 1]  # 명사이면서 길이가 1보다 긴 것만 선택
    preprocessed_text = ' '.join(nouns)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([preprocessed_text])

    num_samples = X.shape[0]
    if num_samples < num_clusters:
        num_clusters = num_samples

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)

    cluster_centers = kmeans.cluster_centers_
    features = vectorizer.get_feature_names_out()
    top_keywords = []
    for cluster_center in cluster_centers:
        top_keyword_indices = cluster_center.argsort()[-num_keywords:][::-1]
        keywords = ['#' + features[int(i)] for i in top_keyword_indices]
        top_keywords.append(keywords)
    return ' '.join([' '.join(keywords) for keywords in top_keywords])

documents = []
with open('Korea_DB_0413.csv', mode='r', encoding='cp949') as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = row['title']
        date=row['date']
        article = row['article']
        documents.append({'title': title, 'date':date, 'article': article})

boolean_model = BooleanModel(documents)
query = input("Enter your query: ")

search_result = boolean_model.search(query)

print("[[ Search results ]]")

graph.draw_graph(search_result, documents)

print("Below are the articles relevant with the keyword '{}':".format(query))
if search_result:
    for doc_id in search_result:
        print("Title: ", documents[doc_id]['title'],documents[doc_id]['date'])
        keywords = extract_keywords(documents[doc_id]['article'])
        print(keywords, '\n')


else:
    print("No matching documents found.")

selected_title = input("\nEnter the title you want to read: ")
print()

for doc in documents:
    if doc['title'] == selected_title:
        print("Title:", doc['title'],"\n")
        print("Article:\n", doc['article'],"/n/n")
        break
else:
    print("Selected title not found in the search results.")