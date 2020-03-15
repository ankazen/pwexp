# filter_exp

## nomral
'''
    qs = Pet.select()
    exp = 'id=1'
    qs = filter_exp(qs, exp)
'''
=>

SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" WHERE ("t1"."id" = 1)

## join
'''
    qs = Pet.select()

    exp = 'owner.id>1'
    qs = filter_exp(qs, exp)
'''

=>

SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" INNER JOIN "person" AS "t2" ON ("t1"."owner_id" = "t2"."id") WHERE ("t2"."id" > 1)

## parameter
'''
    qs = Pet.select()

    u = Person.get(Person.id==1)
    context = {'self': u}
    exp = 'owner.id=[self]'
    qs = filter_exp(qs, exp, context)
'''
=>
SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" INNER JOIN "person" AS "t2" ON ("t1"."owner_id" = "t2"."id") WHERE ("t2"."id" = 1)

## muti
'''
    qs = Pet.select()

    exp = 'owner.id>1'
    qs = filter_exp(qs, exp)

    exp = 'id=2'
    qs = filter_exp(qs, exp)
'''

=>

SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" INNER JOIN "person" AS "t2" ON ("t1"."owner_id" = "t2"."id") WHERE (("t2"."id" > 1) AND ("t1"."id" = 2))


# filter_rule
same with filter_exp, but like this:
'''
    exp = 'pet:owner.id>1'
    qs = filter_exp(qs, exp)
'''
mean if you select table pet, must add expression "owner.id>1"