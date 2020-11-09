from lightfm import LightFM
from lightfm.datasets import fetch_movielens
import numpy as py
import numpy as np


data = fetch_movielens(min_rating=4.0)



model = LightFM(loss='warp')
model.fit(data['train'], epochs=30, num_threads=2)



def sample_recommendation(model,data,user_ids):
	n_users,n_items = data['train'].shape
	for user_id in user_ids:
		known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]
		scores = model.predict(user_id,np.arange(n_items))
		top_items = data['item_labels'][np.argsort(-scores)]
		for x in top_items[:3]:
			print("%s"%x)

sample_recommendation(model,data,[3
                                  ])