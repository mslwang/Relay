import schema as sch

db = sch.initial()
#sch.User("123", email="test@gmail.com", first_name="test", last_name="last", accounts=[sch.Account(integration="messenger", username="test", utype="username", password="123")]).save()
#test = sch.User.objects.get({'_id': "123"}).accounts
sch.User("123", messenger=sch.Messenger(email="test@gmail.com", password="123"), accounts_available=[]).save()
#sch.User.objects.raw({'_id': "123"}).update({"$pull": {"accounts": {"integration": "instagram"}}})
#sch.User.objects.raw({'_id': "123"}).update({"$push": {"accounts": {"integration": "instagram", "username": "test123", "utype": "email", "password": "456", '_cls': 'schema.Account'}}})
#test = sch.User.objects.get({'_id': "123"}).accounts
#print(test)
#test.append(sch.Account.from_document({"integration": "instagram", "username": "test123", "utype": "email", "password": "456"}))
#sch.User.objects.raw({'_id': "1"}).update({'$addToSet': {"accounts": {"integration": "instagram", "username": "test123", "utype": "email", "password": "456", '_cls': 'schema.Account'}}})
#db.Relay.find_one_and_update({'_id': "123"}, {'$addToSet': {"accounts": sch.Account.from_document({"integration": "instagram", "username": "test123", "utype": "email", "password": "456"})}})
