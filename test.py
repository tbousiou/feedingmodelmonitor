import database

results = database.get_user_models()

for model in results:
    print(model['title'])