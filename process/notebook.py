# ---
import pandas as pd
from fn import convertToVec

df = pd.read_csv('./dataset/summary.csv', encoding='ISO-8859-1', sep=",")
df.head()
# ---
# generate summary vector
dfvecs = pd.DataFrame(columns=['Vector'])

for i in range(len(df)):
    summary = df['Summary'][i]
    sumdf = pd.DataFrame([
        {"Vector": convertToVec(summary)}
    ])
    dfvecs = dfvecs._append(sumdf, ignore_index=True)

dfvecs.to_csv('./dataset/summary_vectors.csv', index=False)
dfvecs.head()
# ---
# generate title vector
df = pd.read_csv('./dataset_spain_sdgs_diperbaiki.csv',
                 encoding='ISO-8859-1', sep=",")

dfvecs = pd.DataFrame(columns=['Vector'])
for i in range(len(df)):
    title = df['Title'][i]
    sumdf = pd.DataFrame([
        {"Vector": convertToVec(title)}
    ])
    dfvecs = dfvecs._append(sumdf, ignore_index=True)

dfvecs.to_csv('./dataset/title_vectors.csv', index=False)
dfvecs.head()
# ---
# merge dataset

df = pd.read_csv('./dataset_spain_sdgs_diperbaiki.csv',
                 encoding='ISO-8859-1', sep=",")

dfsummary = pd.read_csv('./dataset/summary.csv',
                        encoding='ISO-8859-1', sep=",")

dfsummaryvectors = pd.read_csv('./dataset/summary_vectors.csv',
                               encoding='ISO-8859-1', sep=",")

dftitlevectors = pd.read_csv('./dataset/title_vectors.csv',
                             encoding='ISO-8859-1', sep=",")

# insert summary, and vectors to df

df['Summary'] = dfsummary['Summary']
df['Summary_Vector'] = dfsummaryvectors['Vector']
df['Title_Vector'] = dftitlevectors['Vector']

df.to_csv('./dataset/merged_dataset.csv', index=False)

df.head()
# ---
