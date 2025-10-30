#!/bin/bash

# TODO Should some of these be arguments rather than hardcoded?
TEMP_DB="temp.db"
PROD_DB="data.db"
DATA_FOLDER="/opt/urotheliome-data/clean"
METADATA_FILE="$DATA_FOLDER/metadata_v5.tsv"

# Delete temporary DB if already exists
if [ -f "$TEMP_DB" ] ; then
    rm "$TEMP_DB"
fi

# Create DB from schema
sqlite3 $TEMP_DB < schema.sql > /dev/null

# Populate DB
# TODO In what circumstances are errors thrown?
python data_upload.py $TEMP_DB $METADATA_FILE $DATA_FOLDER
success=$?

# If success, move DB to prod
if [ $success -eq 0 ]; 
then 
    echo "Database built successfully"
    mv $TEMP_DB $PROD_DB
fi
