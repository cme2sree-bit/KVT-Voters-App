from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

voters = [
    {"name": "Ramesh", "guardian": "Krishna", "houseno": "101", "party": "LDF"},
    {"name": "Suresh", "guardian": "Gopalan", "houseno": "102", "party": "UDF"},
    {"name": "Rajesh", "guardian": "Ravi", "houseno": "103", "party": "NDA"}
]

@app.route("/")
def home():
    return render_template("home.html", voters=voters)

@app.route("/search", methods=["GET", "POST"])
def search_voter():
    result = []
    query = ""
    if request.method == "POST":
        query = request.form["query"].lower()
        for voter in voters:
            if query in voter["name"].lower() or query in voter["houseno"].lower() or query in voter["party"].lower():
                result.append(voter)
    return render_template("search.html", result=result, query=query)

@app.route("/add", methods=["GET", "POST"])
def add_voter():
    if request.method == "POST":
        voters.append({
            "name": request.form["name"],
            "guardian": request.form["guardian"],
            "houseno": request.form["houseno"],
            "party": request.form["party"]
        })
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<houseno>", methods=["GET", "POST"])
def edit_voter(houseno):
    voter = next((v for v in voters if v["houseno"] == houseno), None)
    if not voter:
        return "Voter not found!", 404
    if request.method == "POST":
        voter["name"] = request.form["name"]
        voter["guardian"] = request.form["guardian"]
        voter["party"] = request.form["party"]
        return redirect(url_for("home"))
    return render_template("edit.html", voter=voter)

@app.route("/delete/<houseno>")
def delete_voter(houseno):
    global voters
    voters = [v for v in voters if v["houseno"] != houseno]
    return redirect(url_for("home"))

@app.route("/summary")
def vote_summary():
    party_counts = {"LDF": 0, "UDF": 0, "NDA": 0}
    for voter in voters:
        party = voter["party"]
        if party in party_counts:
            party_counts[party] += 1
    total_votes = sum(party_counts.values())
    return render_template("summary.html", party_counts=party_counts, total_votes=total_votes)

@app.route("/logout")
def logout():
    return "Logout working!"

if __name__ == "__main__":
    app.run(debug=True)
