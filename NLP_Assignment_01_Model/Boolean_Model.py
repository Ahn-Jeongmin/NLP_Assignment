import csv

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
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Article'])
        for doc in documents:
            writer.writerow([doc['title'], doc['article']])
            

documents = []
with open('Korea_DB.csv', mode='r', encoding='cp949') as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = row['title']
        article = row['article']
        documents.append({'title': title, 'article': article})

boolean_model = BooleanModel(documents)
query = input("Enter your query: ")

search_result = boolean_model.search(query)
count=0
print("[[ Search results ]]")
print("Below are the articles relevant with the keyword '{}':".format(query))
if search_result:
    for doc_id in search_result:
        print("Title: ", documents[doc_id]['title'], "\n")
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

# Save extracted articles to a CSV file
output_file = 'extracted_articles.csv'
save_articles_to_csv(documents, output_file)
print(f"\nExtracted articles saved to {output_file}.")