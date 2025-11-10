#!/bin/bash

# Variables passed as arguments
TEMP_DB=$1
PROD_DB=$2
DATA_FOLDER=$3
METADATA_FILE=$4

# Delete temporary DB if already exists
if [ -f "$TEMP_DB" ] ; then
    rm "$TEMP_DB"
fi

# Create DB from schema
sqlite3 $TEMP_DB < schema.sql > /dev/null

# Populate DB
# TODO In what circumstances are errors thrown?
python3 data_upload.py $TEMP_DB $METADATA_FILE $DATA_FOLDER
success=$?

# If success, move DB to prod
if [ $success -eq 0 ]; 
then 
    echo "Database built successfully"
    mv $TEMP_DB $PROD_DB
fi
