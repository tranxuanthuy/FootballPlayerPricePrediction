import pandas as pd 
import numpy as np 
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
PATH_TO_PROJECT = '/home/thuy/Desktop/ML_project'
import sys
sys.path.append(PATH_TO_PROJECT)


__all__ = [
	'load_data',
	'process_transform',
	'preprocessing',
	'convert_to_nummeric',
	'process_missing',
	'delete_columns',
	'transform_atts'
]

sup_conv_club = {
	'Manchester United':0, 'Manchester City':0, 'Chelsea FC':0,
	'Arsenal FC':0, 'Tottenham Hotspur':0, 'Liverpool FC':0,
	'Paris Saint-Germain':0, 'Borussia Dortmund':0, 'Bayern Munich':0,
	'Real Madrid':0, 'Atlético de Madrid':0, 'FC Barcelona':0,
	'Juventus FC' :0, 'AC Milan':0, 'Inter Milan':0
}

sup_conv_country = {
	'Brazil':2,'France':1,'Italy':1,'Spain':1,'Germany':1,'Uruguay':2,
	'Chile':2,'Belgium':1,'Canada':2,'Netherlands':1,'Martinique':2,
	'Portugal':1, 'Honduras':2, 'Denmark':1, 'Argentina':2,'Costa Rica':2, 'Switzerland':1,
	'Jamaica':2, 'England':0, 'Ireland':1, 'United States':2,'Wales':1, 'Serbia':1, 'Slovakia':1,
	'Hungary':1, 'Georgia':1, 'Czech Republic':1, 'Russia':1, 'Colombia':2,'Poland':1,'Sweden':1,
	'North Macedonia':1,'Slovenia':1, 'Croatia':1, 'NorthernIreland':1,
	'Bosnia-Herzegovina':1, 'Norway':1, 'Turkey':1, 'Mexico':2, 'Greece':1, 
	'Guadeloupe':2, 'Finland':1, 'Romania':1,'Albania':1, 'Israel':1, 'Suriname':2, 'Scotland':1,
	'Lithuania':1, 'Ukraine':1, 'Paraguay':2, 'Kosovo':2, 'Montenegro':1, 'Ecuador':2, 'Zimbabwe':2, 
	'Luxembourg':1, 'Bulgaria':1, 'French Guiana':2, 'Grenada':2,'Dominican Republic':2, 'Panama':2
}

sup_conv_position = {
	'midfield':2, 'Defender':1, 'Goalkeeper':0, 'attack':3
}

sup_conv_league = {
	'Ligue 1':4, 'Serie A':2 , 'LaLiga':1 , 'Bundesliga':3, 'Premier League':0
}

