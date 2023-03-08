from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=128, null=False)


class Mission(models.Model):
    id = fields.IntField(pk=True)
    mission_name = fields.CharField(max_length=50, unique=True)
    mission_detail = fields.CharField(max_length=200, null=True)
    
    targets: fields.ReverseRelation["Target"]


class Platform(models.Model):
    id = fields.IntField(pk=True)
    platform_name = fields.CharField(max_length=20, unique=True)

    targets: fields.ReverseRelation["Target"]



class Target(models.Model):
    id = fields.IntField(pk=True)
    profile_id = fields.CharField(max_length=50)
    url = fields.CharField(max_length=200, unique=True)
    platform: fields.ForeignKeyRelation[Platform] = fields.ForeignKeyField("models.Platform", related_name="targets", on_delete=fields.CASCADE)
    mission: fields.ForeignKeyRelation[Mission] = fields.ForeignKeyField("models.Mission", related_name="targets", on_delete=fields.CASCADE)

    status = fields.BooleanField(default=True) 
    added_time = fields.DatetimeField(auto_now_add=True)
    disabled_time = fields.DatetimeField(auto_now=True)
    active_img = fields.CharField(max_length=1000, unique=True)
    disabled_img = fields.CharField(max_length=1000, unique=True)
