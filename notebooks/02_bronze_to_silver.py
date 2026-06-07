from pyspark.sql.functions import col, trim, current_timestamp, lower, to_date

# RENTAL_UNITS_RAW
rental_units = spark.table("bronze.rental_units_raw")

rental_units_clean = (
    rental_units
    .select(
        col("id").alias("rental_unit_id"),
        col("property_id"),
        trim(col("unit_name")).alias("unit_name"),
        col("size_m2").cast("double").alias("size_m2"),
        col("monthly_rent").cast("double").alias("monthly_rent"),
        col("max_tenants").cast("int").alias("max_tenants"),
        col("created_at").cast("timestamp").alias("created_at"),
        col("updated_at").cast("timestamp").alias("updated_at"),
    )
    .filter(col("rental_unit_id").isNotNull())
    .filter(col("property_id").isNotNull())
    .filter(col("monthly_rent") > 0)
    .filter(col("size_m2") > 0)
    .withColumn("_silver_processed_at", current_timestamp())
)

rental_units_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.rental_units_clean")

display(spark.table("silver.rental_units_clean"))

# PROPERTIES_RAW
properties = spark.table("bronze.properties_raw")

properties_clean = (
    properties
    .select(
        col("id").alias("property_id"),
        col("agency_id"),
        trim(col("property_name")).alias("property_name"),
        trim(col("city")).alias("city"),
        trim(col("country")).alias("country"),
        col("created_at").cast("timestamp").alias("created_at"),
        col("updated_at").cast("timestamp").alias("updated_at"),
    )
    .filter(col("property_id").isNotNull())
    .filter(col("agency_id").isNotNull())
    .withColumn("_silver_processed_at", current_timestamp())
)

properties_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.properties_clean")

display(spark.table("silver.properties_clean"))

# TENANTS_RAW
tenants = spark.table("bronze.tenants_raw")

tenants_clean = (
    tenants
    .select(
        col("id").alias("tenant_id"),
        col("agency_id"),
        trim(col("first_name")).alias("first_name"),
        trim(col("last_name")).alias("last_name"),
        lower(trim(col("email"))).alias("email"),
        trim(col("onboarding_status")).alias("onboarding_status"),
        col("created_at").cast("timestamp").alias("created_at"),
        col("updated_at").cast("timestamp").alias("updated_at"),
    )
    .filter(col("tenant_id").isNotNull())
    .filter(col("agency_id").isNotNull())
    .filter(col("email").isNotNull())
    .dropDuplicates(["email"])
    .withColumn("_silver_processed_at", current_timestamp())
)

tenants_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.tenants_clean")

display(spark.table("silver.tenants_clean"))

# INVITATIONS_RAW
invitations = spark.table("bronze.invitations_raw")

invitations_clean = (
    invitations
    .select(
        col("id").alias("invitation_id"),
        col("agency_id"),
        col("rental_unit_id"),
        lower(trim(col("tenant_email"))).alias("tenant_email"),
        trim(col("tenant_name")).alias("tenant_name"),
        to_date(col("start_date")).alias("start_date"),
        trim(col("status")).alias("status"),
        col("created_at").cast("timestamp").alias("created_at"),
    )
    .filter(col("invitation_id").isNotNull())
    .filter(col("agency_id").isNotNull())
    .filter(col("rental_unit_id").isNotNull())
    .filter(col("tenant_email").isNotNull())
    .withColumn("_silver_processed_at", current_timestamp())
)

invitations_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.invitations_clean")

display(spark.table("silver.invitations_clean"))

# AGENCIES
agencies = spark.table("bronze.agencies_raw")

agencies_clean = (
    agencies
    .select(
        col("id").alias("agency_id"),
        col("user_id"),
        trim(col("agency_name")).alias("agency_name"),
        lower(trim(col("contact_email"))).alias("contact_email"),
        trim(col("phone")).alias("phone"),
        trim(col("address")).alias("address"),
        col("created_at").cast("timestamp").alias("created_at"),
        col("updated_at").cast("timestamp").alias("updated_at"),
    )
    .filter(col("agency_id").isNotNull())
    .withColumn("_silver_processed_at", current_timestamp())
)

agencies_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("silver.agencies_clean")

display(spark.table("silver.agencies_clean"))

# VALIDATION
silver_tables = [
    "agencies_clean",
    "properties_clean",
    "rental_units_clean",
    "tenants_clean",
    "invitations_clean",
]

for silver_table in silver_tables:
    full_table_name = f"silver.{silver_table}"
    df = spark.table(full_table_name)

    print("\n" + "=" * 80)
    print(full_table_name)
    print("=" * 80)
    print(f"Rows: {df.count()}")
    df.printSchema()
    display(df.limit(10))