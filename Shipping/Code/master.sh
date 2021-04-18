#!/bin/bash

Rscript 10_pack_portfolios.r
Rscript 11_packandsign_predictors.r
./20_zip_and_move.sh
