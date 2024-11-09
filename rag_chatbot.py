from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your WordPress site URL and API credentials
WORDPRESS_URL = "https://your-wordpress-site.com"
API_USERNAME = "your_username"
API_PASSWORD = "your_password"
CHATBOT_API_URL = "https://example-rag-api.com/query"  # RAG system's API endpoint

# Basic authentication for WordPress REST API
AUTH = (API_USERNAME, API_PASSWORD)

@app.route("/index-content", methods=["GET"])
def index_content():
    """Fetch and index WordPress content."""
    try:
        # Fetch posts and pages from WordPress
        response = requests.get(
            f"{WORDPRESS_URL}/wp-json/wp/v2/posts?per_page=100", auth=AUTH
        )
        posts = response.json()
        content_data = []

        for post in posts:
            content_data.append({
                "id": post["id"],
                "title": post["title"]["rendered"],
                "content": post["content"]["rendered"],
                "url": post["link"],
                "metadata": {
                    "date": post["date"],
                    "author": post["author"]
                },
            })

        # Send the content to the RAG system
        rag_response = requests.post(
            f"{CHATBOT_API_URL}/index",
            json=content_data
        )

        if rag_response.status_code == 200:
            return jsonify({"message": "Content indexed successfully!"})
        else:
            return jsonify({"error": "Failed to index content with RAG system."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chatbot", methods=["POST"])
def chatbot():
    """Handle chatbot queries."""
    try:
        user_query = request.json.get("query")
        if not user_query:
            return jsonify({"error": "Query parameter is missing"}), 400

        # Query the RAG system
        response = requests.post(
            CHATBOT_API_URL,
            json={"query": user_query}
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch response from RAG system."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
