


from backend import langchain, haystack

hs = haystack.HaystackBackend()

hs.IndexDocuments()

print(hs.DocStore)