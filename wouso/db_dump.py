from sys import argv
import json
from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from core.artifacts.models import Artifact, Group
from core.qpool.models import Question, Answer, Tag
from games.quest.models import Quest


def dump_db():
    dump_file = open('../db_dump.json', 'w')
    users = User.objects.all()
    qpool = Question.objects.all()
    qpool_tag = Tag.objects.all()
    qpool_answ = Answer.objects.all()
    artifacts_ar = Artifact.objects.all()
    artifacts_gr = Group.objects.all()
    quest = Quest.objects.all()
    all_objects = list(list(users) + list(qpool_tag) + list(qpool) + \
                  list(qpool_answ) + list(artifacts_gr) + list(artifacts_ar) + \
                  list(quest))
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(all_objects, ensure_ascii=True, stream=dump_file)
    dump_file.close()

def restore_db():
    dec = json.JSONDecoder()
    dump_file = open('../db_dump.json', 'r')
    data_list = dec.decode(dump_file.read())
    for elem in data_list:
        l = elem['model'].split('.')
        object = ContentType.objects.get(app_label=l[0], model=l[1]).model_class()()
        object.pk = elem['pk']
        for key, value in elem['fields'].iteritems():
            if hasattr(object, key):
                setattr(object,key,value)
            elif hasattr(object, '%s_id' % key):
                setattr(object,'%s_id' % key,value)
            else:
                print('%s does not have attribute %s' % (elem['model'], key))
        object.save()

def usage():
    print('Usage: %s command\n' % argv[0])
    print('Available commands:\n  dump\n  restore\n  help')

if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == 'dump':
            dump_db()
        elif argv[1] == 'restore':
            restore_db()
        elif argv[1] == 'help':
            usage()
    else:
        usage()