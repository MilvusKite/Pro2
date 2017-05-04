##18.4.2017: Functions used for calculation
## written by: Ali Hadizadeh Esfahani, esfahani@aices.rwth-aachen.de

#Remember for these functions to work you need to set working directory to where FUNCS.R folder

##This section will run only once to import Chaperome gene list from S1 table:
if(!file.exists("PNs.rds")){
  require(xlsx)
  PNs <- read.xlsx(file = "S1_Table.xlsx",sheetIndex = 1,startRow = 11)
  PNs <- PNs[!is.na(PNs$Gene),!is.na(PNs[1,])]
  saveRDS(object = PNs,file = "PNs.rds")
}
if(!file.exists("Proteasome.rds")){
  require(xlsx)
  Protea <- read.xlsx(file = "S1_Table.xlsx",sheetIndex = 2,startRow = 11)
  Protea <- Protea[!is.na(Protea$Gene),!is.na(Protea[1,])]
  saveRDS(object = Protea, file = "Proteasome.rds")
}
##

#prepare necessary data formats and annotations for next steps:
prepareStuffTCGA <- function(mode="ALL") {
  
  ##loading data up (TCGA are downloaded using FireBrowse(http://firebrowse.org) and VOOM transformed(Using Limma package), easy
  #to reproduce but still if the exact TCGA.rds and TCGAAnnot.rds are needed you can contact esfahani@aices.rwth-aachen.de)
  TCGA <- readRDS(file = "./TCGA.rds")
  TCGAAnnot <- readRDS(file = "./TCGAAnnot.rds")
  
  PNs <- readRDS(file = "./PNs.rds")
  Proteasome <- readRDS(file = "./Proteasome.rds")
  PNL1EntrezID <- list()
  for (Level in levels(PNs$Level1)) {
    PNL1EntrezID[[Level]] <- PNs$EntrezID[PNs$Level1 == Level]
  }
  PNL1EntrezID[["Others"]] <- setdiff(x = rownames(TCGA),y = unlist(PNL1EntrezID))
  
  CHAPL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    CHAPL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  
  PNL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    PNL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  PNL2EntrezID[["Proteasome"]] <- Proteasome$EntrezID
  #PNL2EntrezID[["Others"]] <- setdiff(x = rownames(TCGA),y = unlist(PNL2EntrezID))
  
  gexMat <- TCGA - apply(X = TCGA,MARGIN = 1,FUN = mean) # Centering genes as a basic normalization
  
  diseaseLevels <- as.factor(TCGAAnnot$sampleTissueAnnotation)
  
  if(mode=="ALL") {
    grup1 <- c("Solid Tissue Normal, Bladder Urothelial Carcinoma", "Solid Tissue Normal, Breast invasive carcinoma",
               "Solid Tissue Normal, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Solid Tissue Normal, Cholangiocarcinoma", "Solid Tissue Normal, Esophageal carcinoma ",
               "Solid Tissue Normal, Glioblastoma multiforme","Solid Tissue Normal, Head and Neck squamous cell carcinoma",
               "Solid Tissue Normal, Kidney Chromophobe","Solid Tissue Normal, Kidney renal clear cell carcinoma",
               "Solid Tissue Normal, Kidney renal papillary cell carcinoma","Solid Tissue Normal, Liver hepatocellular carcinoma",
               "Solid Tissue Normal, Lung adenocarcinoma","Solid Tissue Normal, Lung squamous cell carcinoma",
               "Solid Tissue Normal, Pancreatic adenocarcinoma","Solid Tissue Normal, Pheochromocytoma and Paraganglioma",
               "Solid Tissue Normal, Prostate adenocarcinoma","Solid Tissue Normal, Sarcoma", "Solid Tissue Normal, Skin Cutaneous Melanoma",
               "Solid Tissue Normal, Stomach adenocarcinoma","Solid Tissue Normal, Thyroid carcinoma","Solid Tissue Normal, Thymoma",
               "Solid Tissue Normal, Uterine Corpus Endometrial Carcinoma")
    grup2 <- c("Primary solid Tumor, Bladder Urothelial Carcinoma", "Primary solid Tumor, Breast invasive carcinoma",
               "Primary solid Tumor, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Primary solid Tumor, Cholangiocarcinoma", "Primary solid Tumor, Esophageal carcinoma ",
               "Primary solid Tumor, Glioblastoma multiforme","Primary solid Tumor, Head and Neck squamous cell carcinoma",
               "Primary solid Tumor, Kidney Chromophobe","Primary solid Tumor, Kidney renal clear cell carcinoma",
               "Primary solid Tumor, Kidney renal papillary cell carcinoma","Primary solid Tumor, Liver hepatocellular carcinoma",
               "Primary solid Tumor, Lung adenocarcinoma","Primary solid Tumor, Lung squamous cell carcinoma",
               "Primary solid Tumor, Pancreatic adenocarcinoma","Primary solid Tumor, Pheochromocytoma and Paraganglioma",
               "Primary solid Tumor, Prostate adenocarcinoma","Primary solid Tumor, Sarcoma", "Primary solid Tumor, Skin Cutaneous Melanoma",
               "Primary solid Tumor, Stomach adenocarcinoma","Primary solid Tumor, Thyroid carcinoma","Primary solid Tumor, Thymoma",
               "Primary solid Tumor, Uterine Corpus Endometrial Carcinoma")
  } else if(mode=="tripleFirst2") {
    grup1 <- c("Solid Tissue Normal, Breast invasive carcinoma",
               "Solid Tissue Normal, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Solid Tissue Normal, Esophageal carcinoma ",
               "Solid Tissue Normal, Head and Neck squamous cell carcinoma",
               "Solid Tissue Normal, Pancreatic adenocarcinoma","Solid Tissue Normal, Pheochromocytoma and Paraganglioma",
               "Solid Tissue Normal, Prostate adenocarcinoma","Solid Tissue Normal, Sarcoma", "Solid Tissue Normal, Skin Cutaneous Melanoma",
               "Solid Tissue Normal, Thyroid carcinoma")
    grup2 <- c("Primary solid Tumor, Breast invasive carcinoma",
               "Primary solid Tumor, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Primary solid Tumor, Esophageal carcinoma ",
               "Primary solid Tumor, Head and Neck squamous cell carcinoma",
               "Primary solid Tumor, Pancreatic adenocarcinoma","Primary solid Tumor, Pheochromocytoma and Paraganglioma",
               "Primary solid Tumor, Prostate adenocarcinoma","Primary solid Tumor, Sarcoma", "Primary solid Tumor, Skin Cutaneous Melanoma",
               "Primary solid Tumor, Thyroid carcinoma")
  } else if(mode=="tripleSecond2") {
    grup2 <- c("Metastatic, Breast invasive carcinoma",
               "Metastatic, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Metastatic, Esophageal carcinoma ",
               "Metastatic, Head and Neck squamous cell carcinoma",
               "Metastatic, Pancreatic adenocarcinoma","Metastatic, Pheochromocytoma and Paraganglioma",
               "Metastatic, Prostate adenocarcinoma","Metastatic, Sarcoma", "Metastatic, Skin Cutaneous Melanoma",
               "Metastatic, Thyroid carcinoma")
    grup1 <- c("Primary solid Tumor, Breast invasive carcinoma",
               "Primary solid Tumor, Cervical squamous cell carcinoma and endocervical adenocarcinoma",
               "Primary solid Tumor, Esophageal carcinoma ",
               "Primary solid Tumor, Head and Neck squamous cell carcinoma",
               "Primary solid Tumor, Pancreatic adenocarcinoma","Primary solid Tumor, Pheochromocytoma and Paraganglioma",
               "Primary solid Tumor, Prostate adenocarcinoma","Primary solid Tumor, Sarcoma", "Primary solid Tumor, Skin Cutaneous Melanoma",
               "Primary solid Tumor, Thyroid carcinoma")
  }
  
  return(list("gexMat"=gexMat, "diseaseLevels"=diseaseLevels, "grup1"=grup1, "grup2"=grup2,
              "PNL1EntrezID"=PNL1EntrezID,"PNL2EntrezID"=PNL2EntrezID,"CHAPL2EntrezID"=CHAPL2EntrezID))
  
}

