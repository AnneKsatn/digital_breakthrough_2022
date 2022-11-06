from flask import Flask, jsonify, request
import pandas as pd
import json
from flask_cors import CORS, cross_origin
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import ast

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login")
@cross_origin()
def login():
    login = request.args.get('login')
    password = request.args.get('pass')
    response = False

    print(login, password)

    if(login =="admin" and password == "admin"):
        response = True

    return jsonify(response) 


@app.route("/postmats/rivals")
@cross_origin()
def get_rival_postmats():
    df = pd.read_csv('postsomats.csv', delimiter=',')
    df = df[['Широта', 'Долгота']]
    
    result = df.to_json(orient="split")
    parsed = json.loads(result)
    resp = json.dumps(parsed, indent=4, ensure_ascii=False) 

    return resp


@app.route("/postmats/reccomended")
@cross_origin()
def get_recommended_postmats():

    df = pd.read_excel(r'Реестр_домов_geop_area_dist_not_all.xls')
    df1 = pd.read_csv(r'Primary-Places.csv')
    df2 = pd.read_csv(r'postsomats.csv')
    df3 = pd.read_csv(r'prises_norm.csv')
    df4 = pd.read_csv(r'zk.csv')

    priceStd = np.std(np.array(df3['price/m']))
    priceMean = np.mean(np.array(df3['price/m']))
    priceMax = np.max(np.array(df3['price/m']))

    def calc(n, city_areas):
        df_only_arr = df[df['city_area'].isin(city_areas)]
        lon = df_only_arr['coord_lst'].apply(lambda x: ast.literal_eval(x)[0]).values
        lat = df_only_arr['coord_lst'].apply(lambda x: ast.literal_eval(x)[1]).values
        geo = []
        for i in range(len(df_only_arr)):
            geo.append([float(lon[i]), float(lat[i])])
    
        kmeans = KMeans(n_clusters=n).fit(np.array(geo))
        centers = kmeans.cluster_centers_
        
        df_final = pd.DataFrame()
        
        for center in centers:
            
            min_p = 1000
            priority_row = df1.iloc[0]
            for i in range(len(df1)):
                p = np.array([float(df1['Широта'][i]),float(df1['Долгота'][i])])
                if np.linalg.norm(center-p) < min_p:
                    min_p=np.linalg.norm(center-p)
                    priority_row = df1.iloc[i]  

            min_p = 1000
            zk_row = df4.iloc[0]
            
            for i in range(len(df4)):
                p = np.array([float(df4['Широта'][i]),float(df4['Долгота'][i])])
                if np.linalg.norm(center-p) < min_p:
                    min_p=np.linalg.norm(center-p)
                    zk_row = df4.iloc[i] 

            df_final = df_final.append(zk_row)
    #         df_final = df_final.append(priority_row)
        return df_final

    districs = request.args.get('districts[]').split(",")
    print(districs)
    amount = int(request.args.get('amount'))
    print(amount)

    df = calc(amount, districs)
    df = df[['Наименование', 'Описание', 'Адрес', 'Широта', 'Долгота']]
    
    result = df.to_json(orient="split")
    parsed = json.loads(result)
    resp = json.dumps(parsed, indent=4, ensure_ascii=False) 

    return resp


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')