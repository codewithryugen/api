from anime import Gogoanime

gogo = Gogoanime()
res = gogo.search_anime("onimai")
print(res[0])
print()
eps = gogo.get_episode_url(res[0]["catagory_url"])
print(eps)
print()
stream = gogo.get_stream_url(eps[0])
print(stream)
print()
recent = gogo.get_recent_release()
print(recent)