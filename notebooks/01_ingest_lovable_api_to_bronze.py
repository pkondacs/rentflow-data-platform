
# display(dbutils.fs.ls("/Volumes/workspace/default/rentflow_raw/"))

from pyspark.sql.functions import explode, col, current_timestamp, lit

# Load one table first into a df
volume_path = "/Volumes/workspace/default/rentflow_raw"

raw_df = spark.read.option("multiline", "true").json(
    f"{volume_path}/rental_units_*.json"
)

df = (
    raw_df
    .select(explode(col("records")).alias("record"))
    .select("record.*")
    .withColumn("_source_system", lit("rentflow_lovable_cloud"))
    .withColumn("_source_table", lit("rental_units"))
    .withColumn("_ingested_at", current_timestamp())
)

display(df)

# Write bronze table
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .saveAsTable("bronze.rental_units_raw")

# Validate table creation
bronze_df = spark.table("bronze.rental_units_raw")
print("Row count:", bronze_df.count())
print("Schema:")
bronze_df.printSchema()

display(
    bronze_df.limit(10)
)



