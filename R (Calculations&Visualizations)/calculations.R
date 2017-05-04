##18.4.2017: Calculating values for paper "A Systematic Atlas of Chaperome Deregulation Topologies Across the Human Cancer Landscape",
#http://biorxiv.org/content/early/2017/03/29/122044
## written by: Ali Hadizadeh Esfahani, esfahani@aices.rwth-aachen.de

source("./FUNCS.R")

#For making Figure 2 plots:
if (FALSE) {
  prepareStuffOuti <- prepareStuffTCGA()
  PNList <- "CHAPL2EntrezID"
  #Doing GSA on TCGA for Chaperome groups:
  gsaRevTableScores <-
    gsaReviewWrapperAll(
      gexMat = prepareStuffOuti$gexMat,
      grup1 = prepareStuffOuti$grup1,
      grup2 = prepareStuffOuti$grup2,
      PNList = prepareStuffOuti[[PNList]],
      diseaseLevels = prepareStuffOuti$diseaseLevels,
      mode = "score",
      SEED = 0
    )
  #Cancer names abbrevating:
  rownames(gsaRevTableScores) <-
    sapply(strsplit(rownames(gsaRevTableScores), split = ", "), function(x)
      x[2])
  rownames(gsaRevTableScores)[5] <-
    "Esophageal carcinoma" #except "Esophageal carcinoma ", weird error from TissueSourceSite file downloaded from TCGA
  TCGAAbbrevConv <-
    read.csv("./TCGANamesAbbrevConvTable.csv",
             sep = ";",
             header = F)
  rownames(gsaRevTableScores) <-
    TCGAAbbrevConv$V1[match(rownames(gsaRevTableScores), TCGAAbbrevConv$V2)]
  
  #Plotting:
  pdf(file = "./Results/Fig2_TCGAGsaRevTableScoresL3HeatmapChapFinalVersionForPaper.pdf",
      width = 10,
      height = 10)
  require(gplots)
  heatTmp <-
    heatmap.2(
      x = gsaRevTableScores,
      col = colorRampPalette(c("blue", "white", "red"))(n = 100),
      Rowv = T,
      Colv = T,
      trace = "none",
      key.title = NA,
      keysize = 1,
      cexCol = 1,
      cexRow = 1,
      srtCol = 45,
      key.par = list(cex = 0.8),
      margins = c(5, 28),
      colsep = 1:ncol(gsaRevTableScores),
      rowsep = 1:nrow(gsaRevTableScores),
      sepcolor = "black",
      sepwidth = c(0.01, 0.01),
      main = "Chaperome Analysis of TCGA using GSA",
      distfun = function(x)
        dist(x, method = "euclidean")
    )
  dev.off()
  
  #Save heatmap(in Order) for WEbtool and other stuff:
  write.csv(x = gsaRevTableScores[heatTmp$rowInd, heatTmp$colInd],
            file = "./Results/Fig2_TCGAGsaRevTableScoresL3HeatmapChapFinalVersionForPaper.csv")
  
  #Doing for Chaperome as a whole (vs. everything else):
  PNList <- "PNL1EntrezID"
  
  gsaRevTableScores100 <-
    gsaReviewEqualRamdomized(
      prepareStuffOuti$gexMat,
      prepareStuffOuti$grup1,
      prepareStuffOuti$grup2,
      prepareStuffOuti[[PNList]],
      prepareStuffOuti$diseaseLevels,
      SEED = 72,
      repetations = 100
    ) # This may take some time!
  # gsaRevTableScores100 <- readRDS("gsaRevTableScores100.rds")
  gsaChaperomeReview <- gsaReviewEqualRamdomizedSummarizer(gsaReviewEqualRamdomizedOutput = gsaRevTableScores100)
  
  #Cancer names abbrevating:
  rownames(gsaChaperomeReview) <-
    sapply(strsplit(rownames(gsaChaperomeReview), split = ", "), function(x)
      x[2])
  rownames(gsaChaperomeReview)[5] <-
    "Esophageal carcinoma" #except "Esophageal carcinoma ", weird error from TissueSourceSite file downloaded from TCGA
  TCGAAbbrevConv <-
    read.csv("./TCGANamesAbbrevConvTable.csv",
             sep = ";",
             header = F)
  rownames(gsaChaperomeReview) <-
    TCGAAbbrevConv$V1[match(rownames(gsaChaperomeReview), TCGAAbbrevConv$V2)]
  
  #Plotting just Chaperome:
  pdf(file = "./Results/Fig2_TCGAGsaRevTableScoresL1HeatmapOnlyChaperomeFinalVersionForPaper.pdf",
      width = 10,
      height = 10)
  require(gplots)
  heatTmp2 <-
    heatmap.2(
      x = gsaChaperomeReview[rev(heatTmp$rowInd),],
      col = colorRampPalette(c("blue", "white", "red"))(n = 100),
      Rowv = F,
      Colv = F,
      trace = "none",
      key.title = NA,
      keysize = 1,
      cexCol = 1,
      cexRow = 1,
      srtCol = 45,
      key.par = list(cex = 0.8),
      margins = c(5, 44),
      colsep = NULL,
      rowsep = 1:nrow(gsaChaperomeReview),
      sepcolor = rgb(0,0,0,1,maxColorValue = 1),
      sepwidth = c(0.01, 0.01),
      main = "Chaperome Analysis of TCGA using GSA",
      #labCol="Chaperome",
      distfun = function(x)
        dist(x, method = "euclidean")
    )
  dev.off()
  
  #Save heatmap(in Order) for WEbtool and other stuff:
  write.csv(x = gsaChaperomeReview,
            file = "./Results/Fig2_TCGAGsaRevTableScoresL1HeatmapOnlyChaperomeFinalVersionForPaper.csv")
}

