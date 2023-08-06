import pandas as pd
p = '/home/loan/Documents/freelance/jsl/nlu/nlu4realgit/tmp/nlu_hc/all_models/HC_23_feb.csv'
df = pd.read_csv(p)

df['nlu_ref']= df.name.str.split("_")

df[['name','language']].sort_values(by=['name','language']).drop_duplicates().to_csv('sorted.csv',index=False)
df.to_csv('./resDf.csv')