parseEval <- function (c1, c2, c3, cipi12, cipi23, voweld, anchor=15, var_anchor=3, types, words=12, simN=1000, RE_rsd, CC_rsd, LE_rsd) {
  # basic validy-check ... input parameters
  c1<-as.numeric(c1)
  c2<-as.numeric(c2)
  c3<-as.numeric(c3)
  cipi12<-as.numeric(cipi12)
  cipi23<-as.numeric(cipi23)
  voweld<-as.numeric(voweld)
  anchor<-as.integer(anchor)
  var_anchor<-as.integer(var_anchor)
  types<-as.integer(types)
  words<-as.integer(words)
  simN<-as.integer(simN)
  RE_rsd<-as.numeric(RE_rsd)
  CC_rsd<-as.numeric(CC_rsd)
  LE_rsd<-as.numeric(LE_rsd)
  # phonetic parameters
  C1p<-c3[1] # plateau duration of the first consonant in triconsonantal clusters
  C1stdv<-c3[2] # standard deviation of the first consonant in triconsonantal clusters
  C2p<-c2[1] # plateau duration of the second consonant in triconsonantal clusters and the first consonant in bi-consonantal clusters
  C2stdv<-c2[2] # standard deviation of the second consonant in triconsonantal clusters and the first consonant in bi-consonantal clusters 
  C3p<-c1[1] # plateau duration of the immediately prevocalic consonant
  C3stdv<-c1[2] # standard deviation of the immediately prevocalic consonant
  C12ipi<-cipi12[1] # the duration of the interval between the plateaus of the first two consonants in triconsonantal clusters
  C12stdv<-cipi12[2] # the standard deviation of the interval between the plateaus of the first two consonants in triconsonantal clusters
  C23ipi<-cipi23[1] # the duration of the interval between the plateaus of the first two consonants in biconsonantal clusters and between the second two consonants in triconsonantal clusters
  C23stdv<-cipi23[2] # the standard deviation of the interval between the plateaus of the first two consonants in biconsonantal clusters and between the second two consonants in triconsonantal clusters
  vowel_duration<-voweld # the duration of the vowel
  variability_range<-anchor # number of stepwise increases in variability simulated by the model
  variability_resolution<-var_anchor # size of each stepwise increase in variability
  words_per_word_type<-words # the number of words (stimuli) per word type, aka "little n"
  word_types<-types # number of different word types, e.g. #CV-, #CCV-, #CCCV-
  data_RSD<-c(RE_rsd, LE_rsd, CC_rsd) # lumps RSD measures into single array
  #creating matrices for later use
  A_simp <- matrix(nrow=variability_range, ncol=words_per_word_type)
  A_comp <- matrix(nrow=variability_range, ncol=words_per_word_type)
  # creating matrices to hold the SD values
  LE_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  LE_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_SD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_SD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  # creating matrices to hold the RSD values
  LE_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  LE_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  RE_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_RSD_simp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  CC_RSD_comp<-matrix(nrow=simN, ncol=variability_range, byrow=TRUE)
  if (word_types==3) {
    tepa<-c("Testing Triads")
    # print(c("Simulating Data (Triads)"), quote=F)
    # pb <- txtProgressBar(min = 0, max = simN, style = 3)
    for (count in 1:simN) {
      # setTxtProgressBar(pb, count)
      # generate CCC tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for C3
      e <- C3stdv*(rnorm(1))
      # generate R(ight plateau edge = Release) of prevocalic consonant
      # generate words_per_word_type/word_types Gaussian distributed numbers (for CCC tokens only)
      # with mean 500, variance 10
      CCCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20))
      # generate L(eft plateau edge = Target) of prevocalic consonant  
      CCCL3 <- CCCR3 - C3p + e #generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCCM3 <- ((CCCR3 + CCCL3) / 2)
      # generate timestamps for C2
      # generate general error-term for C2
      e1 <- C23stdv * (rnorm(1)) #normally distributed random error mean=0, sd=1
      e2 <- C2stdv * (rnorm(1)) #normally distributed random error mean=0, sd=1
      # Generate right edge of C2
      CCCR2 <- CCCL3 - C23ipi + e1 # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCCL2 <- CCCR2 - C2p + e2 # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCCM2 <- ((CCCR2+CCCL2)/2)
      # generate timestamps for C1
      # generate general error-term for C1
      e1 <- C12stdv * (rnorm(1)) # normally distributed random error
      e2 <- C3stdv * (rnorm(1))
      # Generate right edge 
      CCCR1 <- CCCL2 - C12ipi + e1 # generate right edge of C1 from left edge of C2 assuming ipi of 40ms
      # generate L(eft plateau edge = Target) of C1
      CCCL1 <- CCCR1 - C3p + e2 # generate L2 corresponding to CR1 by assuming a plateau of 10ms
      # calculate midpoint of prevocalic consonant
      CCCM1 <-  ((CCCR1 + CCCL1)/2) # right edge of C1
      #generate CC tokens
      #generate timestamps for C3 (prevocalic consonant)
      # generate general error-term for C3
      e <- C3stdv * (rnorm(1)) # normally distributed random error
      # generate R(ight plateau edge = Release) of prevocalic consonant
      CCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant
      CCL3 <- CCR3 - C3p + e # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCM3 <- ((CCR3 + CCL3) / 2)
      #generate timestamps for C2
      # generate general error-term for C2
      e1 <- C23stdv * (rnorm(1))
      e2 <- C2stdv * (rnorm(1))
      # Generate right edge of C2
      CCR2 <- CCL3 - C23ipi + e1 # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCL2 <- CCR2 - C2p + e2 # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCM2 <- ((CCR2 + CCL2) / 2)
      # generate C tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for C3
      e <- C3stdv * (rnorm(1))
      # Generate R(ight plateau edge = Release) of prevocalic consonant
      CR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant 
      CL3 <- CR3 - C3p + e # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CM3 <- ((CR3 + CL3) / 2)
      # generate timestamps for CCglobal
      # for CCC clusters
      CCglobal <- apply(cbind(CCCM1, CCCM2, CCCM3), 1, mean) #mean of consonant plateaux midpoints        
      # for CC clusters
      CCglobal <- append(CCglobal, apply(cbind(CCM2, CCM3), 1, mean)) # mean of consonant plateaux midpoints
      # for C clusters
      CCglobal <- append(CCglobal, CM3)
      # populate a single array with the midpoint of the pre-vocalic
      # consonant of every word type; this array will be used to generate anchors
      # for CCC clusters
      Global_CM3 <- CCCM3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CM3 <- append(Global_CM3, CCM3) # mean of consonant plateaux midpoints
      # for C clusters
      Global_CM3 <- append(Global_CM3, CM3)
      # populate a single array with the Left_edge of the consonant cluster for every token
      # this array will be used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CL1 <- CCCL1 # Assigns the left edge of tri-consonantal tokens to the first third of Global_Cl1
      # for CC clusters
      Global_CL1 <- append(Global_CL1, CCL2) # Assigns the left edge of bi-consonantal tokens to the second third of Global_Cl1
      # for C clusters
      Global_CL1 <- append(Global_CL1, CL3) # Assigns the left edge of mono-consonantal tokens to the last third of Global_Cl1
      # populate a single array with the Right_edge of the consonant cluster for every token
      # this array is used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CR3 <- CCCR3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CR3 <- append(Global_CR3, CCR3) # mean of consonant plateaux midpoints
      # for C clusters
      Global_CR3 <- append(Global_CR3, CR3) # CCglobal synchronous with prevocalic consonant's plateau midpoint
      # generate series of anchor points increasing  in variability and/or distance from
      # the prevocalic consonant reset the anchor array to zero
      # one row for each anchor and one column for each token
      
      # loop produces data/anchor for each token based on Simplex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset anchor-error-term
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(n=1)) #normally distributed random error, assuming mean of 0
          A_simp[cycle, m] <- Global_CM3[m] + vowel_duration + Ae #generate anchor A according to the simplex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # loop produces data/anchor for each token based on Complex Hypothesis
      stdv <- 0 # reset the value of the anchor stdev to zero
      Ae <- NULL # reset anchor-error-term
      for (cycle in 1:variability_range) { #creates multiple anchor points for each token
        for (m in 1:words_per_word_type) { #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(1)) #normally distributed random error, assuming mean of 0
          A_comp[cycle, m]<-CCglobal[m]+vowel_duration+Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      # Note about consonantal landmarks:
      # they are replaced with each cycle of the simulation
      # in constrast, RSD values for each landmark are stored across simulations.
      # creating matrices to hold the SD values
      x <- function(x) {sd(x-Global_CL1)}
      y <- function(y) {sd(y-Global_CR3)}
      z <- function(z) {sd(z-CCglobal)}
      # computing the SD values
      LE_SD_simp[count,] <- apply(A_simp, 1, x)
      LE_SD_comp[count,] <- apply(A_comp, 1, x)
      RE_SD_simp[count,] <- apply(A_simp, 1, y)
      RE_SD_comp[count,] <- apply(A_comp, 1, y)
      CC_SD_simp[count,] <- apply(A_simp, 1, z)
      CC_SD_comp[count,] <- apply(A_comp, 1, z)
      # computing the RSD values
      LE_RSD_simp[count,] <- (apply(A_simp, 1, x))/((apply(A_simp, 1, mean))-mean(Global_CL1))
      LE_RSD_comp[count,] <- (apply(A_comp, 1, x))/((apply(A_comp, 1, mean))-mean(Global_CL1))
      RE_RSD_simp[count,] <- (apply(A_simp, 1, y))/((apply(A_simp, 1, mean))-mean(Global_CR3))
      RE_RSD_comp[count,] <- (apply(A_comp, 1, y))/((apply(A_comp, 1, mean))-mean(Global_CR3))
      CC_RSD_simp[count,] <- (apply(A_simp, 1, z))/(apply(A_simp, 1, mean)-mean(CCglobal))
      CC_RSD_comp[count,] <- (apply(A_comp, 1, z))/(apply(A_comp, 1, mean)-mean(CCglobal))
    }
    # close(pb)
  }
  if (word_types==2) {
    tepa<-c("Testing Dyads")
    # print(c("Simulating Data (Dyads)"), quote=F)
    # pb <- txtProgressBar(min = 0, max = simN, style = 3)
    for (count in 1:simN) {
      # setTxtProgressBar(pb, count)
      # generate CCC tokens
      # generate timestamps for C3 (the prevocalic consonant)
      # generate general error-term for C3
      e <- C3stdv * (rnorm(1))
      # generate R(ight plateau edge = Release) of prevocalic consonant
      # generate words_per_word_type/word_types Gaussian distributed numbers (for CCC tokens only)
      # with mean 500, variance 10
      CCCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20))
      # generate L(eft plateau edge = Target) of prevocalic consonant  
      CCCL3 <- abs(CCCR3 - C3p + e) #generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCCM3 <- abs((CCCR3 + CCCL3) / 2)
      # generate timestamps for C2
      # generate general error-term for C2
      e1 <- C23stdv * (rnorm(1)) #normally distributed random error
      e2 <- C2stdv * (rnorm(1)) #normally distributed random error
      # Generate right edge of C2
      CCCR2 <- abs(CCCL3 - C23ipi + e1) # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCCL2 <- abs(CCCR2 - C2p + e2) # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCCM2 <- abs((CCCR2 + CCCL2) / 2)
      # generate timestamps for C1
      # generate general error-term for C1
      e1 <- C12stdv * (rnorm(1)) # normally distributed random error
      e2<-C3stdv * (rnorm(1))
      # Generate right edge 
      CCCR1 <- abs(CCCL2 - C12ipi + e1) # generate right edge of C1 from left edge of C2 assuming ipi of 40ms
      # generate L(eft plateau edge = Target) of C1
      CCCL1 <- abs(CCCR1 - C3p + e2) # generate L2 corresponding to CR1 by assuming a plateau of 10ms
      # calculate midpoint of prevocalic consonant
      CCCM1 <-  abs((CCCR1 + CCCL1) / 2) # right edge of C1
      #generate CC tokens
      #generate timestamps for C3 (prevocalic consonant)
      # generate general error-term for C3
      e <- C3stdv * (rnorm(1)) # normally distributed random error, 0 mean
      # generate R(ight plateau edge = Release) of prevocalic consonant
      CCR3 <- rnorm(words_per_word_type/word_types, mean=500, sd=sqrt(20)) # generate N Gaussian distributed numbers with mean 500, variance 10
      # generate L(eft plateau edge = Target) of prevocalic consonant
      CCL3 <- abs(CCR3 - C3p + e) # generate L3 corresponding to R3 by assuming a plateau duration of C3p
      # calculate midpoint of prevocalic consonant plateau
      CCM3 <- abs((CCR3 + CCL3) / 2)
      #generate timestamps for C2
      # generate general error-term for C2
      e1 <- C23stdv * (rnorm(1))
      e2 <- C2stdv * (rnorm(1))
      # Generate right edge of C2
      CCR2 <- abs(CCL3 - C23ipi + e) # generate right edge of C2 from left edge of C3 assuming an ipi of C23ipi
      # Generate left edge of C2
      CCL2 <- abs(CCR2 - C2p + e) # generate left edge from right edge by assuming a plateau duration
      # Calculate midpoint of C2
      CCM2 <- abs((CCR2 + CCL2) / 2)
      # generate timestamps for CCglobal
      # for CCC clusters
      CCglobal <- apply(cbind(CCCM1, CCCM2, CCCM3), 1, mean) #mean of consonant plateaux midpoints        
      # for CC clusters
      CCglobal <- append(CCglobal, apply(cbind(CCM2, CCM3), 1, mean)) # mean of consonant plateaux midpoints
      # populate a single array with the midpoint of the pre-vocalic
      # consonant of every word type; this array will be used to generate anchors
      # for CCC clusters
      Global_CM3 <- CCCM3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CM3 <- append(Global_CM3, CCM3, after=length(CCCM3)) # mean of consonant plateaux midpoints
      # populate a single array with the Left_edge of the consonant cluster for every token
      # this array will be used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CL1 <- CCCL1 # Assigns the left edge of tri-consonantal tokens to the first third of Global_Cl1
      # for CC clusters
      Global_CL1 <- append(Global_CL1, CCL2, after=length(CCCL1)) # Assigns the left edge of bi-consonantal tokens to the second third of Global_Cl1
      # populate a single array with the Right_edge of the consonant cluster for every token
      # this array is used to calculate SD and RSD for EDGE to Anchor intervals
      # for CCC clusters
      Global_CR3 <- CCCR3 # mean of consonant plateaux midpoints
      # for CC clusters
      Global_CR3 <- append(Global_CR3, CCR3, after=length(CCCR3)) # mean of consonant plateaux midpoints
      # generate series of anchor points increasing
      # in variability and/or distance from the prevocalic consonant
      stdv <- 0
      Ae <- NULL
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(n=1)) #normally distributed random error, assuming mean of 0
          A_simp[cycle, m]<-Global_CM3[m] + vowel_duration + Ae #generate anchor A according to the simplex onset hypothesis
        }
        stdv<-stdv+variability_resolution
      }
      # loop produces anchor for each token based on Complex Hypothesis
      stdv <- 0
      Ae <- NULL
      for (cycle in 1:variability_range){ #creates multiple anchor points for each token
        for (m in 1:words_per_word_type){ #creates anchor point for each token from the right edge of the token
          Ae<-stdv*(rnorm(1)) #normally distributed random error, assuming mean of 0
          A_comp[cycle, m]<-CCglobal[m]+vowel_duration+Ae #generate anchor A according to the complex onset hypothesis
        }
        stdv<-stdv+variability_resolution #creates new anchor point
      }
      #creating matrices to hold the SD values
      x <- function(x) {sd(x-Global_CL1)}
      y <- function(y) {sd(y-Global_CR3)}
      z <- function(z) {sd(z-CCglobal)}
      # computing the SD values
      LE_SD_simp[count,] <- abs(apply(A_simp, 1, x))
      LE_SD_comp[count,] <- abs(apply(A_comp, 1, x))
      RE_SD_simp[count,] <- abs(apply(A_simp, 1, y))
      RE_SD_comp[count,] <- abs(apply(A_comp, 1, y))
      CC_SD_simp[count,] <- abs(apply(A_simp, 1, z))
      CC_SD_comp[count,] <- abs(apply(A_comp, 1, z))
      # computing the RSD values
      LE_RSD_simp[count,] <- abs((apply(A_simp, 1, x))/((apply(A_simp, 1, mean))-mean(Global_CL1)))
      LE_RSD_comp[count,] <- abs((apply(A_comp, 1, x))/((apply(A_comp, 1, mean))-mean(Global_CL1)))
      RE_RSD_simp[count,] <- abs((apply(A_simp, 1, y))/((apply(A_simp, 1, mean))-mean(Global_CR3)))
      RE_RSD_comp[count,] <- abs((apply(A_comp, 1, y))/((apply(A_comp, 1, mean))-mean(Global_CR3)))
      CC_RSD_simp[count,] <- abs((apply(A_simp, 1, z))/(apply(A_simp, 1, mean)-mean(CCglobal)))
      CC_RSD_comp[count,] <- abs((apply(A_comp, 1, z))/(apply(A_comp, 1, mean)-mean(CCglobal)))
    }
  }
  # close(pb)
  # pb <- txtProgressBar(min = 1, max = variability_range, style = 3)
  # assorted variables for diagnostics / plotting
  aip_1<-rep(c(1:variability_range), 3)
  edgep_1<-rep(c("LE_RSD", "RE_RSD", "CC_RSD"), each=variability_range)
  LE_RSD_simp_median<-apply(apply(LE_RSD_simp, 2, sort), 2, median)
  RE_RSD_simp_median<-apply(apply(RE_RSD_simp, 2, sort), 2, median)
  CC_RSD_simp_median<-apply(apply(CC_RSD_simp, 2, sort), 2, median)
  LE_RSD_comp_median<-apply(apply(LE_RSD_comp, 2, sort), 2, median)
  RE_RSD_comp_median<-apply(apply(RE_RSD_comp, 2, sort), 2, median)
  CC_RSD_comp_median<-apply(apply(CC_RSD_comp, 2, sort), 2, median)
  simp<-c(LE_RSD_simp_median, RE_RSD_simp_median, CC_RSD_simp_median)
  comp<-c(LE_RSD_comp_median, RE_RSD_comp_median, CC_RSD_comp_median)
  RE_RSD_median<-c(RE_RSD_simp_median, RE_RSD_comp_median)
  CC_RSD_median<-c(CC_RSD_simp_median, CC_RSD_comp_median)
  # median RDSs across simulations as a function of anchorindex
  plot.1<-data.frame(anchorindex=aip_1, edge=edgep_1, parse_s=simp, parse_c=comp)
  # aggregating data for goodness of fit evaluation
  RE_RSD_simp<-t(RE_RSD_simp)
  LE_RSD_simp<-t(LE_RSD_simp)
  CC_RSD_simp<-t(CC_RSD_simp)
  RE_RSD_comp<-t(RE_RSD_comp)
  LE_RSD_comp<-t(LE_RSD_comp)
  CC_RSD_comp<-t(CC_RSD_comp)
  # looping through the data to get the gof results
  data_simp<-matrix(ncol=4)
  data_comp<-matrix(ncol=4)
  sigfit<-function(x) {
    if(x > 98.503) {
      SigFit<-1
    } else {
      SigFit<-0
    }
  }
  # analyzing data simplex
  # print(c("Analysing... simple parse"), quote=F)
  for (i in 1 : variability_range) {
    # setTxtProgressBar(pb, i)
    sim_RSD<-cbind(RE_RSD_simp[i,], LE_RSD_simp[i,],CC_RSD_simp[i,])
    temp<-apply(sim_RSD, 1, function(x) (lm(data_RSD ~ x)))
    # organizing data for final analyses
    # creating anchor-index
    anchor_idx<-rep(i, times=simN)
    # extracting F-Statistics
    fstat<-unlist(lapply(temp, function(x) summary(x)$fstatistic[1]))
    # extracting R-Squared values
    rsquared<-unlist(lapply(temp, function(x) summary(x)$r.squared))
    # check for SigFit
    sgf<-sapply(fstat, sigfit)
    # aggregating data
    agg_mat<-matrix(data=c(anchor_idx, fstat, rsquared, sgf), nrow=length(anchor_idx), ncol=4, dimnames=list(c(NULL), c("Anchorindex", "Fratio", "Rsquared", "SigFit")))
    # adding sgf to existing data
    data_simp<-rbind(data_simp, agg_mat)
  }
  outp_sp<-temp
  data_simp<-data_simp[complete.cases(data_simp),]
  data_simp<-as.data.frame(data_simp)
  data_simp$Anchorindex<-as.factor(data_simp$Anchorindex)
  output_simp<-tapply(data_simp$SigFit, data_simp$Anchorindex, sum)
  # analyzing data complex
  # print(c("Analysing... complex parse"), quote=F)
  for (i in 1 : variability_range) {
    # setTxtProgressBar(pb, i)
    sim_RSD<-cbind(RE_RSD_comp[i,], LE_RSD_comp[i,],CC_RSD_comp[i,])
    temp<-apply(sim_RSD, 1, function(x) (lm(data_RSD ~ x)))
    # organizing data for final analyses
    anchor_idx<-rep(i, times=simN)
    # extracting F-Statistics
    fstat<-unlist(lapply(temp, function(x) summary(x)$fstatistic[1]))
    # extracting R-Squared values
    rsquared<-unlist(lapply(temp, function(x) summary(x)$r.squared))
    # check for SigFit
    sgf<-sapply(fstat, sigfit)
    # aggregating data
    agg_mat<-matrix(data=c(anchor_idx, fstat, rsquared, sgf), nrow=length(anchor_idx), ncol=4, dimnames=list(c(NULL), c("Anchorindex", "Fratio", "Rsquared", "SigFit")))
    # adding sgf to existing data
    data_comp<-rbind(data_comp, agg_mat)
  }
  outp_cp<-temp
  data_comp<-data_comp[complete.cases(data_comp),]
  data_comp<-as.data.frame(data_comp)
  data_comp$Anchorindex<-as.factor(data_comp$Anchorindex)
  output_comp<-tapply(data_comp$SigFit, data_comp$Anchorindex, sum)
  # diagnostic plot 2
  output_plot.2<-cbind(output_simp, output_comp)
  names(output_plot.2)<-NULL
  colnames(output_plot.2)<-c("parse_s", "parse_c")
  aip_2<-(1:variability_range)
  plot.2<-data.frame(anchorindex=aip_2, output_plot.2, hitr_s=(output_simp/simN), hitr_c=(output_comp/simN))
  # assessing overall model quality
  # sum of hits per number of simulations
  modq_s<-(sum(plot.2[,2]))/simN
  modq_c<-(sum(plot.2[,3]))/simN
  # assorted data for third diagnostic plot
  # sorting by Rsquared (asc), tie-breaker by Fratio (asc)
  data_simp_o<-data_simp[order(data_simp[,3], data_simp[,2]),]
  data_comp_o<-data_comp[order(data_comp[,3], data_comp[,2]),]
  aip_3<-rep(c(1:variability_range), 2)
  parse.f<-rep(c("simp","comp"), each=variability_range)
  # median
  simp_rs_median<-tapply(data_simp_o$Rsquared, data_simp_o$Anchorindex, median)
  comp_rs_median<-tapply(data_comp_o$Rsquared, data_comp_o$Anchorindex, median)
  simp_fr_median<-tapply(data_simp_o$Fratio, data_simp_o$Anchorindex, median)
  comp_fr_median<-tapply(data_comp_o$Fratio, data_comp_o$Anchorindex, median)
  rs_median<-c(simp_rs_median, comp_rs_median)
  fr_median<-c(simp_fr_median, comp_fr_median)
  plot.3_median<-data.frame(anchorindex=aip_3, parse=parse.f, rs_median=rs_median, fr_median=fr_median)
  # mean
  simp_rs_mean<-tapply(data_simp_o$Rsquared, data_simp_o$Anchorindex, mean)
  comp_rs_mean<-tapply(data_comp_o$Rsquared, data_comp_o$Anchorindex, mean)
  simp_fr_mean<-tapply(data_simp_o$Fratio, data_simp_o$Anchorindex, mean)
  comp_fr_mean<-tapply(data_comp_o$Fratio, data_comp_o$Anchorindex, mean)
  rs_mean<-c(simp_rs_mean, comp_rs_mean)
  fr_mean<-c(simp_fr_mean, comp_fr_mean)
  plot.3_mean<-data.frame(anchorindex=aip_3, parse=parse.f, rs_mean=rs_mean, fr_mean=fr_mean)
  # prepare for output
  # close(pb)
  output<-list("perf"=list("Performance Simple"=modq_s, "Performance Complex"=modq_c), "mode"=tepa, "Plot_1"=plot.1, "Plot_2"=plot.2, "Plot_3"=list("mean"=plot.3_mean, "median"=plot.3_median), "reg"=list("simplex_parse"<-outp_sp, "complex_parse"<-outp_cp), "sim_RSD"=list("simp"=data_simp, "comp"=data_comp))
  cat("\n", "\n","Overall Quality of Modell-Performance", "\t", "(", tepa, ")", "\n",
      "(Ratio of:","\t", "Total Number of Hits / Number of Simulations)","\n",
      "------------------------","\n",
      "Simple Modelling:", "\t", modq_s, "\t","\t","\t","\t", sum(plot.2[,2])," / ", simN, "\n", "\n",
      "Complex Modelling:", "\t", modq_c, "\t","\t","\t","\t", sum(plot.2[,3])," / ", simN, "\n", "\n", sep="")
  return(invisible(output))
}