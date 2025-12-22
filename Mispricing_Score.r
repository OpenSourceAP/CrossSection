##
library(data.table)
library(tidyverse)
library(dtplry)
library(magrittr)
DT_CRSP <- fread("Data/CRSP.csv")
## Standard Filter is applied to the DT_CRSP 
DT_CRSP$Date = DT_CRSP$date %>% ceiling_date(., "m") %>% add(-1)
DT_CRSP <- DT_CRSP %>% filter( SHRCD %in% c(10,11), EXCHCD %in% c(1,2,3)) %>% as_dt
DT_CRSP$date <- NULL
DT_CRSP$Date %<>% ymd()

###### From OAPS 

DT_Mom12 <- fread("Data/Misp/Mom12m.csv")
DT_Share1Y <- fread("Data/Misp/ShareIss1Y.csv")
DT_Accrual <- fread("Data/Misp/Accruals.csv")
DT_NOA <- fread("Data/Misp/NOA.csv")
DT_GP <- fread("Data/Misp/GP.csv")
DT_Roa <- fread("Data/Misp/roaq.csv")
DT_AG <- fread("Data/Misp/AssetGrowth.csv")
DT_PPE <- fread("Data/Misp/InvestPPEInv.csv")
DT_Comp <- fread("Data/Misp/CompEquIss.csv")
DT_Failure <- fread("Data/FailureProbability.csv")

################################
DT_OAPS_CRSP <- DT_CRSP %>% select(PERMNO,Date,ALTPRC) %>% 
  filter( abs(ALTPRC) > 5 ) %>% as_dt 
###################
DT_OAPS_CRSP <- DT_OAPS_CRSP %>% rename(permno = PERMNO) %>% 
  left_join(DT_Mom12) %>% left_join(DT_Share1Y) %>%
  left_join(DT_Accrual) %>% left_join(DT_NOA) %>%
  left_join(DT_GP) %>%
  left_join(DT_Roa) %>% left_join(DT_AG) %>%
  left_join(DT_PPE) %>% left_join(DT_Comp) %>%
  left_join(DT_Failure) %>% as_dt
#
DT_OAPS_CRSP$Date <- DT_OAPS_CRSP$yyyymm * 100 + 1
DT_OAPS_CRSP$Date <- ymd(DT_OAPS_CRSP$Date)
DT_OAPS_CRSP$Date <- ceiling_date(DT_OAPS_CRSP$Date ,"m") -1 

DT_OAPS_CRSP %>% 
  group_by(Date) %>% 
  mutate( N_Roa = sum( (!is.na(roaq)) ) , 
          N_ShareIss1Y = sum( (!is.na(ShareIss1Y))),
          N_Mom12 = sum( (!is.na(Mom12m))),
          N_GP = sum( (!is.na(GP))),
          N_Accruals = sum( (!is.na(Accruals))), 
          N_NOA = sum( (!is.na(NOA))),
          N_Comp = sum( (!is.na(CompEquIss))),
          N_Inv = sum( (!is.na(InvestPPEInv))),
          N_Failure = sum( (!is.na(FailureProbability)))
          ) %>% ungroup() %>% 
  as_dt -> DT_OAPS_CRSP


DT_OAPS_CRSP <- DT_OAPS_CRSP %>%
  mutate( roaq = ifelse(N_Roa < 30 , roaq, NA), 
          ShareIss1Y = ifelse(N_ShareIss1Y < 30 , ShareIss1Y, NA),
          Mom12m = ifelse(N_Mom12 < 30 , Mom12m, NA),
          GP = ifelse(N_GP < 30 , GP, NA),
          Accruals = ifelse(N_Accruals < 30 , Accruals, NA),
          NOA = ifelse(N_NOA < 30 , NOA, NA),
          CompEquIss = ifelse(N_Comp < 30 , CompEquIss, NA),
          InvestPPEInv = ifelse(N_Inv < 30 , InvestPPEInv, NA), 
          FailureProbability = ifelse(N_Failure < 30 , FailureProbability, NA)
        ) %>% 
  as_dt 


DT_OAPS_CRSP_MISP <- DT_OAPS_CRSP %>% 
  select(-ALTPRC) %>%
  group_by(Date) %>%
  mutate( Anom1_Rank = percent_rank(Mom12m ) ,
          Anom2_Rank = percent_rank(-ShareIss1Y) ,
          Anom3_Rank = percent_rank(-Accruals) ,
          Anom4_Rank = percent_rank(-NOA) ,
          Anom5_Rank = percent_rank(GP) ,
          Anom6_Rank = percent_rank(roaq) ,
          Anom7_Rank = percent_rank(-AssetGrowth) ,
          Anom8_Rank = percent_rank(-CompEquIss) ,
          Anom9_Rank = percent_rank(-InvestPPEInv) ,
          Anom10_Rank = percent_rank(FailureProbability)
  ) %>% 
  ungroup() %>% as_dt 

DT_Misp_OAPS_New <- DT_OAPS_CRSP_MISP %>%
  mutate(
    valid_anomalies = (!is.na(Anom1_Rank)) +  (!is.na(Anom2_Rank)) + (!is.na(Anom3_Rank)) +
      (!is.na(Anom4_Rank)) + (!is.na(Anom5_Rank)) + (!is.na(Anom6_Rank)) +
      (!is.na(Anom7_Rank)) + (!is.na(Anom8_Rank)) + (!is.na(Anom9_Rank)) +
      (!is.na(Anom10_Rank))   ,
    Anom1_Rank_NA = ifelse(is.na(Anom1_Rank),0,Anom1_Rank),
    Anom2_Rank_NA = ifelse(is.na(Anom2_Rank),0,Anom2_Rank),
    Anom3_Rank_NA = ifelse(is.na(Anom3_Rank),0,Anom3_Rank),
    Anom4_Rank_NA = ifelse(is.na(Anom4_Rank),0,Anom4_Rank),
    Anom5_Rank_NA = ifelse(is.na(Anom5_Rank),0,Anom5_Rank),
    Anom6_Rank_NA = ifelse(is.na(Anom6_Rank),0,Anom6_Rank),
    Anom7_Rank_NA = ifelse(is.na(Anom7_Rank),0,Anom7_Rank),
    Anom8_Rank_NA = ifelse(is.na(Anom8_Rank),0,Anom8_Rank),
    Anom9_Rank_NA = ifelse(is.na(Anom9_Rank),0,Anom9_Rank),
    Anom10_Rank_NA = ifelse(is.na(Anom10_Rank),0,Anom10_Rank),
    MISP = ifelse(valid_anomalies >= 5 , 
                  (Anom1_Rank_NA + Anom2_Rank_NA + Anom3_Rank_NA + Anom4_Rank_NA + 
                     Anom5_Rank_NA + Anom6_Rank_NA + Anom7_Rank_NA + Anom8_Rank_NA + 
                     Anom9_Rank_NA + Anom10_Rank_NA  ) / valid_anomalies , NA)
  ) %>% select( PERMNO , Date , MISP) %>%
 mutate( OAPS_MISP = 100 - 100 * MISP) %>% select(-MISP) %>% as_dt

# Construct average rank for equity with at least 5 anomaly information




