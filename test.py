import schema as sch

db = sch.initial()
sch.User("123", first_name="test", last_name="last", accounts=[sch.Account(platform="MESSENGER", username="test", utype="USERNAME", password="123")]).save()
