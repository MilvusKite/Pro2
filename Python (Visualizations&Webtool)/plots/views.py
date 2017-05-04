from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from plots.models import Plot, HeatMat
import os


def FullToAbrvNameTCGA(FULLNAMES):
    convTable = {'PheochromocytomaAndParaganglioma':'PCPG',
                 'SkinCutaneousMelanoma':'SKCM',
                 'ThyroidCarcinoma':'THCA',
                 'KidneyRenalClearCellCarcinoma':'KIRC',
                 'UterineCorpusEndometrialCarcinoma':'UCEC',
                 'Thymoma':'THYM',
                 'StomachAdenocarcinoma':'STAD',
                 'Sarcoma':'SARC',
                 'ProstateAdenocarcinoma':'PRAD',
                 'PancreaticAdenocarcinoma':'PAAD',
                 'LungSquamousCellCarcinoma':'LUSC',
                 'LungAdenocarcinoma':'LUAD',
                 'LiverHepatocellularCarcinoma':'LIHC',
                 'KidneyRenalPapillaryCellCarcinoma':'KIRP',
                 'KidneyChromophobe':'KICH',
                 'HeadAndNeckSquamousCellCarcinoma':'HNSC',
                 'GlioblastomaMultiforme':'GBM',
                 'EsophagealCarcinoma':'ESCA',
                 'CholangioCarcinoma':'CHOL',
                 'CervicalSquamousCellCarcinomaAndEndocervicalAdenocarcinoma':'CESC',
                 'BreastInvasiveCarcinoma':'BRCA',
                 'BladderUrothelialCarcinoma':'BLCA'}
    if type(FULLNAMES) == type([]):
        return([convTable[FULLNAME] for FULLNAME in FULLNAMES])
    else:
        return(convTable[FULLNAMES])

def FullToAbrvNameNeuro(FULLNAMES):
    convTable = {'AlzheimerDisease':'AD',
                 'HuntingtonDisease':'HD',
                 'ParkinsonDisease':'PD'}
    if type(FULLNAMES) == type([]):
        return([convTable[FULLNAME] for FULLNAME in FULLNAMES])
    else:
        return(convTable[FULLNAMES])

def UnCamelCaser(STRING):
    import re
    return(re.sub("([a-z])([A-Z])","\g<1> \g<2>",STRING))

def TissueAddRemover(alles,eins):
    if eins in alles:
        alles.remove(eins)
    else:
        alles.append(eins)
    return(alles)

# Create your views here.
def UndiConsti(request,*ExtraCrap):
    return render(request,'underconstruction.html',{'nbar':'UC'})

def TutorialShower(request):
    return render(request,'tutorial.html')

def AboutShower(request):
    return render(request,'about.html')

def PrivacyShower(request):
    return render(request,'privacy.html')

def TermsShower(request):
    return render(request,'termsofuse.html')

def HelpShower(request):
    if request.user.is_authenticated():
        return render(request,'help.html')
    else:
        return HttpResponseRedirect('/login/')

def HomePage(request):
    return render(request,'home.html',{'nbar':'HOME'})

def HomeLogin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashmain/')
    else:
        return HttpResponseRedirect('/accounts/login/')

def HomeDash(request):
    if request.user.is_authenticated():
        return render(request,'dashboard.html',{'nbar':'DASH','STEP':1})
    else:
        return HttpResponseRedirect('/accounts/login/')

def DiseaseDash(request,LEVEL):
    if request.user.is_authenticated():
        return render(request,'dashboard.html',{'nbar':'DASH','STEP':2,'LEVEL':LEVEL})
    else:
        return HttpResponseRedirect('/accounts/login/')

def TissueDashIntro(request,LEVEL,DISEASE):
    if request.user.is_authenticated():
        return render(request,'dashboard.html',{'nbar':'DASH','STEP':3,'LEVEL':LEVEL,'DISEASE':DISEASE})
    else:
        return HttpResponseRedirect('/accounts/login/')

def TissueDash(request,LEVEL,DISEASE):
    if request.user.is_authenticated():
        if 'PLOTTYPE' in request.session and request.session['PLOTTYPE']:
           PLOTTYPE = request.session['PLOTTYPE']
           NEXT = True
        else:
           PLOTTYPE = ""
           NEXT = False
        if 'TissueName' in request.POST and request.POST['TissueName']:
            AllTissueNames = request.session['AllTissueNames']
            if request.method == "POST":
                TISSUENAME = request.POST.get("TissueName","SomethingIsWrongWithTISSUEPOST")
                AllTissueNames = TissueAddRemover(AllTissueNames,TISSUENAME)
                request.session['AllTissueNames'] = AllTissueNames
        else:
            AllTissueNames = []
            request.session['AllTissueNames'] = AllTissueNames
        return render(request,'dashboardTissue.html',{'nbar':'DASH','LEVEL':LEVEL,'DISEASE':DISEASE,
                                                      'AllTissueNames':AllTissueNames,
                                                      'NEXT':NEXT,
                                                      'PLOTTYPE':PLOTTYPE})
    else:
        return HttpResponseRedirect('/accounts/login/')

def PlotTypeDashIntro(request,LEVEL,DISEASE,TISSUE):
    if request.user.is_authenticated():
        return render(request,'dashboard.html',{'nbar':'DASH','STEP':4,'LEVEL':LEVEL,'DISEASE':DISEASE,
                                                             'TISSUE':TISSUE, 'TISSUEunCameled':UnCamelCaser(TISSUE)})
    else:
        return HttpResponseRedirect('/accounts/login/')

def PlotTypeDash(request,LEVEL,DISEASE,TISSUE,PLOTTYPE):
    if request.user.is_authenticated():
        request.session['PLOTTYPE'] = PLOTTYPE
        plotTitel = ""
        if LEVEL == 'PN':
            which_Level_To_Plot = 'L1'
            if PLOTTYPE=="heat":
                plotTitel = 'PN GSA results heatmap'
            elif PLOTTYPE=="polar":
                plotTitel = 'PN polar map'
            elif PLOTTYPE=="2D":
                plotTitel = 'PN 2D meta-network'
            elif PLOTTYPE=="topo":
                plotTitel = 'PN 3D topographic map'
        elif LEVEL == 'chaperome':
            which_Level_To_Plot = 'L3'
            if PLOTTYPE=="heat":
                plotTitel = 'Chaperome GSA results heatmap'
            elif PLOTTYPE=="polar":
                plotTitel = 'Chaperome M-scores polar map'
            elif PLOTTYPE=="2D":
                plotTitel = 'Chaperome M-scores 2D meta-network'
            elif PLOTTYPE=="topo":
                plotTitel = 'Chaperome 3D topographic map'
        else:
            raise ValueError('A problem with specifying plot Level!')
        if DISEASE == 'TCGA':
            title = TISSUE+'fromTCGA'
        elif DISEASE == 'neuro':
            title = TISSUE+'fromNeuro'
        else:
            raise ValueError('A problem with specifying plot Title!')
        if 'AllTissueNames' in request.session: #and request.session['AllTissueNames']:
            AllTissueNames = request.session['AllTissueNames']
        else:
            raise ValueError('AllTissueNames nowhere to be found!!')
        if TISSUE == 'multiplotter':
            return render(request,'dashboardPlottype.html',{'nbar':'DASH','LEVEL':LEVEL,'DISEASE':DISEASE,
                                                            'TISSUE':TISSUE,'PLOTTYPE':PLOTTYPE,
                                                            'PLOTADD':os.path.join("/",PLOTTYPE,which_Level_To_Plot,""),
                                                            'AllTissueNames':AllTissueNames,
                                                            'TISSUEunCameled':UnCamelCaser(TISSUE),
                                                            'plotTitel':plotTitel})
        else:
            return render(request,'dashboardPlottype.html',{'nbar':'DASH','LEVEL':LEVEL,'DISEASE':DISEASE,
                                                        'TISSUE':TISSUE,'PLOTTYPE':PLOTTYPE,
                                                        'PLOTADD':os.path.join("/",PLOTTYPE,which_Level_To_Plot,title),
                                                        'AllTissueNames':"SinglePlotting",
                                                        'TISSUEunCameled':UnCamelCaser(TISSUE)})
    else:
        return HttpResponseRedirect('/accounts/login/')

