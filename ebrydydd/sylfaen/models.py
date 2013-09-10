from django.db import models

'''
Llinell HAS Dadansoddiad (one-to-many)
Dosbarth HAS Dadansoddiad (one-to-many)
'''

class Llinell(models.Model):
    llinyn = models.CharField(max_length=100)
    awdur = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self):
        s = self.llinyn
        if awdur:
            s += '    [' + awdur + ']'
        return s


class Dosbarth(models.Model):
    DOSBARTH_BAI = (
        ('CAM', 'Camacennu)'
        ('CAR', 'Carnymorddiwes'),
        ('COS', 'Camosodiad'),
        ('CRY', 'Crych a llyfn'),
        ('DYB', 'Dybryd sain'),
        ('LLE', 'Lleddf a thalgron'),
        ('LLY', 'Llysiant llusg'),
        ('PRO', 'Proest i\'r odl'),
        ('RHY', 'Rhy debyg'),
        ('TAY', 'Trwm ac ysgafn'),
        ('TWY', 'Twyll gynghanedd'),
        ('TWY', 'Twyll odl'),
    }
    DOSBARTH_CYNGHANEDD = (
        ('XX', 'Dim Cynghanedd'),
        ('CR', 'Croes'),
        ('TR', 'Traws'),
        ('SA', 'Sain'),
        ('LL', 'Llusg'),
        ('CG', 'Croes o Gyswllt'),
        ('TF', 'Traws Fantach'),
    )
    DOSBARTH_ACENNIAD = (
        ('CAC', 'Cytbwys Acennog'),
        ('CDI', 'Cytbwys Ddiacen'),
        ('ADI', 'Anghytbwys Ddisgynedig'),
        ('ADY', 'Anghytbwys Ddyrchafedig'),
    )
    DOSBARTH_ODL = (
        ('OG', 'Odl Gyflawn'),
        ('PG', 'Proest Gyflawn'),
        ('OL', 'Anghytbwys Ddisgynedig'),
        ('PL', 'Anghytbwys Ddyrchafedig'),
    )
    dosbarth_cynghanedd = models.CharField(max_length=2, choices=DOSBARTH_CYNGHANEDD)
    dosbarth_acenniad = models.CharField(max_length=3, choices=DOSBARTH_ACENNIAD, null=True, blank=True)
    dosbarth_odl = models.CharField(max_length=2, choices=DOSBARTH_ODL, null=True, blank=True)
    dosbarth_bai = models.CharField(max_length=3, choices=DOSBARTH_BAI, null=True, blank=True)

    def __unicode__(self):
        s = self.dosbarth_cynghanedd 
        if self.dosbarth_acennu:
            s += self.dosbarth_acenniad
        if self.dosbarth_odl:
            s += self.dosbarth_odl
        return s


class Dadansoddiad(models.Model):
    llinell = models.ForeignKey(Llinell)
    dosbarth = models.ForeignKey(Dosbarth)
    dadansoddwr = models.CharField(max_length=100, blank=True)
    nodiadau = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        s = self.llinell + '\n' + self.dosbarth + '\n[' + self.dadansoddwr
        if self.nodiadau:
            s += '\n(' + self.nodiadau
        return s