# Next three functions prepare stuff for NeuroDegenerative disease calculations(genes expressions
# are downloaded from corrisponding publications referenced in our paper):
prepareStuffAD <- function() {

  # loading data up
  AD <- read.csv2(file = "./NeuroD expression data/ADAllGenes.csv",skip=1,sep = ";",header = F) # it has german "," for decimal!!! couldn't solve it with read.csv2!!
  ADGex <- as.matrix(AD[-1,-c(1,2)])
  ADGexNum <- apply(X = ADGex,MARGIN = 2,function(x) as.numeric(sub(pattern = ",",replacement = ".",x)))
  
  # Make it log-scale? :
  ADGexNum <- log2(ADGexNum)
  
  
  rownames(ADGexNum) <- AD$V1[-1]
  colnames(ADGexNum) <- as.character(as.matrix(AD[1,-c(1,2)]))
  
  
  PNs <- readRDS(file = "./PNs.rds")
  Proteasome <- readRDS(file = "./Proteasome.rds")
  PNL1EntrezID <- list()
  for (Level in levels(PNs$Level1)) {
    PNL1EntrezID[[Level]] <- PNs$EntrezID[PNs$Level1 == Level]
  }
  PNL1EntrezID[["Others"]] <- setdiff(x = rownames(ADGexNum),y = unlist(PNL1EntrezID))
  
  CHAPL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    CHAPL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  
  PNL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    PNL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  PNL2EntrezID[["Proteasome"]] <- Proteasome$EntrezID
  #PNL2EntrezID[["Others"]] <- setdiff(x = rownames(TCGA),y = unlist(PNL2EntrezID))
  
  gexMat <- ADGexNum - apply(X = ADGexNum,MARGIN = 1,FUN = mean)
  
  diseaseLevels <- as.factor(colnames(gexMat))
  
  
  grup1 <- c("normal")
  
  grup2 <- c("AD")
  
  
  return(list("gexMat"=gexMat, "diseaseLevels"=diseaseLevels, "grup1"=grup1, "grup2"=grup2,
              "PNL1EntrezID"=PNL1EntrezID,"PNL2EntrezID"=PNL2EntrezID,"CHAPL2EntrezID"=CHAPL2EntrezID))
  
}
prepareStuffHD <- function(mode) {
  
  # loading data up
  HD <- read.csv2(file = "./NeuroD expression data/HDAllGenes.csv",skip=1,sep = ";",header = F) # it has german "," for decimal!!! couldn't solve it with read.csv2!! 
  HDGex <- as.matrix(HD[-1,-c(1,2)])
  HDGexNum <- apply(X = HDGex,MARGIN = 2,function(x) as.numeric(sub(pattern = ",",replacement = ".",x)))
  #Data is not log-scale:
  HDGexNum <- log2(HDGexNum)
  rownames(HDGexNum) <- HD$V1[-1]
  colnames(HDGexNum) <- as.character(as.matrix(HD[1,-c(1,2)]))
  
  PNs <- readRDS(file = "./PNs.rds")
  Proteasome <- readRDS(file = "./Proteasome.rds")
  PNL1EntrezID <- list()
  for (Level in levels(PNs$Level1)) {
    PNL1EntrezID[[Level]] <- PNs$EntrezID[PNs$Level1 == Level]
  }
  PNL1EntrezID[["Others"]] <- setdiff(x = rownames(HDGexNum),y = unlist(PNL1EntrezID))
  
  CHAPL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    CHAPL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  
  PNL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    PNL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  PNL2EntrezID[["Proteasome"]] <- Proteasome$EntrezID
  #PNL2EntrezID[["Others"]] <- setdiff(x = rownames(TCGA),y = unlist(PNL2EntrezID))
  
  if(mode == "binary" | mode == "binaryOhneGrade4" | mode == "binaryOhneGrade3&4"){
    # Just for now -> turning different grades of annotation into a binary healthy/disease:
    colnames(HDGexNum) <- c(rep("control",32),rep("HD",38))
  }
  
  gexMat <- HDGexNum - apply(X = HDGexNum,MARGIN = 1,FUN = mean)
  
  if(mode=="binary") {
    grup1 <- c("control")
    grup2 <- c("HD")
  } else if(mode=="notBinary") {
    grup1 <- c("control","grade 0","grade 1","grade 2")
    grup2 <- c("grade 0","grade 1","grade 2","grade 3")
  } else if(mode == "binaryOhneGrade4"){
    grup1 <- c("control")
    grup2 <- c("HD")
    gexMat <- gexMat[,-70]
  } else if(mode == "binaryOhneGrade3&4"){
    grup1 <- c("control")
    grup2 <- c("HD")
    gexMat <- gexMat[,-c(65:70)]
  } else stop("what kind of mode is this!!!")
  
  diseaseLevels <- as.factor(colnames(gexMat))
  
  
  return(list("gexMat"=gexMat, "diseaseLevels"=diseaseLevels, "grup1"=grup1, "grup2"=grup2,
              "PNL1EntrezID"=PNL1EntrezID,"PNL2EntrezID"=PNL2EntrezID,"CHAPL2EntrezID"=CHAPL2EntrezID))
  
}
prepareStuffPD <- function() {
  
  # loading data up
  PD <- read.csv2(file = "./NeuroD expression data/PDAllGenes.csv",skip=1,sep = ";",header = F) # it has german "," for decimal!!! couldn't solve it with read.csv2!!
  PDGex <- as.matrix(PD[-1,-c(1,2)])
  PDGexNum <- apply(X = PDGex,MARGIN = 2,function(x) as.numeric(sub(pattern = ",",replacement = ".",x)))
  
  # Make it log-scale? :
  PDGexNum <- log2(PDGexNum)
  
  rownames(PDGexNum) <- PD$V1[-1]
  colnames(PDGexNum) <- as.character(as.matrix(PD[1,-c(1,2)]))
  
  PNs <- readRDS(file = "./PNs.rds")
  Proteasome <- readRDS(file = "./Proteasome.rds")
  PNL1EntrezID <- list()
  for (Level in levels(PNs$Level1)) {
    PNL1EntrezID[[Level]] <- PNs$EntrezID[PNs$Level1 == Level]
  }
  PNL1EntrezID[["Others"]] <- setdiff(x = rownames(PDGexNum),y = unlist(PNL1EntrezID))
  
  CHAPL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    CHAPL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  
  PNL2EntrezID <- list()
  for (Level in levels(PNs$Level2)) {
    PNL2EntrezID[[Level]] <- PNs$EntrezID[PNs$Level2 == Level]
  }
  PNL2EntrezID[["Proteasome"]] <- Proteasome$EntrezID
  #PNL2EntrezID[["Others"]] <- setdiff(x = rownames(TCGA),y = unlist(PNL2EntrezID))
  
  gexMat <- PDGexNum - apply(X = PDGexNum,MARGIN = 1,FUN = mean)
  
  diseaseLevels <- as.factor(colnames(gexMat))
  
  
  grup1 <- c("control")
  
  grup2 <- c("Parkinson's")
  
  
  return(list("gexMat"=gexMat, "diseaseLevels"=diseaseLevels, "grup1"=grup1, "grup2"=grup2,
              "PNL1EntrezID"=PNL1EntrezID,"PNL2EntrezID"=PNL2EntrezID,"CHAPL2EntrezID"=CHAPL2EntrezID))
  
}

