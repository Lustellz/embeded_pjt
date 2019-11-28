import pickle

userlst = [ {'name':'a','id':'1'}, {'name':'b','id':'3'},{'name':'asd','id':'4'}]
infos = {'users':3, 'real':33}

# data = {
#     'dd': [1, 2.0, 3, 4+6j],
#     'b': ("character string", "byte string"),
#     'c': {None, True, False}
# }
userlst.append({'names':'h','id': '33'})

data = {
    'infos':infos,
    'userlst':userlst
}
with open('data.txt', 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

