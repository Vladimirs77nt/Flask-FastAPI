import faker

fake = faker.Faker('ru_RU')

for i in range(10):
    print(f" - Фамилия: {fake.last_name()}, имя: {fake.first_name()}")
    print("Email :", fake.email())