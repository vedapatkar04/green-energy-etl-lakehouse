import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, when, lower, to_timestamp

# Initialize Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# 1. READ: Load data from the Bronze Table we just created
datasource = glueContext.create_dynamic_frame.from_catalog(
    database = "energy_db", 
    table_name = "energy_consumption"
)

# Convert to Spark DataFrame
df = datasource.toDF()

# 2. TRANSFORM: Clean the data
cleaned_df = df.withColumn(
    # Normalize energy_source to lowercase (fixing 'Soar' vs 'solar')l
    "energy_source", lower(col("energy_source"))
).withColumn(
    # Cast consumption to Double and fill nulls with 0
    "consumption_kwh", col("consumption_kwh").cast("double")
).fillna({"consumption_kwh": 0})

# 3. WRITE: Save to the Silver Layer as Parquet
# Note: Replace 'you-project-name' with your actual S3 bucket name
target_path = "s3://you-project-name/02-silver-stage/fact_energy_usage/"

cleaned_df.write.mode("overwrite").parquet(target_path)

job.commit()