# For figure 3 (& ...): copied from quantForPaper.R
if (FALSE) {
  PNs <- readRDS(file = "./PNs.rds")
  prepareStuffOuti <- prepareStuffTCGA()
  PNList <- "CHAPL2EntrezID"
  names(PNs)[5:6] <- c("Type","ATP.dependence")
  PNs$ATP.dependence[PNs$Type == "CO-CHAP"] <- NA
  
  require(limma)
  LiMmaOutputs <- list()
  for (K in 1:length(prepareStuffOuti$grup1)) {
    GLUPH <- prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup1[K]
    GLUPC <-
      prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup2[K]
    
    dEannots <-
      as.factor(c(rep("Normal", sum(GLUPH)), rep("Tumor", sum(GLUPC))))
    
    onlyChapGenes <-
      match(PNs$EntrezID,
            rownames(prepareStuffOuti$gexMat),
            nomatch = 0)
    
    subMat <-
      cbind(prepareStuffOuti$gexMat[onlyChapGenes, GLUPH], prepareStuffOuti$gexMat[onlyChapGenes, GLUPC])
    
    design <- model.matrix( ~ 0 + as.factor(dEannots))
    colnames(design) <- c("Normal", "Tumor")
    
    fit <- lmFit(subMat, design)
    fitC <-
      contrasts.fit(fit, makeContrasts(Tumor - Normal, levels = design))
    
    #fit2 <- eBayes(fit)
    #output <- topTable(fit2, coef = 2)
    fit2 <- eBayes(fitC)
    output <- topTable(fit2, number = Inf)
    ## or
    # fit2 <- treat(fit)
    # output <- topTreat(fit2, coef = 2)
    LiMmaOutputs[[substr(
      x = prepareStuffOuti$grup1[K],
      start = 22,
      stop = nchar(prepareStuffOuti$grup1[K])
    )]] <- output
  }
  
  forBarPlot <- list()
  forParCoord <- matrix(NA, nrow = length(LiMmaOutputs), ncol = 8)
  rownames(forParCoord) <- names(LiMmaOutputs)
  colnames(forParCoord) <-
    c(
      "UP_ATP_Dep",
      "UP_ATP_Indie",
      "UP_Chap",
      "UP_CoChap",
      "DN_ATP_Dep",
      "DN_ATP_Indie",
      "DN_Chap",
      "DN_CoChap"
    )
  ATPFisher <- numeric(length = length(LiMmaOutputs)) * NA
  names(ATPFisher) <- names(LiMmaOutputs)
  CHAPFisher <- numeric(length = length(LiMmaOutputs)) * NA
  names(CHAPFisher) <- names(LiMmaOutputs)
  for (K in 1:length(LiMmaOutputs)) {
    upGenes <-
      rownames(LiMmaOutputs[[K]])[LiMmaOutputs[[K]]$adj.P.Val < 0.05 &
                                    LiMmaOutputs[[K]]$logFC > 0]
    dnGenes <-
      rownames(LiMmaOutputs[[K]])[LiMmaOutputs[[K]]$adj.P.Val < 0.05 &
                                    LiMmaOutputs[[K]]$logFC < 0]
    upGenesAnnot <-
      PNs$ATP.dependence[match(upGenes, PNs$EntrezID, nomatch = 0)]
    dnGenesAnnot <-
      PNs$ATP.dependence[match(dnGenes, PNs$EntrezID, nomatch = 0)]
    forBarPlot[[names(LiMmaOutputs)[K]]] <-
      matrix(NA,
             nrow = 2,
             ncol = 2,
             dimnames = list(c("DOWN", "UP"), c("ATP_indie", "ATP_dep")))
    forBarPlot[[names(LiMmaOutputs)[K]]][1, ] <- table(dnGenesAnnot)
    forBarPlot[[names(LiMmaOutputs)[K]]][2, ] <- table(upGenesAnnot)
    forBarPlot[[K]][, 2] <-
      forBarPlot[[K]][, 2] * 38 / 50 # normalize for different groups sizes
    ATPFisher[K] <-
      fisher.test(x = forBarPlot[[names(LiMmaOutputs)[K]]], alternative = "two.sided")$p.value
    forParCoord[K, c(6, 2, 5, 1)] <-
      c(forBarPlot[[K]]) / sum(forBarPlot[[K]])
    pdf(file = paste0("./Results/ATPLimmaGroupwiseNormed/",names(LiMmaOutputs)[K],".pdf"))
    barplot(
      forBarPlot[[names(LiMmaOutputs)[K]]],
      beside = T,
      legend.text = rownames(forBarPlot[[names(LiMmaOutputs)[K]]]),
      main = names(LiMmaOutputs)[K]
    )
    dev.off()
  }
  forBarPlot <- list()
  for (K in 1:length(LiMmaOutputs)) {
    upGenes <-
      rownames(LiMmaOutputs[[K]])[LiMmaOutputs[[K]]$adj.P.Val < 0.05 &
                                    LiMmaOutputs[[K]]$logFC > 0]
    dnGenes <-
      rownames(LiMmaOutputs[[K]])[LiMmaOutputs[[K]]$adj.P.Val < 0.05 &
                                    LiMmaOutputs[[K]]$logFC < 0]
    upGenesAnnot <-
      PNs$Type[match(upGenes, PNs$EntrezID, nomatch = 0)]
    dnGenesAnnot <-
      PNs$Type[match(dnGenes, PNs$EntrezID, nomatch = 0)]
    forBarPlot[[names(LiMmaOutputs)[K]]] <-
      matrix(NA,
             nrow = 2,
             ncol = 2,
             dimnames = list(c("DOWN", "UP"), c("CHAP", "CO_CHAP")))
    forBarPlot[[names(LiMmaOutputs)[K]]][1, ] <- table(dnGenesAnnot)
    forBarPlot[[names(LiMmaOutputs)[K]]][2, ] <- table(upGenesAnnot)
    forBarPlot[[K]][, 1] <-
      forBarPlot[[K]][, 1] * 244 / 88 # normalize for different groups sizes
    CHAPFisher[K] <-
      fisher.test(x = forBarPlot[[names(LiMmaOutputs)[K]]], alternative = "two.sided")$p.value
    forParCoord[K, c(7, 3, 8, 4)] <-
      c(forBarPlot[[K]]) / sum(forBarPlot[[K]])
    pdf(file = paste0("./Results/CHAPLimmaGroupwiseNormed/",names(LiMmaOutputs)[K],".pdf"))
    barplot(
      forBarPlot[[names(LiMmaOutputs)[K]]],
      beside = T,
      legend.text = rownames(forBarPlot[[names(LiMmaOutputs)[K]]]),
      main = names(LiMmaOutputs)[K]
    )
    dev.off()
  }
  
  # write.csv(x = cbind(ATPFisher,CHAPFisher),file = "./FisherTwoSidedResults.csv")
  
  forParCoord <-
    forParCoord[-c(14, 17, 18, 21), ] # Removing cancers which didn't have enough differentially expressed genes
  nameConvTabelle <-
    read.csv(file = "./TCGANamesAbbrevConvTable.csv",
             sep = ";",
             header = F)
  InDxEs <- match(rownames(forParCoord), nameConvTabelle$V2)
  InDxEs[5] <- 9
  rownames(forParCoord) <- nameConvTabelle$V1[InDxEs]
  
  forParCoordTmp <- forParCoord
  
  forParCoord <- forParCoordTmp[, c(1, 5, 2, 6)] #ATP related ones
  require(scatterplot3d)
  rbPal <- colorRampPalette(c('blue', 'red'))
  xAxis <- 2
  yAxis <- 4
  zAxis <- 3
  CoLoR <- 1
  rbCol <-
    rbPal(100)[as.numeric(cut(forParCoord[, CoLoR], breaks = 100))]
  pdf(file = "./Results/Fig3_3DScatterIdeaPlot1ATP.pdf")
  s3d <-
    scatterplot3d(
      forParCoord[, xAxis],
      forParCoord[, yAxis],
      forParCoord[, zAxis],
      pch = 16,
      type = "p",
      angle = 45,
      color = rbCol,
      xlab = colnames(forParCoord)[xAxis],
      ylab = colnames(forParCoord)[yAxis],
      zlab = colnames(forParCoord)[zAxis],
      main = colnames(forParCoord)[CoLoR],
      cex.symbols = 2,
      box = T,
      grid = T,
      xlim = c(0, 0.5),
      ylim = c(0, 0.5),
      zlim = c(0, 0.5)
    )
  text(
    s3d$xyz.convert(forParCoord[, xAxis], forParCoord[, yAxis], forParCoord[, zAxis]),
    labels = rownames(forParCoord),
    pos = 1,
    cex = 0.5
  )
  dev.off()
  ###Make a color legend here:
  pdf(file = "./Results/Fig3_3DScatterIdeaPlot1ATPColorLegend.pdf",width = 6,height = 6)
  image(
    x = 1:100,
    y = c(1),
    z = matrix(1:100, nrow = 100),
    col = rbPal(100),
    xaxt = "n",
    yaxt = "n",
    xlab = "",
    ylab = "",
    main = "Color legend"
  )
  axis(1,
       at = as.numeric(cut(forParCoord[, CoLoR], breaks = 100)),
       labels = round(forParCoord[, CoLoR], digits = 2))
  dev.off()
  ############################
  
  # Doing a two-overlayed boxplots:
  CancerGroup2 <- c(8, 9, 10, 14, 17)
  pdf(file = "./Results/Fig3_OverlayedBoxPlotsATP.pdf")
  boxplot(
    list(
      "UP_ATP_Dep" = forParCoord[-CancerGroup2, 1],
      "DN_ATP_Dep" = forParCoord[-CancerGroup2, 2],
      "UP_ATP_Indie" = forParCoord[-CancerGroup2, 3],
      "DN_ATP_Indie" = forParCoord[-CancerGroup2, 4]
    ),
    col = "red"
  )
  boxplot(
    list(forParCoord[CancerGroup2, 1], forParCoord[CancerGroup2, 2], forParCoord[CancerGroup2, 3], forParCoord[CancerGroup2, 4]),
    add = T,
    col = "steelblue1",
    xaxt = "n"
  )
  dev.off()
  
  #Cluster according to ATP results and check validation:(for figure3)
  require(fpc)
  km.bootATP <- clusterboot(
    forParCoord,
    B = 1000,
    bootmethod = "boot",
    clustermethod = kmeansCBI,
    krange = 2,
    seed = 0
  )
  require(cluster)
  summary(silhouette(
    x = kmeans(x = forParCoord, centers = 2)$cluster,
    dist = dist(forParCoord)
  )) #Reported the median in paper
  
  
  #Same for Chap/CoChap:
  forParCoord <- forParCoordTmp[, c(3, 7, 4, 8)]#Chap/CoChap related ones
  require(scatterplot3d)
  rbPal <- colorRampPalette(c('blue', 'red'))
  xAxis <- 4
  yAxis <- 2
  zAxis <- 3
  CoLoR <- 1
  rbCol <-
    rbPal(100)[as.numeric(cut(forParCoord[, CoLoR], breaks = 100))]
  pdf(file = "./Results/Fig3_3DScatterIdeaPlot1CHAP.pdf")
  s3d <-
    scatterplot3d(
      forParCoord[, xAxis],
      forParCoord[, yAxis],
      forParCoord[, zAxis],
      pch = 16,
      type = "p",
      angle = 45,
      color = rbCol,
      xlab = colnames(forParCoord)[xAxis],
      ylab = colnames(forParCoord)[yAxis],
      zlab = colnames(forParCoord)[zAxis],
      main = colnames(forParCoord)[CoLoR],
      cex.symbols = 2,
      box = T,
      grid = T,
      xlim = c(0, 0.5),
      ylim = c(0, 0.5),
      zlim = c(0, 0.5)
    )
  text(
    s3d$xyz.convert(forParCoord[, xAxis], forParCoord[, yAxis], forParCoord[, zAxis]),
    labels = rownames(forParCoord),
    pos = 1,
    cex = 0.5
  )
  dev.off()
  ###Make a color legend here:
  pdf(file = "./Results/Fig3_3DScatterIdeaPlot1CHAPColorLegend.pdf",width = 6,height = 6)
  image(
    x = 1:100,
    y = c(1),
    z = matrix(1:100, nrow = 100),
    col = rbPal(100),
    xaxt = "n",
    yaxt = "n",
    xlab = "",
    ylab = "",
    main = "Color legend"
  )
  axis(1,
       at = as.numeric(cut(forParCoord[, CoLoR], breaks = 100)),
       labels = round(forParCoord[, CoLoR], digits = 2))
  dev.off()
  ############################
  
  # Doing a two-overlayed boxplots:
  pdf(file = "./Results/Fig3_OverlayedBoxPlotsCHAP.pdf")
  boxplot(
    list(
      "UP_CHAP" = forParCoord[-CancerGroup2, 1],
      "DN_CHAP" = forParCoord[-CancerGroup2, 2],
      "UP_CoCHAP" = forParCoord[-CancerGroup2, 3],
      "DN_CoCHAP" = forParCoord[-CancerGroup2, 4]
    ),
    col = "red"
  )
  boxplot(
    list(forParCoord[CancerGroup2, 1], forParCoord[CancerGroup2, 2], forParCoord[CancerGroup2, 3], forParCoord[CancerGroup2, 4]),
    add = T,
    col = "steelblue1",
    xaxt = "n"
  )
  dev.off()
  
  #Cluster according to Chap results and check validation:(for figure3)
  require(fpc)
  km.bootChap <- clusterboot(
    forParCoord,
    B = 1000,
    bootmethod = "boot",
    clustermethod = kmeansCBI,
    krange = 2,
    seed = 0
  )
  summary(silhouette(
    x = kmeans(x = forParCoord, centers = 2)$cluster,
    dist = dist(forParCoord)
  )) #Reported the median in paper
}


