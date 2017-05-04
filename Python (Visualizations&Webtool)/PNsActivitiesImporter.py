import os, csv, cPickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PRO2.settings")

import django
django.setup()


from plots.models import Plot, HeatMat

#Before import I delete everything to prevent duplications:
Plot.objects.all().delete()
HeatMat.objects.all().delete()

with open('RawDataToImport/PN&ChaperMetaPCAResults.csv','rb') as csvfile:
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot(title = rows[''],folding = float(rows['Folding']),
                       trafficking = float(rows['Trafficking']),
                       clearance = float(rows['Clearance']),
                       metabolism = float(rows['PN-metabolism']),
                       signaling = float(rows['PN-signaling']),
                       synthesis = float(rows['Protein synthesis']),
                       ER = float(rows['ER']),
                       HSP100 = float(rows['HSP100']),
                       HSP40 = float(rows['HSP40']),
                       HSP60 = float(rows['HSP60']),
                       HSP70 = float(rows['HSP70']),
                       HSP90 = float(rows['HSP90']),
                       MITO = float(rows['MITO']),
                       PFD = float(rows['PFD']),
                       sHSP = float(rows['sHSP']),
                       TPR = float(rows['TPR']))
        plotTmp.save()

with open('RawDataToImport/PN&ChaperMetaPCAResultsQ95.csv','rb') as csvfile: # I'm gonna have 5 <-> 95 % range!
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot.objects.get(title__icontains=rows[''])
        plotTmp.foldingMax = float(rows['Folding'])
        plotTmp.traffickingMax = float(rows['Trafficking'])
        plotTmp.clearanceMax = float(rows['Clearance'])
        plotTmp.metabolismMax = float(rows['PN-metabolism'])
        plotTmp.signalingMax = float(rows['PN-signaling'])
        plotTmp.synthesisMax = float(rows['Protein synthesis'])
        plotTmp.ERMax = float(rows['ER'])
        plotTmp.HSP100Max = float(rows['HSP100'])
        plotTmp.HSP40Max = float(rows['HSP40'])
        plotTmp.HSP60Max = float(rows['HSP60'])
        plotTmp.HSP70Max = float(rows['HSP70'])
        plotTmp.HSP90Max = float(rows['HSP90'])
        plotTmp.MITOMax = float(rows['MITO'])
        plotTmp.PFDMax = float(rows['PFD'])
        plotTmp.sHSPMax = float(rows['sHSP'])
        plotTmp.TPRMax = float(rows['TPR'])
        plotTmp.save()

with open('RawDataToImport/PN&ChaperMetaPCAResultsQ5.csv','rb') as csvfile: # I'm gonna have 5 <-> 95 % range!
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot.objects.get(title__icontains=rows[''])
        plotTmp.foldingMin = float(rows['Folding'])
        plotTmp.traffickingMin = float(rows['Trafficking'])
        plotTmp.clearanceMin = float(rows['Clearance'])
        plotTmp.metabolismMin = float(rows['PN-metabolism'])
        plotTmp.signalingMin = float(rows['PN-signaling'])
        plotTmp.synthesisMin = float(rows['Protein synthesis'])
        plotTmp.ERMin = float(rows['ER'])
        plotTmp.HSP100Min = float(rows['HSP100'])
        plotTmp.HSP40Min = float(rows['HSP40'])
        plotTmp.HSP60Min = float(rows['HSP60'])
        plotTmp.HSP70Min = float(rows['HSP70'])
        plotTmp.HSP90Min = float(rows['HSP90'])
        plotTmp.MITOMin = float(rows['MITO'])
        plotTmp.PFDMin = float(rows['PFD'])
        plotTmp.sHSPMin = float(rows['sHSP'])
        plotTmp.TPRMin = float(rows['TPR'])
        plotTmp.save()

with open('RawDataToImport/GSAChaperomeTCGAHeatmap_6_4_2017_With72SEED_Ordered.csv','rb') as csvfile:

    # activities = csv.DictReader(csvfile)
    activities = csv.reader(csvfile)
    activitiesListed = []
    activitiesListedFurNDArray = []
    diseaseNames = []
    groupNames = []

    # for line in activities:
    #     activitiesListed.append(line)
    #     activitiesListedFurNDArray.append(line.values()[1:])
    #     groupNames = line.keys()[1:]
    #     diseaseNames.append(line.values()[0])
    for row in activities:
        if row[0] == '':
            groupNames = row[1:]
        else:
            diseaseNames.append(row[0])
            activitiesListedFurNDArray.append(row[1:])

    activities_pickled = cPickle.dumps(activitiesListedFurNDArray)
    groups_pickled = cPickle.dumps(groupNames)
    diseases_pickled = cPickle.dumps(diseaseNames)

    heatTmp = HeatMat(title = 'TCGAChaperome',pickledValueMatrix = activities_pickled,
                      pickledValueRowDiseaseNames = diseases_pickled, pickledValueColGroupNames = groups_pickled)
    heatTmp.save()
    # activities_inflated = cPickle.loads(activities_pickled)

