from tests.pwExample import Pet, Person
from pwexp import filter_exp
from datetime import date
import pytest


def setup_module():
    Person.delete().execute()
    Pet.delete().execute()

    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    uncle_bob.save() # bob is now stored in the database
    grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
    herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
    grandma.name = 'Grandma L.'
    grandma.save()  # Update grandma's name in the database.


    bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
    herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
    herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
    herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')


def teardown_module():
    pass



def test_nomral():
    qs = Pet.select()
    exp = 'id=1'
    qs = filter_exp(qs, exp)

    result = []
    for row in qs:
        result.append(row.id)

    assert result == [1]


def test_dot():
    qs = Pet.select()

    exp = 'owner.id>1'
    qs = filter_exp(qs, exp)

    result = []
    for row in qs:
        result.append(row.id)

    assert result == [2,3,4]


def test_dict():

    qs = Pet.select()

    u = Person.get(Person.id==1)
    context = {'self': u}
    exp = 'owner.id=[self]'
    qs = filter_exp(qs, exp, context)

    result = []
    for row in qs:
        result.append(row.id)

    assert result == [1]


def test_muti():

    qs = Pet.select()

    exp = 'owner.id>1'
    qs = filter_exp(qs, exp)

    exp = 'id=2'
    qs = filter_exp(qs, exp)

    result = []
    for row in qs:
        result.append(row.id)

    assert result == [2]
