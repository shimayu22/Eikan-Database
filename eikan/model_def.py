from .models import Teams 

def finish_year():
    if Teams.objects.all():
        return Teams.objects.latest('pk').year
    else:
        return 9999

def start_year():
    if Teams.objects.all():
        if Teams.objects.latest('pk').period == 1:
            return Teams.objects.latest('pk').year - 2
        else:
            return Teams.objects.latest('pk').year - 1
    else:
        return 1939

def default_admission_year():
    return Teams.objects.latest('pk').year \
           if Teams.objects.all() else 1939

def default_team_id():
    return Teams.objects.latest('pk').id if Teams.objects.all() else 0
