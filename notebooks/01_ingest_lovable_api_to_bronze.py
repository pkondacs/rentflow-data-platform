# %sql
# CREATE SCHEMA IF NOT EXISTS bronze;
# CREATE SCHEMA IF NOT EXISTS silver;
# CREATE SCHEMA IF NOT EXISTS gold;

# display(dbutils.fs.ls("/Volumes/workspace/default/rentflow_raw/"))

from pyspark.sql.functions import explode, col, current_timestamp, lit

volume_path = "/Volumes/workspace/default/rentflow_raw"

# Generic validate table function
def validate_table(table_name: str):
    df = spark.table(table_name)

    print("=" * 50)
    print(f"TABLE: {table_name}")
    print("=" * 50)
    print(f"Rows: {df.count()}")

    print("\nSchema:")
    df.printSchema()

    display(df.limit(10))


# Generic Bronze ingestion function
def load_table(source_table: str):

    print(f"Loading source table: {source_table}")

    # 1. Read raw JSON landing files from the Volume
    raw_df = spark.read.option("multiline", "true").json(
        f"{volume_path}/{source_table}_*.json"
    )

    # 2. Check whether the records array contains any rows
    records_count = (
        raw_df
        .select(explode(col("records")).alias("record"))
        .count()
    )

    if records_count == 0:
        print(
            f"Skipping bronze.{source_table}_raw: "
            f"source export contains 0 records"
        )
        return

    # 3. Flatten the API payload and enrich with ingestion metadata
    df = (
        raw_df
        .select(explode(col("records")).alias("record"))
        .select("record.*")
        .withColumn("_source_system", lit("rentflow_lovable_cloud"))
        .withColumn("_source_table", lit(source_table))
        .withColumn("_ingested_at", current_timestamp())
    )

    target_table = f"bronze.{source_table}_raw"

    # 4. Persist the raw dataset into the Bronze Delta layer
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable(target_table)

    # 5. Generate basic ingestion audit information
    row_count = spark.table(target_table).count()

    print(
        f"Successfully loaded {target_table} "
        f"with {row_count} records"
    )

    # 6. Validate the Bronze table
    validate_table(target_table)

# CALLING THE LOAD TABLE FUNCTION
source_tables = [
    "agencies",
    "properties",
    "rental_units",
    "tenants",
    "invitations",
    "tenancies",
    "email_send_log",
]

for source_table in source_tables:
    load_table(source_table)


# COMMAND ----------
# Schema inspection for Bronze tables

bronze_tables_df = spark.sql("SHOW TABLES IN bronze")

print("Existing tables in bronze:")
bronze_tables_df.show(truncate=False)

existing_tables_rows = bronze_tables_df.select("tableName").collect()

existing_tables = set()

for row in existing_tables_rows:
    existing_tables.add(row["tableName"])

print("\nExisting table names:")
print(existing_tables)

expected_bronze_tables = [
    "agencies_raw",
    "properties_raw",
    "rental_units_raw",
    "tenants_raw",
    "invitations_raw",
    "tenancies_raw",
    "email_send_log_raw",
]

for bronze_table in expected_bronze_tables:
    full_table_name = f"bronze.{bronze_table}"

    if bronze_table not in existing_tables:
        print(f"\nSkipping {full_table_name} — table does not exist")
        continue

    print("\n" + "=" * 80)
    print(f"SCHEMA FOR: {full_table_name}")
    print("=" * 80)

    df = spark.table(full_table_name)

    df.printSchema()

    print(f"Row count: {df.count()}")

    display(df.limit(10))



