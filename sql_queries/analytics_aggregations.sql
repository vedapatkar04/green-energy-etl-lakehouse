SELECT 
    energy_source, 
    SUM(consumption_kwh) as total_consumption,
    AVG(consumption_kwh) as avg_consumption
FROM "energy_db"."fact_energy_usage"
GROUP BY energy_source
ORDER BY total_consumption DESC;