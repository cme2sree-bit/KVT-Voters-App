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
        results = df[
            (df['Name'].str.lower().str.contains(query)) |
            (df["Guardian's Name"].str.lower().str.contains(query))
        ].to_dict('records')
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
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
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
    df = df.drop(index).reset_index(drop=True)
    write_voters(df)
    return redirect(url_for('home'))

@app.route('/summary')
def summary():
    df = read_voters()
    parties = df['Political Party'].value_counts().to_dict()
    return render_template('summary.html', parties=parties)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
DATA_PATH = 'sec.kerala.gov.csv'

@app.route('/')
def home():
    df = pd.read_csv(DATA_PATH)
    return render_template("summary.html", voters=df.to_dict('records'), is_admin=True) # admin logic as needed

@app.route('/edit/<int:voter_id>', methods=['POST', 'GET'])
def edit_voter(voter_id):
    df = pd.read_csv(DATA_PATH)
    if request.method == 'POST':
        # Collect new data from form (implement form modal separately) & update voter
        new_name = request.form.get('name')
        df.loc[df['id'] == voter_id, 'name'] = new_name
        # Repeat for other fields...
        df.to_csv(DATA_PATH, index=False)
        return redirect('/')
    else:
        voter = df[df['id'] == voter_id].to_dict('records')[0]
        return render_template("edit_voter.html", voter=voter)

@app.route('/delete/<int:voter_id>', methods=['POST'])
def delete_voter(voter_id):
    df = pd.read_csv(DATA_PATH)
    df = df[df['id'] != voter_id]
    df.to_csv(DATA_PATH, index=False)
    return redirect('/')