#This function makes 3d topographic maps:
def Actual3DPlotter(request,LevelOfPlot,whatToPlot):


    if not request.user.is_authenticated(): # Check authentication!
        return HttpResponseRedirect('/accounts/login/')

    import numpy as np
    import plotly.offline as py
    import plotly.graph_objs as go
    import pandas as pd

    # Import values from database to plot:
    if 'fromTCGA' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','SolidTissueNormal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','PrimarysolidTumor'))
        # PlotingA = 'Healthy'
        plotTitel = whatToPlot.replace('fromTCGA','')
    elif 'fromNeuro' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','Normal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','NeuroDegenerated'))
        plotTitel = UnCamelCaser(whatToPlot.replace('fromNeuro',''))
    else:
        raise ValueError('A problem with finding ' + whatToPlot + ' in database!')

    # Initialize plotting params:
    n = np.array([200]) # Number of points to plot in each dimension
    mnAx = np.array([-4]) # (Actual) Min value in plotting in each dimension
    mxAx = np.array([4]) # (Actual) Max value in plotting in each dimension
    x = np.linspace(mnAx, mxAx, n+1) # Intrapolating to make the vector of each plot point x-axis value
    y = x[:,np.newaxis] # Initializing y-axis values

    def ConvertAxisToIndex(inpt,Mn,Mx,N):
        return np.floor(((inpt-Mn)/(Mx-Mn))*(N+1)).astype('int')

    # Calculating z values
    if LevelOfPlot == "L1":
        ###From Angelina's Script(which came from iGraph info in R):
        scaleFactor = 1.1
        xShift = 0
        yShift = 1
        Node_coordinates_kk = {'synthesis': (0.1571498 * scaleFactor + xShift, -0.8406522 * scaleFactor + yShift),
                               'signaling': (1.1680855 * scaleFactor + xShift, 0.4819439 * scaleFactor + yShift),
                               'trafficking': (-1.4381153 * scaleFactor + xShift, -1.3164438 * scaleFactor + yShift),
                           'folding': (-0.7883174 * scaleFactor + xShift, 0.5295084 * scaleFactor + yShift),
                               'clearance': (0.1166911 * scaleFactor + xShift, -2.504868 * scaleFactor + yShift),
                               'metabolism': (1.7274107 * scaleFactor + xShift, -1.3934034 * scaleFactor + yShift)}

        Node_size = { 'folding' : 179 , 'clearance' : 743 , 'trafficking' : 323 , 'synthesis' : 25 , 'signaling' : 100 , 'metabolism' : 20 }
        ###

        Node_size_ordered = np.array([Node_size['folding'],Node_size['trafficking'],Node_size['clearance'],
                             Node_size['metabolism'],Node_size['signaling'],Node_size['synthesis']],'float')
        Node_size_ordered_Normd = ((Node_size_ordered - Node_size_ordered.min())/
                                   (Node_size_ordered.max()-Node_size_ordered.min()))+0.75


        Node_coor_x = [Node_coordinates_kk['folding'][0],Node_coordinates_kk['trafficking'][0],Node_coordinates_kk['clearance'][0],
                       Node_coordinates_kk['metabolism'][0],Node_coordinates_kk['signaling'][0],Node_coordinates_kk['synthesis'][0]]
        Node_coor_x_indx = ConvertAxisToIndex(Node_coor_x,mnAx,mxAx,n)
        Node_coor_y = [Node_coordinates_kk['folding'][1],Node_coordinates_kk['trafficking'][1],Node_coordinates_kk['clearance'][1],
                       Node_coordinates_kk['metabolism'][1],Node_coordinates_kk['signaling'][1],Node_coordinates_kk['synthesis'][1]]
        Node_coor_y_indx = ConvertAxisToIndex(Node_coor_y,mnAx,mxAx,n)

        Node_z = [plotObjTumor.folding - plotObjNormal.folding, plotObjTumor.trafficking - plotObjNormal.trafficking,
                  plotObjTumor.clearance - plotObjNormal.clearance, plotObjTumor.metabolism - plotObjNormal.metabolism,
                  plotObjTumor.signaling - plotObjNormal.signaling, plotObjTumor.synthesis - plotObjNormal.synthesis]

        AxSetTitle = UnCamelCaser(plotTitel)


    if LevelOfPlot == "L3":
        ###From Angelina's Script(which came from iGraph info in R):
        scaleFactor = 1.5
        Node_coordinates_kk = {'HSP70': (0.549106097 * scaleFactor, 0.508699501 * scaleFactor),
                               'TPR': (-0.385391578 * scaleFactor, 0.336751962 * scaleFactor),
                               'sHSP': (0.537861181 * scaleFactor, 1.152749631 * scaleFactor),
                               'HSP100': (0.457229181 * scaleFactor, -0.696813360 * scaleFactor),
                               'HSP40': (-0.270951306 * scaleFactor, 1.277369321 * scaleFactor),
                               'ER': (0.987839259 * scaleFactor, 0.078540297 * scaleFactor),
                               'MITO': (-1.062533012 * scaleFactor, -0.558359667 * scaleFactor),
                               'PFD': (-1.516060869 * scaleFactor, 0.727729883 * scaleFactor),
                               'HSP60': (0.933374477 * scaleFactor, -1.710523361 * scaleFactor),
                               'HSP90': (-0.005235842 * scaleFactor, -0.007823429 * scaleFactor)}

        Node_size = { "HSP100" : 1 , "HSP90" : 18 , "TPR" : 43 , "sHSP" : 15 , "MITO" : 2 , "ER" : 13 , "HSP70" : 14 ,
                      "HSP40" : 8 , "HSP60" : 10 , "PFD" : 4 }
        ###

        Node_size_ordered = np.array([Node_size['ER'],Node_size['HSP100'],Node_size['HSP40'],
                             Node_size['HSP60'],Node_size['HSP70'],Node_size['HSP90'],
                             Node_size['MITO'],Node_size['PFD'],Node_size['sHSP'],
                             Node_size['TPR']],'float')
        Node_size_ordered_Normd = ((Node_size_ordered - Node_size_ordered.min())/
                                   (Node_size_ordered.max()-Node_size_ordered.min()))+0.4


        Node_coor_x = [Node_coordinates_kk['ER'][0],Node_coordinates_kk['HSP100'][0],Node_coordinates_kk['HSP40'][0],
                             Node_coordinates_kk['HSP60'][0],Node_coordinates_kk['HSP70'][0],Node_coordinates_kk['HSP90'][0],
                             Node_coordinates_kk['MITO'][0],Node_coordinates_kk['PFD'][0],Node_coordinates_kk['sHSP'][0],
                             Node_coordinates_kk['TPR'][0]]
        Node_coor_x_indx = ConvertAxisToIndex(Node_coor_x,mnAx,mxAx,n)
        Node_coor_y = [Node_coordinates_kk['ER'][1],Node_coordinates_kk['HSP100'][1],Node_coordinates_kk['HSP40'][1],
                             Node_coordinates_kk['HSP60'][1],Node_coordinates_kk['HSP70'][1],Node_coordinates_kk['HSP90'][1],
                             Node_coordinates_kk['MITO'][1],Node_coordinates_kk['PFD'][1],Node_coordinates_kk['sHSP'][1],
                             Node_coordinates_kk['TPR'][1]]
        Node_coor_y_indx = ConvertAxisToIndex(Node_coor_y,mnAx,mxAx,n)

        Node_z = [plotObjTumor.ER - plotObjNormal.ER, plotObjTumor.HSP100 - plotObjNormal.HSP100,
                  plotObjTumor.HSP40 - plotObjNormal.HSP40, plotObjTumor.HSP60 - plotObjNormal.HSP60,
                  plotObjTumor.HSP70 - plotObjNormal.HSP70, plotObjTumor.HSP90 - plotObjNormal.HSP90,
                  plotObjTumor.MITO - plotObjNormal.MITO, plotObjTumor.PFD - plotObjNormal.PFD,
                  plotObjTumor.sHSP - plotObjNormal.sHSP, plotObjTumor.TPR - plotObjNormal.TPR]

        AxSetTitle = UnCamelCaser(plotTitel)


    # Initializing "layout" for plotly plotting:
    layout = go.Layout(
        title=AxSetTitle,
        autosize=False,
        showlegend=False,
        width=1000,
        height=1000,
        ##For making plots for paper:
        # width=5000,
        # height=5000,
        ##
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        ),
        titlefont=dict(
                #family='Arial, sans-serif',
                size=30,
                #color='lightgrey'
            ),
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=False
        ),
    )

    def MakeGaussian(X, Y, X0, Y0, FWHM,
                     MAG):  # Each PN-group is plotted as a gaussian, so I use this func to make gaussians
        outi = MAG * np.exp(-4 * np.log(2) * ((X - X0) ** 2 + (Y - Y0) ** 2) / FWHM ** 2)
        return (outi)

    for Ind in range(len(Node_coor_x)): # Making gaussians for each PN-group in this loop
        if Ind == 0:
            plotz4 = MakeGaussian(x, y, Node_coor_x[Ind], Node_coor_y[Ind], Node_size_ordered_Normd[Ind], Node_z[Ind])
        else:
            plotz4 = MakeGaussian(x, y, Node_coor_x[Ind], Node_coor_y[Ind], Node_size_ordered_Normd[Ind], Node_z[Ind]) + plotz4

    plotz4 = pd.DataFrame(plotz4) # For working with plotly's surface I need a pandas DataFrame
    # Making the actual plot here using
    data = go.Surface(
            z=plotz4.as_matrix(),
            #opacity=0.999, # Doesn't work properly, or at least I couldn't!
            name='Topographic Surface',
            cmin=-2,
            cmax=2,
            visible=True,
            lighting=dict(
                fresnel=0.2,
                roughness=0.5,
                specular=0.05,
                ambient=0.8,
                diffuse=0, # for colors not changing by change in point of view
            ),
            colorscale=[[0, 'rgba(0,0,255,0)'],[0.5, 'rgba(255,255,255,1)'], [1, 'rgba(255,0,0,0)']],
            colorbar=dict(
                #y=2,
                showticklabels=True,
                len=0.2,
            ),
            hidesurface=False,
            contours=dict(
                x=dict(
                  show=False,
                  highlightwidth=1,
                  project=dict(
                      y=False,
                      x=False,
                      z=False,
                  ),
                width=4,
                highlight=False,
                usecolormap=True,
                ),
                y=dict(
                  show=False,
                  highlightwidth=1,
                    project=dict(
                      y=False,
                      x=False,
                      z=False,
                  ),
                width=4,
                highlight=False,
                usecolormap=True,
                ),
                z=dict(
                  show=False,
                  highlightwidth=1,
                    project=dict(
                      y=False,
                      x=False,
                      z=False,
                  ),
                width=4,
                highlight=False,
                usecolormap=True,
                ),
            ),

        )

    if LevelOfPlot == "L1":
        ANNOTText = go.Scatter3d(
                x=Node_coor_x_indx,
                y=Node_coor_y_indx,
                z=plotz4.as_matrix()[Node_coor_y_indx,Node_coor_x_indx] +
                  np.sign(plotz4.as_matrix()[Node_coor_y_indx,Node_coor_x_indx])*0.2,
                text=['Folding', 'Trafficking', 'Clearance', 'Metabolism', 'Signaling', 'Protein Synthesis'],
                mode='text',
                name='Annotations',
                textfont=dict(
                    # family='sans serif',
                    # size=38,
                    # color='#1f77b4'
                ),
                )
    if LevelOfPlot == "L3":
        ANNOTText = go.Scatter3d(
                x=Node_coor_x_indx,
                y=Node_coor_y_indx,
                z=plotz4.as_matrix()[Node_coor_y_indx,Node_coor_x_indx] +
                  np.sign(plotz4.as_matrix()[Node_coor_y_indx,Node_coor_x_indx])*0.2,
                text=['ER', 'HSP100', 'HSP40', 'HSP60', 'HSP70', 'HSP90', 'MITO', 'PFD', 'sHSP', 'TPR'],
                mode='text',
                name='Annotations',
                textfont=dict(
                    # family='sans serif',
                    # size=38,
                    # color='#1f77b4'
                ),
                )

    fig = go.Figure(data=[ANNOTText,data], layout=layout)
    plotHTML = py.plot(fig, auto_open=False, output_type='div')
    plotHTML = plotHTML.replace('Export to plot.ly','')
    return HttpResponse(plotHTML)

