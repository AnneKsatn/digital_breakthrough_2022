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
    df5 = pd.read_csv('Реестр_домов_v10.csv') # house_data

    priceStd = np.std(np.array(df3['price/m']))
    priceMean = np.mean(np.array(df3['price/m']))
    priceMax = np.max(np.array(df3['price/m']))
    def HuffPro(A,D,alpha,beta):
        return pow(A,alpha)/pow(D,beta)

    def HuffModel(mx,alpha,beta,att_field):
        cbg_sum = {}
        for i,row in mx.iterrows():
            if mx.loc[i]["census_block_group"] not in cbg_sum.keys():
                A = mx.loc[i][att_field]
                D = mx.loc[i]["distance"]
                cbg_sum[mx.loc[i]["census_block_group"]] = HuffPro(A,D,alpha,beta)
            else:
                A = mx.loc[i][att_field]
                D = mx.loc[i]["distance"]
                cbg_sum[mx.loc[i]["census_block_group"]] += HuffPro(A,D,alpha,beta)
        mx["pro"] = ""
        mx["h_sum"] = ""
        for i,row in mx.iterrows():
            mx.loc[i,"h_sum"] = cbg_sum[mx.loc[i]["census_block_group"]]
            A = mx.loc[i][att_field]
            D = mx.loc[i]["distance"]
            mx.loc[i,"pro"] =  HuffPro(A,D,alpha,beta)/mx.loc[i]["h_sum"]
        return mx

    def mor_les(x):
        if x['Площадь м2']>=x['mean_sq']:
            return 1
        else:
            return -1
        
    def get_dst(x):
        coord_lst_house = x['coord_lst_house']
        coord_lst = ast.literal_eval(x['coord_lst'])
        return (
            (coord_lst_house[0]-coord_lst[0])**2 + 
            (coord_lst_house[1]-coord_lst[1])**2
        )**0.5

    def CalcHuff(house_data, df_only_arr, area_list, post, labels):
        house_data=house_data.drop_duplicates(subset=['Адрес'])

        house_data_geo_new_feat = df_only_arr.merge(house_data[['Адрес','Площадь м2']], on='Адрес', how='left')

    #     house_data_geo_new_feat = df_only_arr#house_data_geo_new_feat[house_data_geo_new_feat['city_area'].isin(area_list)]#df_only_arr
        
        post_df = pd.DataFrame(post).reset_index().rename(columns={'index':'id'})
        post_df['coord_lst_house'] = post_df.apply(lambda x: [x[0],x[1]], axis=1)
        post_df = post_df.drop(columns=[0,1])
    #     post_df.iloc[0]['id']
        
    #     df_mg = pd.DataFrame(columns=['id_house', 'id_post', 'coord_lst_house'])
    #     for i in range(len(post_df)):
    #         for j in range(len(house_data_geo_new_feat)):
    #             df_mg = df_mg.append({'id_house':post_df.iloc[i]['id'], 
    #                           'id_post':house_data_geo_new_feat.iloc[j]['id'], 
    #                           'coord_lst_house':post_df.iloc[i]['coord_lst']
    #                          }, ignore_index=True)
        house_data_geo_new_feat['id_house'] = labels
        
        df_mg_merged = house_data_geo_new_feat.merge(post_df.rename(columns={'id':'id_house'}), on='id_house')
        df_mg_merged = df_mg_merged.rename(columns={'id':'id_post'})
        #df_mg.merge(house_data_geo_new_feat.rename(columns={'id':'id_post'}), on='id_post')
        df_mg_merged['distance'] = df_mg_merged.apply(lambda x:  get_dst(x),axis=1)
        
        df_mg_merged_huff = df_mg_merged.rename(columns={'id_post':'census_block_group'})
        df_mg_merged_huff = df_mg_merged_huff[df_mg_merged_huff['Площадь м2'] != 'Не заполнено']
        df_mg_merged_huff = df_mg_merged_huff[df_mg_merged_huff['Площадь м2'].notna()]
        df_mg_merged_huff = df_mg_merged_huff[df_mg_merged_huff['Площадь м2'].apply(lambda x: isinstance(x,str) or isinstance(x,int) or isinstance(x,float))]
        df_mg_merged_huff['Площадь м2'] = df_mg_merged_huff['Площадь м2'].astype(float)
        df_mg_merged_huff = df_mg_merged_huff[df_mg_merged_huff.distance < 0.04]
        maaax = HuffModel(df_mg_merged_huff,0.5,0.5,'Площадь м2')
        maaax['pro'] = maaax['pro'].astype(float)
        maaax['coord_lst'] = maaax.apply(lambda x: ast.literal_eval(x['coord_lst']), axis=1)
        maaax['vec_0'] = maaax.apply(lambda x: x['coord_lst_house'][0]-x['coord_lst'][0],axis=1 )
        maaax['vec_1'] = maaax.apply(lambda x: x['coord_lst_house'][1]-x['coord_lst'][1],axis=1 )

        agg_res = maaax.groupby('id_house').agg({'Площадь м2':'mean'}).reset_index().rename(columns={'Площадь м2':'mean_sq'})

        maaax_mean = maaax.merge(agg_res, on='id_house')

        def mor_les(x):
            if x['Площадь м2']>=x['mean_sq']:
                return 1
            else:
                return -1

        maaax_mean['more_or_less'] = maaax_mean.apply(lambda x: mor_les(x),axis=1)

        maaax_mean['shift_0'] = maaax_mean['vec_0']*maaax_mean['more_or_less']*(1-maaax_mean['pro'])
        maaax_mean['shift_1'] = maaax_mean['vec_1']*maaax_mean['more_or_less']*(1-maaax_mean['pro'])
        
        agg_shift = maaax_mean.groupby('id_house').agg({'coord_lst_house':list,'shift_0':'mean', 'shift_1':'mean'}).reset_index().rename(columns={'coord_lst_house':'coord_lst_house_lst','shift_0':'shift_0_res','shift_1':'shift_1_res'})
        agg_shift['coord_lst_house'] = agg_shift['coord_lst_house_lst'].apply(lambda x: x[0])
        agg_shift['coord_new'] = agg_shift.apply(lambda x: [x['coord_lst_house'][0] + x['shift_0_res'], x['coord_lst_house'][1] + x['shift_1_res']],axis=1)

        res_lst = []
        for h in agg_shift['coord_new'].values:
            res_lst.append(h)

        result_huff = np.array(res_lst)
        
        return result_huff
        
    def calc(n, city_areas):

        df_only_arr = df[df['city_area'].isin(city_areas)]
        lon = df_only_arr['coord_lst'].apply(lambda x: ast.literal_eval(x)[0]).values
        lat = df_only_arr['coord_lst'].apply(lambda x: ast.literal_eval(x)[1]).values
        geo = []
        for i in range(len(df_only_arr)):
            geo.append([float(lon[i]), float(lat[i])])
    
        kmeans = KMeans(n_clusters=n).fit(np.array(geo))
        centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        centers = CalcHuff(df5, df_only_arr, city_areas, centers, labels)
        
        
        filan_list = []
        coord = []
        coord1 = []
        coord2 = []
        address = []
        discript = []
        area = []
        name = []
        label = 0
        
        for center in centers:
            min_p1 = 1000
            df_row = df_only_arr.iloc[0]
            geos = []
            for i in range(len(df_only_arr)):
                if labels[i]==label:
                    dist =  np.linalg.norm(center-geo[i])
                    if dist < min_p1:
                        min_p1=dist
                        df_row = df_only_arr.iloc[i]
                        geos = geo[i]
            min_p2 = 1000
            priority_row = df1.iloc[0]
            for i in range(len(df1)):
                p = np.array([float(df1['Широта'][i]),float(df1['Долгота'][i])])
                dist = np.linalg.norm(center-p)
                if dist < min_p2:
                    min_p2 = dist
                    priority_row = df1.iloc[i]  

            min_p3 = 1000
            zk_row = df4.iloc[0]
            for i in range(len(df4)):
                p = np.array([float(df4['Широта'][i]),float(df4['Долгота'][i])])
                dist = np.linalg.norm(center-p)
                if dist < min_p3:
                    min_p3 = dist
                    zk_row = df4.iloc[i] 

            if min_p2 <= min(min_p1, min_p3):
                filan_list.append(priority_row)
                name.append(priority_row['Наименование'])
                address.append(priority_row['Адрес'])
                discript.append(priority_row['Рубрики'])
                area.append(priority_row['Округ'])
                coord.append(np.array([float(priority_row['Широта']),float(priority_row['Долгота'])]))
                coord1.append(float(priority_row['Широта']))
                coord2.append(float(priority_row['Долгота']))
            else:
                if min_p3 <= min_p1:
                    filan_list.append(zk_row)
                    name.append(zk_row['Наименование'])
                    address.append(zk_row['Адрес'])
                    discript.append(zk_row['Описание'])
                    area.append(zk_row['Округ'])
                    coord1.append(float(priority_row['Широта']))
                    coord2.append(float(priority_row['Долгота']))
                    coord.append( np.array([float(zk_row['Широта']),float(zk_row['Долгота'])]))
                else:
                    filan_list.append(df_row)
                    address.append(df_row['Адрес'])
                    discript.append('Отсутствует')
                    name.append('Здание')
                    area.append(df_row['city_area'])
                    coord1.append(geos[0])
                    coord2.append(geos[1])
                    coord.append(geos)
                    
        df_final = pd.DataFrame(filan_list)
        df_final = pd.DataFrame({'Адрес':address,
                                'Наименование':name,
                                'Описание':discript,
                                'Округ':area,
                                'Координаты':coord,
                                'Широта':coord1,
                                'Долгота':coord2})  
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