# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Imienne(models.Model):
    id_biletu = models.IntegerField()
    data_aktywacji = models.DateTimeField(blank=True, null=True)
    data_waznosci = models.DateTimeField(blank=True, null=True)
    id_transakcji = models.IntegerField(primary_key=True)
    id_pasazera = models.ForeignKey('NosnikiElektroniczne', models.DO_NOTHING, db_column='id_pasazera')
    id_nosnika = models.IntegerField(blank=True, null=True)
    id_ulgi = models.IntegerField(blank=True, null=True)
    id_typu = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Imienne'
        unique_together = (('id_transakcji', 'id_biletu'),)


class MetodyPlatnosci(models.Model):
    id_metody_platnosci = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Metody_platnosci'


class MiejscaTransakcji(models.Model):
    id_miejsca_transakcji = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30, blank=True, null=True)
    ulica = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Miejsca_transakcji'


class Nieimienne(models.Model):
    id_biletu = models.IntegerField()
    data_aktywacji = models.DateTimeField(blank=True, null=True)
    data_waznosci = models.DateTimeField(blank=True, null=True)
    id_transakcji = models.IntegerField(primary_key=True)
    id_nosnika = models.ForeignKey('NosnikiKartonikowe', models.DO_NOTHING, db_column='id_nosnika', blank=True, null=True)
    id_typu = models.IntegerField(blank=True, null=True)
    id_typu_ulgi = models.ForeignKey('TypyUlgi', models.DO_NOTHING, db_column='id_typu_ulgi', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Nieimienne'
        unique_together = (('id_transakcji', 'id_biletu'),)


class NosnikiElektroniczne(models.Model):
    id_nosnika = models.IntegerField()
    data_waznosci = models.DateTimeField()
    id_pasazera = models.OneToOneField('Pasazerowie', models.DO_NOTHING, db_column='id_pasazera', primary_key=True)
    id_ulgi = models.IntegerField()
    id_typu_nosnika = models.ForeignKey('TypyNosnikow', models.DO_NOTHING, db_column='id_typu_nosnika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Nosniki_elektroniczne'
        unique_together = (('id_pasazera', 'id_nosnika', 'id_ulgi'),)


class NosnikiKartonikowe(models.Model):
    id_nosnika = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Nosniki_kartonikowe'


class Pasazerowie(models.Model):
    id_pasazera = models.IntegerField(primary_key=True)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    id_ulgi = models.ForeignKey('Ulgi', models.DO_NOTHING, db_column='id_ulgi')

    class Meta:
        managed = False
        db_table = 'Pasazerowie'
        unique_together = (('id_pasazera', 'id_ulgi'),)


class Transakcje(models.Model):
    id_transakcji = models.IntegerField()
    data_zakupu = models.DateTimeField()
    kwota = models.IntegerField()
    id_miejsca_transakcji = models.ForeignKey(MiejscaTransakcji, models.DO_NOTHING, db_column='id_miejsca_transakcji')
    id_metody_platnosci = models.ForeignKey(MetodyPlatnosci, models.DO_NOTHING, db_column='id_metody_platnosci')

    class Meta:
        managed = False
        db_table = 'Transakcje'


class TypyBiletow(models.Model):
    id_typu_biletu = models.IntegerField(primary_key=True)
    czas_waznosci = models.DateTimeField()
    cena = models.IntegerField()
    strefa = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'Typy_biletow'


class TypyNosnikow(models.Model):
    id_typu_nosnika = models.IntegerField(primary_key=True)
    nazwa = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Typy_nosnikow'


class TypyUlgi(models.Model):
    id_typu_ulgi = models.IntegerField(primary_key=True)
    kod_podstawowy = models.IntegerField()
    wielkosc_ulgi = models.IntegerField()
    nazwa = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Typy_ulgi'


class Ulgi(models.Model):
    id_ulgi = models.IntegerField(primary_key=True)
    data_waznosci = models.IntegerField()
    id_typu_ulgi = models.ForeignKey(TypyUlgi, models.DO_NOTHING, db_column='id_typu_ulgi', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Ulgi'
