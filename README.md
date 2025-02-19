# Azure Events
## <b> OBJECTIVE: Implement a Data pipeline Solution with Azure Events with real-time data


Network Monitoring and Analytics with FlexRIC & Azure Synapse
Technologies: FlexRIC (Near-RT RIC), xApp, Azure Blob Storage, Azure Synapse Analytics, JSON, PySpark

  Deployed FlexRIC in simulation mode with a gNB agent (emu_agent_gnb), Near-RT RIC, and an xApp to monitor network performance.<br>
  Captured and processed real-time network monitoring logs from the xApp, converting them into structured JSON files.<br>
  Automated the ingestion of monitoring data into Azure Blob Storage for centralized storage and further processing.<br>
  Integrated Azure Synapse Analytics to analyze and visualize network insights using PySpark and SQL queries.<br>
  Developed a cloud-based data pipeline for efficient monitoring, storage, and analysis of RAN performance metrics.<br>

  1. Modify xApp to Stream Logs Directly – AZURE EVENT HUB
  
  2. Set Up Azure Event Hub for Real-Time Data Ingestion
  Azure Event Hub will act as a real-time buffer for incoming xApp logs.
  
  3. Process Data in Real-Time Using Azure Stream Analytics
  Create an Azure Stream Analytics Job.
  Input: Select Azure Event Hub as the source.
  Output: Send processed data to Blob Storage.
  Query: Use SQL queries to filter and transform and analyse data.
  
  4. Visualize Data in Real-Time in Azure Synapse
  Use Power BI to create real-time visualizations.
  Query the Synapse table in real-time to track network performance.
