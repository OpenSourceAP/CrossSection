# Check for and potentially install missing packages
install.packages(setdiff(c('tidyverse', 'zoo', 'tm', 'data.table'), rownames(installed.packages())))

library(tidyverse)

# Parse arguments
args = commandArgs(trailingOnly = "TRUE")
if (length(args)) {
  arg1 <- args[1]
} else {
  message('Supply path')
}

# check system for dl method
dlmethod = 'auto'
sysinfo = Sys.info()
if (sysinfo[1] == "Linux") {
    dlmethod = 'wget'
}


tmp <- tempfile()
# Download 1
download.file("http://www.nber.org/~jbessen/dynass.dta.zip",
              destfile = tmp,
              method = dlmethod)

dynass = haven::read_dta(unz(tmp,"dynass.dta"))

#data.table::fwrite(dynass, file = '../DataRaw/dynass.csv')

# Download 2
download.file("http://www.nber.org/~jbessen/cite76_06.dta.zip",
              destfile = tmp,
              method = dlmethod)

cite76_06 = haven::read_dta(unz(tmp,"cite76_06.dta"))

#data.table::fwrite(cite76_06, file = '../DataRaw/cite76_06.csv')

# Download 3
download.file("http://www.nber.org/~jbessen/pat76_06_assg.dta.zip",
              destfile = tmp,
              method = dlmethod)

pat76_06_assg = haven::read_dta(unz(tmp,"pat76_06_assg.dta"))

#data.table::fwrite(pat76_06_assg, file = '../DataRaw/pat76_06_assg.csv')

# Number of patents
#~~~~~~~~~~~~~~~~~~
df_npat = pat76_06_assg %>%
  # count number of patents by company and year
  group_by(pdpass, gyear) %>%
  summarise(npat = n()) %>%
  ungroup() %>%
  # Match gvkey identifier
  left_join(dynass, by = "pdpass") %>%
  mutate(gvkey = "") %>%
  select(pdpass, gyear, npat, gvkey, everything()) %>% 
  # Sort correct gvkey depending on time
  mutate(gvkey = case_when(
    gyear >= begyr1 & gyear <= endyr1 ~ gvkey1,
    gyear >= begyr2 & gyear <= endyr2 ~ gvkey2,
    gyear >= begyr3 & gyear <= endyr3 ~ gvkey3,
    gyear >= begyr4 & gyear <= endyr4 ~ gvkey4,
    gyear >= begyr5 & gyear <= endyr5 ~ gvkey5)) %>%
  mutate(year = as.numeric(gyear),
         gvkey = as.numeric(gvkey)) %>%
  filter(gvkey != "") %>%
  select(pdpass, gvkey, year, npat) %>%
  distinct()


# Number of patent citations
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

df_cite_match = pat76_06_assg %>%
  select(patent, pdpass, gyear, cat, subcat) %>%
  filter(pdpass != "")

df_cite = cite76_06 %>%
  # Match twice to get citing and cited patent info
  left_join(df_cite_match, by = c("cited"="patent")) %>%
  left_join(df_cite_match, by = c("citing" = "patent")) %>%
  filter(pdpass.x != "" & pdpass.y != "" & gyear.x != "" & gyear.y != "") %>%
  mutate(gdiff = gyear.y - gyear.x) %>%
  # Only consider citations in first 5 years after patent
  filter(gdiff <= 5) %>%
  select(-ncites7606) 

df_scale = df_npat %>%
  left_join(df_cite, by = c("pdpass" = "pdpass.x", "year" = "gyear.y")) %>%
  filter(cited != "") %>%
  select(pdpass, gvkey, year, gyear.x, subcat.x) %>%
  # Number of citations
  group_by(pdpass, gvkey, year, gyear.x, subcat.x) %>%
  summarise(ncites = n()) %>% 
  # Scale by average cites in same subcategory
  group_by(year, gyear.x, subcat.x) %>%
  mutate(citscale = ncites / mean(ncites, na.rm = TRUE)) %>%
  group_by(gvkey, year) %>%
  summarise(ncitscale = sum(citscale, na.rm = TRUE)) %>%
  ungroup() 

# Merge number of patents and (scaled) number of citations
df_patents = df_npat %>%
  group_by(gvkey, year) %>% 
  summarise(npat = sum(npat)) %>%   # remove some duplicates due to pdpass mapping to multiple gvkeys
  ungroup() %>% 
  left_join(df_scale, by = c("gvkey", "year")) 

rm(df_npat, df_cite_match, df_cite, df_scale, pat76_06_assg, cite76_06, dynass)

# Expand to balanced panel (within units and add 0 if no patent in expanded year)
df_patents %>%
  group_by(gvkey)%>%
  expand(gvkey = sort(unique(gvkey)),
         year = seq(from = min(year), to = max(year))) %>%
  ungroup() %>%
  left_join(df_patents) -> df_patents

df_patents = df_patents %>% 
  mutate(npat = ifelse(is.na(npat), 0 , npat),
         ncitscale = ifelse(is.na(ncitscale), 0 ,ncitscale))

# Save for Stata
haven::write_dta(df_patents, path =  paste0(arg1, '/Signals/Data/Intermediate/PatentDataProcessed.dta'))
