# PA195 project - Spark + Cassandra demo

## Installation

1. Download the data, unarchive and place it to `./data` folder such that `data/charts.csv` file exists
https://www.kaggle.com/dhruvildave/spotify-charts

2. Spin up the containers

```
docker-compose up
```

3. Create Cassandra DB scheme
```
docker exec -it pa195-cassandra cqlsh -u cassandra -p cassandra -f /scripts/init_cassandra.cql
```

4. Download & install DS bulk

```
wget -P ./downloads "https://downloads.datastax.com/dsbulk/dsbulk-1.8.0.tar.gz"

tar -xzvf ./downloads/dsbulk-1.8.0.tar.gz -s /^dsbulk-1.8.0/dsbulk/
```

5. Import the data into Cassandra
```
./dsbulk/bin/dsbulk load \
    -url data/charts.csv \
    -h '["localhost:9042"]' \
    -maxErrors -1 \
    -header true \
    -u cassandra -p cassandra \
    -k pa195 \
    -t charts
```

## Queries

### Query 0
Just the performance testing query.
Normally, it does not make very sense to use Spark when pure Cassandra can be used.

> Number of records in Spotify’s top 200 for Slovakia region

Cassandra's CQL for the query:

```
SELECT COUNT(*) FROM charts WHERE region='Slovakia' AND chart='top200' ALLOW FILTERING;
```

### Query 1

> The number of days each artist was on the 1th place in the Spotify's top 200 chart

### Query 2
> The number of days the BTS band was on its highest rank in each region in Spotify's top 200 chart

## Python

### Query 0
```
docker exec -it pa195-spark-master spark-submit \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
    --driver-memory 2g \
    --executor-memory 2g \
    /scripts/python/query0.py
```

### Query 1
```
docker exec -it pa195-spark-master spark-submit \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
    --driver-memory 2g \
    --executor-memory 2g \
    /scripts/python/query1.py
```

### Query 2

```
docker exec -it pa195-spark-master spark-submit \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
    --driver-memory 2g \
    --executor-memory 2g \
    /scripts/python/query2.py
```

## Java

Before use, the worker has to be started:

```
docker exec -it pa195-spark-master start-worker.sh spark://pa195-spark-master:7077
```

#### Query 0

```
docker exec -it pa195-spark-master spark-submit \
    --class cz.muni.fi.pa195.SpotifyChartsSlovakia \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
    --driver-memory 2g \
    --executor-memory 2g \
    /scripts/java/spotify-charts/target/spotify-charts-1.jar
```

#### Query 1

```
docker exec -it pa195-spark-master spark-submit \
    --class cz.muni.fi.pa195.SpotifyChartsRankOneArtists \
    --conf spark.cassandra.connection.host=cassandra \
    --conf spark.cassandra.auth.username=cassandra \
    --conf spark.cassandra.auth.password=cassandra \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 \
    --driver-memory 2g \
    --executor-memory 2g \
    /scripts/java/spotify-charts/target/spotify-charts-1.jar
```
