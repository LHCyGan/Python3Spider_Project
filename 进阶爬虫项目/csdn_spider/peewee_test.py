from peewee import *

db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="root")


class Person(Model):
    name = CharField(max_length=20)
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.
        # table_name = "users"

#数据的增、删、改、查

if __name__ == "__main__":
    # db.create_tables([Person])
    from datetime import date

    #生成数据
    # uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    # uncle_bob.save()  # bob is now stored in the database
    #
    # uncle_bob = Person(name='bobby', birthday=date(1988, 1, 15))
    # uncle_bob.save()  # bob is now stored in the database

    #查询数据（只获取一条） get方法在取不到数据会抛出异常
    # bobby = Person.select().where(Person.name == 'Bob').get()
    # print(bobby.birthday)
    # a = 1
    # bobby = Person.get(Person.name == 'bobb')
    # print(bobby.birthday)
    #query是modelselect对象 可以当做list来操作 __getitem__
    query = Person.select().where(Person.name == 'Bob')
    for person in query:
        person.delete_instance()
        # person.birthday = date(1960, 1, 17)
        # person.save() #在没有数据存在的时候新增数据，存在的时候修改数据
