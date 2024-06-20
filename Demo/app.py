from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample data to search
documents = [
    "Hello World",
    "hello World",
    "hello world",
]

def perform_search(query, mode):
    query_words = query.split()
    results = []

    for doc in documents:
        doc_words = doc.split()

        if mode == "OR":
            if any(q in doc_words for q in query_words):
                results.append(doc)
        elif mode == "AND":
            if all(q in doc_words for q in query_words):
                results.append(doc)
        elif mode == "NOT":
            if not any(q in doc_words for q in query_words):
                results.append(doc)
        else:
            results.append("Invalid search mode specified")
    
    return results

# Basic home route
@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome to CyberMiner</h1>
        <form action="/search" method="get">
            <input type="text" name="query" placeholder="Enter your search query">
            <select name="mode">
                <option value="OR">OR</option>
                <option value="AND">AND</option>
                <option value="NOT">NOT</option>
            </select>
            <input type="submit" value="Search">
        </form>
        <h2>Manage Documents</h2>
        <form action="/add" method="post">
            <input type="text" name="document" placeholder="Enter document to add">
            <input type="submit" value="Add Document">
        </form>
        <form action="/delete" method="post">
            <input type="text" name="document" placeholder="Enter document to delete">
            <input type="submit" value="Delete Document">
        </form>
        <h3>Current Documents</h3>
        <ul>
            {% for doc in documents %}
            <li>{{ doc }}</li>
            {% endfor %}
        </ul>
    ''', documents=documents)


# Search route
@app.route('/search')
def search():
    query = request.args.get('query')
    mode = request.args.get('mode')
    if query:
        results = perform_search(query, mode)
        return render_template_string('''
            <h2>Search Results for: {{ query }} (Mode: {{ mode }})</h2>
            <ul>
                {% for result in results %}
                <li>{{ result }}</li>
                {% endfor %}
            </ul>
            <a href="/">Go back</a>
        ''', query=query, mode=mode, results=results)
    return "<h2>No query provided</h2>"

@app.route('/add', methods=['POST'])
def add_document():
    new_doc = request.form.get('document')
    if new_doc and new_doc not in documents:
        documents.append(new_doc)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete_document():
    del_doc = request.form.get('document')
    if del_doc in documents:
        documents.remove(del_doc)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)