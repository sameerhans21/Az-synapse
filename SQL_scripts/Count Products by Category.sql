-- -- This is auto-generated code
-- SELECT
--     TOP 100 *
-- FROM
--     OPENROWSET(
--         BULK 'https://datalake0ghz8yx.dfs.core.windows.net/files/product_data/products.csv',
--         FORMAT = 'CSV',
--         PARSER_VERSION = '2.0',
--         HEADER_ROW = TRUE

--     ) AS [result]
 SELECT
    Category, COUNT(*) AS ProductCount
 FROM
    OPENROWSET(
         BULK 'https://datalake0ghz8yx.dfs.core.windows.net/files/product_data/products.csv',
         FORMAT = 'CSV',
         PARSER_VERSION='2.0',
         HEADER_ROW = TRUE
     ) AS [result]
 GROUP BY Category;