#This function makes 2d Meta networks:
def Actual2DPlotter(request,LevelOfPlot,whatToPlot):

    from networkx import Graph, get_node_attributes# Package for the creation, manipulation and study of networks
    from plotly.offline import plot as PLOTT
    from plotly.graph_objs import Scatter, Line, Marker, Figure, Data, Layout, XAxis, YAxis
    import numpy as np

    #Making the 2D layout here:
    if LevelOfPlot == 'L1':
        #Dict with node coordinates (2 different layouts)
        scaleFactor = 1.1
        xShift = 0
        yShift = 1.2
        Node_coordinates_kk = {'Protein synthesis': (0.1571498 * scaleFactor + xShift, -0.8406522 * scaleFactor + yShift),
                               'PN-signaling': (1.1680855 * scaleFactor + xShift, 0.4819439 * scaleFactor + yShift),
                               'Trafficking': (-1.4381153 * scaleFactor + xShift, -1.3164438 * scaleFactor + yShift),
                           'Folding': (-0.7883174 * scaleFactor + xShift, 0.5295084 * scaleFactor + yShift),
                               'Clearance': (0.1166911 * scaleFactor + xShift, -2.504868 * scaleFactor + yShift),
                               'PN-metabolism': (1.7274107 * scaleFactor + xShift, -1.3934034 * scaleFactor + yShift)}

        # normalized sizes here:
        sizeShift = 20
        sizeScale = 10
        Node_size = { 'Folding' : 179/sizeScale + sizeShift , 'Clearance' : 743/sizeScale + sizeShift ,
                      'Trafficking' : 323/sizeScale + sizeShift ,'Protein synthesis' : 25/sizeScale + sizeShift ,
                      'PN-signaling' : 100/sizeScale + sizeShift , 'PN-metabolism' : 20/sizeScale + sizeShift }

        sizeShiftEdge = 2
        sizeScaleEdge = 1.5
        Edge_dic = {('Protein synthesis', 'Protein synthesis'): np.log2(6)*sizeScaleEdge + sizeShiftEdge, ('Trafficking', 'Trafficking'): np.log2(447)*sizeScaleEdge + sizeShiftEdge,
                    ('PN-signaling', 'Protein synthesis'): np.log2(11)*sizeScaleEdge + sizeShiftEdge, ('Clearance', 'Clearance'): np.log2(2461)*sizeScaleEdge + sizeShiftEdge,
                    ('Folding', 'Trafficking'): np.log2(136)*sizeScaleEdge + sizeShiftEdge, ('Clearance', 'Protein synthesis'): np.log2(30)*sizeScaleEdge + sizeShiftEdge,
                    ('Protein synthesis', 'Trafficking'): np.log2(12)*sizeScaleEdge + sizeShiftEdge, ('Folding', 'Folding'): np.log2(225)*sizeScaleEdge + sizeShiftEdge,
                    ('Clearance', 'PN-metabolism'): np.log2(22)*sizeScaleEdge + sizeShiftEdge, ('Clearance', 'Folding'): np.log2(413)*sizeScaleEdge + sizeShiftEdge,
                    ('Clearance', 'Trafficking'): np.log2(467)*sizeScaleEdge + sizeShiftEdge, ('Folding', 'PN-signaling'): np.log2(96)*sizeScaleEdge + sizeShiftEdge,
                    ('Folding', 'PN-metabolism'): np.log2(9)*sizeScaleEdge + sizeShiftEdge, ('Folding', 'Protein synthesis'): np.log2(5)*sizeScaleEdge + sizeShiftEdge,
                    ('PN-signaling', 'PN-signaling'): np.log2(107)*sizeScaleEdge + sizeShiftEdge, ('PN-signaling', 'Trafficking'): np.log2(107)*sizeScaleEdge + sizeShiftEdge,
                    ('PN-metabolism', 'Trafficking'): np.log2(9)*sizeScaleEdge + sizeShiftEdge, ('PN-metabolism', 'PN-signaling'): np.log2(5)*sizeScaleEdge + sizeShiftEdge,
                    ('PN-metabolism', 'Protein synthesis'): np.log2(1)*sizeScaleEdge + sizeShiftEdge, # less that 1 will remove the edge!
                    ('PN-metabolism', 'PN-metabolism'): np.log2(15)*sizeScaleEdge + sizeShiftEdge,
                    ('Clearance', 'PN-signaling'): np.log2(279)*sizeScaleEdge + sizeShiftEdge}

    if LevelOfPlot == 'L3':
        # Dict with node coordinates (2 different layouts)

        scaleFactor = 1
        Node_coordinates_kk = {'HSP70': (0.549106097 * scaleFactor, 0.508699501 * scaleFactor),
                               'TPR': (-0.385391578 * scaleFactor, 0.336751962 * scaleFactor),
                               'sHSP': (0.537861181 * scaleFactor, 1.152749631 * scaleFactor),
                               'HSP100': (0.457229181 * scaleFactor, -0.696813360 * scaleFactor),
                               'HSP40': (-0.270951306 * scaleFactor, 1.277369321 * scaleFactor),
                               'ER': (0.987839259 * scaleFactor, 0.078540297 * scaleFactor),
                               'MITO': (-1.062533012 * scaleFactor, -0.558359667 * scaleFactor),
                               'PFD': (-1.516060869 * scaleFactor, 0.727729883 * scaleFactor),
                               'HSP60': (0.933374477 * scaleFactor, -1.710523361 * scaleFactor),
                               'HSP90': (-0.005235842 * scaleFactor, -0.007823429 * scaleFactor)}

        # Dict wih node sizes
        sizeShift=5
        Node_size = { "HSP100" : 1 + sizeShift , "HSP90" : 18 + sizeShift , "TPR" : 43 + sizeShift ,
                      "sHSP" : 15 + sizeShift , "MITO" : 2 + sizeShift , "ER" : 13 + sizeShift ,
                      "HSP70" : 14 + sizeShift , "HSP40" : 8 + sizeShift , "HSP60" : 10 + sizeShift ,
                      "PFD" : 4 + sizeShift }

        sizeShiftEdge = 2
        Edge_dic = {('ER', 'sHSP'): 1, ('HSP90', 'TPR'): 27, ('HSP40', 'HSP90'): 2,
                    ('HSP70', 'sHSP'): 7, ('HSP100', 'HSP90'): 1, ('MITO', 'TPR'): 1,
                    ('ER', 'TPR'): 5, ('ER', 'HSP70'): 2, ('HSP100', 'HSP70'): 3,
                    ('HSP100', 'TPR'): 2, ('HSP100', 'HSP60'): 1, ('PFD', 'TPR'): 5,
                    ('ER', 'HSP90'): 1, ('HSP90', 'MITO'): 1, ('TPR', 'sHSP'): 9,
                    ('HSP40', 'TPR'): 2, ('HSP40', 'sHSP'): 1, ('HSP70', 'TPR'): 18,
                    ('HSP70', 'HSP90'): 4, ('ER', 'HSP100'): 1, ('HSP40', 'HSP70'): 13,
                    ('HSP90', 'sHSP'): 4}

    #Importing M-scores from database:
    if 'fromTCGA' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','SolidTissueNormal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','PrimarysolidTumor'))
        # PlotingA = 'Healthy'
        plotTitel = UnCamelCaser(whatToPlot.replace('fromTCGA',''))
    elif 'fromNeuro' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','Normal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','NeuroDegenerated'))
        plotTitel = UnCamelCaser(whatToPlot.replace('fromNeuro',''))
    else:
        raise ValueError('A problem with finding ' + whatToPlot + ' in database!')

    G = Graph()# Creation of empty graph
    # Choosing which layout to use
    Node_coordinates = Node_coordinates_kk                      # Kamada and Kawai layout
    #Node_coordinates = Node_coordinates_fr                     # Fruchterman and Reingold layout

    # Add nodes to the graph with position and size attributes
    for node in list( Node_coordinates.keys() ) :
        G.add_node( node , pos = Node_coordinates[node] , size = Node_size[node] * 2)

    # Add edges to the graph with weight attribute (nb of edges between two nodes)
    for edge in list( Edge_dic.keys() ) :
        G.add_edge( edge[0] , edge[1] , weight = Edge_dic[edge] )

    # Extraction of positions for drawing
    pos = get_node_attributes( G , 'pos' )

    # Creation of positions of node labels (take node position and move the coordinates )
    label_pos = {}
    for key in list(pos.keys()):
        label_pos[key] = ( pos[key][0] , pos[key][1] + 0.2 )

    # Extraction of edge width for drawing(Old ver.)
    weights = [G[u][v]['weight'] for u,v in G.edges()]

    # Extraction of node size(Old ver.)
    size = [ G.node[u]['size'] for u in G.nodes()]
    # Function for adding edges:
    def edge_tracer_adder(G):
        edge_tracer_outi = []
        for edge in G.edges():
            x0, y0 = G.node[edge[0]]['pos']
            x1, y1 = G.node[edge[1]]['pos']
            edge_trace_instant = Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=Line(width=G[edge[0]][edge[1]]['weight'],color='#888'),
                hoverinfo='none',
                mode='lines')
            edge_tracer_outi.append(edge_trace_instant)
        return edge_tracer_outi

    all_edge_traced = edge_tracer_adder(G) #Adding the edges

    # Initializing the 2D plot skeleton:
    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        textposition='middle left',
        textfont=dict(
            size=18
        ),
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='[[0, rgb(0,0,255,1), [1, rgb(255,0,0,1)]]',
            reversescale=False,
            cmin=-2,
            cmax=2,
            color=[],
            size=[],
            opacity=1,
            colorbar=dict(
                thickness=10,
                title='Node Connections',
                xanchor='left',
                titleside='right',
                len=0.1,
                x=1.02,
                y=1,
            ),
            line=dict(width=2)))
    # adding node values to the plot
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
    # adding edge values to the plot
    for node,nUm in zip(G.nodes(),range(len(G.nodes()))):
        node_trace['marker']['color'].append(plotObjTumor[node]-plotObjNormal[node])
        node_trace['marker']['size'].append(G.node[node]['size'])
        node_trace['text'].append(node)

    all_edge_traced.append(node_trace)

    # Finally making the 2D graph:
    fig = Figure(data=Data(all_edge_traced),
                 layout=Layout(
                    title=plotTitel,
                    titlefont=dict(size=24),
                    showlegend=False,
                    hovermode='closest',
                    #margin=dict(b=20,l=5,r=5,t=40),
                    # width= 1100,
                    # height= 1000,
                    # width= 1000, # Used this for exportting for compendium for paper, -> just remember to use chrome, print as pdf, page size A4
                    # height= 900, # Used this for exportting for compendium for paper, -> just remember to use chrome, print as pdf, page size A4
                    # annotations=[ dict(
                    #     text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    #     showarrow=False,
                    #     xref="paper", yref="paper",
                    #     x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=True, zeroline=True, showticklabels=True, range=[-2.7,2.2,1], autorange= False),
                    yaxis=YAxis(showgrid=True, zeroline=True, showticklabels=True, range=[-2.7,2.2,1], autorange= False)))

    plotHTML = PLOTT(fig, auto_open=False, output_type='div')
    # plotHTML = plotHTML.replace('<div>','<div style="width: 50%; margin: 0 auto;">') # Having the heatmap in the middle of iFrame
    plotHTML = plotHTML.replace('Export to plot.ly','')
    return HttpResponse(plotHTML)

