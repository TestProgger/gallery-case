import asyncio
from peewee import DateTimeField, ForeignKeyField, IntegerField, ManyToManyField, Model  , AutoField , CharField
from peewee_async import Manager ,  PooledPostgresqlDatabase

loop = asyncio.new_event_loop()
database = PooledPostgresqlDatabase('PTO_YONVOS' , user = "postgres" , password = "ros1337ini" , host="localhost" , port = 5432 , max_connections=20)
objects = Manager(database = database , loop=loop)

class BaseModel(Model):
    class Meta:
        database = database

class Vendor(BaseModel):
    id = AutoField(null = False , unique=True , primary_key=True , column_name = "id" , verbose_name = "id")
    name = CharField(null = False , unique=False,  max_length=128  , column_name = "vendor_name" , verbose_name = "vendor_name")

    class Meta:
        table_name = "vendor"

class DeviceInfo(BaseModel):
    id = AutoField(null = False , unique=True , primary_key=True , column_name = "id" , verbose_name = "id")
    bilboard_id = IntegerField(null = False , unique=False , column_name = "bilboard_id" , verbose_name = "bilboard_id")
    mac = CharField(null = False , unique=False,  max_length=18  , column_name = "mac" , verbose_name = "mac")
    timestamp = DateTimeField(null = False , unique=False, column_name = "timestamp" , verbose_name = "Timestamp")
    vendor = ForeignKeyField(Vendor , backref="catched_devices")

    class Meta:
        table_name = "device_info"

class ActivityType(BaseModel):
    id = AutoField(null = False , unique=True , primary_key=True , column_name = "id" , verbose_name = "id")
    name = CharField(null = False , unique=True,  max_length=64  , column_name = "activity_type_name" , verbose_name = "activity_type_name")
    vendors = ManyToManyField(Vendor , backref="activity_types")
    class Meta:
        table_name = "activity_type"

class OUI(BaseModel):
    id = AutoField(null = False , unique=True , primary_key=True , column_name = "id" , verbose_name = "id")
    oui = CharField(null = False , unique=False,  max_length=10  , column_name = "oui" , verbose_name = "oui")
    vendor = ForeignKeyField(Vendor , backref="ouis")

    class Meta:
        table_name = "vendor_oui"

VendorToActivityType = ActivityType.vendors.get_through_model()

database.connect()
database.create_tables([ DeviceInfo , Vendor , ActivityType , OUI  ,VendorToActivityType ])