# For figure 4 (& ...); CCTs and stuff: (copied from allFunctionalized.R)
if(FALSE){
  prepareStuffOuti <- prepareStuffTCGA()
  PNs <- readRDS(file = "./PNs.rds")
  HSP60GenesEtrez <- prepareStuffOuti$CHAPL2EntrezID$HSP60
  HSP60Genes <- PNs$Gene[match(HSP60GenesEtrez,PNs$EntrezID)]
  CCTTestResults <- matrix(NA,nrow = length(prepareStuffOuti$grup1),ncol = length(HSP60Genes))
  rownames(CCTTestResults) <- substr(prepareStuffOuti$grup1,start = 22,
                                     stop=nchar(prepareStuffOuti$grup1))
  nameConvTabelle <- read.csv(file = "./TCGANamesAbbrevConvTable.csv",sep = ";",header = F)
  InDxEs <- match(rownames(CCTTestResults),nameConvTabelle$V2)
  InDxEs[5] <- 9
  rownames(CCTTestResults) <- nameConvTabelle$V1[InDxEs]
  colnames(CCTTestResults) <- HSP60Genes
  for(K in 1:ncol(CCTTestResults)){
    geneIndx <- rownames(prepareStuffOuti$gexMat) == HSP60GenesEtrez[K]
    if(sum(geneIndx) != 1) {
      warning(paste("There is a gene matching problem here! in ", HSP60GenesEtrez[K]))
      next
    }
    for(J in 1:nrow(CCTTestResults)){
      if(J == 18) next
      healthyIndx <- prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup1[J]
      cancerIndx <- prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup2[J]
      TinTTest <- t.test(x = prepareStuffOuti$gexMat[which(geneIndx),which(cancerIndx)],
                         y = prepareStuffOuti$gexMat[which(geneIndx),which(healthyIndx)])
      CCTTestResults[J,K] <- (1-TinTTest$p.value)*sign(TinTTest$statistic)
      #CCTTestResults[J,K] <- TinTTest$statistic
    }
  }
  #Plotting only for CCT Complex:
  require(gplots)
  pdf("./Results/Fig4_CCTsHeatTTest.pdf")
  heatmap.2(x = CCTTestResults[-18,c(3:10,12:13)],col=colorRampPalette(c("blue", "white", "red"))(n = 100),Rowv = T,Colv = T,
            trace = "none",key.title = NA,keysize = 1,cexCol=0.7,cexRow=0.7,srtCol = 45,key.par = list(cex=0.8),
            margins=c(5,19),colsep=1:ncol(CCTTestResults[-18,c(3:10,12:13)]),rowsep = 1:nrow(CCTTestResults[-18,c(3:10,12:13)]),sepcolor="black",
            sepwidth=c(0.01,0.01),main="T.Test stats on CCTs")
  dev.off()
  
  #Writing the values in a csv:
  write.csv(x = CCTTestResults[-18,c(3:10,12:13)],file = "./Results/Fig4_CCTsHeatTTest.csv")
  
  #Do GSA on proteosome:
  PNList <- "PNL2EntrezID"
  gsaRevTableScores <-
    gsaReviewWrapperAll(
      gexMat = prepareStuffOuti$gexMat,
      grup1 = prepareStuffOuti$grup1,
      grup2 = prepareStuffOuti$grup2,
      PNList = prepareStuffOuti[[PNList]],
      diseaseLevels = prepareStuffOuti$diseaseLevels,
      mode = "score",
      SEED = 76
    )
  
  #Cancer names abbrevating:
  rownames(gsaRevTableScores) <-
    sapply(strsplit(rownames(gsaRevTableScores), split = ", "), function(x)
      x[2])
  rownames(gsaRevTableScores)[5] <-
    "Esophageal carcinoma" #except "Esophageal carcinoma ", weird error from TissueSourceSite file downloaded from TCGA
  TCGAAbbrevConv <-
    read.csv("./TCGANamesAbbrevConvTable.csv",
             sep = ";",
             header = F)
  rownames(gsaRevTableScores) <-
    TCGAAbbrevConv$V1[match(rownames(gsaRevTableScores), TCGAAbbrevConv$V2)]
  
  #Plotting:
  pdf(file = "./Results/Fig4_TCGAGsaRevTableScoresL3HeatmapProteasome.pdf",
      width = 10,
      height = 10)
  require(gplots)
  heatTmp <-
    heatmap.2(
      x = gsaRevTableScores,
      col = colorRampPalette(c("blue", "white", "red"))(n = 100),
      Rowv = T,
      Colv = T,
      trace = "none",
      key.title = NA,
      keysize = 1,
      cexCol = 1,
      cexRow = 1,
      srtCol = 45,
      key.par = list(cex = 0.8),
      margins = c(5, 28),
      colsep = 1:ncol(gsaRevTableScores),
      rowsep = 1:nrow(gsaRevTableScores),
      sepcolor = "black",
      sepwidth = c(0.01, 0.01),
      main = "Proteasome Analysis of TCGA using GSA",
      distfun = function(x)
        dist(x, method = "euclidean")
    )
  dev.off()
  
  #Writing the values in a csv:
  write.csv(x = gsaRevTableScores[heatTmp$rowInd,heatTmp$colInd],file = "./Results/Fig4_TCGAGsaRevTableScoresL3HeatmapProteasome.csv")
  
  #Plotting just Proteasome:
  pdf(file = "./Results/Fig4_TCGAGsaRevTableScoresL3HeatmapOnlyProteasome.pdf",
      width = 10,
      height = 10)
  require(gplots)
  heatTmp <-
    heatmap.2(
      x = gsaRevTableScores[,c(11,11)],
      col = colorRampPalette(c("blue", "white", "red"))(n = 100),
      Rowv = T,
      Colv = F,
      trace = "none",
      key.title = NA,
      keysize = 1,
      cexCol = 1,
      cexRow = 1,
      srtCol = 45,
      key.par = list(cex = 0.8),
      margins = c(5, 46),
      colsep = NULL,
      rowsep = 1:nrow(gsaRevTableScores),
      sepcolor = rgb(0,0,0,1,maxColorValue = 1),
      sepwidth = c(0.01, 0.01),
      main = "Proteasome Analysis of TCGA using GSA",
      labCol="Proteasome",
      distfun = function(x)
        dist(x, method = "euclidean")
    )
  dev.off()
  
}

