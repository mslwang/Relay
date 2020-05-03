import schema as sch

db = sch.initial()
sch.User("123", email="test@gmail.com", first_name="test", last_name="last", accounts=[sch.Account(integration="messenger", username="test", utype="username", password="123")]).save()
