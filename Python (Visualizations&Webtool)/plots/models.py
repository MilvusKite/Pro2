from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Plot(models.Model):


    title = models.CharField(max_length=100)

    folding = models.FloatField(null=True, blank=True)
    trafficking = models.FloatField(null=True, blank=True)
    clearance = models.FloatField(null=True, blank=True)
    metabolism = models.FloatField(null=True, blank=True)
    signaling = models.FloatField(null=True, blank=True)
    synthesis = models.FloatField(null=True, blank=True)
    ER = models.FloatField(null=True, blank=True)
    HSP100 = models.FloatField(null=True, blank=True)
    HSP40 = models.FloatField(null=True, blank=True)
    HSP60 = models.FloatField(null=True, blank=True)
    HSP70 = models.FloatField(null=True, blank=True)
    HSP90 = models.FloatField(null=True, blank=True)
    MITO = models.FloatField(null=True, blank=True)
    PFD = models.FloatField(null=True, blank=True)
    sHSP = models.FloatField(null=True, blank=True)
    TPR = models.FloatField(null=True, blank=True)

    foldingMax = models.FloatField(null=True, blank=True)
    traffickingMax = models.FloatField(null=True, blank=True)
    clearanceMax = models.FloatField(null=True, blank=True)
    metabolismMax = models.FloatField(null=True, blank=True)
    signalingMax = models.FloatField(null=True, blank=True)
    synthesisMax = models.FloatField(null=True, blank=True)
    ERMax = models.FloatField(null=True, blank=True)
    HSP100Max = models.FloatField(null=True, blank=True)
    HSP40Max = models.FloatField(null=True, blank=True)
    HSP60Max = models.FloatField(null=True, blank=True)
    HSP70Max = models.FloatField(null=True, blank=True)
    HSP90Max = models.FloatField(null=True, blank=True)
    MITOMax = models.FloatField(null=True, blank=True)
    PFDMax = models.FloatField(null=True, blank=True)
    sHSPMax = models.FloatField(null=True, blank=True)
    TPRMax = models.FloatField(null=True, blank=True)

    foldingMin = models.FloatField(null=True, blank=True)
    traffickingMin = models.FloatField(null=True, blank=True)
    clearanceMin = models.FloatField(null=True, blank=True)
    metabolismMin = models.FloatField(null=True, blank=True)
    signalingMin = models.FloatField(null=True, blank=True)
    synthesisMin = models.FloatField(null=True, blank=True)
    ERMin = models.FloatField(null=True, blank=True)
    HSP100Min = models.FloatField(null=True, blank=True)
    HSP40Min = models.FloatField(null=True, blank=True)
    HSP60Min = models.FloatField(null=True, blank=True)
    HSP70Min = models.FloatField(null=True, blank=True)
    HSP90Min = models.FloatField(null=True, blank=True)
    MITOMin = models.FloatField(null=True, blank=True)
    PFDMin = models.FloatField(null=True, blank=True)
    sHSPMin = models.FloatField(null=True, blank=True)
    TPRMin = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.title
    def __getitem__(self, key):
        if key=='Folding': return self.folding
        if key=='PN-signaling': return self.signaling
        if key=='Trafficking': return self.trafficking
        if key=='Protein synthesis': return self.synthesis
        if key=='Clearance': return self.clearance
        if key=='PN-metabolism': return self.metabolism
        if key=='HSP40': return self.HSP40
        if key=='HSP60': return self.HSP60
        if key=='HSP70': return self.HSP70
        if key=='HSP90': return self.HSP90
        if key=='HSP100': return self.HSP100
        if key=='PFD': return self.PFD
        if key=='MITO': return self.MITO
        if key=='sHSP': return self.sHSP
        if key=='TPR': return self.TPR
        if key=='ER': return self.ER

class HeatMat(models.Model):


    title = models.CharField(max_length=100)

    pickledValueMatrix = models.TextField()
    pickledValueRowDiseaseNames = models.TextField()
    pickledValueColGroupNames = models.TextField()

    def __unicode__(self):
        return self.title