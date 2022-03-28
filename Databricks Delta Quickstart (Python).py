# Databricks notebook source
# DBTITLE 1,Read Databricks dataset  
# Define the input format and path.
read_format = 'delta'
load_path = '/databricks-datasets/learning-spark-v2/people/people-10m.delta'

# Load the data from its source.
people = spark.read \
  .format(read_format) \
  .load(load_path)

# Show the results.
display(people)

# COMMAND ----------

# DBTITLE 1,Write out DataFrame as Databricks Delta data
# Define the output format, output mode, columns to partition by, and the output path.
write_format = 'delta'
write_mode = 'overwrite'
partition_by = 'gender'
save_path = '/tmp/delta/people-10m'

# Write the data to its target.
people.write \
  .format(write_format) \
  .partitionBy(partition_by) \
  .mode(write_mode) \
  .save(save_path)

# COMMAND ----------

# DBTITLE 1,Query the data file path
# Load the data from the save location.
people_delta = spark.read.format(read_format).load(save_path)

display(people_delta)

# COMMAND ----------

# DBTITLE 1,Create table
table_name = 'people10m'

display(spark.sql("DROP TABLE IF EXISTS " + table_name))

display(spark.sql("CREATE TABLE " + table_name + " USING DELTA LOCATION '" + save_path + "'"))

# COMMAND ----------

# DBTITLE 1,Query the table
display(spark.table(table_name).select('id', 'salary').orderBy('salary', ascending = False))

# COMMAND ----------

# DBTITLE 1,Visualize data
df_people = spark.table(table_name)
display(df_people.select('gender').orderBy('gender', ascending = False).groupBy('gender').count())

# COMMAND ----------

display(spark.table(table_name).select("salary").orderBy("salary", ascending = False))

# COMMAND ----------

# DBTITLE 1,Count rows
people_delta.count()

# COMMAND ----------

# DBTITLE 1,Show partitions and contents of a partition
display(spark.sql("SHOW PARTITIONS " + table_name))

# COMMAND ----------

dbutils.fs.ls('dbfs:/tmp/delta/people-10m/gender=M/')

# COMMAND ----------

# DBTITLE 1,Optimize table 
display(spark.sql("OPTIMIZE " + table_name))

# COMMAND ----------

# DBTITLE 1,Show table history
display(spark.sql("DESCRIBE HISTORY " + table_name))

# COMMAND ----------

# DBTITLE 1,Show table details
display(spark.sql("DESCRIBE DETAIL " + table_name))

# COMMAND ----------

# DBTITLE 1,Show the table format
display(spark.sql("DESCRIBE FORMATTED " + table_name))

# COMMAND ----------

# DBTITLE 1,Clean up
# Delete the table.
spark.sql("DROP TABLE " + table_name)
# Delete the Delta files.
dbutils.fs.rm(save_path, True)
