import pandas as pd
import json
p = '/home/ckl/Documents/freelance/jsl/nlu/nlu4realgit2/tmp/find_unused_models_in_s3/metadata.csv'
df=pd.read_csv(p)
import nlu
# CLEAN RESULT REGEX
# .\d.\d.\d.\d.\d.\d.\d,True,\d*-\d*-\d*T\d*:\d*:\d*.\d*Z,True,\D*,
unused = []
unused_idx =[]
for idx,row in df.iterrows():
    if row['language'] in nlu.Spellbook.pretrained_pipe_references.keys():
        if row['name'] in nlu.Spellbook.pretrained_pipe_references[row['language']].values(): continue

    if row['language'] in nlu.Spellbook.pretrained_models_references.keys():
        if row['name'] in nlu.Spellbook.pretrained_models_references[row['language']].values():
            continue

    unused.append(row['name'] + ' ->' + row['language'] + ' ->' + row['time'] + '\n')
    unused_idx.append(idx)

# for nlp_ref in unused : print(nlp_ref)
print('NUM UNSUED:\n', '\n'.join(unused))
#
# print('hi')
# # 1. translate_[from]_[to] (pipe)
# #  2. opus_mt_[from]_[to]
df['nlu_ref'] = ''

opus_idx = df.name.str.contains('opus_mt')
opus_idx = opus_idx[opus_idx==True].index
cand = df.iloc[opus_idx].name.str.split('_')
f = lambda x : 'xx.'+x[3] +'.marian.translate_to.' + x[2]
nlu_opus_refs = cand.map(f)
df.nlu_ref.iloc[opus_idx] = nlu_opus_refs[opus_idx]



translate_idx = df.name.str.contains('translate')
translate_idx = translate_idx[translate_idx==True].index
cand = df.iloc[translate_idx].name.str.split('_')
f = lambda x : 'xx.'+x[2] +'.translate_to.' + x[1]
nlu_translate_refs = cand.map(f)
# df.iloc[translate_idx ]['nlu_ref'] = nlu_translate_refs[translate_idx]
df.nlu_ref.iloc[translate_idx] = nlu_translate_refs[translate_idx]

print('writing the idnx')
print(unused_idx)
df.iloc[unused_idx][['nlu_ref','name']].to_csv('with_3.1_refs_clean.csv', index=False,)
# print(df)
# print(df)
# import json
# df.index = df.name
# # Create OPUS json NLU references. Put these into a JSON formatter, then add to namespace!
# j =df.iloc[opus_idx].to_json()
# d = json.loads(j)
#
# k = d['nlu_ref'].keys()
# v = d['nlu_ref'].values()
# d = dict(zip(v,k))
# print('JSON OPUS:')
# print(d)
#
#
#
# j =df.iloc[translate_idx].to_json()
# d = json.loads(j)
# k = d['nlu_ref'].keys()
# v = d['nlu_ref'].values()
# d = dict(zip(v,k))
# print('JSON TRANSLTE:')
# print(d)
#

## WRITE EVERY translate and opus ref to NLU!
# Marian pipes as default, i.e 'en.translate_to.fr' is default translate pip
# en.marian_to.de  is the model specific selector

# TODO WRITE NEW NLU REFS
# IDEA: the base refs are `en.translate_to.german` i.e. `<lang>.translate_to.<lang>
# add them all into the `xx` namespace
# when parsing, check if reference contains `translate_to`, if yes then prefix it with `xx` before further parsing
# Also set lang to xx since the sparknlp ref is actually also xx