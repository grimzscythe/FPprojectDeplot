from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from joblib import load

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

app =Flask(__name__)
@app.route("/")
def table():
    return render_template("main_page.html")

# death_insight.html
deathrate = pd.read_csv('templates/csv/causes-of-death-All Ages.csv')
dfcountry = pd.DataFrame(np.array(['Global']+list(deathrate['location'].unique())),columns = ['country'])
dfagelist = pd.DataFrame(np.array(['All Ages','Under 5','5-14 years','15-49 years','50-69 years','70+ years']),columns = ['age'])
dfcountry['index'] = [str(i) for i in range(len(dfcountry))]
dfagelist['index'] = [str(i) for i in range(len(dfagelist))]
country = 'Global'
age = 'All Ages'
countryselect = np.where(dfcountry['country'] == country , 1 , 0)
ageselect = np.where(dfagelist['age'] == age , 1 , 0)
dfcountry['check'] = countryselect
dfagelist['check'] = ageselect

@app.route('/death_insight')
def death_insight():
    return render_template('death_insight.html',dfcountry = dfcountry,dfagelist = dfagelist,country = country,age=age)

@app.route('/death_insight', methods = ['POST'])
def death_insight_cont():
    global country
    global age
    countryindex = request.form['country']
    ageindex = request.form['age']
    country = list(dfcountry[dfcountry['index'] == countryindex]['country'])[0]
    age = list(dfagelist[dfagelist['index'] == ageindex]['age'])[0]
    countryselect = np.where(dfcountry['country'] == country , 1 , 0)
    ageselect = np.where(dfagelist['age'] == age , 1 , 0)
    dfcountry['check'] = countryselect
    dfagelist['check'] = ageselect
    return render_template('death_insight.html',dfcountry = dfcountry,dfagelist = dfagelist,country = country,age=age)

@app.route('/causeshow')
def causeshow():
    global country
    global age
    html = country + "_" + age + "_cause.html"
    return render_template("graph/" + html)

@app.route('/categoryshow')
def categoryshow():
    global country
    global age
    html = country + "_" + age + "_category.html"
    return render_template("graph/" + html)

@app.route('/riskshow')
def riskshow():
    global country
    global age
    html = country + "_" + age + "_risk.html"
    return render_template("graph/" + html)    

# data_insight.html

countries = {'Algeria':['World','Africa'], 'Egypt':['World','Africa'], 'Kenya':['World','Africa'], 
             'Liberia':['World','Africa'], 'South Africa':['World','Africa'], 'Zimbabwe':['World','Africa'],
             'China':['World','Asia'], 'India':['World','Asia'], 'Indonesia':['World','Asia'], 
             'Iraq':['World','Asia'], 'Japan':['World','Asia'], 'Thailand':['World','Asia'],
             'Finland':['World','Europe'], 'Germany':['World','Europe'], 'Greece':['World','Europe'], 
             'Spain':['World','Europe'], 'Ukraine':['World','Europe'], 'United Kingdom of Great Britain and Northern Ireland':['World','Europe'],
             'Canada':['World','North America'], 'Cuba':['World','North America'], 'El Salvador':['World','North America'], 
             'Mexico':['World','North America'], 'Panama':['World','North America'], 'United States of America':['World','North America'],
             'Australia':['World','Oceania'], 'New Zealand':['World','Oceania'], 'Papua New Guinea':['World','Oceania'], 
             'Samoa':['World','Oceania'], 'Solomon Islands':['World','Oceania'], 'Tonga':['World','Oceania'],
             'Argentina':['World','South America'], 'Brazil':['World','South America'], 'Colombia':['World','South America'], 
             'Paraguay':['World','South America'], 'Peru':['World','South America'], 'Venezuela (Bolivarian Republic of)':['World','South America']}
countries = dict(sorted(countries.items()))
dfcountry2 = pd.DataFrame(countries.items(),columns = ['country','continent'])
dfcountry2['index'] = [str(i) for i in range(len(dfcountry2))]
country2 = 'Algeria'
country2select = np.where(dfcountry2['country'] == country2 , 1 , 0)
dfcountry2['check'] = country2select
dffactors = pd.DataFrame(['Populational Factors','Economical and Political Factors','Environmental Factors','Health Related Factors','Vaccination Coverage Factors','Disease and Virus Factors'],columns=['factor'])
dffactors['index'] = [str(i) for i in range(len(dffactors))]
factor = 'Populational Factors'
factorselect = np.where(dffactors['factor'] == factor , 1 , 0)
dffactors['check'] = factorselect
continent = "World"

