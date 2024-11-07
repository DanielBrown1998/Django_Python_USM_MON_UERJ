import os
import sys
from pathlib import Path
import django
from django.conf import settings
from django.db.utils import IntegrityError

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 60
NUMBERS_MON = 30
WEEKDAYS = [4, 5, 6, 7]

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False



django.setup()

if __name__ == '__main__':
    import faker
    from datetime import datetime, timedelta
    from home.models import User, Monitorias, DataUser, Matriculas
    from random import choice

    #DataUser.objects.all().delete()
    #Monitorias.objects.all().delete()
    #User.objects.all().delete()

    date_today = datetime.now()
    fmt = "%Y-%m-%d"
    fake = faker.Faker('pt_BR')

    def insert_data_user(user: DataUser, data_user: list[DataUser]):
        user_mon = DataUser(owner = user)
        user_mon.monitorias_marcadas += 1
        data_user.append(
            user_mon
        )

    django_users = []
    matricula = 202_213_313_611
    matriculas = []
    for _ in range(NUMBER_OF_OBJECTS):
        matricula += 1
        
        profile = fake.profile()
        usuario = {}
        usuario['username'] = f"{matricula}"
        usuario['password'] = os.environ['PASSWORD']
        usuario['first_name'], usuario['last_name'] = profile['name'].split(' ', 1)
        usuario['email'] = os.environ['EMAIL']

        django_users.append(
            User(
                username = usuario['username'],
                password = usuario['password'],
                first_name = usuario['first_name'],
                last_name = usuario['last_name'],
                email = usuario['email']
                )
        )
        matriculas.append(
            Matriculas(
                matricula = f"{matricula}",
                status = True
            )
        )
    
    monitorias = []
    data_user = []
    for _ in range(NUMBERS_MON):
        day_diff = choice([item for item in range(30)])
        day = datetime.strftime( date_today + timedelta(days=day_diff), fmt)
        weekday = datetime.strptime(day, fmt).isoweekday()
        my_choice = [choice(django_users), day]
        while weekday in WEEKDAYS or my_choice in monitorias:
            day_diff = choice([item for item in range(30)])
            day = datetime.strftime( date_today + timedelta(days=day_diff), fmt)
            weekday = datetime.strptime(day, fmt).isoweekday()
            my_choice = [choice(django_users), day]

        monitorias.append(
            Monitorias(
                owner = my_choice[0],
                date = my_choice[1]
            )
        )
        if not data_user:
            insert_data_user(my_choice[0], data_user)
        else:
            user = my_choice[0]
            for item in data_user:
                if item.owner == user:
                    item.monitorias_marcadas += 1
                    item.monitorias_presentes += 1
                    user = None
            if user:
                insert_data_user(user, data_user)

    #print(*[(user.owner, user.monitorias_marcadas, user.monitorias_presentes) for user in data_user], sep='\n')
    #print(*[(mon.owner, mon.date) for mon in monitorias], sep='\n')
    #print(*[(user.username, user.first_name, user.last_name) for user in django_users], sep='\n')
    
    if len(django_users) > 0:
        User.objects.bulk_create(django_users)
        print('Usuários Cadastrados')
    
    if len(data_user) > 0:
        DataUser.objects.bulk_create(data_user)
        print('monitorias cadastradas')
    
    if len(monitorias) > 0:
        Monitorias.objects.bulk_create(monitorias)
        print('datas cadastradas')
    
    if len(matriculas) > 0:
        Matriculas.objects.bulk_create(matriculas)
        print('matriculas cadastradas')
    