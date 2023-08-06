# TimeSeriesRNNInterpretor

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)]()

TimeSeriesRNNInterpretor, Interprets the RNN black box model. It internally uses shap.DeepExplainer. We have tried to interpret only single instance with respect to time. We have additionally included monthly effect of the instance.
 

- ✨TimeSeriesRNNInterpretor✨

## Parameters

Parameters required to Pass

| Parameter | To be passed | Format
| ------ | ------ |------|
| model | RNN model | tensorflow V1 behaviour
| background | training data sample| Numpy array
| test | Instance data which we want to explain | Numpy array
| features | feature_names or column names| df.columns
| max_output | max output value(1) | 1 for binary classification
|max_display | max display features for waterfall plot | a number < no of features
|decision_range | max display features for decision plot | a number < no of features
|Measure | "absolute" or "relative" or "total " | for plotting waterfall plot w.r.t basevalue
|dependence_feature_3 | 3rd feature name to plot dependence plot | a feature name or index of feature
|dependence_feature_2 | 2nd feature name to plot dependence plot | a feature name or index of the feature

## Calling

```sh
from TimeSeriesRNNInterpretor import TimeSeriesRNNInterpretor

temp = TimeSeriesInterpretorRNN(model=model,background=background,test=test,features=features,max_output=1,max_display=15,decision_range=30,Measure="absolute",dependence_feature_3="age.",dependence_feature_2="gender")

```

Plotting Different Plots

```sh
temp.global_patient() # To the know the feature importance of a instance
temp.monthly_chart() # timeframe charts of a instance (day,month, or any time frame)
temp.two_month_compare(17, 18) # Specify two timeframe numbers of a instancee to compare (days,months, or any time frames)
temp.single_month(18) # Specify the required specific timeframe number of instance(day,month, or any time frame)
```