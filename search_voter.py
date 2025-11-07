from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
FILENAME = "sec.kerala.gov.csv"

def read_voters():
    return pd.read_csv(FILENAME, encoding="utf-8")

def write_voters(df):
    df.to_csv(FILENAME, encoding="utf-8", index=False)

@app.route('/')
def home():
    df = read_voters()
    voters = df.to_dict('records')
    return render_template('home.html', voters=voters)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['q'].strip().lower()
        df = read_voters()
        results = df[(df['Name'].str.lower().str.contains(query)) | (df["Guardian's Name"].str.lower().str.contains(query))].to_dict('records')
    return render_template('search.html', results=results)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        df = read_voters()
        new_entry = {
            'Name': request.form['name'],
            "Guardian's Name": request.form['guardian'],
            'House No': request.form['house_no'],
            'House Name': request.form['house_name'],
            'Political Party': request.form['party']
        }
        df = df.append(new_entry, ignore_index=True)
        write_voters(df)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    df = read_voters()
    if request.method == 'POST':
        df.at[index, 'Name'] = request.form['name']
        df.at[index, "Guardian's Name"] = request.form['guardian']
        df.at[index, 'House No'] = request.form['house_no']
        df.at[index, 'House Name'] = request.form['house_name']
        df.at[index, 'Political Party'] = request.form['party']
        write_voters(df)
        return redirect(url_for('home'))
    voter = df.iloc[index].to_dict()
    return render_template('edit.html', voter=voter, index=index)

@app.route('/delete/<int:index>')
def delete(index):
    df = read_voters()
    df = df.drop(index)
    write_voters(df.reset_index(drop=True))
    return redirect(url_for('home'))

@app.route('/summary')
def summary():
    df = read_voters()
    total = len(df)
    summary = df['Political Party'].value_counts().to_dict()
    return render_template('summary.html', total=total, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
