# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Interactions(models.Model):
    inter_id = models.IntegerField(primary_key=True)
    rxcui1 = models.CharField(db_column='RXCUI1', max_length=8)
    drug_1_concept_name = models.CharField(max_length=150, blank=True, null=True)
    rxcui2 = models.CharField(db_column='RXCUI2', max_length=8)
    drug_2_concept_name = models.CharField(max_length=150, blank=True, null=True)
    condition_meddra_id = models.CharField(max_length=8)
    condition_concept_name = models.CharField(max_length=100, blank=True, null=True)
    a = models.CharField(db_column='A', max_length=15, blank=True, null=True)  # Field name made lowercase.
    b = models.CharField(db_column='B', max_length=15, blank=True, null=True)  # Field name made lowercase.
    c = models.CharField(db_column='C', max_length=15, blank=True, null=True)  # Field name made lowercase.
    d = models.CharField(db_column='D', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prr = models.CharField(db_column='PRR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prr_error = models.CharField(db_column='PRR_error', max_length=15, blank=True, null=True)  # Field name made lowercase.
    mean_reporting_frequency = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interactions'
        unique_together = (('rxcui1', 'rxcui2', 'condition_meddra_id'),)


class Junction(models.Model):
    pk = models.CompositePrimaryKey('inter_id', 'result_id')
    inter_id = models.ForeignKey(Interactions, models.DO_NOTHING, db_column='inter_id', to_field='inter_id', related_name='junction_inter_id_set') 
    result = models.ForeignKey('Results', on_delete = models.CASCADE)
    #condition_meddra = models.ForeignKey(Interactions, models.DO_NOTHING, to_field='condition_meddra_id', related_name='junction_condition_meddra_set')

    class Meta:
        managed = True
        db_table = 'junction'
        unique_together = (('inter_id', 'result'),)


class Results(models.Model):
    dt_generated = models.DateTimeField(blank=True, null=True)
    result_name = models.CharField(max_length=50, blank=True, null=True)
    result_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', on_delete = models.CASCADE)

    class Meta:
        managed = True
        db_table = 'results'


class Rxnconso(models.Model):
    rxcui = models.CharField(db_column='RXCUI', max_length=8)  # Field name made lowercase.
    lat = models.CharField(db_column='LAT', max_length=3)  # Field name made lowercase.
    ts = models.CharField(db_column='TS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lui = models.CharField(db_column='LUI', max_length=8, blank=True, null=True)  # Field name made lowercase.
    stt = models.CharField(db_column='STT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sui = models.CharField(db_column='SUI', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ispref = models.CharField(db_column='ISPREF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rxaui = models.CharField(db_column='RXAUI', primary_key=True, max_length=20)  # Field name made lowercase.
    saui = models.CharField(db_column='SAUI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scui = models.CharField(db_column='SCUI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sdui = models.CharField(db_column='SDUI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sab = models.CharField(db_column='SAB', max_length=20)  # Field name made lowercase.
    tty = models.CharField(db_column='TTY', max_length=20)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50)  # Field name made lowercase.
    str = models.CharField(db_column='STR', max_length=3000)  # Field name made lowercase.
    srl = models.CharField(db_column='SRL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    suppress = models.CharField(db_column='SUPPRESS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cvf = models.CharField(db_column='CVF', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rxnconso'

    def __str__(self):
        return self.name


class Rxnrel(models.Model):
    rxcui1 = models.CharField(db_column='RXCUI1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rxaui1 = models.CharField(db_column='RXAUI1', max_length=10)  # Field name made lowercase.
    stype1 = models.CharField(db_column='STYPE1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rel = models.CharField(db_column='REL', max_length=4)  # Field name made lowercase.
    rxcui2 = models.CharField(db_column='RXCUI2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rxaui2 = models.CharField(db_column='RXAUI2', max_length=10)  # Field name made lowercase.
    stype2 = models.CharField(db_column='STYPE2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rela = models.CharField(db_column='RELA', max_length=100)  # Field name made lowercase.
    rui = models.CharField(db_column='RUI', primary_key=True, max_length=12)  # Field name made lowercase.
    srui = models.CharField(db_column='SRUI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sab = models.CharField(db_column='SAB', max_length=20)  # Field name made lowercase.
    sl = models.CharField(db_column='SL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    dir = models.CharField(db_column='DIR', max_length=3, blank=True, null=True)  # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=10, blank=True, null=True)  # Field name made lowercase.
    suppress = models.CharField(db_column='SUPPRESS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cvf = models.CharField(db_column='CVF', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rxnrel'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    password_hash = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'