# For figure 5 (& ...); Neuro stuff: (copied from neuroProcessing.R)
if(FALSE){
  PNs <- readRDS(file = "./PNs.rds")
  prepareStuffOutiAD <- prepareStuffAD()
  PNList <- "CHAPL2EntrezID"
  gsaRevTableScoresAD <- gsaReviewWrapperAll(gexMat = prepareStuffOutiAD$gexMat,
                                             grup1 = prepareStuffOutiAD$grup1,
                                             grup2 = prepareStuffOutiAD$grup2,
                                             PNList = prepareStuffOutiAD[[PNList]],
                                             diseaseLevels = prepareStuffOutiAD$diseaseLevels,mode = "score",
                                             SEED = 0)
  
  prepareStuffOutiHD <- prepareStuffHD(mode="binary")
  PNList <- "CHAPL2EntrezID"
  gsaRevTableScoresHD <- gsaReviewWrapperAll(gexMat = prepareStuffOutiHD$gexMat,
                                             grup1 = prepareStuffOutiHD$grup1,
                                             grup2 = prepareStuffOutiHD$grup2,
                                             PNList = prepareStuffOutiHD[[PNList]],
                                             diseaseLevels = prepareStuffOutiHD$diseaseLevels,mode = "score",
                                             SEED = 0)
  
  prepareStuffOutiPD <- prepareStuffPD()
  PNList <- "CHAPL2EntrezID"
  gsaRevTableScoresPD <- gsaReviewWrapperAll(gexMat = prepareStuffOutiPD$gexMat,
                                             grup1 = prepareStuffOutiPD$grup1,
                                             grup2 = prepareStuffOutiPD$grup2,
                                             PNList = prepareStuffOutiPD[[PNList]],
                                             diseaseLevels = prepareStuffOutiPD$diseaseLevels,mode = "score",
                                             SEED=0)
  
  rownames(gsaRevTableScoresAD) <- "Alzheimer's disease"
  rownames(gsaRevTableScoresHD) <- "Huntington's disease"
  rownames(gsaRevTableScoresPD) <- "Parkinson's disease"
  gsaRevTableScoresALL <- rbind(gsaRevTableScoresAD,gsaRevTableScoresHD,gsaRevTableScoresPD)
  
  gsaRevTableScoresChaperome <- gsaRevTableScoresALL
  
  gsaRevTableScoresChaperome <- gsaRevTableScoresChaperome[,order(apply(X = gsaRevTableScoresChaperome,MARGIN = 2,FUN = mean))]
  
  pdf(file = "./Results/GSAChaperomeADHDPD(WOClustering)(ALLHDGrades)(OnlyChap).pdf",width = 10,height = 10)
  require(gplots)
  heatmap.2(x = gsaRevTableScoresChaperome,col=colorRampPalette(c("blue", "white", "red"))(n = 100),Rowv = F,Colv = F,
            trace = "none",key.title = NA,keysize = 1,cexCol=1,cexRow=1,srtCol = 45,key.par = list(cex=0.8),
            margins=c(38,15),colsep=1:ncol(gsaRevTableScoresChaperome),rowsep = 1:nrow(gsaRevTableScoresChaperome),sepcolor="black",
            sepwidth=c(0.01,0.01),main="Chaperome Analysis of AD, HD and PD using GSA")
  #cellnote = round(gsaRevTableScores,2),notecex = 0.4,notecol="black")
  dev.off()
  write.csv(x = sort(apply(X = gsaRevTableScoresChaperome,MARGIN = 2,FUN = mean)), 
            file = "./Results/Fig5_GSAChaperomeADHDPD(WOClustering)(ALLHDGrades)(OnlyChap).csv")
  #Save heatmap(in Order) for WEbtool:
  require(gplots)
  pdf(file = "~/Desktop/tmp.pdf")
  heatTmp <- heatmap.2(x = gsaRevTableScoresChaperome,col=colorRampPalette(c("blue", "white", "red"))(n = 100),Rowv = T,Colv = T,
                       trace = "none",key.title = NA,keysize = 1,cexCol=1.5,cexRow=1.5,srtCol = 45,key.par = list(cex=0.8),
                       margins=c(32,15),colsep=1:ncol(gsaRevTableScoresChaperome),rowsep = 1:nrow(gsaRevTableScoresChaperome),sepcolor="black",
                       sepwidth=c(0.01,0.01),main="PN Analysis of AD, HD and PD using GSA")
  dev.off()
  write.csv(x = gsaRevTableScoresChaperome[heatTmp$rowInd,heatTmp$colInd],
            file = "./Results/GSAChaperomeADHDPD(WOClustering)(ALLHDGrades)(OnlyChap)OrderedForTool.csv") #Convert names to abbreviations later!!
  
  
  # Doing for Chaperome as a group vs everything else for all Neuro:
  PNList <- "PNL1EntrezID"
  gsaRevTableScoresAD100 <-
    gsaReviewEqualRamdomized(
      prepareStuffOutiAD$gexMat,
      prepareStuffOutiAD$grup1,
      prepareStuffOutiAD$grup2,
      prepareStuffOutiAD[[PNList]],
      prepareStuffOutiAD$diseaseLevels,
      SEED = 72,
      repetations = 100
    ) # This may take some time!
  
  gsaChaperomeReviewAD <- gsaReviewEqualRamdomizedSummarizer(gsaReviewEqualRamdomizedOutput = gsaRevTableScoresAD100)
  
  gsaRevTableScoresHD100 <-
    gsaReviewEqualRamdomized(
      prepareStuffOutiHD$gexMat,
      prepareStuffOutiHD$grup1,
      prepareStuffOutiHD$grup2,
      prepareStuffOutiHD[[PNList]],
      prepareStuffOutiHD$diseaseLevels,
      SEED = 72,
      repetations = 100
    ) # This may take some time!
  
  gsaChaperomeReviewHD <- gsaReviewEqualRamdomizedSummarizer(gsaReviewEqualRamdomizedOutput = gsaRevTableScoresHD100)
  
  gsaRevTableScoresPD100 <-
    gsaReviewEqualRamdomized(
      prepareStuffOutiPD$gexMat,
      prepareStuffOutiPD$grup1,
      prepareStuffOutiPD$grup2,
      prepareStuffOutiPD[[PNList]],
      prepareStuffOutiPD$diseaseLevels,
      SEED = 72,
      repetations = 100
    ) # This may take some time!
  
  gsaChaperomeReviewPD <- gsaReviewEqualRamdomizedSummarizer(gsaReviewEqualRamdomizedOutput = gsaRevTableScoresPD100)
  
  rownames(gsaChaperomeReviewAD) <- "Alzheimer's disease"
  rownames(gsaChaperomeReviewHD) <- "Huntington's disease"
  rownames(gsaChaperomeReviewPD) <- "Parkinson's disease"
  gsaRevTableScoresALL <- rbind(gsaChaperomeReviewAD,gsaChaperomeReviewHD,gsaChaperomeReviewPD)
  
  gsaRevTableScoresChaperome <- gsaRevTableScoresALL
  
  pdf(file = "./Results/Fig5_GSAChapVsAllElse(WOClustering).pdf",width = 10,height = 10)
  require(gplots)
  heatmap.2(x = gsaRevTableScoresChaperome,col=colorRampPalette(c("blue", "white", "red"))(n = 100),Rowv = F,Colv = F,
            trace = "none",key.title = NA,keysize = 1,cexCol=1,cexRow=1,srtCol = 45,key.par = list(cex=0.8),
            margins=c(38,41),colsep=1:ncol(gsaRevTableScoresChaperome),rowsep = 1:nrow(gsaRevTableScoresChaperome),sepcolor="black",
            sepwidth=c(0.01,0.01),main="Chaperome Analysis of AD, HD and PD using GSA")
  #cellnote = round(gsaRevTableScores,2),notecex = 0.4,notecol="black")
  dev.off()
  write.csv(x = sort(apply(X = gsaRevTableScoresChaperome,MARGIN = 2,FUN = mean)), 
            file = "./Results/Fig5_GSAChapVsAllElse(WOClustering).csv")
  
}