#Calculates relevant rotations and PC values of a list of paired healthy-disease groups:
groupsVsDirectionCalculator <- function(PNList, numOfPCs=3, diseaseLevels, gexMat, grup1, grup2, representativeVersion, thresh=1e-4) {
  
  
  PNListBigEnough <- rmSmallPNGroups(PNList = PNList, numOfPCs = numOfPCs)
  relevantValues <- list()
  relevantRotations <- list()
  
  for(j in 1:length(grup1)){
    group1 <- grup1[j]
    group2 <- grup2[j]
    if((sum(diseaseLevels==group1) < numOfPCs) | (sum(diseaseLevels==group2) < numOfPCs)) {
      relevantValues[[paste(group1,"Vs",group2)]] <- "not enough samples!"
      relevantRotations[[paste(group1,"Vs",group2)]] <- "not enough samples!"
      next
    }
    tmpCalcPCs <- calcPairPCs(gexMat = gexMat,group1 = group1,group2 = group2,PNList = PNListBigEnough,
                              numOfPCs = numOfPCs,diseaseLevels = diseaseLevels)
    tmpReview <- PCSeperationReview(onlyPairPCValues = tmpCalcPCs$onlyPairPCValues,numOfPCs = numOfPCs,
                                    representativeVersion = representativeVersion, thresh=thresh)
    relevantValues[[paste(group1,"Vs",group2)]] <- tmpReview$onlyPairPCValuesWinners
    tmpRot <- tmpCalcPCs$PCRotations
    tmpRot <- lapply(X = 1:length(tmpRot), function(n) tmpRot[[n]][,tmpReview$winnerPCs[n]])
    tmpRot <- tmpRot[sapply(X = tmpRot,function(x) length(x)!=0)]
    names(tmpRot) <- rownames(relevantValues[[paste(group1,"Vs",group2)]])
    relevantRotations[[paste(group1,"Vs",group2)]] <- tmpRot
    print(paste((j/length(grup1))*100, "% finished"))
  }
  
  
  workedIndx <- sapply(X = relevantValues, function(x) is.numeric(x))
  
  
  relevantValuesSub <- relevantValues[workedIndx]
  relevantRotSub <- relevantRotations[workedIndx]
  relevantRotSub <- makeAllDirectionsPositive(relevantRotSub)
  return(list("relevantValuesSub"=relevantValuesSub,
              "relevantRotSub"=relevantRotSub,"PNListBigEnough"=PNListBigEnough,
              "relevantValues"=relevantValues,"relevantRotations"=relevantRotations))
}

