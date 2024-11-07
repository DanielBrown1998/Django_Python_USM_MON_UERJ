import sys
from pathlib import Path
from django import setup
import os



BASE_DIR = Path(__file__).parent.parent
path = sys.path
path.append(str(BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
setup()

if __name__ == '__main__':
    from home.models import Monitorias
    monitorias = Monitorias.objects.all()
    for monitoria in monitorias:
        monitoria.status = "MARCADA"
        monitoria.save()

    print(*[monitoria.status for monitoria in monitorias], sep=' ')
    

