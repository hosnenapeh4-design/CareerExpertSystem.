
from flask import Flask, render_template, request

app = Flask(__name__)

# Expert System: rules for the seven college departments
DEPARTMENTS = {
    "Artificial Intelligence": {
        "rules": ["programming", "ai", "math", "problem_solving", "data"],
        "description": "AI, machine learning, algorithms, and intelligent applications.",
        "advice": "Practice Python, mathematics, logic, and basic machine learning."
    },
    "Cybersecurity": {
        "rules": ["security", "networks", "problem_solving", "programming"],
        "description": "Protecting computers, networks, and information from attacks.",
        "advice": "Learn networking basics, Linux, programming, and safe security labs."
    },
    "Data Science": {
        "rules": ["data", "math", "statistics", "programming", "analysis"],
        "description": "Analyzing data, finding patterns, and supporting decisions.",
        "advice": "Practice statistics, spreadsheets, Python, and data visualization."
    },
    "Mechatronics": {
        "rules": ["robotics", "electronics", "mechanics", "math"],
        "description": "Combining mechanics, electronics, and intelligent machines.",
        "advice": "Strengthen physics, electronics, mechanical concepts, and robotics."
    },
    "Autotronics": {
        "rules": ["cars", "electronics", "sensors", "mechanics"],
        "description": "Vehicle electronics, sensors, and automotive control systems.",
        "advice": "Explore vehicle systems, sensors, electronics, and basic mechanics."
    },
    "Clothing Technology": {
        "rules": ["clothing", "design", "creativity", "manufacturing"],
        "description": "Clothing design, textiles, materials, and production methods.",
        "advice": "Explore fabric types, garment construction, design, and production."
    },
    "Control and Systems": {
        "rules": ["control", "electronics", "math", "problem_solving", "automation"],
        "description": "Automation, control systems, and monitoring industrial processes.",
        "advice": "Practice mathematics, electronics, automation, and control basics."
    }
}


def calculate_results(form):
    selected_skills = set(form.getlist("skills"))
    results = []

    math_level = form.get("math_level", "")
    english_level = form.get("english_level", "")
    preferred = form.get("preferred_department", "")

    # Add relevant knowledge inferred from self-reported levels.
    if math_level in ("good", "excellent"):
        selected_skills.update(["math", "problem_solving"])

    if form.get("programming_level") in ("good", "excellent"):
        selected_skills.add("programming")

    if form.get("ai_level") in ("good", "excellent"):
        selected_skills.add("ai")

    for name, department in DEPARTMENTS.items():
        rules = set(department["rules"])
        matched = rules.intersection(selected_skills)

        # Score based on how many department-specific rules match.
        score = round(len(matched) / len(rules) * 100)

        # A preferred department gets a small bonus, not an automatic win.
        if preferred == name:
            score = min(100, score + 10)

        reasons = []
        if matched:
            reasons.append(
                "Your answers match these areas: "
                + ", ".join(sorted(matched))
                + "."
            )
        else:
            reasons.append(
                "Your answers have not shown a strong match yet; "
                "explore this department before deciding."
            )

        if english_level in ("good", "excellent"):
            reasons.append(
                "Your reported English level may help when learning "
                "from technical resources."
            )

        results.append({
            "field": name,
            "score": score,
            "description": department["description"],
            "advice": department["advice"],
            "reasons": reasons
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:3]


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        results = calculate_results(request.form)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