#Calculate M-Scores from  main axis:
calcScoresSingularAxes <- function(inptVec, mainAxeses){
  wholeLength <- length(mainAxeses)
  outptVecList <- numeric(length = wholeLength)
  for(k in 1:wholeLength){
    geneNames <- names(mainAxeses[[k]])
    indx <- match(x = geneNames, table = names(inptVec))
    outptVecList[k] <- inptVec[na.omit(indx)] %*% mainAxeses[[k]][which(!is.na(indx))]
  }
  names(outptVecList) <- names(mainAxeses)
  return(outptVecList)
}

#Remove groups that has only a few genes (if you have less variables than PC
## dimensions you want to calculate, you're gonna have a problem):
rmSmallPNGroups <- function(PNList, numOfPCs){
  PNLength <- sapply(X = PNList, FUN = length)
  return(PNList[PNLength > numOfPCs])
}

#Combine all rotations(Axises) to one main axis:
makeMainAxisFromReleventRotations <- function(relevantRotSub, PNGroup = "ALL", PNList) {
  if(PNGroup == "ALL") {
    groupNames <- names(PNList)
    mainAxises <- list()
    for(groupName in groupNames){
      tmpMat <- sapply(X = relevantRotSub,function(x) 
        ifelse(length(grep(paste0("^",groupName," "),names(x)))!=0,x[grep(paste0("^",groupName," "),names(x))],"Didn't have that group"))
      notCharIndx <- sapply(X = tmpMat, function(x) !is.character(x)) # what if the first one didn't have the group? then in the next 2 line you'd have a problem!
      if(all(!notCharIndx)) stop(paste("No results found for",groupName))
      tmpMat <- as.matrix(as.data.frame(tmpMat[!sapply(tmpMat,FUN = is.character)],row.names = names(tmpMat[[which(notCharIndx)[1]]])))
      mainAxises[[groupName]] <- apply(X = tmpMat,MARGIN = 1,FUN = mean)
      resPCA <- pca(t(tmpMat), method="svd", center=F, nPcs=2,scale = "none")
      print(cor(resPCA@loadings[,1],apply(X = tmpMat,MARGIN = 1,FUN = mean)))
    }
  } else {
    tmpMat <- sapply(X = relevantRotSub,function(x) 
      ifelse(length(grep(paste0("^",PNGroup," "),names(x)))!=0,x[grep(paste0("^",PNGroup," "),names(x))],"Didn't have that group"))
    notCharIndx <- sapply(X = tmpMat, function(x) !is.character(x))
    if(all(!notCharIndx)) stop(paste("No results found for",groupName))
    tmpMat <- as.matrix(as.data.frame(tmpMat[!sapply(tmpMat,FUN = is.character)],row.names = names(tmpMat[[which(notCharIndx)[1]]])))
    mainAxises <- apply(X = tmpMat,MARGIN = 1,FUN = mean)
  }
  return(mainAxises)
}

