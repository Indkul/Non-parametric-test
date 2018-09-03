import pandas as pd
from scipy.stats import chi2
import plotly
import plotly.graph_objs as go


def kruskal_wallis_test(df, column1_name, column2_name, alpha):

	k = df[column2_name].nunique()

	N = df[column2_name].count()

	df['rank'] = df[column1_name].rank(ascending=True)
	table1 = df.groupby(column2_name).sum()
	table2 = df.groupby(column2_name).count()

	sub_component = 0
	for i in range(0, k):
		sub_component = (table1.iloc[i, 1] ** 2 / table2.iloc[i, 1]) + sub_component

	test_statistic = ((12 / (N * (N + 1))) * sub_component) - 3 * (N + 1)

	degrees_of_freedom = k - 1
	a = alpha / 100
	chi_critical_value = round(chi2.isf(q=a, df=degrees_of_freedom), 2)
	p_value = chi2.sf(test_statistic, degrees_of_freedom)

	print('\n Rejection Criteria: Reject null hypothesis at', alpha, '% level of significance '
			'if Test Statistic is greater than or equal ',chi_critical_value, '.')

	table = {'Variable': column1_name + ' grouped by ' + column2_name, 'Test Statistic': round(test_statistic,4),
			   'Critical Value': chi_critical_value,'P value': p_value}

	trace = go.Table(
		header=dict(values=list(table.keys()),
					fill=dict(color='#C2D4FF'),
					align=['left'] * 5),
		cells=dict(values=list(table.values()),
				   fill=dict(color='#F5F8FF'),
				   align=['left'] * 5))

	data = [trace]

	plotly.offline.plot({'data': data}, filename='Table.html')

"""Applying Kruskal Wallis Test for Tensile Strength data set"""

data = pd.read_csv('Tensile Strength.csv')
kruskal_wallis_test(data, column1_name='Tensile Strength', column2_name='Mixing Technique', alpha=5)







