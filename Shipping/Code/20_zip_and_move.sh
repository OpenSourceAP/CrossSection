#!/bin/bash

PATHPROJECT="/cm/chen/anomalies.com/cfr1/"
PATHSTORAGE="/cm/scratch3/ayc_storage/anomalies.com_storage/to_gdrive/2021.03/"

echo "building folders in $PATHSTORAGE"

cd $PATHSTORAGE
mkdir Portfolios
cd Portfolios
mkdir Full_Sets_Extended
mkdir Full_Sets_Main
mkdir Individual


echo "zipping files to $PATHSTORAGE"

### ZIP SIGNALS

## Full sets
cd $PATHPROJECT/Signals/Data/
zip -r $PATHSTORAGE/PredictorsIndiv.zip Predictors/
zip -r $PATHSTORAGE/PlacebosIndiv.zip Placebos/

# DELETE CRSP PREDICTORS
zip -d $PATHSTORAGE/PredictorsIndiv.zip "Predictors/Size.csv"
zip -d $PATHSTORAGE/PredictorsIndiv.zip "Predictors/Price.csv"
zip -d $PATHSTORAGE/PredictorsIndiv.zip "Predictors/STreversal.csv"

## full sets processed
# note signed_predictors_dl_wide isn't in the main code, only in packaging
cd $PATHSTORAGE/temp/
zip $PATHSTORAGE/signed_predictors_dl_wide.zip signed_predictors_dl_wide.csv
zip $PATHSTORAGE/signed_predictors_all_wide.zip signed_predictors_all_wide.csv


### ZIP PORTFOLIOS

## Full sets main
cd $PATHPROJECT/Portfolios/Data/Portfolios

# these files don't need to be zipped
cp PredictorSummary.xlsx $PATHSTORAGE/Portfolios/Full_Sets_Main
cp PredictorLSretWide.csv $PATHSTORAGE/Portfolios/Full_Sets_Main
cp PredcitorPortsFull.csv $PATHSTORAGE/Portfolios/Full_Sets_Main

# zip these
# zip $PATHSTORAGE/Portfolios/Full_Sets_Main/PredictorPortsFull.zip  PredictorPortsFull.csv
zip $PATHSTORAGE/Portfolios/Full_Sets_Main/CheckPredictorPorts_Deciles.zip CheckPredictorPorts_Deciles.csv
zip $PATHSTORAGE/Portfolios/Full_Sets_Main/CheckPredictorPorts_Quintiles.zip CheckPredictorPorts_Quintiles.csv

## Full sets extended
for FILE in CheckPredictorLS*.csv
do
    zip $PATHSTORAGE/Portfolios/Full_Sets_Extended/${FILE%.*}.zip $FILE
done

for FILE in Placebo*.csv
do
    zip $PATHSTORAGE/Portfolios/Full_Sets_Extended/${FILE%.*}.zip $FILE
done

## finish up 
cd $PATHSTORAGE
zip -r Portfolios.zip Portfolios
