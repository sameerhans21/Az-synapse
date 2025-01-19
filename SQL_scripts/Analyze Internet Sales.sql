--  This query joins the fact table for Internet sales to a time dimension table based on the order date,
--   and aggregates the sales amount measure in the fact table by the calendar month attribute of the dimension table.


--  SELECT  d.CalendarYear AS Year,
--          SUM(i.SalesAmount) AS InternetSalesAmount
--  FROM FactInternetSales AS i
--  JOIN DimDate AS d ON i.OrderDateKey = d.DateKey
--  GROUP BY d.CalendarYear
--  ORDER BY Year;


-- SELECT  d.CalendarYear AS Year,
--          d.MonthNumberOfYear AS Month,
--          SUM(i.SalesAmount) AS InternetSalesAmount
--  FROM FactInternetSales AS i
--  JOIN DimDate AS d ON i.OrderDateKey = d.DateKey
--  GROUP BY d.CalendarYear, d.MonthNumberOfYear
--  ORDER BY Year, Month;

--  show yearly Internet sales totals for each region
--  SELECT  d.CalendarYear AS Year,
--          g.EnglishCountryRegionName AS Region,
--          SUM(i.SalesAmount) AS InternetSalesAmount
--  FROM FactInternetSales AS i
--  JOIN DimDate AS d ON i.OrderDateKey = d.DateKey
--  JOIN DimCustomer AS c ON i.CustomerKey = c.CustomerKey
--  JOIN DimGeography AS g ON c.GeographyKey = g.GeographyKey
--  GROUP BY d.CalendarYear, g.EnglishCountryRegionName
--  ORDER BY Year, Region;


-- aggregate the yearly regional sales by product category
 SELECT  d.CalendarYear AS Year,
         pc.EnglishProductCategoryName AS ProductCategory,
         g.EnglishCountryRegionName AS Region,
         SUM(i.SalesAmount) AS InternetSalesAmount
 FROM FactInternetSales AS i
 JOIN DimDate AS d ON i.OrderDateKey = d.DateKey
 JOIN DimCustomer AS c ON i.CustomerKey = c.CustomerKey
 JOIN DimGeography AS g ON c.GeographyKey = g.GeographyKey
 JOIN DimProduct AS p ON i.ProductKey = p.ProductKey
 JOIN DimProductSubcategory AS ps ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey
 JOIN DimProductCategory AS pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
 GROUP BY d.CalendarYear, pc.EnglishProductCategoryName, g.EnglishCountryRegionName
 ORDER BY Year, ProductCategory, Region;

