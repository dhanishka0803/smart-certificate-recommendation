# smart_certificate_platform.py
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

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

# HTML template embedded in Flask
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BlogPage - Smart Certificate Recommender</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f0f2f5; }
        header { background: #4CAF50; color: white; text-align: center; padding: 20px 0; }
        main { padding: 20px; max-width: 800px; margin: auto; }
        input, select { padding: 10px; width: 70%; margin-right: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
        .card { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .card h3 { margin: 0; }
        .card p { margin: 5px 0; }
    </style>
</head>
<body>
    <header>
        <h1>BlogPage - Smart Certificate Recommender</h1>
    </header>
    <main>
        <h2>Discover Certificates by Skill</h2>
        <div>
            <select id="skill">
                <option value="">--Select a Skill--</option>
                <option value="AI">AI</option>
                <option value="Python">Python</option>
                <option value="Web Development">Web Development</option>
            </select>
            <button onclick="getRecommendation()">Get Recommendations</button>
        </div>
        <div id="result"></div>
    </main>
    <script>
        async function getRecommendation() {
            let skill = document.getElementById("skill").value;
            if(skill === "") { alert("Please select a skill"); return; }

            let response = await fetch("/recommend", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: "skill=" + encodeURIComponent(skill)
            });
            let data = await response.json();

            let html = "";
            if(data.length === 0) {
                html = "<p>No recommendations found.</p>";
            } else {
                data.forEach(cert => {
                    html += `<div class="card">
                                <h3>${cert.name}</h3>
                                <p><strong>Provider:</strong> ${cert.provider}</p>
                                <p><strong>Credibility:</strong> ${cert.credibility}</p>
                                <p><strong>Cost:</strong> ${cert.cost}</p>
                             </div>`;
                });
            }
            document.getElementById("result").innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/recommend", methods=["POST"])
def recommend():
    skill = request.form.get("skill")
    recs = certificates.get(skill, [])
    return jsonify(recs)

if __name__ == "__main__":
    print("Starting BlogPage - Smart Certificate Recommender...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)
