from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ⚠️ REPLACE THIS WITH YOUR ACTUAL API KEY
GIPHY_API_KEY = 'Yi8h2mzR6zAyIdo6R1BzlGqbdAk2U2yR'

def get_gifs(query=None):
    """Fetches GIFs from Giphy. Defaults to trending if no query is provided."""
    if query:
        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=20&rating=g"
    else:
        url = f"https://api.giphy.com/v1/gifs/trending?api_key={GIPHY_API_KEY}&limit=20&rating=g"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Parse the JSON to get only what we need
        gifs = []
        for item in data.get('data', []):
            gifs.append({
                "title": item.get("title", "Untitled Cat Meme"),
                "url": item["images"]["original"]["url"],
                "preview": item["images"]["fixed_height"]["url"] # Better for grid loading
            })
        return gifs
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search')
    
    # If user searched, get specific memes. Otherwise, get trending cats.
    if search_query:
        gifs = get_gifs(search_query)
        header_text = f"Results for '{search_query}'"
    else:
        # Default search for 'cats' to ensure cat content on trending
        gifs = get_gifs("cats") 
        header_text = "Trending Cat Memes"

    return render_template('index.html', gifs=gifs, header=header_text)

if __name__ == '__main__':
    app.run(debug=True)