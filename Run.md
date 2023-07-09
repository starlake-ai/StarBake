1. Run the load for each day
2. Run the transform
4. Run the test

mkdir tmp & cd tmp
sh /Users/elarib/Work/Starlake/starlake/distrib/starlake.sh


sh /Users/elarib/Work/Starlake/starlake/distrib/starlake.sh bootstrap --template userguide


```
export SL_ENV=BQ && sh /Users/elarib/Work/Starlake/starlake/distrib/starlake.sh import

export SL_ENV=BQ && export SL_AUDIT_SINK_TYPE=BigQuerySink && export SL_HIVE=false && export TEMPORARY_GCS_BUCKET=starlake-app && sh /Users/elarib/Work/Starlake/starlake/distrib/starlake.sh watch

```

Retirer les .ack de userguide
Load sans spark with bq native