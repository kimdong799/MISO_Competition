# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
# import joblib
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics.pairwise import linear_kernel
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

# Flask 객체로 app 변수 생성
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

# 기본경로에 사용자가 접속했을 때 GET, POST 메소드로 처리
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('user_input.html')

    if request.method == 'POST':
        user_sex = request.form['sex']
        user_cat = request.form['cat']
        user_usage = request.form['usage']   
        
        user_select_df = pd.DataFrame(np.array([[user_sex, user_cat, user_usage]]))
        user_select_df.columns = ['성별', '카테고리', '용도']
        user_select_df = user_select_df.reset_index()
        user_select_df.rename(columns={'index':'상품명'}, inplace=True)
        user_select_df['상품명'] = 'user_preference'

        product_df_org = pd.read_excel('./data/추천시스템용 유아복데이터.xlsx')
        product_df=product_df_org[['상품명','성별','카테고리','용도']]

        product_df = product_df.append(user_select_df).reset_index()
        product_df.drop('index', axis=1)

        product_df_ohc=pd.get_dummies(data=product_df,columns=['성별'],prefix='성별')
        product_df_ohc=pd.get_dummies(data=product_df_ohc,columns=['카테고리'],prefix='카테고리')
        product_df_ohc=pd.get_dummies(data=product_df_ohc,columns=['용도'],prefix='용도')
        product_df_ohc.drop('index', axis=1, inplace=True)

        def cos_sim(A, B):
            return dot(A, B)/(norm(A)*norm(B))
            
        product_df_ohc.set_index(['상품명'],inplace=True)

        cosine_sim = linear_kernel(product_df_ohc, product_df_ohc)
        # 코사인 유사도가 1이 초과하는 경우로 인한 /3 처리
        cosine_sim = cosine_sim/3
        
        indices =pd.Series(range(len(product_df_ohc)),index=product_df_ohc.index)
        indices1=pd.Series(product_df_ohc.index)

        product_df = product_df.reset_index()
        product_df.drop('index', axis=1, inplace=True)
        
        def get_recommendations(title, cosine_sim=cosine_sim):
            # 선택한 영화의 타이틀로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 영화를 가지고 연산할 수 있습니다.
            idx = indices[title]

            # 모든 영화에 대해서 해당 상품과의 유사도를 구합니다.
            sim_scores = list(enumerate(cosine_sim[idx]))

            # 유사도에 따라 상품들을 정렬합니다.
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # 가장 유사한 10개의 상품을 받아옵니다.
            sim_scores = sim_scores[1:11]
    
            # 가장 유사한 10개의 상품의 인덱스를 받아옵니다.
            item_indices = [i[0] for i in sim_scores]
            sim_scores_for_df = [i[1] for i in sim_scores]
            print(sim_scores_for_df)
    
            result=pd.DataFrame(indices1[item_indices])
            laster=pd.merge(result,product_df_org,how='left' )
    
            # user_preference가 출력되는 오류 방지
            if laster['상품명'].str.contains('user_preference').any():
                print('start condition code')
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:12]
                item_indices = [i[0] for i in sim_scores]
                sim_scores_for_df = [i[1] for i in sim_scores]
                result=pd.DataFrame(indices1[item_indices])
                laster=pd.merge(result,product_df_org,how='left')
        
            laster = laster[['상품명', '이미지링크', '정상가', '할인가']]
            sim_socres_df = pd.DataFrame({'유사도':sim_scores_for_df})
            sim_socres_df = sim_socres_df['유사도'].round(1)
            result = pd.concat([laster, sim_socres_df], axis=1)
    
            # user_preference 삭제
            if (result['상품명'] == 'user_preference').any():
                result = result[result['상품명'] != 'user_preference']
        
            # 가장 유사한 10개의 상품명 리턴합니다.
            return result

        result_df = get_recommendations('user_preference')

        return render_template('index.html', recommend_list = result_df)

# main 함수로 정의해서 플라스크 구동
if __name__ == '__main__':
    app.run(debug=True)