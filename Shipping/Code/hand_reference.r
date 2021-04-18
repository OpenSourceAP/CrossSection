### HOW DID WE BUILD OUR CHARACTERISTICS LIST?
# characteristics list building
us = alldocumentation %>%
    filter(Predictability.in.OP != '9_drop') %>%
    select(signalname, Authors, Predictability.in.OP) 



hxzall  = read_xlsx(
    paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'HXZ'
) %>% transmute(HXZname, signalname = ClosestMatch) 

hxzall %>%
    arrange(signalname) %>%
    group_by(signalname) %>%
    filter(row_number() > 1) %>%
    as.data.frame
    
hxz = hxzall %>%
    select(signalname) %>%
    mutate(hxz = T) %>%
    distinct()


mp  = read_xlsx(
    paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'MP'
) %>%
    transmute(signalname = ClosestMatch) %>%
    mutate(mp = T)

ghzall  = read_xlsx(
    paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'GHZ'
) %>%   transmute(signalname = ClosestMatch) 

ghzall %>% 
    arrange(signalname) %>%
    group_by(signalname) %>%
    filter(row_number() > 1) %>%
    as.data.frame

ghz = ghzall %>%
    filter(signalname != '_missing_') %>%
    mutate(ghz = T) %>%
    distinct()

hlz  = read_xlsx(
    paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'HLZ'
)


all = us %>% left_join(hxz) %>% left_join(mp) %>% left_join(ghz) %>%
    replace(is.na(.), FALSE)

all = all %>%
    mutate(add_from_mp_ghz = !hxz & (mp | ghz) )

sum(all$hxz )
sum(all$add_from_mp_ghz )

dim(all)[1] - 240 - 49

### REDUNDANCY


doc = alldocumentation %>%
    filter(Predictability.in.OP != '9_drop') 


doc  %>% group_by(Authors,Year) %>% summarize(nsignal = n()) %>% group_by(nsignal) %>% summarize(n())




doc %>% filter(Cat.Signal == 'Predictor') 
doc %>% filter(Cat.Signal == 'Predictor')  %>% distinct(Authors,Year)
doc %>% filter(Cat.Signal == 'Predictor')  %>% group_by(Authors,Year) %>% summarize(nsignal = n()) %>% group_by(nsignal) %>% summarize(n())


doc %>% filter(Cat.Signal == 'Predictor')  %>% group_by(Authors,Year) %>% summarize(nsignal = n()) %>% filter( nsignal > 3)


doc %>% distinct(Authors,Year)