with open('RawDataToImport/GSAPNTCGAHeatmap_With72SEED_Ordered.csv','rb') as csvfile:

    # activities = csv.DictReader(csvfile)
    activities = csv.reader(csvfile)
    activitiesListed = []
    activitiesListedFurNDArray = []
    diseaseNames = []
    groupNames = []

    # for line in activities:
    #     activitiesListed.append(line)
    #     activitiesListedFurNDArray.append(line.values()[1:])
    #     groupNames = line.keys()[1:]
    #     diseaseNames.append(line.values()[0])
    for row in activities:
        if row[0] == '':
            groupNames = row[1:]
        else:
            diseaseNames.append(row[0])
            activitiesListedFurNDArray.append(row[1:])

    activities_pickled = cPickle.dumps(activitiesListedFurNDArray)
    groups_pickled = cPickle.dumps(groupNames)
    diseases_pickled = cPickle.dumps(diseaseNames)

    heatTmp = HeatMat(title = 'TCGAPN',pickledValueMatrix = activities_pickled,
                      pickledValueRowDiseaseNames = diseases_pickled, pickledValueColGroupNames = groups_pickled)
    heatTmp.save()


# The damn CamelCase Names of Plots are not correct! Correcting them here:
## You actually don't need to do this: 'icontains' in Objects.get is case insensetive, all the folloing code was a waste
## of my time! :d
if(False):
    tstPlotObj = Plot.objects.get(title__icontains='ThyroidcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'ThyroidCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='ThyroidcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'ThyroidCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='StomachadenocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'StomachAdenocarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='StomachadenocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'StomachAdenocarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='ProstateadenocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'ProstateAdenocarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='ProstateadenocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'ProstateAdenocarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='PheochromocytomaandParagangliomaPrimarysolidTumor')
    tstPlotObj.title = u'PheochromocytomaAndParagangliomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='PheochromocytomaandParagangliomaSolidTissueNormal')
    tstPlotObj.title = u'PheochromocytomaAndParagangliomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='PancreaticadenocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'PancreaticAdenocarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='PancreaticadenocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'PancreaticAdenocarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='LungsquamouscellcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'LungSquamousCellCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='LungsquamouscellcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'LungSquamousCellCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='LungadenocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'LungAdenocarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='LungadenocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'LungAdenocarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='LiverhepatocellularcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'LiverHepatocellularCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='LiverhepatocellularcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'LiverHepatocellularCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='KidneyrenalpapillarycellcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'KidneyRenalPapillaryCellCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='KidneyrenalpapillarycellcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'KidneyRenalPapillaryCellCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='KidneyrenalclearcellcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'KidneyRenalClearCellCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='KidneyrenalclearcellcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'KidneyRenalClearCellCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='HeadandNecksquamouscellcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'HeadAndNeckSquamousCellCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='HeadandNecksquamouscellcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'HeadAndNeckSquamousCellCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='GlioblastomamultiformePrimarysolidTumor')
    tstPlotObj.title = u'GlioblastomaMultiformePrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='GlioblastomamultiformeSolidTissueNormal')
    tstPlotObj.title = u'GlioblastomaMultiformeSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='EsophagealcarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'EsophagealCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='EsophagealcarcinomaSolidTissueNormal')
    tstPlotObj.title = u'EsophagealCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='CholangiocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'CholangioCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='CholangiocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'CholangioCarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='CervicalsquamouscellcarcinomaandendocervicaladenocarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'CervicalSquamousCellCarcinomaAndEndocervicalAdenocarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='CervicalsquamouscellcarcinomaandendocervicaladenocarcinomaSolidTissueNormal')
    tstPlotObj.title = u'CervicalSquamousCellCarcinomaAndEndocervicalAdenocarcinomaSolidTissueNormal'
    tstPlotObj.save()


    tstPlotObj = Plot.objects.get(title__icontains='BreastinvasivecarcinomaPrimarysolidTumor')
    tstPlotObj.title = u'BreastInvasiveCarcinomaPrimarysolidTumor'
    tstPlotObj.save()

    tstPlotObj = Plot.objects.get(title__icontains='BreastinvasivecarcinomaSolidTissueNormal')
    tstPlotObj.title = u'BreastInvasiveCarcinomaSolidTissueNormal'
    tstPlotObj.save()




#Neuro Importing:
with open('RawDataToImport/PN&ChaperMetaPCANeuroResults.csv','rb') as csvfile:
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot(title = rows[''],folding = float(rows['Folding']),
                       trafficking = float(rows['Trafficking']),
                       clearance = float(rows['Clearance']),
                       metabolism = float(rows['PN-metabolism']),
                       signaling = float(rows['PN-signaling']),
                       synthesis = float(rows['Protein synthesis']),
                       ER = float(rows['ER']),
                       HSP100 = float(rows['HSP100']),
                       HSP40 = float(rows['HSP40']),
                       HSP60 = float(rows['HSP60']),
                       HSP70 = float(rows['HSP70']),
                       HSP90 = float(rows['HSP90']),
                       MITO = float(rows['MITO']),
                       PFD = float(rows['PFD']),
                       sHSP = float(rows['sHSP']),
                       TPR = float(rows['TPR']))
        plotTmp.save()

