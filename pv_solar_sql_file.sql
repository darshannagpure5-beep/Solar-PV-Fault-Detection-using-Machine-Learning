USE solar_pv;

-- Table 
SELECT 
    *
FROM
    solar_pv;

-- How many solar panel records are present?
SELECT 
    COUNT(*) AS total_records
FROM
    solar_pv;

-- 1. How many panels belong to each fault type?
SELECT 
    Panel_Class, COUNT(*) AS total_panels
FROM
    solar_pv
GROUP BY Panel_Class
ORDER BY total_panels DESC;

-- 2. Average Power Output by Fault Type
SELECT 
    Panel_Class, AVG(`AC_Power_(W)`) AS avg_power
FROM
    solar_pv
GROUP BY Panel_Class
ORDER BY avg_power DESC;
-- Insight: Clean panels should produce higher power.

-- 3. Compare efficiency across different panel conditions.
SELECT 
    Panel_Class, AVG(Efficiency) AS avg_efficiency
FROM
    solar_pv
GROUP BY Panel_Class
ORDER BY avg_efficiency DESC;
-- Faulty panels → lower efficiency.

-- 4. How does irradiance vary for different panel classes?
SELECT 
    Panel_Class, AVG(Irradiance) AS avg_irradiance
FROM
    solar_pv
GROUP BY Panel_Class;

-- 5. Calculate power loss between DC and AC.
SELECT 
    Panel_Class, AVG(`DC_power_(W)` - `AC_Power_(W)`) AS avg_power_loss
FROM
    solar_pv
GROUP BY Panel_Class
ORDER BY avg_power_loss DESC;

-- 6. Which fault damages panel most.
SELECT 
    Panel_Class,
    AVG(`DC_power_(W)` - `AC_Power_(W)`) AS avg_power_loss
FROM
    solar_pv
GROUP BY Panel_Class
ORDER BY avg_power_loss DESC;

-- 7. Temperature Effect on Efficiency
SELECT 
    CASE
        WHEN Avg_Temperature < 30 THEN 'Low Temp'
        WHEN Avg_Temperature BETWEEN 30 AND 40 THEN 'Medium Temp'
        ELSE 'High Temp'
    END AS temp_category,
    AVG(Efficiency) AS avg_efficiency
FROM
    solar_pv
GROUP BY temp_category;

-- 8. Find Maximum and Minimum Power
SELECT 
    MAX(`AC_Power_(W)`) AS max_power,
    MIN(`AC_Power_(W)`) AS min_power
FROM
    solar_pv;

-- 9. Top 10 Highest Power Producing Panels
SELECT 
    *
FROM
    solar_pv
ORDER BY `AC_Power_(W)` DESC
LIMIT 10;