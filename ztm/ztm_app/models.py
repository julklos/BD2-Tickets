# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Imienne(models.Model):
    id_biletu = models.AutoField(primary_key=True)
    data_aktywacji = models.DateTimeField(blank=True, null=True)
    data_waznosci = models.DateTimeField(blank=True, null=True)
    id_transakcji = models.IntegerField()
    id_pasazera = models.ForeignKey('NosnikiElektroniczne', models.DO_NOTHING, db_column='id_pasazera')
    id_nosnika = models.IntegerField(blank=True, null=True)
    id_ulgi = models.IntegerField(blank=True, null=True)
    id_typu = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Imienne'
        unique_together = (('id_transakcji', 'id_biletu'),)


class MetodyPlatnosci(models.Model):
    id_metody_platnosci = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Metody_platnosci'


class MiejscaTransakcji(models.Model):
    id_miejsca_transakcji = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    miasto = models.CharField(max_length=30, blank=True, null=True)
    ulica = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Miejsca_transakcji'


class Nieimienne(models.Model):
    id_biletu = models.AutoField(primary_key=True)
    data_aktywacji = models.DateTimeField(blank=True, null=True)
    data_waznosci = models.DateTimeField(blank=True, null=True)
    id_transakcji = models.IntegerField()
    id_nosnika = models.ForeignKey('NosnikiKartonikowe', models.DO_NOTHING, db_column='id_nosnika', blank=True, null=True)
    id_typu = models.IntegerField(blank=True, null=True)
    id_typu_ulgi = models.ForeignKey('TypyUlgi', models.DO_NOTHING, db_column='id_typu_ulgi', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Nieimienne'


class NosnikiElektroniczne(models.Model):
    id_nosnika = models.AutoField( primary_key=True)
    data_waznosci = models.DateTimeField()
    id_pasazera = models.OneToOneField('Pasazerowie', models.DO_NOTHING, db_column='id_pasazera')
    id_ulgi = models.IntegerField()
    id_typu_nosnika = models.ForeignKey('TypyNosnikow', models.DO_NOTHING, db_column='id_typu_nosnika')

    class Meta:
        managed = False
        db_table = 'Nosniki_elektroniczne'
        unique_together = (('id_pasazera', 'id_nosnika', 'id_ulgi'),)


class NosnikiKartonikowe(models.Model):
    id_nosnika = models.AutoField(primary_key=True)
    kod = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Nosniki_kartonikowe'


class Pasazerowie(models.Model):
    id_pasazera = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    id_ulgi = models.ForeignKey('Ulgi', models.DO_NOTHING, db_column='id_ulgi')

    class Meta:
        managed = False
        db_table = 'Pasazerowie'
        unique_together = (('id_pasazera', 'id_ulgi'),)


class Transakcje(models.Model):
    id_transakcji = models.AutoField(primary_key=True)
    data_zakupu = models.DateTimeField(auto_now_add=True)
    kwota = models.FloatField(default=0)
    id_miejsca_transakcji = models.ForeignKey(MiejscaTransakcji, models.DO_NOTHING, db_column='id_miejsca_transakcji')
    id_metody_platnosci = models.ForeignKey(MetodyPlatnosci, models.DO_NOTHING, db_column='id_metody_platnosci')

    class Meta:
        managed = False
        db_table = 'Transakcje'


class TypyBiletow(models.Model):
    id_typu_biletu = models.AutoField(primary_key=True)
    cena = models.FloatField()
    strefa = models.CharField(max_length=3)
    czas_waznosci = models.DurationField()

    class Meta:
        managed = False
        db_table = 'Typy_biletow'


class TypyNosnikow(models.Model):
    id_typu_nosnika = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'Typy_nosnikow'


class TypyUlgi(models.Model):
    id_typu_ulgi = models.AutoField(primary_key=True)
    kod_podstawowy = models.IntegerField()
    wielkosc_ulgi = models.IntegerField()
    nazwa = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Typy_ulgi'


class Ulgi(models.Model):
    id_ulgi = models.AutoField(primary_key=True)
    id_typu_ulgi = models.ForeignKey(TypyUlgi, models.DO_NOTHING, db_column='id_typu_ulgi', blank=True, null=True)
    data_waznosci = models.DateField()

    class Meta:
        managed = False
        db_table = 'Ulgi'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
