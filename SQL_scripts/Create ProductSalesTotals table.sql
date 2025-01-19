 CREATE EXTERNAL TABLE ProductSalesTotals
     WITH (
         LOCATION = 'sales/productsales/',
         DATA_SOURCE = sales_data,
         FILE_FORMAT = ParquetFormat
     )
 AS
 SELECT Item AS Product,
     SUM(Quantity) AS ItemsSold,
     ROUND(SUM(UnitPrice) - SUM(TaxAmount), 2) AS NetRevenue
 FROM
     OPENROWSET(
         BULK 'sales/csv/*.csv',
         DATA_SOURCE = 'sales_data',
         FORMAT = 'CSV',
         PARSER_VERSION = '2.0',
         HEADER_ROW = TRUE
     ) AS orders
 GROUP BY Item;