## Calculating M-Scores for figures 6 and 7 (Plots themselves are made by PRO2 webtool,
#check source code of PRO2, especially functions in Views.py)
if(FALSE){
  prepareStuffOuti <- prepareStuffTCGA()
  PNList <- "CHAPL2EntrezID" 
  groupVsOuti <- groupsVsDirectionCalculator(PNList=prepareStuffOuti[[PNList]], numOfPCs=3, diseaseLevels=prepareStuffOuti$diseaseLevels, 
                                             gexMat=prepareStuffOuti$gexMat, grup1=prepareStuffOuti$grup1, grup2=prepareStuffOuti$grup2,
                                             representativeVersion = T) # Check this 'representative' stuff later!
  mainAxes <- makeMainAxisFromReleventRotations(relevantRotSub = groupVsOuti$relevantRotSub,PNList = groupVsOuti$PNListBigEnough)
  pcaScoreOfSamples <- matrix(NA,nrow = length(mainAxes),ncol = ncol(prepareStuffOuti$gexMat))
  rownames(pcaScoreOfSamples) <- names(mainAxes)
  colnames(pcaScoreOfSamples) <- colnames(prepareStuffOuti$gexMat)
  require(R.utils)
  pb <- txtProgressBar(min = 0, max = 100, style = 3)
  for(k in 1:ncol(pcaScoreOfSamples)){
    pcaScoreOfSamples[,k] <- calcScoresSingularAxes(inptVec = prepareStuffOuti$gexMat[,k],mainAxeses = mainAxes)
    setTxtProgressBar(pb, 100*round(k/ncol(pcaScoreOfSamples),digits = 2))
  }
  close(pb)
  write.csv(x = pcaScoreOfSamples,file = "./Results/ChaperomeMScoresForTCGA.csv")
  # Exporting some M-Scores to CSV for WEbtool:
  ## Mean of L2 Chaperome:
  pcaScoresMean <- matrix(NA,nrow = length(mainAxes),
                            ncol = 2*length(prepareStuffOuti$grup1))
  rownames(pcaScoresMean) <- names(mainAxes)
  cOlNAmEs <- character()
  for(K in 1:length(prepareStuffOuti$grup1)){
    if(K == 18) { # One sample there!!
      pcaScoresMean[,((K*2)-1)] <- pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]]
    } else {
      pcaScoresMean[,((K*2)-1)] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]],MARGIN = 1,
                                               FUN = mean)
    }
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup1[K],split = ", ")[[1]][2:1],collapse = " "))
    pcaScoresMean[,((K*2))] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup2[K]],MARGIN = 1,
                                           FUN = mean)
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup2[K],split = ", ")[[1]][2:1],collapse = " "))
    print(K)
  }
  colnames(pcaScoresMean) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresMean),file = "./Results/PN&ChaperMetaPCAResults.csv")
  ## Q5 of L2 Chaperome:
  pcaScoresQ5 <- matrix(NA,nrow = length(mainAxes),
                          ncol = 2*length(prepareStuffOuti$grup1))
  rownames(pcaScoresQ5) <- names(mainAxes)
  cOlNAmEs <- character()
  for(K in 1:length(prepareStuffOuti$grup1)){
    if(K == 18) { # One sample there!!
      pcaScoresQ5[,((K*2)-1)] <- pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]]
    } else {
      pcaScoresQ5[,((K*2)-1)] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]],MARGIN = 1,
                                         FUN = function(x) quantile(x,probs = c(0.05)))
    }
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup1[K],split = ", ")[[1]][2:1],collapse = " "))
    pcaScoresQ5[,((K*2))] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup2[K]],MARGIN = 1,
                                     FUN = function(x) quantile(x,probs = c(0.05)))
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup2[K],split = ", ")[[1]][2:1],collapse = " "))
    print(K)
  }
  colnames(pcaScoresQ5) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresQ5),file = "./Results/PN&ChaperMetaPCAResultsQ5.csv")
  ## Q95 of L2 Chaperome:
  pcaScoresQ95 <- matrix(NA,nrow = length(mainAxes),
                        ncol = 2*length(prepareStuffOuti$grup1))
  rownames(pcaScoresQ95) <- names(mainAxes)
  cOlNAmEs <- character()
  for(K in 1:length(prepareStuffOuti$grup1)){
    if(K == 18) { # One sample there!!
      pcaScoresQ95[,((K*2)-1)] <- pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]]
    } else {
      pcaScoresQ95[,((K*2)-1)] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup1[K]],MARGIN = 1,
                                       FUN = function(x) quantile(x,probs = c(0.95)))
    }
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup1[K],split = ", ")[[1]][2:1],collapse = " "))
    pcaScoresQ95[,((K*2))] <- apply(X = pcaScoreOfSamples[,prepareStuffOuti$diseaseLevels==prepareStuffOuti$grup2[K]],MARGIN = 1,
                                   FUN = function(x) quantile(x,probs = c(0.95)))
    cOlNAmEs <- c(cOlNAmEs,paste(strsplit(prepareStuffOuti$grup2[K],split = ", ")[[1]][2:1],collapse = " "))
    print(K)
  }
  colnames(pcaScoresQ95) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresQ95),file = "./Results/PN&ChaperMetaPCAResultsQ95.csv")
  
  #Making M-Scores for neuro diseases for webtool:
  prepareStuffOutiAD <- prepareStuffAD()
  pcaScoreOfSamplesAD <- matrix(NA,nrow = length(mainAxes),ncol = ncol(prepareStuffOutiAD$gexMat))
  rownames(pcaScoreOfSamplesAD) <- names(mainAxes)
  colnames(pcaScoreOfSamplesAD) <- prepareStuffOutiAD$diseaseLevels
  for(k in 1:ncol(pcaScoreOfSamplesAD)){
    pcaScoreOfSamplesAD[,k] <- calcScoresSingularAxes(inptVec = prepareStuffOutiAD$gexMat[,k],mainAxeses = mainAxes)
    print(100*round(k/ncol(pcaScoreOfSamplesAD),digits = 2))
  }
  
  prepareStuffOutiHD <- prepareStuffHD(mode="binary")
  pcaScoreOfSamplesHD <- matrix(NA,nrow = length(mainAxes),ncol = ncol(prepareStuffOutiHD$gexMat))
  rownames(pcaScoreOfSamplesHD) <- names(mainAxes)
  colnames(pcaScoreOfSamplesHD) <- prepareStuffOutiHD$diseaseLevels
  for(k in 1:ncol(pcaScoreOfSamplesHD)){
    pcaScoreOfSamplesHD[,k] <- calcScoresSingularAxes(inptVec = prepareStuffOutiHD$gexMat[,k],mainAxeses = mainAxes)
    print(100*round(k/ncol(pcaScoreOfSamplesHD),digits = 2))
  }
  
  prepareStuffOutiPD <- prepareStuffPD()
  pcaScoreOfSamplesPD <- matrix(NA,nrow = length(mainAxes),ncol = ncol(prepareStuffOutiPD$gexMat))
  rownames(pcaScoreOfSamplesPD) <- names(mainAxes)
  colnames(pcaScoreOfSamplesPD) <- prepareStuffOutiPD$diseaseLevels
  for(k in 1:ncol(pcaScoreOfSamplesPD)){
    pcaScoreOfSamplesPD[,k] <- calcScoresSingularAxes(inptVec = prepareStuffOutiPD$gexMat[,k],mainAxeses = mainAxes)
    print(100*round(k/ncol(pcaScoreOfSamplesPD),digits = 2))
  }
  
  ## Mean of L2 Chaperome:
  pcaScoresNeuroMean <- matrix(NA,nrow = length(mainAxes),
                          ncol = 2*3)
  rownames(pcaScoresNeuroMean) <- names(mainAxes)
  cOlNAmEs <- character()
  pcaScoresNeuroMean[,1] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup1],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","Normal"))
  
  pcaScoresNeuroMean[,2] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup2],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","NeuroDegenerated"))
  
  pcaScoresNeuroMean[,3] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup1],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","Normal"))
  
  pcaScoresNeuroMean[,4] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup2],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","NeuroDegenerated"))
  
  pcaScoresNeuroMean[,5] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup1],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","Normal"))
  
  pcaScoresNeuroMean[,6] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup2],
                                   MARGIN = 1,FUN = mean)
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","NeuroDegenerated"))
  
  colnames(pcaScoresNeuroMean) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresNeuroMean),file = "./Results/PN&ChaperMetaPCANeuroResults.csv")
  
  ## Q5 of L2 Chaperome:
  pcaScoresNeuroQ5 <- matrix(NA,nrow = length(mainAxes),
                               ncol = 2*3)
  rownames(pcaScoresNeuroQ5) <- names(mainAxes)
  cOlNAmEs <- character()
  pcaScoresNeuroQ5[,1] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup1],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","Normal"))
  
  pcaScoresNeuroQ5[,2] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup2],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","NeuroDegenerated"))
  
  pcaScoresNeuroQ5[,3] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup1],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","Normal"))
  
  pcaScoresNeuroQ5[,4] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup2],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","NeuroDegenerated"))
  
  pcaScoresNeuroQ5[,5] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup1],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","Normal"))
  
  pcaScoresNeuroQ5[,6] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup2],
                                  MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.05)))
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","NeuroDegenerated"))
  
  colnames(pcaScoresNeuroQ5) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresNeuroQ5),file = "./Results/PN&ChaperMetaPCANeuroResultsQ5.csv")
  
  ## Q95 of L2 Chaperome:
  pcaScoresNeuroQ95 <- matrix(NA,nrow = length(mainAxes),
                             ncol = 2*3)
  rownames(pcaScoresNeuroQ95) <- names(mainAxes)
  cOlNAmEs <- character()
  pcaScoresNeuroQ95[,1] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup1],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","Normal"))
  
  pcaScoresNeuroQ95[,2] <- apply(X = pcaScoreOfSamplesAD[,colnames(pcaScoreOfSamplesAD)==prepareStuffOutiAD$grup2],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("AlzheimerDisease","NeuroDegenerated"))
  
  pcaScoresNeuroQ95[,3] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup1],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","Normal"))
  
  pcaScoresNeuroQ95[,4] <- apply(X = pcaScoreOfSamplesHD[,colnames(pcaScoreOfSamplesHD)==prepareStuffOutiHD$grup2],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("HuntingtonDisease","NeuroDegenerated"))
  
  pcaScoresNeuroQ95[,5] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup1],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","Normal"))
  
  pcaScoresNeuroQ95[,6] <- apply(X = pcaScoreOfSamplesPD[,colnames(pcaScoreOfSamplesPD)==prepareStuffOutiPD$grup2],
                                MARGIN = 1,FUN = function(x) quantile(x,probs = c(0.95)))
  cOlNAmEs <- c(cOlNAmEs,paste("ParkinsonDisease","NeuroDegenerated"))
  
  colnames(pcaScoresNeuroQ95) <- gsub(pattern = " ",replacement = "",x = cOlNAmEs)
  write.csv(x = t(pcaScoresNeuroQ95),file = "./Results/PN&ChaperMetaPCANeuroResultsQ95.csv")
}


