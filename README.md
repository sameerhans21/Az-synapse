# Az-synapse
## <b> OBJECTIVE: Implement a Data Analytics Solution with Azure Synapse Analytics

<iI><b>Synapse Studio</b> is a web-based portal in which you can manage and work with the resources in your Azure Synapse Analytics workspace.</i>

### 1) Use Azure Synapse serverless SQL pool to query files in a data lake
<u><i>use a serverless SQL pool to query data files in a data lake</i></u>
<li>Transform data using CREATE EXTERNAL TABLE AS SELECT (CETAS) statements</li>
A simple way to use SQL to transform data in a file and persist the results in another file is to use a CREATE EXTERNAL TABLE AS SELECT (CETAS) statement. This statement creates a table based on the requests of a query, but the data for the table is stored as files in a data lake. The transformed data can then be queried through the external table, or accessed directly in the file system (for example, for inclusion in a downstream process to load the transformed data into a data warehouse).

### 2) Analyze data with Apache Spark in Azure Synapse Analytics
<u><i>use a Spark pool to analyze and visualize data from files in a data lake</i></u>

Apache Spark applications run as independent sets of processes on a cluster, coordinated by the SparkContext object in your main program (called the driver program). The SparkContext connects to the cluster manager, which allocates resources across applications using an implementation of Apache Hadoop YARN. Once connected, Spark acquires executors on nodes in the cluster to run your application code.

The SparkContext runs the main function and parallel operations on the cluster nodes, and then collects the results of the operations. The nodes read and write data from and to the file system and cache transformed data in-memory as Resilient Distributed Datasets (RDDs).<br>
![spark_overview](./images/sp.png)

### 3) Use Delta Lake in Azure Synapse Analytics
<u><i>use a Spark pool in Azure Synapse Analytics to create and query Delta Lake tables, and query Delta Lake data from a serverless SQL pool</i></u>

Delta Lake is an open-source storage layer that adds relational database semantics to Spark-based data lake processing.

### 4) Analyze data in a relational data warehouse

 <u><i>explore a data warehouse</i></u>
<li> Dimension tables: Dimension tables describe business entities, such as products, people, places, and dates. Dimension tables contain columns for attributes of an entity. For example, a customer entity might have a first name, a last name, an email address, and a postal address.  They include two key columns:

<i>a surrogate key </i>that is specific to the data warehouse and uniquely identifies each row in the dimension table in the data warehouse - usually an incrementing integer number.<br>
<i>An alternate key</i>, often a natural or business key that is used to identify a specific instance of an entity in the transactional source system from which the entity record originated - such as a product code or a customer ID.<br>

<li>Fact tables: store details of observations or events; for example, sales orders, stock balances, exchange rates, or recorded temperatures. A fact table contains columns for numeric values that can be aggregated by dimensions<br><br>

Azure Synapse Analytics dedicated SQL pools use a massively parallel processing (MPP) architecture. In an MPP system, the data in a table is distributed for processing across a pool of nodes. Synapse Analytics supports the following kinds of distribution:

<li>Hash: A deterministic hash value is calculated for the specified column and used to assign the row to a compute node.
<li>Round-robin: Rows are distributed evenly across all compute nodes.
<li>Replicated: A copy of the table is stored on each compute node.

### 5) Build a data pipeline in Azure Synapse Analytics
 <u><i>implement a run an Azure Synapse Analytics pipeline that transfers and transforms data</i></u>

Pipelines in Azure Synapse Analytics encapsulate a sequence of activities that perform data movement and processing tasks. You can use a pipeline to define data transfer and transformation activities, and orchestrate these activities through control flow activities that manage branching, looping, and other typical processing logic.<br>
![pipeline](./images/pipeline.png)

A Data Flow is a commonly used activity type to define data flow and transformation. Data flows consist of:

<li>Sources - The input data to be transferred.
<li>Transformations – Various operations that you can apply to data as it streams through the data flow.
<li>Sinks – Targets into which the data will be loaded.
