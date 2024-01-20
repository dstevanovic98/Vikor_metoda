from calculate_vikor import vikor
import numpy as np

from flask import Flask, render_template, request, redirect, url_for , session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/',methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    number_of_criteria = int(request.form.get('number_of_criteria'))
    number_of_alternatives = int(request.form.get('number_of_alternatives'))
    session['num_of_criteria'] = number_of_criteria
    session['num_of_alternatives'] = number_of_alternatives
    return redirect('/add_criterias')


# CRITERIAS
@app.route('/add_criterias/')
def add_num_of_criterias():
    return render_template('add_criterias.html', num_of_criteria = range(session['num_of_criteria']))

@app.route('/add_criterias', methods=['POST'])
def add_criterias_new():
    criteries = []
    for i in range(session["num_of_criteria"]):
        current_criteria = request.form.get(f"Kriterij{i+1}")
        criteries.append(current_criteria)
    
    session["criteria_values"] = criteries   
    print(criteries)
    return redirect('/add_alternatives')


# ALTERNATIVES
@app.route('/add_alternatives/')
def add_num_of_alternatives():
    return render_template('add_alternatives.html',num_of_alternatives = range(session['num_of_alternatives']), num_of_criteria = range(session['num_of_criteria']))

@app.route('/add_alternatives/', methods=['POST'])
def add_alternatives_names():
    alternative_names = []
    alternative_values = []
    for i in range(session['num_of_alternatives']):
        current_alternative_name = request.form.get(f"Alternativa{i+1}")
        alternative_names.append(current_alternative_name)
        for j in range(session['num_of_criteria']):
            current_alternative_value = request.form.get(f"Alternativa_kriterij{ j + 1 }+{ i + 1 }")
            alternative_values.append(current_alternative_value)
        
    session["criteria_alternative_names"] = alternative_names
    session["criteria_alternative_values"] = alternative_values   
    print(alternative_names)
    print(alternative_values)
    return redirect('/add_weights')


# WEIGHTS
@app.route('/add_weights/')
def add_num_of_weights():
    return render_template('add_weights.html',num_of_weights = range(session['num_of_criteria']))

@app.route('/add_weights/', methods=['POST'])
def add_weights_new():
    weights = []
    atributes = []
    for i in range(session['num_of_criteria']):
        current_weight = float(request.form.get(f"Weight{i+1}").replace(',', '.'))
        current_atribute = request.form.get(f"Atribute{i+1}") == "True"
        weights.append(current_weight)
        atributes.append(current_atribute)
    
    session["weight_values"] = weights
    session["atribute_values"] = atributes
    print(weights)
    print(atributes)
    return redirect('/main')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/main/')
def main():
    number_of_criteria = session['num_of_criteria']
    number_of_alternatives = session['num_of_alternatives'] 
    alternative_values = session["criteria_alternative_values"]
    alternative_names = session["criteria_alternative_names"]
    atribute_values = session["atribute_values"]
    weights = session["weight_values"]
    data2 = np.array([float(n) for n in alternative_values]).reshape(number_of_alternatives, number_of_criteria)
    
    print(data2)
    print(atribute_values)
    print(weights)
    print(alternative_values)
    result = vikor(data2,alternative_names,atribute_values,weights,0.5)
    print(result)
    return render_template('main.html', result = result)



if __name__ == '__main__':
    app.run(debug=True)