with open('RawDataToImport/PN&ChaperMetaPCANeuroResultsQ95.csv','rb') as csvfile: # I'm gonna have 5 <-> 95 % range!
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot.objects.get(title__icontains=rows[''])
        plotTmp.foldingMax = float(rows['Folding'])
        plotTmp.traffickingMax = float(rows['Trafficking'])
        plotTmp.clearanceMax = float(rows['Clearance'])
        plotTmp.metabolismMax = float(rows['PN-metabolism'])
        plotTmp.signalingMax = float(rows['PN-signaling'])
        plotTmp.synthesisMax = float(rows['Protein synthesis'])
        plotTmp.ERMax = float(rows['ER'])
        plotTmp.HSP100Max = float(rows['HSP100'])
        plotTmp.HSP40Max = float(rows['HSP40'])
        plotTmp.HSP60Max = float(rows['HSP60'])
        plotTmp.HSP70Max = float(rows['HSP70'])
        plotTmp.HSP90Max = float(rows['HSP90'])
        plotTmp.MITOMax = float(rows['MITO'])
        plotTmp.PFDMax = float(rows['PFD'])
        plotTmp.sHSPMax = float(rows['sHSP'])
        plotTmp.TPRMax = float(rows['TPR'])
        plotTmp.save()

with open('RawDataToImport/PN&ChaperMetaPCANeuroResultsQ5.csv','rb') as csvfile: # I'm gonna have 5 <-> 95 % range!
    activities = csv.DictReader(csvfile)
    for rows in activities:
        plotTmp = Plot.objects.get(title__icontains=rows[''])
        plotTmp.foldingMin = float(rows['Folding'])
        plotTmp.traffickingMin = float(rows['Trafficking'])
        plotTmp.clearanceMin = float(rows['Clearance'])
        plotTmp.metabolismMin = float(rows['PN-metabolism'])
        plotTmp.signalingMin = float(rows['PN-signaling'])
        plotTmp.synthesisMin = float(rows['Protein synthesis'])
        plotTmp.ERMin = float(rows['ER'])
        plotTmp.HSP100Min = float(rows['HSP100'])
        plotTmp.HSP40Min = float(rows['HSP40'])
        plotTmp.HSP60Min = float(rows['HSP60'])
        plotTmp.HSP70Min = float(rows['HSP70'])
        plotTmp.HSP90Min = float(rows['HSP90'])
        plotTmp.MITOMin = float(rows['MITO'])
        plotTmp.PFDMin = float(rows['PFD'])
        plotTmp.sHSPMin = float(rows['sHSP'])
        plotTmp.TPRMin = float(rows['TPR'])
        plotTmp.save()


with open('RawDataToImport/GSAChaperomeNeuroHeatmap_27_1_2017_With0SEED_Ordered.csv','rb') as csvfile:

    # activities = csv.DictReader(csvfile)
    activities = csv.reader(csvfile)
    activitiesListed = []
    activitiesListedFurNDArray = []
    diseaseNames = []
    groupNames = []

    # for line in activities:
    #     activitiesListed.append(line)
    #     activitiesListedFurNDArray.append(line.values()[1:])
    #     groupNames = line.keys()[1:]
    #     diseaseNames.append(line.values()[0])
    for row in activities:
        if row[0] == '':
            groupNames = row[1:]
        else:
            diseaseNames.append(row[0])
            activitiesListedFurNDArray.append(row[1:])

    activities_pickled = cPickle.dumps(activitiesListedFurNDArray)
    groups_pickled = cPickle.dumps(groupNames)
    diseases_pickled = cPickle.dumps(diseaseNames)

    heatTmp = HeatMat(title = 'NeuroChaperome',pickledValueMatrix = activities_pickled,
                      pickledValueRowDiseaseNames = diseases_pickled, pickledValueColGroupNames = groups_pickled)
    heatTmp.save()
    # activities_inflated = cPickle.loads(activities_pickled)

with open('RawDataToImport/GSAPNNeuroHeatmap_27_1_2017_With0SEED_Ordered.csv','rb') as csvfile:

    # activities = csv.DictReader(csvfile)
    activities = csv.reader(csvfile)
    activitiesListed = []
    activitiesListedFurNDArray = []
    diseaseNames = []
    groupNames = []

    # for line in activities:
    #     activitiesListed.append(line)
    #     activitiesListedFurNDArray.append(line.values()[1:])
    #     groupNames = line.keys()[1:]
    #     diseaseNames.append(line.values()[0])
    for row in activities:
        if row[0] == '':
            groupNames = row[1:]
        else:
            diseaseNames.append(row[0])
            activitiesListedFurNDArray.append(row[1:])

    activities_pickled = cPickle.dumps(activitiesListedFurNDArray)
    groups_pickled = cPickle.dumps(groupNames)
    diseases_pickled = cPickle.dumps(diseaseNames)

    heatTmp = HeatMat(title = 'NeuroPN',pickledValueMatrix = activities_pickled,
                      pickledValueRowDiseaseNames = diseases_pickled, pickledValueColGroupNames = groups_pickled)
    heatTmp.save()