# Calculate PC values and rotations for a pair group of disease:
calcPairPCs <- function(gexMat,group1,group2,PNList,numOfPCs,diseaseLevels) {
  indx <- group1 == diseaseLevels | group2 == diseaseLevels
  gexTmp <- gexMat[,indx]
  onlyPairPCValues <- matrix(NA,nrow = length(PNList)*numOfPCs,ncol = ncol(gexTmp))
  PCRotations <- list()
  require(pcaMethods)
  for(k in 1:length(PNList)){
    gexTmpSub <- gexTmp[na.omit(match(PNList[[k]],rownames(gexTmp))),]
    resPCA <- pca(t(gexTmpSub), method="svd", center=TRUE, nPcs=numOfPCs)
    scoreS <- resPCA@scores
    onlyPairPCValues[(1+(numOfPCs*(k-1))):(numOfPCs*k),] <- t(scoreS)
    PCRotations[[k]] <- resPCA@loadings
  }
  colnames(onlyPairPCValues) <- diseaseLevels[indx]
  rownames(onlyPairPCValues) <- paste(rep(names(PNList),each=numOfPCs),1:numOfPCs)
  names(PCRotations) <- names(PNList)
  return(list("onlyPairPCValues"=onlyPairPCValues,"PCRotations"=PCRotations))
}

