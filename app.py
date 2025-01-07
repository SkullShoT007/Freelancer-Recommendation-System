from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import difflib

app = Flask(__name__)

# Load the pre-trained models and data
similarity = pickle.load(open('similarity.pkl', 'rb'))
freelance_data = pickle.load(open('freelance.pkl', 'rb'))
freelance_data = pd.DataFrame(freelance_data)

def recommend(search):
    list_of_all_roles = freelance_data['Role'].tolist()

    find_close_match = difflib.get_close_matches(search, list_of_all_roles)

    if not find_close_match:
        return []

    close_match = find_close_match[0]
    index_of_close_match = freelance_data[freelance_data['Role'] == close_match]['Index'].values[0]
    
    similarity_score = list(enumerate(similarity[index_of_close_match]))
    sorted_similar_matches = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    list_of_freelancers = []
    for i, match in enumerate(sorted_similar_matches[:10], start=1):  
        index = match[0]
        
        name_from_index = freelance_data[freelance_data.index == index]['Name'].values[0]
        skills_from_index = freelance_data[freelance_data.index == index]['Skills'].values[0]
        country_from_index = freelance_data[freelance_data.index == index]['Country'].values[0]
        Hourly_Rate_from_index = freelance_data[freelance_data.index == index]['Hourly_Rate'].values[0]

        list_of_freelancers.append({
            'Name': name_from_index,
            'Skills': skills_from_index,
            'Country': country_from_index,
            'Hourly_Rate': Hourly_Rate_from_index
        })

    return list_of_freelancers

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    search = request.form.get('search')
    recommendations = recommend(search)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True) #(Wait for index file) 