# Functions making the polar plots:
def ActualPolarPlotter(request,LevelOfPlot,whatToPlot):

    if not request.user.is_authenticated(): # Check authentication!
        return HttpResponseRedirect('/login/')

    import numpy as np
    import plotly.offline as py
    import plotly.graph_objs as go
    from PolarPlotterFuncs import meiScale, getX, getY, makePolarBG, makeCloud

    #Importing M-scores from database:
    if 'fromTCGA' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','SolidTissueNormal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromTCGA','PrimarysolidTumor'))
        # PlotingA = 'Healthy'
        plotTitel = UnCamelCaser(whatToPlot.replace('fromTCGA',''))
    elif 'fromNeuro' in whatToPlot:
        plotObjNormal = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','Normal'))
        plotObjTumor = Plot.objects.get(title__icontains=whatToPlot.replace('fromNeuro','NeuroDegenerated'))
        plotTitel = UnCamelCaser(whatToPlot.replace('fromNeuro',''))
    else:
        raise ValueError('A problem with finding ' + whatToPlot + ' in database!')

    if LevelOfPlot == "L1":

        numberOfAxises = 6
        plotRange = 10
        numOfCircles = 5

        HealthyMeanValues = np.array([plotObjNormal.folding, plotObjNormal.synthesis, plotObjNormal.clearance,
                                      plotObjNormal.trafficking,plotObjNormal.signaling,plotObjNormal.metabolism])
        HealthyMinValues = np.array([plotObjNormal.foldingMin, plotObjNormal.synthesisMin, plotObjNormal.clearanceMin,
                                      plotObjNormal.traffickingMin,plotObjNormal.signalingMin,plotObjNormal.metabolismMin])
        HealthyMaxValues = np.array([plotObjNormal.foldingMax, plotObjNormal.synthesisMax, plotObjNormal.clearanceMax,
                                      plotObjNormal.traffickingMax,plotObjNormal.signalingMax,plotObjNormal.metabolismMax])

        CancerMeanValues = np.array([plotObjTumor.folding, plotObjTumor.synthesis, plotObjTumor.clearance,
                                      plotObjTumor.trafficking,plotObjTumor.signaling,plotObjTumor.metabolism])
        CancerMinValues = np.array([plotObjTumor.foldingMin, plotObjTumor.synthesisMin, plotObjTumor.clearanceMin,
                                      plotObjTumor.traffickingMin,plotObjTumor.signalingMin,plotObjTumor.metabolismMin])
        CancerMaxValues = np.array([plotObjTumor.foldingMax, plotObjTumor.synthesisMax, plotObjTumor.clearanceMax,
                                      plotObjTumor.traffickingMax,plotObjTumor.signalingMax,plotObjTumor.metabolismMax])

        ### These values are used for having fix values for making plots for paper:
        # axisMin = -34
        # axisMaxTmp = 28
        axisMin = np.floor(np.min([np.min(HealthyMeanValues),np.min(HealthyMaxValues),np.min(HealthyMinValues),
                                   np.min(CancerMeanValues),np.min(CancerMaxValues),np.min(CancerMinValues)]))
        axisMaxTmp = np.ceil(np.max([np.max(HealthyMeanValues),np.max(HealthyMaxValues),np.max(HealthyMinValues),
                                   np.max(CancerMeanValues),np.max(CancerMaxValues),np.max(CancerMinValues)]))
        axisMax = (np.floor_divide(axisMaxTmp-axisMin,plotRange) + 1) * plotRange + axisMin
        axisTicks = np.linspace(axisMin,axisMax,num=numOfCircles+1)

        HealthyMeanValuesScaled = meiScale(HealthyMeanValues,axisMin,axisMax,plotRange)
        HealthyMinValuesScaled = meiScale(HealthyMinValues,axisMin,axisMax,plotRange)
        HealthyMaxValuesScaled = meiScale(HealthyMaxValues,axisMin,axisMax,plotRange)

        HealthyMeanValuesScaledX = getX(HealthyMeanValuesScaled,numberOfAxises)
        HealthyMeanValuesScaledY = getY(HealthyMeanValuesScaled,numberOfAxises)
        HealthyMinValuesScaledX = getX(HealthyMinValuesScaled,numberOfAxises)
        HealthyMinValuesScaledY = getY(HealthyMinValuesScaled,numberOfAxises)
        HealthyMaxValuesScaledX = getX(HealthyMaxValuesScaled,numberOfAxises)
        HealthyMaxValuesScaledY = getY(HealthyMaxValuesScaled,numberOfAxises)

        CancerMeanValuesScaled = meiScale(CancerMeanValues,axisMin,axisMax,plotRange)
        CancerMinValuesScaled = meiScale(CancerMinValues,axisMin,axisMax,plotRange)
        CancerMaxValuesScaled = meiScale(CancerMaxValues,axisMin,axisMax,plotRange)

        CancerMeanValuesScaledX = getX(CancerMeanValuesScaled,numberOfAxises)
        CancerMeanValuesScaledY = getY(CancerMeanValuesScaled,numberOfAxises)
        CancerMinValuesScaledX = getX(CancerMinValuesScaled,numberOfAxises)
        CancerMinValuesScaledY = getY(CancerMinValuesScaled,numberOfAxises)
        CancerMaxValuesScaledX = getX(CancerMaxValuesScaled,numberOfAxises)
        CancerMaxValuesScaledY = getY(CancerMaxValuesScaled,numberOfAxises)

        trace0 = go.Scatter(
            x=np.append(HealthyMeanValuesScaledX,HealthyMeanValuesScaledX[0]),
            y=np.append(HealthyMeanValuesScaledY,HealthyMeanValuesScaledY[0]),
            hoverinfo='none',
            mode = 'lines+markers',
            line = dict(
                color = ('rgb(67, 113, 222)'),
                width = 4,
                # shape='spline',
            ),
            name="Normal Tissue",
        )
        trace1 = go.Scatter(
            x=np.append(CancerMeanValuesScaledX,CancerMeanValuesScaledX[0]),
            y=np.append(CancerMeanValuesScaledY,CancerMeanValuesScaledY[0]),
            hoverinfo='none',
            mode = 'lines+markers',
            line = dict(
                color = ('rgb(219, 15, 53)'),
                width = 4,
                # shape='spline',
            ),
            name="Ailing Tissue",
        )

        data = [trace0,trace1]

        bgWidth = 0.5
        bgColor = 'rgba(200, 200, 200, 1)'
        zeroCirclePos = np.divide(np.abs(np.float(axisMin)),np.float(axisMax)-np.float(axisMin)) * 10

        layout = go.Layout(
            showlegend='False',
            title=plotTitel,
            titlefont=dict(
                #family='Arial, sans-serif',
                size=30,
                #color='lightgrey'
            ),
            xaxis=go.XAxis(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
                range=[-11, 11],
            ),
            yaxis=go.YAxis(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
                range=[-11, 11],
            ),
            width= 900,
            height= 800,
            # width= 1000, # For plotting compendium for paper, actually this size here doesn't matter -> just remember to use chrome, print as pdf, page size A4
            # height= 900, # For plotting compendium for paper, actually this size here doesn't matter -> just remember to use chrome, print as pdf, page size A4
            shapes= [
                # making background circles
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -2,
                    'y0': -2,
                    'x1': 2,
                    'y1': 2,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                    },
                },
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -4,
                    'y0': -4,
                    'x1': 4,
                    'y1': 4,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                    },
                },
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -6,
                    'y0': -6,
                    'x1': 6,
                    'y1': 6,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                    },
                },
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -8,
                    'y0': -8,
                    'x1': 8,
                    'y1': 8,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                    },
                },
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -10,
                    'y0': -10,
                    'x1': 10,
                    'y1': 10,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                    },
                },
                # Zero circle:
                {
                    'type': 'circle',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': -zeroCirclePos,
                    'y0': -zeroCirclePos,
                    'x1': zeroCirclePos,
                    'y1': zeroCirclePos,
                    'line': {
                        'color': bgColor,
                        'width':1,
                    },
                },
                # # filled circle
                # # {
                # #     'type': 'circle',
                # #     'xref': 'x',
                # #     'yref': 'y',
                # #     'fillcolor': 'rgba(50, 171, 96, 0.7)',
                # #     'x0': 3,
                # #     'y0': 3,
                # #     'x1': 4,
                # #     'y1': 4,
                # #     'line': {
                # #         'color': 'rgba(50, 171, 96, 1)',
                # #     },
                # # },
                # making background lines for 6 groups
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 6*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 6*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 1*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 1*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 2*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 2*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 3*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 3*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 4*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 4*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 10*np.cos(np.pi/2 + 5*2*np.pi/6),
                    'y1': 10*np.sin(np.pi/2 + 5*2*np.pi/6),
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                # x-axis
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 11,
                    'y1': 0,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                # cloud
                {
                    'type': 'path',
                    'path': 'M ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[1]) +','+ np.array_str(HealthyMinValuesScaledY[1]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[2]) +','+ np.array_str(HealthyMinValuesScaledY[2]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[3]) +','+ np.array_str(HealthyMinValuesScaledY[3]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[4]) +','+ np.array_str(HealthyMinValuesScaledY[4]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[5]) +','+ np.array_str(HealthyMinValuesScaledY[5]) +
                            ' L ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[1]) +','+ np.array_str(HealthyMaxValuesScaledY[1]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[2]) +','+ np.array_str(HealthyMaxValuesScaledY[2]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[3]) +','+ np.array_str(HealthyMaxValuesScaledY[3]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[4]) +','+ np.array_str(HealthyMaxValuesScaledY[4]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[5]) +','+ np.array_str(HealthyMaxValuesScaledY[5]) +
                            ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                            'Z',
                    'fillcolor': 'rgba(67, 113, 222, 0.25)',
                    'line': {
                        'color': 'rgb(67, 113, 222)',
                        'width': 0,
                    },
                },
                {
                    'type': 'path',
                    'path': 'M ' + np.array_str(CancerMinValuesScaledX[0]) +','+ np.array_str(CancerMinValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[1]) +','+ np.array_str(CancerMinValuesScaledY[1]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[2]) +','+ np.array_str(CancerMinValuesScaledY[2]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[3]) +','+ np.array_str(CancerMinValuesScaledY[3]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[4]) +','+ np.array_str(CancerMinValuesScaledY[4]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[5]) +','+ np.array_str(CancerMinValuesScaledY[5]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[0]) +','+ np.array_str(CancerMinValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[0]) +','+ np.array_str(CancerMaxValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[1]) +','+ np.array_str(CancerMaxValuesScaledY[1]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[2]) +','+ np.array_str(CancerMaxValuesScaledY[2]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[3]) +','+ np.array_str(CancerMaxValuesScaledY[3]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[4]) +','+ np.array_str(CancerMaxValuesScaledY[4]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[5]) +','+ np.array_str(CancerMaxValuesScaledY[5]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[0]) +','+ np.array_str(CancerMaxValuesScaledY[0]) +
                            'Z',
                    'fillcolor': 'rgba(219, 15, 53, 0.25)',
                    'line': {
                        'color': 'rgb(219, 15, 53)',
                        'width': 0,
                    },
                },
            ],

            # Writing axis labels:
            annotations=go.Annotations([
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 6*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 6*2*np.pi/6),
                    showarrow=False,
                    text='Folding',
                    xref='x',
                    yref='y',
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                    textangle=180 - np.rad2deg(np.pi/2 + 6*2*np.pi/6) - 90, # 180 - because the direction of rotation of the text is clockwise (reverse of polar plot)
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 1*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 1*2*np.pi/6),
                    showarrow=False,
                    text='Protein Synthesis',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 1*2*np.pi/6) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 2*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 2*2*np.pi/6),
                    showarrow=False,
                    text='Clearance',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 2*2*np.pi/6) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 3*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 3*2*np.pi/6),
                    showarrow=False,
                    text='Trafficking',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 3*2*np.pi/6) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 4*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 4*2*np.pi/6),
                    showarrow=False,
                    text='Signaling',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 4*2*np.pi/6) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 5*2*np.pi/6),
                    y=11*np.sin(np.pi/2 + 5*2*np.pi/6),
                    showarrow=False,
                    text='PN Metabolism',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 5*2*np.pi/6) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                # x-axis annotation
                go.Annotation(
                    x=0 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[0].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=2 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[1].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=4 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[2].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=6 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[3].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=8 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[4].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=10 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[5].astype('int')),
                    xref='x',
                    yref='y',
                ),
                #Zero
                go.Annotation(
                    x=zeroCirclePos + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text='0',
                    xref='x',
                    yref='y',
                ),
            ]),
        )
        fig = go.Figure(data=data,layout=layout)
        # py.plot(fig)
        plotHTML = py.plot(fig, auto_open=False, output_type='div')
        plotHTML = plotHTML.replace('Export to plot.ly','')
        return HttpResponse(plotHTML)

    if LevelOfPlot == "L3":

        numberOfAxises = 10
        plotRange = 10
        numOfCircles = 5

        HealthyMeanValues = np.array([plotObjNormal.HSP90,plotObjNormal.HSP60,plotObjNormal.PFD,plotObjNormal.MITO,
                                      plotObjNormal.HSP100,plotObjNormal.TPR,plotObjNormal.HSP70,
                                      plotObjNormal.HSP40,plotObjNormal.ER,plotObjNormal.sHSP])
        HealthyMinValues = np.array([plotObjNormal.HSP90Min,plotObjNormal.HSP60Min,plotObjNormal.PFDMin,plotObjNormal.MITOMin,
                                      plotObjNormal.HSP100Min,plotObjNormal.TPRMin,plotObjNormal.HSP70Min,
                                      plotObjNormal.HSP40Min,plotObjNormal.ERMin,plotObjNormal.sHSPMin])
        HealthyMaxValues = np.array([plotObjNormal.HSP90Max,plotObjNormal.HSP60Max,plotObjNormal.PFDMax,plotObjNormal.MITOMax,
                                      plotObjNormal.HSP100Max,plotObjNormal.TPRMax,plotObjNormal.HSP70Max,
                                      plotObjNormal.HSP40Max,plotObjNormal.ERMax,plotObjNormal.sHSPMax])

        CancerMeanValues = np.array([plotObjTumor.HSP90,plotObjTumor.HSP60,plotObjTumor.PFD,plotObjTumor.MITO,
                                      plotObjTumor.HSP100,plotObjTumor.TPR,plotObjTumor.HSP70,
                                      plotObjTumor.HSP40,plotObjTumor.ER,plotObjTumor.sHSP])
        CancerMinValues = np.array([plotObjTumor.HSP90Min,plotObjTumor.HSP60Min,plotObjTumor.PFDMin,plotObjTumor.MITOMin,
                                      plotObjTumor.HSP100Min,plotObjTumor.TPRMin,plotObjTumor.HSP70Min,
                                      plotObjTumor.HSP40Min,plotObjTumor.ERMin,plotObjTumor.sHSPMin])
        CancerMaxValues = np.array([plotObjTumor.HSP90Max,plotObjTumor.HSP60Max,plotObjTumor.PFDMax,plotObjTumor.MITOMax,
                                      plotObjTumor.HSP100Max,plotObjTumor.TPRMax,plotObjTumor.HSP70Max,
                                      plotObjTumor.HSP40Max,plotObjTumor.ERMax,plotObjTumor.sHSPMax])

        axisMin = np.floor(np.min([np.min(HealthyMeanValues),np.min(HealthyMaxValues),np.min(HealthyMinValues),
                               np.min(CancerMeanValues),np.min(CancerMaxValues),np.min(CancerMinValues)]))
        axisMaxTmp = np.ceil(np.max([np.max(HealthyMeanValues),np.max(HealthyMaxValues),np.max(HealthyMinValues),
                                   np.max(CancerMeanValues),np.max(CancerMaxValues),np.max(CancerMinValues)]))


        # axisMin = -34
        # axisMaxTmp = 28
        axisMax = (np.floor_divide(axisMaxTmp-axisMin,plotRange) + 1) * plotRange + axisMin
        axisTicks = np.linspace(axisMin,axisMax,num=numOfCircles+1)


        HealthyMeanValuesScaled = meiScale(HealthyMeanValues,axisMin,axisMax,plotRange)
        HealthyMinValuesScaled = meiScale(HealthyMinValues,axisMin,axisMax,plotRange)
        HealthyMaxValuesScaled = meiScale(HealthyMaxValues,axisMin,axisMax,plotRange)

        HealthyMeanValuesScaledX = getX(HealthyMeanValuesScaled,numberOfAxises)
        HealthyMeanValuesScaledY = getY(HealthyMeanValuesScaled,numberOfAxises)
        HealthyMinValuesScaledX = getX(HealthyMinValuesScaled,numberOfAxises)
        HealthyMinValuesScaledY = getY(HealthyMinValuesScaled,numberOfAxises)
        HealthyMaxValuesScaledX = getX(HealthyMaxValuesScaled,numberOfAxises)
        HealthyMaxValuesScaledY = getY(HealthyMaxValuesScaled,numberOfAxises)

        CancerMeanValuesScaled = meiScale(CancerMeanValues,axisMin,axisMax,plotRange)
        CancerMinValuesScaled = meiScale(CancerMinValues,axisMin,axisMax,plotRange)
        CancerMaxValuesScaled = meiScale(CancerMaxValues,axisMin,axisMax,plotRange)

        CancerMeanValuesScaledX = getX(CancerMeanValuesScaled,numberOfAxises)
        CancerMeanValuesScaledY = getY(CancerMeanValuesScaled,numberOfAxises)
        CancerMinValuesScaledX = getX(CancerMinValuesScaled,numberOfAxises)
        CancerMinValuesScaledY = getY(CancerMinValuesScaled,numberOfAxises)
        CancerMaxValuesScaledX = getX(CancerMaxValuesScaled,numberOfAxises)
        CancerMaxValuesScaledY = getY(CancerMaxValuesScaled,numberOfAxises)

        trace0 = go.Scatter(
            x=np.append(HealthyMeanValuesScaledX,HealthyMeanValuesScaledX[0]),
            y=np.append(HealthyMeanValuesScaledY,HealthyMeanValuesScaledY[0]),
            hoverinfo='none',
            mode = 'lines+markers',
            line = dict(
                color = ('rgb(67, 113, 222)'),
                width = 4,
                # shape='spline',
            ),
            name="Normal Tissue",
        )
        trace1 = go.Scatter(
            x=np.append(CancerMeanValuesScaledX,CancerMeanValuesScaledX[0]),
            y=np.append(CancerMeanValuesScaledY,CancerMeanValuesScaledY[0]),
            hoverinfo='none',
            mode = 'lines+markers',
            line = dict(
                color = ('rgb(219, 15, 53)'),
                width = 4,
                # shape='spline',
            ),
            name="Ailing Tissue",
        )
        data = [trace0,trace1]


        bgWidth = 0.5
        bgColor = 'rgba(200, 200, 200, 1)'
        zeroCirclePos = np.divide(np.abs(np.float(axisMin)),np.float(axisMax)-np.float(axisMin)) * 10

        layout = go.Layout(
            showlegend='False',
            title=plotTitel,
            titlefont=dict(
                #family='Arial, sans-serif',
                size=30,
                #color='lightgrey'
            ),
            xaxis=go.XAxis(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
                range=[-11, 11],
            ),
            yaxis=go.YAxis(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=False,
                range=[-11, 11],
            ),
            width= 900,
            height= 800,
            shapes= makePolarBG(plotRange,numOfCircles,numberOfAxises,bgColor,bgWidth,1,zeroCirclePos) +
                    makeCloud(HealthyMinValuesScaledX,HealthyMinValuesScaledY,'rgba(67, 113, 222)') +
                    [
                        {'type': 'path',
                        'path': 'M ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[1]) +','+ np.array_str(HealthyMinValuesScaledY[1]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[2]) +','+ np.array_str(HealthyMinValuesScaledY[2]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[3]) +','+ np.array_str(HealthyMinValuesScaledY[3]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[4]) +','+ np.array_str(HealthyMinValuesScaledY[4]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[5]) +','+ np.array_str(HealthyMinValuesScaledY[5]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[6]) +','+ np.array_str(HealthyMinValuesScaledY[6]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[7]) +','+ np.array_str(HealthyMinValuesScaledY[7]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[8]) +','+ np.array_str(HealthyMinValuesScaledY[8]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[9]) +','+ np.array_str(HealthyMinValuesScaledY[9]) +
                                ' L ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[1]) +','+ np.array_str(HealthyMaxValuesScaledY[1]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[2]) +','+ np.array_str(HealthyMaxValuesScaledY[2]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[3]) +','+ np.array_str(HealthyMaxValuesScaledY[3]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[4]) +','+ np.array_str(HealthyMaxValuesScaledY[4]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[5]) +','+ np.array_str(HealthyMaxValuesScaledY[5]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[6]) +','+ np.array_str(HealthyMaxValuesScaledY[6]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[7]) +','+ np.array_str(HealthyMaxValuesScaledY[7]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[8]) +','+ np.array_str(HealthyMaxValuesScaledY[8]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[9]) +','+ np.array_str(HealthyMaxValuesScaledY[9]) +
                                ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                                'Z',
                        'fillcolor': 'rgba(67, 113, 222, 0.25)',
                        'line': {
                            'color': 'rgb(67, 113, 222)',
                            'width': 0,
                        },
                    }] +
                    [
                # x-axis
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': 11,
                    'y1': 0,
                    'line': {
                        'color': bgColor,
                        'width':bgWidth,
                        # 'dash': 'dot',
                    },
                },
                # cloud
                # {
                #     'type': 'path',
                #     'path': 'M ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[1]) +','+ np.array_str(HealthyMinValuesScaledY[1]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[2]) +','+ np.array_str(HealthyMinValuesScaledY[2]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[3]) +','+ np.array_str(HealthyMinValuesScaledY[3]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[4]) +','+ np.array_str(HealthyMinValuesScaledY[4]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[5]) +','+ np.array_str(HealthyMinValuesScaledY[5]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[6]) +','+ np.array_str(HealthyMinValuesScaledY[6]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[7]) +','+ np.array_str(HealthyMinValuesScaledY[7]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[8]) +','+ np.array_str(HealthyMinValuesScaledY[8]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[9]) +','+ np.array_str(HealthyMinValuesScaledY[9]) +
                #             ' L ' + np.array_str(HealthyMinValuesScaledX[0]) +','+ np.array_str(HealthyMinValuesScaledY[0]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[1]) +','+ np.array_str(HealthyMaxValuesScaledY[1]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[2]) +','+ np.array_str(HealthyMaxValuesScaledY[2]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[3]) +','+ np.array_str(HealthyMaxValuesScaledY[3]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[4]) +','+ np.array_str(HealthyMaxValuesScaledY[4]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[5]) +','+ np.array_str(HealthyMaxValuesScaledY[5]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[6]) +','+ np.array_str(HealthyMaxValuesScaledY[6]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[7]) +','+ np.array_str(HealthyMaxValuesScaledY[7]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[8]) +','+ np.array_str(HealthyMaxValuesScaledY[8]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[9]) +','+ np.array_str(HealthyMaxValuesScaledY[9]) +
                #             ' L ' + np.array_str(HealthyMaxValuesScaledX[0]) +','+ np.array_str(HealthyMaxValuesScaledY[0]) +
                #             'Z',
                #     'fillcolor': 'rgba(67, 113, 222, 0.25)',
                #     'line': {
                #         'color': 'rgb(67, 113, 222)',
                #         'width': 0,
                #     },
                # },
                {
                    'type': 'path',
                    'path': 'M ' + np.array_str(CancerMinValuesScaledX[0]) +','+ np.array_str(CancerMinValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[1]) +','+ np.array_str(CancerMinValuesScaledY[1]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[2]) +','+ np.array_str(CancerMinValuesScaledY[2]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[3]) +','+ np.array_str(CancerMinValuesScaledY[3]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[4]) +','+ np.array_str(CancerMinValuesScaledY[4]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[5]) +','+ np.array_str(CancerMinValuesScaledY[5]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[6]) +','+ np.array_str(CancerMinValuesScaledY[6]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[7]) +','+ np.array_str(CancerMinValuesScaledY[7]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[8]) +','+ np.array_str(CancerMinValuesScaledY[8]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[9]) +','+ np.array_str(CancerMinValuesScaledY[9]) +
                            ' L ' + np.array_str(CancerMinValuesScaledX[0]) +','+ np.array_str(CancerMinValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[0]) +','+ np.array_str(CancerMaxValuesScaledY[0]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[1]) +','+ np.array_str(CancerMaxValuesScaledY[1]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[2]) +','+ np.array_str(CancerMaxValuesScaledY[2]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[3]) +','+ np.array_str(CancerMaxValuesScaledY[3]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[4]) +','+ np.array_str(CancerMaxValuesScaledY[4]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[5]) +','+ np.array_str(CancerMaxValuesScaledY[5]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[6]) +','+ np.array_str(CancerMaxValuesScaledY[6]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[7]) +','+ np.array_str(CancerMaxValuesScaledY[7]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[8]) +','+ np.array_str(CancerMaxValuesScaledY[8]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[9]) +','+ np.array_str(CancerMaxValuesScaledY[9]) +
                            ' L ' + np.array_str(CancerMaxValuesScaledX[0]) +','+ np.array_str(CancerMaxValuesScaledY[0]) +
                            'Z',
                    'fillcolor': 'rgba(219, 15, 53, 0.25)',
                    'line': {
                        'color': 'rgb(219, 15, 53)',
                        'width': 0,
                    },
                },
            ],

            # Writing axis labels:
            annotations=go.Annotations([
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 10*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 10*2*np.pi/10),
                    showarrow=False,
                    text='HSP90',
                    xref='x',
                    yref='y',
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                    textangle=180 - np.rad2deg(np.pi/2 + 10*2*np.pi/10) - 90, # 180 - because the direction of rotation of the text is clockwise (reverse of polar plot)
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 1*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 1*2*np.pi/10),
                    showarrow=False,
                    text='HSP60',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 1*2*np.pi/10) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 2*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 2*2*np.pi/10),
                    showarrow=False,
                    text='PFD',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 2*2*np.pi/10) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 3*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 3*2*np.pi/10),
                    showarrow=False,
                    text='MITO',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 3*2*np.pi/10) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 4*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 4*2*np.pi/10),
                    showarrow=False,
                    text='HSP100',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 4*2*np.pi/10) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 5*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 5*2*np.pi/10),
                    showarrow=False,
                    text='TPR',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 5*2*np.pi/10) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 6*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 6*2*np.pi/10),
                    showarrow=False,
                    text='HSP70',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 6*2*np.pi/10) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 7*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 7*2*np.pi/10),
                    showarrow=False,
                    text='HSP40',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 7*2*np.pi/10) + 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 8*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 8*2*np.pi/10),
                    showarrow=False,
                    text='ER',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 8*2*np.pi/10) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                go.Annotation(
                    x=11*np.cos(np.pi/2 + 9*2*np.pi/10),
                    y=11*np.sin(np.pi/2 + 9*2*np.pi/10),
                    showarrow=False,
                    text='sHSP',
                    xref='x',
                    yref='y',
                    textangle=180 - np.rad2deg(np.pi/2 + 9*2*np.pi/10) - 90,
                    font=dict(
                    #     family='sans serif',
                        size=18,
                    #     color='#1f77b4',
                    ),
                ),
                # x-axis annotation
                go.Annotation(
                    x=0 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[0].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=2 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[1].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=4 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[2].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=6 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[3].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=8 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[4].astype('int')),
                    xref='x',
                    yref='y',
                ),
                go.Annotation(
                    x=10 + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text=np.array_str(axisTicks[5].astype('int')),
                    xref='x',
                    yref='y',
                ),
                #Zero
                go.Annotation(
                    x=zeroCirclePos + 0.25,
                    y=0 - 0.25,
                    showarrow=False,
                    text='0',
                    xref='x',
                    yref='y',
                ),
            ]),
        )
        fig = go.Figure(data=data,layout=layout)
        # py.plot(fig)fig = go.Figure(data=data,layout=layout)
        # py.plot(fig)
        plotHTML = py.plot(fig, auto_open=False, output_type='div')
        # plotHTML = plotHTML.replace('<div>','<div style="width: 50%; margin: 0 auto;">') # Having the heatmap in the middle of iFrame
        plotHTML = plotHTML.replace('Export to plot.ly','')
        return HttpResponse(plotHTML)