#Check to see if PCA could separate disease from healthy:
PCSeperationReview <- function(onlyPairPCValues,numOfPCs,representativeVersion, thresh=1e-4) {
  PNGroupsNum <- nrow(onlyPairPCValues)/numOfPCs
  grups <- unique(colnames(onlyPairPCValues))
  if(length(grups)!=2) stop("Not two groups?!?!?!")
  indx1 <- colnames(onlyPairPCValues) == grups[1]
  indx2 <- colnames(onlyPairPCValues) == grups[2]
  winnerPCs <- numeric(length = PNGroupsNum)
  for(k in 1:PNGroupsNum){
    onlyPairPCValuesSub <- onlyPairPCValues[(1+((k-1)*numOfPCs)):(k*numOfPCs),]
    tmp <- apply(X = onlyPairPCValuesSub,MARGIN = 1,function(x) isSeperationPerfekt(grp1 = x[indx1],grp2 = x[indx2],thresh = thresh))
    if(all(is.na(tmp))) {
      winnerPCs[k] <- 0
    } else {
      if(representativeVersion){
        winnerPCs[k] <- 1
      } else {
        winnerPCs[k] <- order(abs(tmp))[1]
      }
    }
  }
  winnerOverallIndx <- winnerPCs+seq.default(from = 0,by = numOfPCs,length.out = PNGroupsNum)
  winnerOverallIndx <- winnerOverallIndx[winnerPCs!=0] # very messy way of removing crappy PCs!!
  onlyPairPCValuesWinners <- as.matrix(as.data.frame(onlyPairPCValues)[winnerOverallIndx,]) # don't want to have matrix2vector conversion
  return(list("winnerPCs"=winnerPCs,"onlyPairPCValuesWinners"=onlyPairPCValuesWinners))
}

