from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
DATA_PATH = 'sec.kerala.gov.csv'

def get_dataframe():
    df = pd.read_csv(DATA_PATH)
    # id column add if missing
    if 'id' not in df.columns:
        df['id'] = df.index + 1
    return df

@app.route('/')
def home():
    df = get_dataframe()
    total_voters = df.shape[0]
    party_counts = df['Political Party'].value_counts()

    if len(party_counts) >= 2:
        top_counts = party_counts.nlargest(2).values
        winning_margin = top_counts[0] - top_counts[1]
    elif len(party_counts) == 1:
        winning_margin = party_counts.iloc[0]
    else:
        winning_margin = 0

    voters = df.to_dict('records')
    is_admin = True

    return render_template('summary.html', voters=voters, total_voters=total_voters,
                           winning_margin=winning_margin, is_admin=is_admin)

@app.route('/add', methods=['POST'])
def add_voter():
    df = get_dataframe()
    name = request.form.get('name')
    guardian = request.form.get("guardian")
    house_no = request.form.get("house_no")
    house_name = request.form.get("house_name")
    party = request.form.get('party')
    new_id = df['id'].max() + 1
    new_voter = {
        'id': new_id,
        'Name': name,
        "Guardian's Name": guardian,
        "House No.": house_no,
        "House Name": house_name,
        'Political Party': party
    }
    df = df.append(new_voter, ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return redirect('/')

@app.route('/edit/<int:voter_id>', methods=['GET', 'POST'])
def edit_voter(voter_id):
    df = get_dataframe()
    if request.method == 'POST':
        name = request.form.get('name')
        guardian = request.form.get("guardian")
        house_no = request.form.get("house_no")
        house_name = request.form.get("house_name")
        party = request.form.get('party')
        df.loc[df['id'] == voter_id, ['Name', "Guardian's Name", "House No.", "House Name", 'Political Party']] = [
            name, guardian, house_no, house_name, party
        ]
        df.to_csv(DATA_PATH, index=False)
        return redirect('/')
    else:
        voter = df[df['id'] == voter_id].to_dict('records')[0]
        return render_template('edit_voter.html', voter=voter)

@app.route('/delete/<int:voter_id>', methods=['POST'])
def delete_voter(voter_id):
    df = get_dataframe()
    df = df[df['id'] != voter_id]
    df.to_csv(DATA_PATH, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render.com-ൽ $PORT environment variable ആണ്
    app.run(debug=False, host='0.0.0.0', port=port)
