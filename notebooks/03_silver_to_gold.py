
from pyspark.sql.functions import col, round, current_timestamp

spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

properties = spark.table("silver.properties_clean")
rental_units = spark.table("silver.rental_units_clean")

property_portfolio_summary = (
    rental_units
    .join(properties, on="property_id", how="left")
    .groupBy(
        "property_id",
        "property_name",
        "city",
        "country"
    )
    .agg(
        {"rental_unit_id": "count", "monthly_rent": "sum", "size_m2": "sum"}
    )
    .withColumnRenamed("count(rental_unit_id)", "number_of_units")
    .withColumnRenamed("sum(monthly_rent)", "total_monthly_rent_potential")
    .withColumnRenamed("sum(size_m2)", "total_size_m2")
    .withColumn(
        "avg_rent_per_m2",
        round(col("total_monthly_rent_potential") / col("total_size_m2"), 2)
    )
    .withColumn("_gold_processed_at", current_timestamp())
)

property_portfolio_summary.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold.property_portfolio_summary")

display(spark.table("gold.property_portfolio_summary"))

# VALIDATION OF GOLD TABLE
df = spark.table("gold.property_portfolio_summary")

print(f"Rows: {df.count()}")
df.printSchema()
display(df)