#Used in PCSeperationReview function:
isSeperationPerfekt <- function(grp1,grp2,thresh=1e-4) {
  testRes <- t.test(grp1,grp2)
  if(testRes$p.value > thresh) {
    return(NA)
  } else if(testRes$statistic > 0) {
    return(testRes$p.value)
  } else if(testRes$statistic < 0) {
    return(-testRes$p.value)
  } else stop("Something went wrong here!")
}

#Make all PCA rotations uni-direction:
makeAllDirectionsPositive <- function(relevantRotSub){
  invertIfNeg <- function(VEC){
    if(sum(VEC) < 0) return(-VEC) else return(VEC)
  }
  relevantRotSubInved <- lapply(X = relevantRotSub, function(q) lapply(q,invertIfNeg))
  return(relevantRotSubInved)
}




#Does GSA (Gene Set Analysis) on a pair of healthy-disease group
gsaReview <- function(gexMat,group1,group2,PNList,diseaseLevels,method="summerize",restandarzation=T, SEED) {
  if(method == "summerize"){
    indx1 <- which(group1 == diseaseLevels)
    indx2 <- which(group2 == diseaseLevels)
    if(length(indx1)==1 & length(indx2)==1){
      stop("TwO SAMPLES ONLY? ARE YOU KIDDING ME???!")
    } else if(length(indx1)==1){
      indx1 <- rep(indx1,length(indx2))
    } else if(length(indx2)==1){
      indx2 <- rep(indx2,length(indx1))
    }
    gexMatReduced <- gexMat[,c(indx1,indx2)]
    classes <- c(rep(1,length(indx1)),rep(2,length(indx2)))
    require(GSA)
    GSA.obj<-tryCatch(GSA(gexMatReduced, classes, genenames=rownames(gexMatReduced),
                 genesets=PNList, resp.type="Two class unpaired", nperms=100,restand=restandarzation,minsize = 1,maxsize = 25000,
                 random.seed = SEED),
                 error = function(e) {NA}) #Sometimes GSA has the weirdest errors, I'll handle them with "try" for now
    return(GSA.obj)
  }
}