class process_transform:
	def __init__(self) -> None:
		pass
	def add_age_square(self, df):
		df_add = df.copy()
		df_add['age_square'] = df_add['age']**2
		return df_add
	def _log_with_b(self, df, lst , b=1.1):
		df_trans = df.copy()
		n = len(lst)
		lst1 = lst[0:n//3]
		lst2 = lst[n//3+1:]
		for i in lst1:
			df_trans[i]+=1
			df_trans[i] = np.log(df_trans[i])/np.log(b)
		for i in lst2:
			df_trans[i]+=1
			df_trans[i] = np.log(df_trans['price'])/np.log(b)		
		return df_trans

	def _log_with_b_(self, df, lst, b=1.1):
		df_trans = df.copy()
		for i in lst:
			df_trans[i]+=1
			df_trans[i] = np.log(df_trans[i])/np.log(b)		
		return df_trans


class process_missing:
	def __init__(self, df):
		self.df = df
	def dropna(self, columns_name=['score', 'price', 'league']):
		_maxmissing = self.df.shape[0]/100
		for _ in columns_name:
			if self.df[_].isna().sum() > _maxmissing:
				raise Exception('column {} has missing > 1/100 ban ghi'.format(_))
		self.df.dropna(subset=columns_name, inplace=True)
	def _foot(self, fill_map):
		if fill_map == 'auto':
			fill_map = {3.0: 'left', 11.0: 'left', '7.0' : 'left'}
		toget_missing = self.df[(self.df.number.isna()) & (self.df.foot.isna())]
		if toget_missing.shape[0] >0:
			self.df.drop(toget_missing.index, inplace= True)
		cond= self.df['foot'].isna()
		res= self.df.loc[cond, 'number'].map(fill_map)
		self.df.loc[cond, 'foot']= res
		self.df['foot'] = self.df[['foot']].fillna('right')
	def _height(self, fill_map):
		if fill_map == 'auto':
			mean_hei = self.df.groupby('position').agg({'height':np.mean})
			fill_map = {}
			for _index, _values in zip(mean_hei.index, mean_hei.values):
				fill_map[_index] = _values[0]
		toget_missing = self.df[(self.df.height.isna()) & (self.df.position.isna())]
		if toget_missing.shape[0] >0:
			self.df.drop(toget_missing.index, inplace= True)
		cond= self.df['height'].isna()
		res= self.df.loc[cond, 'position'].map(fill_map)
		self.df.loc[cond, 'height']= res
	def contractExpires(self, day = '2022-06-30'):
		self.df.contractExpires.astype(str)
		self.df.contractExpires.fillna(day, inplace=True)
	def _follower(self, fill_map):
		if fill_map == 'auto':
			mean_folow_club = self.df.groupby(['club']).agg({'follower': np.median}).fillna(5000)
			fill_map = {}
			for _index, _values in zip(mean_folow_club.index, mean_folow_club.values):
				fill_map[_index] = _values[0]
		toget_missing = self.df[(self.df.follower.isna()) & (self.df.club.isna())]
		if toget_missing.shape[0] >0:
			self.df.drop(toget_missing.index, inplace= True)
		cond= self.df['follower'].isna()
		res= self.df.loc[cond, 'club'].map(fill_map)
		self.df.loc[cond, 'follower']= res
	
	
class convert_to_nummeric:
	def __init__(self, df):
		self.df = df
	def league(self, sup_conv_league = sup_conv_league):
		if type(self.df.league[0]) == np.float64:
			return
		self.df.league = self.df.league.map(sup_conv_league)
		self.df.league.fillna(5, inplace=True)
	
	def position(self, sup_conv_position = sup_conv_position):
		if type(self.df.position[0]) == np.int64:
			return 
		self.df.position = self.df.position.map(sup_conv_position)
		self.df.dropna(subset = ['position'], inplace = True)
	
	def club(self, sup_conv_club = sup_conv_club):
		if type(self.df.club[0]) == np.float64:
			return
		self.df.club = self.df.club.map(sup_conv_club)
		self.df.club.fillna(1, inplace=True)
		
	def country(self, sup_conv_country = sup_conv_country):
		if type(self.df.country[0]) == np.float64:
			return 
		self.df.country = self.df.country.map(sup_conv_country)
		self.df.country.fillna(3, inplace=True)
	def contract_year(self):
		if 'contractExpires' not in self.df.columns:
			return
		self.df.contractExpires = pd.to_datetime(self.df.contractExpires, format="%Y-%m-%d")
		self.df['contractExpires'] = self.df.contractExpires - datetime.today()
		self.df['contractExpires'] = self.df['contractExpires'].astype(str).str.split(' ',expand=True)[0].astype(float)/365
		self.df.rename({'contractExpires': 'contractYear'}, axis=1, inplace=True)
	def score(self, df):
		if 'score' not in df.columns:
			return
		df_gk = df.loc[self.df.position == 0].copy()
		df_ct = df.loc[self.df.position != 0].copy()
		df_gk.loc[:,['appearances', 'nilnil_games', 'goals_conceded', 'minuted']] = 0
		df_ct.loc[:,['appearances', 'goals', 'assists', 'minuted']] = 0
		sup_gk = df_gk[['score']].apply(lambda x:x['score'].split('/')[0:4], axis=1, result_type='expand')
		sup_ct = df_ct[['score']].apply(lambda x:x['score'].split('/')[0:5], axis=1, result_type='expand')
		df_gk.loc[:, 'appearances'] = sup_gk.iloc[:,0].astype(float)
		df_ct.loc[:, 'appearances'] = sup_ct.iloc[:,0].astype(float)
		df_gk.loc[:, 'minuted'] = sup_gk.iloc[:,-1].astype(float)
		df_ct.loc[:, 'minuted'] = sup_ct.iloc[:, -1].astype(float)
		df_gk.loc[:, 'nilnil_games'] = sup_gk.iloc[:,2].astype(float)
		df_ct.loc[:, 'goals'] = sup_ct.iloc[:,1].astype(float)
		df_gk.loc[:, 'goals_conceded'] = sup_gk.iloc[:,1].astype(float)
		df_ct.loc[:, 'assists'] = sup_ct.iloc[:,2].astype(float)
        # self.df = pd.concat([df_ct, df_gk], ignore_index=True)
        # self.df.drop('score', axis=1, inplace=True)
		# df_donenumbering = pd.concat([df_gk, df_ct], ignore_index=True)
		df_ct.drop('score', axis=1, inplace=True)
		df_gk.drop('score', axis=1, inplace=True)
		# df_donenumbering.drop('score', axis=1, inplace=True)
		return  df_ct, df_gk
	# def score(self):
	# 	if 'score' not in self.df.columns:
	# 		return
	# 	df_goalkeeper = self.df[self.df['position'] == 0]
	# 	df_cauthu = self.df[self.df['position'] != 0]
	# 	sup_goalkeeper = df_goalkeeper[['score']].apply(lambda x:x['score'].split('/')[0:4], axis=1, result_type='expand')
	# 	sup_cauthu = df_cauthu[['score']].apply(lambda x:x['score'].split('/')[0:5], axis=1, result_type='expand')
		
	# 	df_goalkeeper[['appearances', 'goals_nilnilgames', 'assists_conceded', 'minuted']]=0
	# 	df_goalkeeper.loc[:, 'appearances'] = sup_goalkeeper.iloc[:,0].astype(float)
	# 	df_cauthu.loc[:, 'appearances'] = sup_cauthu.iloc[:,0].astype(float)
	# 	df_goalkeeper.loc[:, 'minuted'] = sup_goalkeeper.iloc[:,-1].astype(float)
	# 	df_cauthu.loc[:, 'minuted'] = sup_cauthu.iloc[:, -1].astype(float)
	# 	df_goalkeeper.loc[:, 'goals_nilnilgames'] = sup_goalkeeper.iloc[:,2].astype(float)
	# 	df_goalkeeper.loc[:, 'goals_nilnilgames'] = df_goalkeeper.loc[:, 'goals_nilnilgames']/2
	# 	df_cauthu.loc[:, 'goals_nilnilgames'] = sup_cauthu.iloc[:,1].astype(float)
	# 	df_goalkeeper.loc[:, 'assists_conceded'] = sup_goalkeeper.iloc[:,1].astype(float)
	# 	df_goalkeeper.loc[:, 'assists_conceded'] = df_goalkeeper.loc[:, 'assists_conceded']/4
	# 	df_cauthu.loc[:, 'assists_conceded'] = sup_cauthu.iloc[:,2].astype(float)
	# 	self.df = pd.concat([df_cauthu, df_goalkeeper], ignore_index=True)
	# 	self.df.drop('score', axis=1, inplace=True)

def load_data(path):
    df = pd.read_csv(path)
    print(df.shape)
    return df

def delete_columns(df,
lst_columns_name=['number', 'urlInsta', 'agent', 'outfitter', 'Unnamed: 0', 'foot']):
	lstTmp = []
	for _ in lst_columns_name:
		if _ in df.columns.values:
			lstTmp.append(_)
		else:
			print(f"'{_}' not a columns in df")
	df.drop(lstTmp, axis = 1, inplace = True)
	if len(lstTmp) >0:
		print(f'>>Successfully. Deleted columns: {lstTmp}')
	return df

def preprocess_data(_path = PATH_TO_PROJECT+'/data/raw_data/raw_data.csv'):
	def load_data(path):
		return pd.read_csv(path, encoding='utf-8')
	df = load_data(_path)
    #missing
	miss_process = process_missing(df)
	miss_process.dropna(columns_name=['score', 'price', 'league', 'club'])
	miss_process._foot(fill_map='auto')
	miss_process._height(fill_map='auto')
	miss_process.contractExpires()
	miss_process._follower(fill_map='auto')
	delete_columns(df).isna().sum()
	#convert to numeric
	cvt = convert_to_nummeric(df)
	cvt.club()
	cvt.contract_year()
	cvt.country()
	cvt.league()
	cvt.position()
	df = cvt.score(df)
	#noise
	df_ = df[['name', 'league', 'age', 'height', 'position', 'erfolge', 'caps', 'follower', 'club', 
	'contractYear', 'country', 'appearances', 'goals_nilnilgames', 'assists_conceded', 'minuted', 'price']].copy()
	df_['league'] = df_['league'].astype(int)
	df_['position'] = df_['position'].astype(int)
	df_['country'] = df_['country'].astype(int)
	df_['club'] = df_['club'].astype(int)
	df_.to_csv(
    PATH_TO_PROJECT+'/data/raw_data/numeric_data.csv',
    encoding='utf-8',
    index=False
	)

def transform_atts(df_train, df_test, n_components=5):
    sc = StandardScaler()
    pca = PCA(n_components=n_components)
    if 'nilnil_games' in df_train.columns.values:
        #process quati atts
        ##select
        X_train_quati = df_train[['age', 'height', 'erfolge', 'caps',
       'goalsCap', 'follower', 'contractYear', 'appearances',
        'nilnil_games', 'goals_conceded', 'minuted', 'age_square']].copy()
        X_test_quati = df_test[['age', 'height', 'erfolge', 'caps',
       'goalsCap', 'follower', 'contractYear', 'appearances',
        'nilnil_games', 'goals_conceded', 'minuted', 'age_square']].copy()
        ##std
        X_train_quati_std = sc.fit_transform(X_train_quati)
        X_test_quati_std = sc.transform(X_test_quati)
        ##pca 5
        X_train_quati_std_pca = pca.fit_transform(X_train_quati_std)
        X_test_quati_std_pca = pca.transform(X_test_quati_std)
        ##final quati
        X_train_quati_final = pd.DataFrame(X_train_quati_std_pca)
        X_test_quati_final = pd.DataFrame(X_test_quati_std_pca)
        #process quali atts
        ##select
        X_train_quali = df_train[['league', 'club', 'country']].copy()
        X_test_quali = df_test[['league', 'club', 'country']].copy()
        ##encod
        X_train_quali_encod = pd.get_dummies(data=X_train_quali,columns=['league', 'country'],
        drop_first=True)
        X_test_quali_encod = pd.get_dummies(data=X_test_quali,columns=['league', 'country'],
        drop_first=True)
        ##final quali
        X_train_quali_final = pd.DataFrame(X_train_quali_encod).reset_index().drop('index', axis=1)
        X_test_quali_final = pd.DataFrame(X_test_quali_encod).reset_index().drop('index', axis=1)
        #final
        X_train_final = pd.concat([X_train_quati_final, X_train_quali_final], axis=1, join='inner')
        X_test_final = pd.concat([X_test_quati_final, X_test_quali_final], axis=1, join='inner')
        return X_train_final, X_test_final    
    else:
        #process quati atts
        ##select
        X_train_quati = df_train[['age', 'height', 'erfolge', 'caps',
       'goalsCap', 'follower', 'contractYear', 'appearances',
        'goals', 'assists', 'minuted', 'age_square']].copy()
        X_test_quati = df_test[['age', 'height', 'erfolge', 'caps',
       'goalsCap', 'follower', 'contractYear', 'appearances',
        'goals', 'assists', 'minuted', 'age_square']].copy()
        ##std
        X_train_quati_std = sc.fit_transform(X_train_quati)
        X_test_quati_std = sc.transform(X_test_quati)
        ##pca 5
        X_train_quati_std_pca = pca.fit_transform(X_train_quati_std)
        X_test_quati_std_pca = pca.transform(X_test_quati_std)
        ##final quati
        X_train_quati_final = pd.DataFrame(X_train_quati_std_pca)
        X_test_quati_final = pd.DataFrame(X_test_quati_std_pca)
        #process quali atts
        ##select
        X_train_quali = df_train[['league', 'position', 'club', 'country']].copy()
        X_test_quali = df_test[['league', 'position', 'club', 'country']].copy()
        ##encod
        X_train_quali_encod = pd.get_dummies(data=X_train_quali,columns=['league', 'country', 'position'],
        drop_first=True)
        X_test_quali_encod = pd.get_dummies(data=X_test_quali,columns=['league', 'country', 'position'],
        drop_first=True)
        ##final quali
        X_train_quali_final = pd.DataFrame(X_train_quali_encod).reset_index().drop('index', axis=1)
        X_test_quali_final = pd.DataFrame(X_test_quali_encod).reset_index().drop('index', axis=1)
        #final
        X_train_final = pd.concat([X_train_quati_final, X_train_quali_final], axis=1, join='inner')
        X_test_final = pd.concat([X_test_quati_final, X_test_quali_final], axis=1, join='inner')
        return X_train_final, X_test_final

def label_price_gk(df):
	df_gk = df.copy()
	df_gk.loc[df_gk['price']<2.5, 'label_price'] = 0
	df_gk.loc[(df_gk['price']>=2.5) & (df_gk['price']<10), 'label_price'] = 1
	df_gk.loc[(df_gk['price']>=10) & (df_gk['price']<40), 'label_price'] = 2
	df_gk.loc[(df_gk['price']>=40), 'label_price'] = 3
	df_gk['label_price'] = df_gk.label_price.astype(np.int64)
	df_gk.drop(columns=['price'], inplace=True)
	return df_gk
