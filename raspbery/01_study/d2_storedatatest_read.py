import pickle


data = []

dbfile = open('data.txt','rb')
data = pickle.load(dbfile)

infos = data['infos']
# with open('data.txt','rb') as f:
#     data = pickle.load(f)

print(data)
print(infos)