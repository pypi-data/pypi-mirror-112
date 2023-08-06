def chi_squ(dataset_train_df,input_column,output_column):
    import pandas as pd
    import scipy.stats as stats

    col_unique = dataset_train_df[input_column].unique()
    count_dict = dict()
    for count,ele in enumerate(col_unique,1):
        count_dict[ele] = count
    for key,value in count_dict.items():
        dataset_train_df[input_column] = dataset_train_df[input_column].replace(key,value)
    dataset_table=pd.crosstab(dataset_train_df[input_column],dataset_train_df[output_column])

    #Observed Values
    Observed_Values = dataset_table.values 
    
    print("Observed Values :-\n",Observed_Values)
    
    val=stats.chi2_contingency(dataset_table)

    Expected_Values=val[3]
    
    print("Expected_Values",Expected_Values)


    no_of_rows=len(dataset_table.iloc[0:2,0])
    no_of_columns=len(dataset_table.iloc[0,0:2])
    ddof=(no_of_rows-1)*(no_of_columns-1)
    print("Degree of Freedom:-",ddof)
    alpha = 0.05

    from scipy.stats import chi2
    chi_square=sum([(o-e)**2./e for o,e in zip(Observed_Values,Expected_Values)])
    chi_square_statistic=chi_square[0]+chi_square[1]

    print("chi-square statistic:-",chi_square_statistic)

    critical_value=chi2.ppf(q=1-alpha,df=ddof)
    print('critical_value:',critical_value)

    #p-value
    p_value=1-chi2.cdf(x=chi_square_statistic,df=ddof)
    print('p-value:',p_value)
    print('Significance level: ',alpha)
    print('Degree of Freedom: ',ddof)
    print('p-value:',p_value)

    if chi_square_statistic>=critical_value:
        print("Reject H0,There is a relationship between 2 categorical variables",input_column)

    else:
        print("Retain H0,There is no relationship between 2 categorical variables",input_column)

    if p_value<=alpha:
        print("Reject H0,There is a relationship between 2 categorical variables",input_column)

    else:
        print("Retain H0,There is no relationship between 2 categorical variables",input_column)


if __name__ == '__main__':
    chi_squ(dataframe,input_column,output_column)