@app.route('/data_insight')
def data_insight():
    return render_template('data_insight.html',dfcountry = dfcountry2,dffactors = dffactors,country = country2,factor=factor,continent = continent)

@app.route('/data_insight', methods = ['POST'])
def data_insight_cont():
    global country2
    global factor
    global continent
    countryindex = request.form['country']
    continent = request.form['continent']
    factorindex = request.form['factor']
    country3 = list(dfcountry2[dfcountry2['index'] == countryindex]['country'])[0]
    for i in dfcountry2[dfcountry2['country'] == country3]['continent'] :
        for j in i :
            if continent in j :
                continent = j
    if country3 != country2 :
        continent = "World"
        country2 = country3
    factor = list(dffactors[dffactors['index'] == factorindex]['factor'])[0]
    country2select = np.where(dfcountry2['country'] == country2 , 1 , 0)
    factorselect = np.where(dffactors['factor'] == factor , 1 , 0)
    dfcountry2['check'] = country2select
    dffactors['check'] = factorselect
    return render_template('data_insight.html',dfcountry = dfcountry2,dffactors = dffactors,country = country2,factor=factor,continent = continent)

@app.route('/factorshow')
def factorshow():
    global country2
    global continent
    global factor
    html = country2 + " vs " + continent + " - " + factor +".html"
    return render_template("graph2/" + html)

# model.html
loaded_model = load("templates/model.joblib.dat")
data = pd.read_csv('templates/csv/cleandata_impute_all.csv')
data = data.sort_values(['country name','year']).reset_index().iloc[:,1:]
column = data.iloc[:,4:].columns
dfcolumn = pd.DataFrame(column,columns=['c'])
dfcolumn['i'] = [i for i in range(len(dfcolumn))]
dfcolumn['index'] = [i for i in range(len(dfcolumn))]
for i in column :
    data[i] = data[i].astype('int')

countryindata = 'Afghanistan'
yearindata = 2019
dfcountryindata = pd.DataFrame(data['country name'].unique(),columns = ['country'])
dfyearindata = pd.DataFrame([2019-i for i in range(19)],columns = ['year'])
dfcountryindata['index'] = [str(i) for i in range(len(dfcountryindata))]
dfyearindata['index'] = [str(i) for i in range(len(dfyearindata))]
countryindataselect = np.where(dfcountryindata['country'] == countryindata , 1 , 0)
yearindataselect = np.where(dfyearindata['year'] == yearindata , 1 , 0)
dfcountryindata['check'] = countryindataselect
dfyearindata['check'] = yearindataselect
value = data[(data['country name'] == countryindata) & (data['year'] == yearindata)].iloc[0,4:]
dfcolumn['value'] = list(value)
dfcolumn['new_value'] = list(value)
dfcolumn['mark'] = [0 for i in range(len(dfcolumn))]
# About population == 1
mark1 = dfcolumn[dfcolumn['c'].isin(['population', 'urban population', 'population density','age0-14', 'age15-64', 'age65+', 'schooling years'])].index
dfcolumn.loc[mark1,'mark'] = [1 + 0.01*i for i in range(len(mark1))]
dfcolumn.loc[mark1,'i'] = [i for i in range(len(mark1))]
# Economic andPolitic == 2
mark2 = dfcolumn[dfcolumn['c'].isin(['status', 'gdp per capita', 'inflation', 'unemployment','health expenditure', 'corruption index'])].index
dfcolumn.loc[mark2,'mark'] = [2 + 0.01*i for i in range(len(mark2))]
dfcolumn.loc[mark2,'i'] = [i for i in range(len(mark2))]
# Environtment == 3
mark3 = dfcolumn[dfcolumn['c'].isin(['forest area', 'greenhouse emissions','electricity access','energy consumption'])].index
dfcolumn.loc[mark3,'mark'] = [3 + 0.01*i for i in range(len(mark3))]
dfcolumn.loc[mark3,'i'] = [i for i in range(len(mark3))]
# Health == 4
mark4 = dfcolumn[dfcolumn['c'].isin(['bmi', 'asthma','anxiety disorders', 'depressive disorders', 'schizophrenia'])].index
dfcolumn.loc[mark4,'mark'] = [4 + 0.01*i for i in range(len(mark4))]
dfcolumn.loc[mark4,'i'] = [i for i in range(len(mark4))]
# Vaccination == 5
mark5 = dfcolumn[dfcolumn['c'].isin(['DTP3 %vaccinate', 'HepB3 %vaccinate', 'Measles %vaccinate','Polio %vaccinate'])].index
dfcolumn.loc[mark5,'mark'] = [5 + 0.01*i for i in range(len(mark5))]
dfcolumn.loc[mark5,'i'] = [i for i in range(len(mark5))]
# Disease == 6
mark6 = dfcolumn[dfcolumn['c'].isin(['hepatitis b', 'tuberculosis','cardiovascular diseases', 'chronic respiratory diseases','diabetes and kidney diseases', 'enteric infections', 'neoplasms','nutritional deficiencies', 'sexually transmitted infections','tropical diseases and malaria'])].index
dfcolumn.loc[mark6,'mark'] = [6 + 0.01*i for i in range(len(mark6))]
dfcolumn.loc[mark6,'i'] = [i for i in range(len(mark6))]

