from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy database of certifications
certificates = {
    "AI": [
        {"name": "AI Beginner Certificate", "provider": "Coursera", "credibility": "High", "cost": "$49"},
        {"name": "AI Advanced Certificate", "provider": "edX", "credibility": "High", "cost": "$99"}
    ],
    "Python": [
        {"name": "Python Basics", "provider": "Udemy", "credibility": "Medium", "cost": "$19"},
        {"name": "Python Pro", "provider": "Coursera", "credibility": "High", "cost": "$49"}
    ],
    "Web Development": [
        {"name": "Frontend Developer", "provider": "freeCodeCamp", "credibility": "High", "cost": "Free"},
        {"name": "Fullstack Developer", "provider": "edX", "credibility": "High", "cost": "$99"}
    ]
}

# HTML templates
home_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BlogPage - Smart Certificate Recommender</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f0f2f5; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px; }
        main { padding: 30px; max-width: 800px; margin: auto; text-align: center; }
        ul { list-style: none; padding: 0; }
        li { margin: 15px 0; }
        a { text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; display: inline-block; }
        a:hover { background: #45a049; }
    </style>
</head>
<body>
    <header>
        <h1>BlogPage - Smart Certificate Recommender</h1>
    </header>
    <main>
        <h2>Welcome!</h2>
        <ul>
            <li><a href="/recommend">Skill-Based Recommendations</a></li>
            <li><a href="/search">Search Certificates</a></li>
            <li><a href="/filter">Filter by Cost</a></li>
            <li><a href="/favorites">View Favorites</a></li>
        </ul>
    </main>
</body>
</html>
"""
recommend_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Skill-Based Recommendations</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px; }
        main { max-width: 800px; margin: auto; padding: 30px; text-align: center; }
        select, button { padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background: #4CAF50; color: white; border: none; }
        button:hover { background: #45a049; }
        .card { background: white; padding: 15px; margin: 10px auto; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 80%; }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <header><h1>BlogPage - Smart Certificate Recommender</h1></header>
    <main>
        <h2>Select a Skill</h2>
        <form method="POST">
            <select name="skill">
                <option value="">--Select--</option>
                {% for skill in skills %}
                <option value="{{ skill }}">{{ skill }}</option>
                {% endfor %}
            </select>
            <button type="submit">Get Recommendations</button>
        </form>
        {% if results %}
        <h3>Recommendations:</h3>
        {% for cert in results %}
        <div class="card">
            <strong>{{ cert.name }}</strong><br>
            Provider: {{ cert.provider }}<br>
            Cost: {{ cert.cost }}<br>
            <form method="POST" action="/add_favorite">
                <input type="hidden" name="name" value="{{ cert.name }}">
                <input type="hidden" name="provider" value="{{ cert.provider }}">
                <input type="hidden" name="cost" value="{{ cert.cost }}">
                <button type="submit">Add to Favorites</button>
            </form>
        </div>
        {% endfor %}
        {% endif %}
        <a href="/">Back to Home</a>
    </main>
</body>
</html>
"""
search_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Search Certificates</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px; }
        main { max-width: 800px; margin: auto; padding: 30px; text-align: center; }
        input[type="text"], button { padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background: #4CAF50; color: white; border: none; }
        button:hover { background: #45a049; }
        .card { background: white; padding: 15px; margin: 10px auto; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 80%; }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <header><h1>BlogPage - Smart Certificate Recommender</h1></header>
    <main>
        <h2>Search Certificates by Name</h2>
        <form method="POST">
            <input type="text" name="query" placeholder="Enter certificate name">
            <button type="submit">Search</button>
        </form>
        {% if results %}
        <h3>Results:</h3>
        {% for cert in results %}
        <div class="card">
            <strong>{{ cert.name }}</strong><br>
            Provider: {{ cert.provider }}<br>
            Cost: {{ cert.cost }}
        </div>
        {% endfor %}
        {% endif %}
        <a href="/">Back to Home</a>
    </main>
</body>
</html>
"""
filter_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Filter Certificates</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px; }
        main { max-width: 800px; margin: auto; padding: 30px; text-align: center; }
        select, button { padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background: #4CAF50; color: white; border: none; }
        button:hover { background: #45a049; }
        .card { background: white; padding: 15px; margin: 10px auto; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 80%; }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <header><h1>BlogPage - Smart Certificate Recommender</h1></header>
    <main>
        <h2>Filter Certificates by Cost</h2>
        <form method="POST">
            <select name="cost">
                <option value="Free">Free</option>
                <option value="Paid">Paid</option>
            </select>
            <button type="submit">Filter</button>
        </form>
        {% if results %}
        <h3>Filtered Results:</h3>
        {% for cert in results %}
        <div class="card">
            <strong>{{ cert.name }}</strong><br>
            Provider: {{ cert.provider }}<br>
            Cost: {{ cert.cost }}
        </div>
        {% endfor %}
        {% endif %}
        <a href="/">Back to Home</a>
    </main>
</body>
</html>
"""
favorites_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Your Favorites</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px; }
        main { max-width: 800px; margin: auto; padding: 30px; text-align: center; }
        .card { background: white; padding: 15px; margin: 10px auto; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); width: 80%; }
        a { display: inline-block; margin-top: 20px; text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <header><h1>BlogPage - Smart Certificate Recommender</h1></header>
    <main>
        <h2>Your Favorite Certificates</h2>
        {% if favorites %}
        {% for cert in favorites %}
        <div class="card">
            <strong>{{ cert.name }}</strong><br>
            Provider: {{ cert.provider }}<br>
            Cost: {{ cert.cost }}
        </div>
        {% endfor %}
        {% else %}
        <p>No favorites yet.</p>
        {% endif %}
        <a href="/">Back to Home</a>
    </main>
</body>
</html>
"""
# Routes
@app.route("/")
def home():
    return render_template_string(home_template)

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    skills = list(certificates.keys())
    results = []
    if request.method == "POST":
        skill = request.form.get("skill")
        results = certificates.get(skill, [])
    return render_template_string(recommend_template, skills=skills, results=results)

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        query = request.form.get("query", "").lower()
        for skill_list in certificates.values():
            for cert in skill_list:
                if query in cert["name"].lower():
                    results.append(cert)
    return render_template_string(search_template, results=results)

@app.route("/filter", methods=["GET", "POST"])
def filter_cost():
    results = []
    if request.method == "POST":
        cost_type = request.form.get("cost")
        for skill_list in certificates.values():
            for cert in skill_list:
                if cost_type == "Free" and cert["cost"].lower() == "free":
                    results.append(cert)
                elif cost_type == "Paid" and cert["cost"].lower() != "free":
                    results.append(cert)
    return render_template_string(filter_template, results=results)

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    cert = {
        "name": request.form["name"],
        "provider": request.form["provider"],
        "cost": request.form["cost"]
    }
    if "favorites" not in session:
        session["favorites"] = []
    session["favorites"].append(cert)
    session.modified = True
    return redirect(url_for("recommend"))

@app.route("/favorites")
def favorites():
    favs = session.get("favorites", [])
    return render_template_string(favorites_template, favorites=favs)

if __name__ == "__main__":
    print("Smart Certificate Recommender running at http://127.0.0.1:5000")
    app.run(debug=True)