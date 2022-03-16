# script for converting OldOldSignalDocumentation.xlsx into two csvs
# 2022 03 

library(tidyverse)
library(readxl)

# PROCESS BASIC AND ADD INFO ====

# read in basic info
basic_info = read_excel('OldSignalDocumentation.xlsx', sheet = 'BasicInfo') %>% 
  select(-c(`Note on Cat.Signal`, SampleStartMonth, SampleEndMonth) )

# read in add info
add_info   = read_excel('OldSignalDocumentation.xlsx', sheet = 'AddInfo') %>% 
  select(-Authors, -`Cat.Signal Formula`)

# merge, clean, and write
alldoc = 
  basic_info %>% 
  left_join(add_info) %>% 
  arrange(
    `Predictability in OP`, Acronym
  )

  
alldoc = alldoc %>% 
  select(
    Acronym, Cat.Signal,`Predictability in OP`, `Signal Rep Quality`
    , everything()
  )


write_excel_csv(alldoc, 'SignalDoc.csv')

# PROCESS META-REPLICATION COMPARISONS ====
# only keep most relevant columns

mp = read_excel('OldSignalDocumentation.xlsx', sheet = 'MP') %>% 
  transmute(
    metastudy = 'MP', theirname = Predictor, theirlongname = theirname
    , Author, Year = PublicationYear, Journal = NA_character_
    , Predictability.in.OP
    , ourname = ClosestMatch, Note = Notes
    , holdper = NA_integer_
  )

ghz  = read_excel('OldSignalDocumentation.xlsx', sheet = 'GHZ')  %>% 
  transmute(
    metastudy = 'GHZ', theirname = Acronym, theirlongname = RPS
    , Author = `Author(s)`, `Date, Journal` 
    , Predictability.in.OP    
    , ourname = ClosestMatch, Note
    , holdper = NA_integer_    
  ) %>% 
  mutate(
    Year = substr(`Date, Journal`, 1, 4)
    , Journal = substr(`Date, Journal`, 7, nchar(`Date, Journal`))
  ) %>% 
  select(-`Date, Journal`)

# note: Predictability.in.Op.ignoring.holdper is a vlookup, we can do better
hxz = read_excel('OldSignalDocumentation.xlsx', sheet = 'HXZ') %>% 
  transmute(
    metastudy = 'HXZ', theirname = HXZname, theirlongname = Description
    , Author = Authors, Year, Journal
    , Predictability.in.OP = Predictability.in.OP.ignoring.holdper
    , ourname = ClosestMatch, Note
    , holdper
  )


# merge and write
metarep_comp = mp %>% 
  rbind(ghz) %>% 
  rbind(hxz)
    

write_excel_csv(metarep_comp, 'Comparison_to_MetaReplications.csv')

# PROCESS HLZ ====

# HLZ is so different from the meta replications that it needs its own csv
hlz  = read_excel('OldSignalDocumentation.xlsx', sheet = 'HLZ')
write_excel_csv(hlz, 'Comparison_to_HLZ.csv')



