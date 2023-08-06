import shap
import numpy as np
import pandas as pd

class TimeSeriesInterpretorRNN:

  def __init__(self,model,background,test,max_output,features):
    self.model = model
    self.background = background
    self.test = test
    self.max_output = max_output
    self.features = features

  def monthly_chart(self):
    model,background,test,features = self.model,self.background,self.test,self.features
    e = shap.DeepExplainer(model, background)
    shap_values = e.shap_values(test,check_additivity=False)

    d1=model.predict_generator(test)-e.expected_value
    d2=shap_values[0][0].sum()
    d3=d2/d1
    shap_values=(shap_values[0][0]/d3)

    shap_df=(pd.DataFrame(shap_values[0][0])).sum(axis=1)

    fig1 = go.Indicator(mode = "gauge+number",value =model.predict_proba(test).item(0),delta={ "reference": max_output},
                    gauge = {'axis': {'range': [None, 1]},'steps' : [{'range': [0, 0.5], 'color': "lightgray"},{'range': [0.5, 1], 'color': "lightgray"}],'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.5}},
                    domain = {'x': [0.0, 0.4], 'y': [0.0, 1]},
                    title = {'text': "Model Probability"})

    fig2 = go.Indicator(mode = "gauge+number",value =shap_values[0][0].sum()+e.expected_value[0],delta={ "reference": max_output },
                        gauge = {'axis': {'range': [None, 1]},'steps' : [{'range': [0, 0.5], 'color': "lightgray"},{'range': [0.5, 1], 'color': "lightgray"}],'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0.5}},
                      domain = {'x': [0.6, 1.0], 'y': [0., 1.00]},
                      title = {'text': "Shap Probability"})

    layout = go.Layout(height = 600,width = 600,autosize = False,title = 'Comparision of Shap and Model Predicted Value')
    fig = go.Figure(data = [fig1, fig2], layout = layout)
    fig.show()


    fig = go.Figure(data=go.Scatter(x=shap_df.index, y=shap_df.values, mode='lines+markers',name="line plot with respect to months"))
    fig.update_layout(autosize=False,width=2000,height=600,title = "SHAP values - Monthly Time Frame",showlegend = True,font_size=20)
    fig.update_layout(xaxis_title="Months",yaxis_title="Shap Score")

    fig.show()


    text=shap_df.add(e.expected_value[0])
    shap_dff=pd.DataFrame(shap_df)
    shap_dff["Color"] = np.where(shap_dff[0]<0, 'red', 'green')
    fig = go.Figure(go.Bar(orientation = "v",x =shap_dff.index,text = text,y = shap_dff[0].values,marker=dict(color=shap_dff["Color"])))
    fig.update_traces(base=e.expected_value[0], selector=dict(type='Bar'),textfont_size=30,hoverlabel_font_size=20,insidetextfont_size=30)
    fig.update_layout(autosize=False,width=2000,height=700,title = "SHAP values - Monthly Effect (Bar Plot)",showlegend = True,font_size=20)
    fig.update_layout(xaxis_title="Months",yaxis_title="Shap Score")

    fig.show()


    
    fig = go.Figure(go.Waterfall(name = "Visualize", orientation = "v",measure = ["absolute"],x =shap_df.index,text = text,y = shap_df.values,base=e.expected_value[0],connector = {"line":{"color":"rgb(63, 63, 63)"}},))
    fig.update_traces(base=e.expected_value[0], selector=dict(type='waterfall'),textfont_size=30,hoverlabel_font_size=20,insidetextfont_size=30)
    fig.update_layout(autosize=False,width=2000,height=700,title = "SHAP values - Water Fall Plot with respect to Base_Value",showlegend = True,font_size=20)
    fig.update_layout(xaxis_title="Months",yaxis_title="Shap Score with respect to base_value")

    fig.show()

    fig = go.Figure(data=go.Scatter(x=shap_df.index, y=shap_df.values, mode='lines+markers',name="std with respect to months"))
    fig.update_layout(autosize=False,width=2000,height=600,title = "SHAP values - Monthly Time Frame vs Standard Deviation",showlegend = True,font_size=20)
    fig.update_layout(shapes=[dict(type= 'line',xref= 'paper', x0= 0, x1= 1,yref= 'y', y0= shap_df.std(), y1= shap_df.std(),line=dict(color="Red",dash="dashdot"))])
    fig.update_layout(xaxis_title="Months",yaxis_title="Shap Score")

    fig.show()

    std_df=shap_df.sub(shap_df.std())
    fig = go.Figure(data=go.Scatter(x=std_df.index, y=std_df.values, mode='lines+markers',name="std with respect to months"))
    fig.update_layout(autosize=False,width=2000,height=600,title = "SHAP values variation respect to Standard Deviation",showlegend = True,font_size=20)
    fig.update_layout(xaxis_title="Months",yaxis_title="Shap Score")

    fig.show()

    shap.initjs()
    return shap.force_plot(e.expected_value, shap_values[0][0],test[0], feature_names=features,figsize= (20, 5))
    
  def global_patient(self):
    model,background,test,features = self.model,self.background,self.test,self.features
    e = shap.DeepExplainer(model, background)
    shap_values = e.shap_values(test,check_additivity=False)
    d1=model.predict_generator(test)-e.expected_value
    d2=shap_values[0][0].sum()
    d3=d2/d1
    shap_values=(shap_values[0][0]/d3)
    shap_df=(pd.DataFrame(shap_values[0][0])).sum(axis=1)

    p1=shap.summary_plot(shap_values[0][0],test[0],features,plot_type="bar")
    p2=shap.summary_plot(shap_values[0][0], test[0], feature_names=features)
    p3=shap.decision_plot(e.expected_value[0], shap_values[0][0], features)
    p4=shap.dependence_plot(0, shap_values[0][0],test[0], feature_names=features)
    return p1,p2,p3,p4
  
  def single_month(self,month):
    model,background,test,features = self.model,self.background,self.test,self.features
    e = shap.DeepExplainer(model, background)
    shap_values = e.shap_values(test,check_additivity=False)
    d1=model.predict_generator(test)-e.expected_value
    d2=shap_values[0][0].sum()
    d3=d2/d1
    shap_values=(shap_values[0][0]/d3)

    shap_df=(pd.DataFrame(shap_values[0][0])).sum(axis=1)
    test_df=pd.DataFrame(test[0])
    df_reshape=(test_df.iloc[0].values).reshape(1,756)
    
    shap.initjs()
    shap_df_plot=pd.DataFrame(shap_values[0][0])
    return shap.force_plot(e.expected_value, (shap_df_plot.iloc[month]).values,test_df.iloc[month].values, feature_names=features)

  def two_month_compare(self,month1,month2):
    model,background,test,features = self.model,self.background,self.test,self.features
    e = shap.DeepExplainer(model, background)
    shap_values = e.shap_values(test,check_additivity=False)
    d1=model.predict_generator(test)-e.expected_value
    d2=shap_values[0][0].sum()
    d3=d2/d1
    shap_values=(shap_values[0][0]/d3)
    shap_df=(pd.DataFrame(shap_values[0][0])).sum(axis=1)
    shap_df_plot=pd.DataFrame(shap_values[0][0])
    test_df=pd.DataFrame(test[0])
    df_reshape=(test_df.iloc[0].values).reshape(1,756)

    p1=shap.force_plot(e.expected_value, (shap_df_plot.iloc[month1]).values,test_df.iloc[month1].values, feature_names=features)
    p2=shap.force_plot(e.expected_value, (shap_df_plot.iloc[month2]).values,test_df.iloc[month2].values, feature_names=features)
    p3=shap.decision_plot(e.expected_value, shap_df_plot.loc[[month1, month2], :].values,features=test_df.iloc[0].values ,feature_names=features.tolist(),highlight=0,feature_display_range=slice(None, -31, -1),legend_location='lower right',legend_labels=[month1,month2])
    p4=shap.plots._waterfall.waterfall_legacy(e.expected_value[0], shap_df_plot.iloc[month1],features=test_df.iloc[month1].values,feature_names= features.to_list(),max_display=15)
    p5=shap.plots._waterfall.waterfall_legacy(e.expected_value[0], shap_df_plot.iloc[month2],features=test_df.iloc[month2].values,feature_names= features.to_list(),max_display=15)
    return p1,p2,p3,p4,p5


