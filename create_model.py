from MainServer.tables import base
from MainServer.database import engine, Session


base.metadata.create_all(engine)
'''session = Session()

user_data = {
    "login": "admin",
    "password": "admin",
    "type": 1,
    "name": "Vlad",
    "sename": "Skripnik",
    "secondname": "Vicktor",
    "type_learning": 2,
    "place_of_study": "Астраханский технический лицей",
    "learning_stage": "11 класс"
}

organization_data = [
    {"name_organizations": "Астраханский технический лицей", "type_organizations": TypeOrganization.School},
    {"name_organizations": "Астраханский государственный унивирситет им. Татищева", "type_organizations": TypeOrganization.University},
]


user = User(**user_data)
user.password = user_data["password"]
session.add(user)

organization = [EducationalOrganizations(**i) for i in organization_data]

session.add_all(organization)

session.commit()'''