#Supplement correlation plot:
if(FALSE){
  prepareStuffOuti <- prepareStuffTCGA()
  PNList <- "CHAPL2EntrezID" 
  groupVsOuti <- groupsVsDirectionCalculator(PNList=prepareStuffOuti[[PNList]], numOfPCs=3, diseaseLevels=prepareStuffOuti$diseaseLevels, 
                                             gexMat=prepareStuffOuti$gexMat, grup1=prepareStuffOuti$grup1, grup2=prepareStuffOuti$grup2,
                                             representativeVersion = T) # Check this 'representative' stuff later!
  mainAxes <- makeMainAxisFromReleventRotations(relevantRotSub = groupVsOuti$relevantRotSub,PNList = groupVsOuti$PNListBigEnough)
  pcaScoreOfSamples <- matrix(NA,nrow = length(mainAxes),ncol = ncol(prepareStuffOuti$gexMat))
  rownames(pcaScoreOfSamples) <- names(mainAxes)
  colnames(pcaScoreOfSamples) <- colnames(prepareStuffOuti$gexMat)
  require(R.utils)
  pb <- txtProgressBar(min = 0, max = 100, style = 3)
  for(k in 1:ncol(pcaScoreOfSamples)){
    pcaScoreOfSamples[,k] <- calcScoresSingularAxes(inptVec = prepareStuffOuti$gexMat[,k],mainAxeses = mainAxes)
    setTxtProgressBar(pb, 100*round(k/ncol(pcaScoreOfSamples),digits = 2))
  }
  close(pb)
  
  require(limma)
  FCLiMma <- numeric(length = length(prepareStuffOuti$grup1))
  names(FCLiMma) <- substr(x = prepareStuffOuti$grup1,
                           start = 22,stop = nchar(prepareStuffOuti$grup1))
  AELiMma <- numeric(length = length(prepareStuffOuti$grup1))
  names(AELiMma) <- substr(x = prepareStuffOuti$grup1,
                           start = 22,stop = nchar(prepareStuffOuti$grup1))
  TLiMma <- numeric(length = length(prepareStuffOuti$grup1))
  names(TLiMma) <- substr(x = prepareStuffOuti$grup1,
                          start = 22,stop = nchar(prepareStuffOuti$grup1))
  PLiMma <- numeric(length = length(prepareStuffOuti$grup1))
  names(PLiMma) <- substr(x = prepareStuffOuti$grup1,
                          start = 22,stop = nchar(prepareStuffOuti$grup1))
  APLiMma <- numeric(length = length(prepareStuffOuti$grup1))
  names(APLiMma) <- substr(x = prepareStuffOuti$grup1,
                           start = 22,stop = nchar(prepareStuffOuti$grup1))
  
  PNList <- "CHAPL2EntrezID"
  #Doing GSA "GSEScores" on TCGA for Chaperome groups:
  gsaRevTableScoresDesired <-
    gsaReviewWrapperAll(gexMat = prepareStuffOuti$gexMat,
      grup1 = prepareStuffOuti$grup1,
      grup2 = prepareStuffOuti$grup2,
      PNList = prepareStuffOuti[[PNList]],
      diseaseLevels = prepareStuffOuti$diseaseLevels,
      mode = "score",
      submode = "GSAScores",
      SEED = 0
    )
  
  limmaRevTableScoresDesiredT <- matrix(NA,nrow = nrow(gsaRevTableScoresDesired),ncol = ncol(gsaRevTableScoresDesired))
  rownames(gsaRevTableScoresDesired) <- gsub(pattern = "Solid Tissue Normal, ",replacement = "",rownames(gsaRevTableScoresDesired))
  dimnames(limmaRevTableScoresDesiredT) <- dimnames(gsaRevTableScoresDesired)
  limmaRevTableScoresDesiredP <- matrix(NA,nrow = nrow(gsaRevTableScoresDesired),ncol = ncol(gsaRevTableScoresDesired))
  dimnames(limmaRevTableScoresDesiredP) <- dimnames(gsaRevTableScoresDesired)
  for(K in 1:length(prepareStuffOuti$grup1)){
    GLUPH <- prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup1[K]
    GLUPC <- prepareStuffOuti$diseaseLevels == prepareStuffOuti$grup2[K]
    
    dEannots <- as.factor(c(rep("Normal",sum(GLUPH)),rep("Tumor",sum(GLUPC))))
    
    subMat <- cbind(pcaScoreOfSamples[,GLUPH],pcaScoreOfSamples[,GLUPC])
    
    design <- model.matrix(~0+as.factor(dEannots))
    colnames(design) <- c("Normal","Tumor")
    
    fit <- lmFit(subMat, design)
    fitC <- contrasts.fit(fit, makeContrasts(Tumor - Normal, levels = design))
    
    
    fit2 <- eBayes(fitC)
    output <- topTable(fit2)
  
    output <- output[match(colnames(gsaRevTableScoresDesired),rownames(output)),]
    FCLiMma[K] <- cor(output$logFC,gsaRevTableScoresDesired[K,],method = "spearman")
    AELiMma[K] <- cor(output$AveExpr,gsaRevTableScoresDesired[K,],method = "spearman")
    TLiMma[K] <- cor(output$t,gsaRevTableScoresDesired[K,],method = "pearson")
    limmaRevTableScoresDesiredT[K,] <- output$t
    PLiMma[K] <- cor((1-output$P.Value)*sign(output$t),gsaRevTableScoresDesired[K,],method = "spearman")
    APLiMma[K] <- cor((1-output$adj.P.Val)*sign(output$t),gsaRevTableScoresDesired[K,],method = "spearman")
    limmaRevTableScoresDesiredP[K,] <- (1-output$adj.P.Val)*sign(output$t)
  }
  
  pdf(file = paste0("./Results/LimmaTVsGSAScores.pdf"),width = 10,height = 7)
  plot(limmaRevTableScoresDesiredT,gsaRevTableScoresDesired,col=rep(rainbow(22),10),xlab="T-stats from Limma",ylab = "GSA Score",pch=16)
  legend(legend = rownames(limmaRevTableScoresDesiredT),fill = rainbow(22),x = 'bottomright',cex = 0.5)
  fittedLine <- lm(c(gsaRevTableScoresDesired) ~ c(limmaRevTableScoresDesiredT))
  abline(fittedLine$coefficients[1],fittedLine$coefficients[2])
  dev.off()
  cor(c(limmaRevTableScoresDesiredT),c(gsaRevTableScoresDesired), method = "spearman")
  
}




