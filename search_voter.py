from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
DATA_PATH = 'sec.kerala.gov.csv'

@app.route('/')
def home():
    df = pd.read_csv(DATA_PATH)
    total_voters = df.shape[0]
    party_counts = df['party'].value_counts()

    if len(party_counts) >= 2:
        top_counts = party_counts.nlargest(2).values
        winning_margin = top_counts[0] - top_counts[1]
    elif len(party_counts) == 1:
        winning_margin = party_counts.iloc[0]
    else:
        winning_margin = 0

    voters = df.to_dict('records')
    # Admin simulation - replace with real auth in production
    is_admin = True

    return render_template('summary.html', voters=voters, total_voters=total_voters,
                           winning_margin=winning_margin, is_admin=is_admin)

@app.route('/add', methods=['POST'])
def add_voter():
    df = pd.read_csv(DATA_PATH)
    name = request.form.get('name')
    ward = request.form.get('ward')
    party = request.form.get('party')

    new_id = df['id'].max() + 1 if 'id' in df.columns else len(df) + 1
    new_voter = {'id': new_id, 'name': name, 'ward': ward, 'party': party}
    df = df.append(new_voter, ignore_index=True)
    df.to_csv(DATA_PATH, index=False)
    return redirect('/')

@app.route('/edit/<int:voter_id>', methods=['GET', 'POST'])
def edit_voter(voter_id):
    df = pd.read_csv(DATA_PATH)
    if request.method == 'POST':
        name = request.form.get('name')
        ward = request.form.get('ward')
        party = request.form.get('party')
        df.loc[df['id'] == voter_id, ['name', 'ward', 'party']] = [name, ward, party]
        df.to_csv(DATA_PATH, index=False)
        return redirect('/')
    else:
        voter = df[df['id'] == voter_id].to_dict('records')[0]
        return render_template('edit_voter.html', voter=voter)

@app.route('/delete/<int:voter_id>', methods=['POST'])
def delete_voter(voter_id):
    df = pd.read_csv(DATA_PATH)
    df = df[df['id'] != voter_id]
    df.to_csv(DATA_PATH, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
