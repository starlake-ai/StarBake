export SL_ROOT=/Users/hayssams/git/starbake
export TEMPORARY_GCS_BUCKET=starlake-app
export SL_STORAGE_FS=gs://starlake-app
export TEMPORARY_GCS_BUCKET=starlake-app
export SL_ENV=BQ
export GOOGLE_APPLICATION_CREDENTIALS=/Users/hayssams/.gcloud/keys/starlake-hayssams.json
export SL_AUDIT_SINK_TYPE=BigQuerySink
/Users/hayssams/git/public/starlake/distrib/starlake.sh $1