#Does gsa Review on a series of paired disease groups
gsaReviewWrapperAll <- function(gexMat,grup1,grup2,PNList,diseaseLevels,FDRcut=.5,mode="qualitative",submode="BOTH", restandarzation=T
                                , SEED=NULL){
  if(mode=="qualitative") {
    reviewTable <- matrix("Not Signif.",nrow = length(grup1),ncol = length(PNList))
    colnames(reviewTable) <- names(PNList)
    rownames(reviewTable) <- grup1
    for(k in 1:length(grup1)){
      tst <- gsaReview(gexMat = gexMat,group1 = grup1[k], group2 = grup2[k],PNList = PNList,
                       diseaseLevels = diseaseLevels, restandarzation = restandarzation, SEED=SEED)
      tst2 <- GSA.listsets(tst, geneset.names=names(PNList),FDRcut=FDRcut)
      if(!is.null(tst2$negative)) reviewTable[k,as.numeric(tst2$negative[,1])] <- rep("DOWN",nrow(tst2$negative))
      if(!is.null(tst2$positive)) reviewTable[k,as.numeric(tst2$positive[,1])] <- rep("UP",nrow(tst2$positive))
      
      print(k)
    }
  } else if(mode=="score") {
    reviewTable <- matrix(NA,nrow = length(grup1),ncol = length(PNList))
    colnames(reviewTable) <- names(PNList)
    rownames(reviewTable) <- grup1
    for(k in 1:length(grup1)){
      tst <- gsaReview(gexMat = gexMat,group1 = grup1[k], group2 = grup2[k],PNList = PNList,
                                diseaseLevels = diseaseLevels,restandarzation = restandarzation, SEED=SEED)
      if(anyNA(tst)) {
        warning("GSA broke!!!")
        next
      }
      if(anyNA(tst$pvalues.lo)) warning(c("Problem in calculating downregulation p values for",grup1[k],"!"))
      tst$pvalues.lo[is.na(tst$pvalues.lo)] <- 1
      if(anyNA(tst$pvalues.hi)) warning(c("Problem in calculating upregulation p values for",grup1[k],"!"))
      tst$pvalues.hi[is.na(tst$pvalues.hi)] <- 1
      if(submode=="BOTH"){
        reviewTable[k,] <- (1-tst$pvalues.hi) - (1-tst$pvalues.lo)
      } else if(submode=="HI"){
        reviewTable[k,] <- (1-tst$pvalues.hi)
      } else if(submode=="LO"){
        reviewTable[k,] <- - (1-tst$pvalues.lo)
      } else if(submode=="GSAScores"){
        reviewTable[k,] <- tst$GSA.scores
      }
      print(k)
    }
  }
  return(reviewTable)
}

#For calculating a group against all other genome(in randomized same-sized groups for removing the effect of size)
gsaReviewEqualRamdomized <- function(gexMat,grup1,grup2,PNList,diseaseLevels,FDRcut=.5,submode="BOTH"
                                     ,restandarzation=T,SEED=NULL,repetations=10) {
  if(length(PNList) != 2 | names(PNList)[2] != "Others") stop("PNList needs to be two groups: First one the group you want to study and
                                                              second one is all the other genes in gexMax not included in the first group")
  PNListReduced <- PNList
  risaaltz <- list()
  print("Starting ramdomaziation...")
  for(R in 1:repetations){
    cat("Iteration",as.character(R))
    set.seed(R) #Something's messing up the seed, probably GSA that comes later,
    ## if I don't set the seed here in some computers the output of sample will be always the same!!!
    PNListReduced[[2]] <- sample(size = length(PNList[[1]]),x = PNList[[2]])
    risaaltz[[R]] <- gsaReviewWrapperAll(gexMat=gexMat,grup1=grup1,grup2=grup2,PNList=PNListReduced,diseaseLevels=diseaseLevels,
                                         FDRcut=FDRcut,mode="score",submode=submode,restandarzation=restandarzation,SEED=SEED)
  }
  return(risaaltz)
}

#For summarising gsaReviewEqualRamdomized output:
gsaReviewEqualRamdomizedSummarizer <- function(gsaReviewEqualRamdomizedOutput) {
  if(!is.list(gsaReviewEqualRamdomizedOutput)) stop("INPUT WRONG!!!")
  LeN <- length(gsaReviewEqualRamdomizedOutput)
  risaaltzSummed <- unlist(gsaReviewEqualRamdomizedOutput[1])
  risaaltzSummed[is.na(risaaltzSummed)] <- 0 # So one NA won't make everything NA
  for(K in 2:LeN){
    tmpRisaaltz <- unlist(gsaReviewEqualRamdomizedOutput[K])
    tmpRisaaltz[is.na(tmpRisaaltz)] <- 0
    risaaltzSummed <- risaaltzSummed + tmpRisaaltz
  }
  risaaltzSummed <- risaaltzSummed / LeN
  risaaltzSummed <- matrix(data = risaaltzSummed, nrow = nrow(gsaReviewEqualRamdomizedOutput[[1]]), 
                           ncol = ncol(gsaReviewEqualRamdomizedOutput[[1]]))
  dimnames(risaaltzSummed) <- dimnames(gsaReviewEqualRamdomizedOutput[[1]])
  return(risaaltzSummed)
}

