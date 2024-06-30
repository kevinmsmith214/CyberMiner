from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample data to search
documents = [
    "Baseball Historic Moments",
    "The Science of Baseball",
    "Economic Impact of Baseball",
    "Baseball in Japan",
    "Youth Baseball Programs",
    "Fantasy Baseball Trends",
    "Baseball Literature",
    "Role of Baseball in Integration",
    "Technological Advances in Baseball",
    "Baseball Memorabilia Collecting"
]

def paginate_results(results, page, results_per_page):
    """
    Paginate the given results.

    :param results: List of results to paginate.
    :param page: Current page number.
    :param results_per_page: Number of results per page.
    :return: Paginated results for the current page and the total number of pages.
    """
    total_results = len(results)
    total_pages = (total_results + results_per_page - 1) // results_per_page
    results = sorted(results, key=str.lower)
    start_index = (page - 1) * results_per_page
    end_index = start_index + results_per_page
    
    paginated_results = results[start_index:end_index]
    
    return paginated_results, total_pages

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
    ''', documents=documents)


# Search route
@app.route('/search')
def search():
    query = request.args.get('query')
    mode = request.args.get('mode')
    page = int(request.args.get('page', 1))
    results_per_page = int(request.args.get('results_per_page', 4))  # Default to 4 if not provided

    if query:
        results = perform_search(query, mode)
        paginated_results, total_pages = paginate_results(results, page, results_per_page)

        return render_template_string('''
            <h2>Search Results for: {{ query }} (Mode: {{ mode }})</h2>
            <form action="/search" method="get">
                <input type="hidden" name="query" value="{{ query }}">
                <input type="hidden" name="mode" value="{{ mode }}">
                <label for="results_per_page">Results per page:</label>
                <input type="number" name="results_per_page" id="results_per_page" value="{{ results_per_page }}" min="1">
                <input type="submit" value="Set">
            </form>
            <ul>
                {% for result in paginated_results %}
                <li>{{ result }}</li>
                {% endfor %}
            </ul>
            <div>
                {% if page > 1 %}
                <a href="{{ url_for('search', query=query, mode=mode, page=page-1, results_per_page=results_per_page) }}">Previous</a>
                {% endif %}
                {% if page < total_pages %}
                <a href="{{ url_for('search', query=query, mode=mode, page=page+1, results_per_page=results_per_page) }}">Next</a>
                {% endif %}
            </div>
            <a href="/">Go back</a>
        ''', query=query, mode=mode, paginated_results=paginated_results, page=page, total_pages=total_pages, results_per_page=results_per_page)
    
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