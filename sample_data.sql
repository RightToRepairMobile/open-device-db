-- Sample data for Open Device Database
-- Run with: sqlite3 device_database.db < sample_data.sql

INSERT OR IGNORE INTO devices (brand, model_name, model_number, codename, release_date, specs, features_go_no_go, repairability_score, tags, sources)
VALUES 
('Google', 'Pixel 8', 'G1B7-00000', 'shusky', '2023-10-04', 
 '{"chipset":"Google Tensor G3", "ram":"8GB", "storage":"128/256GB", "display":"6.2 inch OLED"}', 
 '{"bootloader_unlock":true, "microsd":false, "headphone_jack":false, "wireless_charging":true}', 
 8.5, 'flagship,repair_friendly', '["https://www.gsmarena.com/google_pixel_8-12546.php"]'),

('Fairphone', 'Fairphone 5', 'FP5', 'fairphone5', '2023-09-14', 
 '{"chipset":"Qualcomm QCM6490", "ram":"8GB", "battery":"4200 mAh replaceable"}', 
 '{"bootloader_unlock":true, "microsd":true, "replaceable_battery":true}', 
 9.5, 'repair_friendly,sustainable', '["https://www.gsmarena.com/fairphone_5-12507.php"]'),

('Samsung', 'Galaxy A54', 'SM-A546', 'a54', '2023-03-15', 
 '{"chipset":"Exynos 1380", "ram":"6/8GB"}', 
 '{"bootloader_unlock":false, "microsd":true}', 
 6.0, 'budget', '["https://www.gsmarena.com/samsung_galaxy_a54-12070.php"]');