deathrate = round(list(data[(data['country name'] == countryindata) & (data['year'] == yearindata)]['death rate'])[0],2)

@app.route('/model')
def model():
    return render_template('model.html',dfcountryindata = dfcountryindata,dfyearindata=dfyearindata,countryindata = countryindata,yearindata=yearindata,deathrate = deathrate)

@app.route('/model', methods = ['POST'])
def model_cont():
    global countryindata
    global yearindata
    countryindex = request.form['country']
    yearindex = request.form['year']
    countryindata = list(dfcountryindata[dfcountryindata['index'] == countryindex]['country'])[0]
    yearindata = list(dfyearindata[dfyearindata['index'] == yearindex]['year'])[0]
    countryindataselect = np.where(dfcountryindata['country'] == countryindata , 1 , 0)
    yearindataselect = np.where(dfyearindata['year'] == yearindata , 1 , 0)
    dfcountryindata['check'] = countryindataselect
    dfyearindata['check'] = yearindataselect
    value = data[(data['country name'] == countryindata) & (data['year'] == yearindata)].iloc[0,4:]
    dfcolumn['value'] = list(value)
    dfcolumn['new_value'] = list(value)
    deathrate = round(list(data[(data['country name'] == countryindata) & (data['year'] == yearindata)]['death rate'])[0],2)
    return render_template('model.html',dfcountryindata = dfcountryindata,dfyearindata=dfyearindata,countryindata = countryindata,yearindata=yearindata,deathrate = deathrate)
original_pred = 0

@app.route('/deploymodel')
def deploymodel():
    global original_pred
    x = np.array([dfcolumn['new_value']])
    trees = loaded_model.estimators_
    y_pred = loaded_model.init_.predict(x.reshape(1, -1))

    for tree in trees:
        pred = tree[0].predict(x.reshape(1, -1))
        y_pred = y_pred + loaded_model.learning_rate*pred
    original_pred = round(y_pred[0],2)
    diff = 0
    return render_template('deploymodel.html',dfcolumn = dfcolumn,original_pred = original_pred, predict =original_pred,diff = diff)

@app.route('/deploymodel', methods = ['POST'])
def deploymodel_cont():
    global dfcolumn
    global original_pred
    input_values = request.form
    for i,j in input_values.items() :
        if isfloat(j) :
            dfcolumn.loc[dfcolumn['index'] == int(i),'new_value'] = int(float(j)//1)
        else :
            dfcolumn.loc[dfcolumn['index'] == int(i),'new_value'] = dfcolumn.loc[dfcolumn['index'] == int(i),'value']
    x = np.array([dfcolumn['new_value']])
    trees = loaded_model.estimators_
    y_pred = loaded_model.init_.predict(x.reshape(1, -1))

    for tree in trees:
        pred = tree[0].predict(x.reshape(1, -1))
        y_pred = round((y_pred + loaded_model.learning_rate*pred)[0],2)
    diff = round(y_pred-original_pred,2)
    return render_template('deploymodel.html',dfcolumn = dfcolumn,original_pred = original_pred , predict =y_pred,diff = diff)