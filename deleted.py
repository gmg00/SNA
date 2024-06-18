import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_submissions = pd.read_csv("C:/Users/leona/Downloads/small_users.csv", usecols = ['author','author_flair_css_class','id'])
                                #prendo lo small perché se lo user che crea il post è deleted la catena è già "compatta"
                                #dall'alto

df_comments_orig = pd.read_csv("C:/Users/leona/Downloads/total_comm.csv", usecols = ['author', 'author_flair_text', 'id','parent_id','link_id'])



# Drop all Nan values.
df_comments = df_comments_orig.dropna(subset=['link_id']).copy()
# Get rid of 't1_' or 't3_'.
def extract_id(parent_id):
    return parent_id[3:]

# Apply the function to create a new column 'parent_comment_id'.
df_comments['parent_comment_id'] = df_comments['parent_id'].apply(extract_id)
# Apply the function to create a new column 'parent_submission_id'.
df_comments['parent_submission_id'] = df_comments['link_id'].apply(extract_id)
# Create an array with all the unique ids.
submissions_ids = df_submissions['id'].unique()
# If 't1_' get rid of the prefix, else return 0
def extract_comm_ids(parent_id):
    if parent_id.startswith('t1_'):
        return parent_id[3:]
    else:
        return 0

# Create an array with all the unique ids.
comments_ids = df_comments['id'].unique()
df_comments = df_comments[df_comments['parent_comment_id'].isin(np.concatenate((comments_ids, submissions_ids)))]
df_comments = df_comments.drop(columns=['author_flair_text','link_id'])
df_full = pd.concat([df_submissions[['id','author']], df_comments_orig[['id','author']]], axis=0)
id_to_auth = df_full.set_index('id')['author'].to_dict()
id_to_parent = df_comments.set_index('id')['parent_comment_id'].to_dict()
while df_comments['parent_comment_id'].apply(lambda x: id_to_auth[x]) == 'deleted':
    df_comments['parent_comment_id'] = df_comments['parent_comment_id'].apply(lambda x: id_to_parent[x])
df_comments['parent_author'] = df_comments['parent_comment_id'].apply(lambda x: id_to_auth[x])
a = df_comments[['author','parent_author']].values.tolist()
b = []
for elem in a:
    if elem[0] != elem[1]:
        b.append(f'{elem[0]} {elem[1]}')