CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_number TEXT,
    codename TEXT,
    aliases TEXT,
    release_date TEXT,
    announced_date TEXT,
    
    -- Core Specs & Features
    specs JSON,
    features_go_no_go JSON,
    msrp_price REAL,
    current_used_price REAL,
    price_last_updated TEXT,
    
    -- Support & Repair Info
    firmware_links JSON,
    warranty_info TEXT,
    update_policy TEXT,
    repairability_score REAL,
    parts_availability JSON,
    known_issues TEXT,
    red_flags_warnings TEXT,
    
    -- Tools & Resources
    usb_drivers_link TEXT,
    flashing_software JSON,
    schematics_link TEXT,
    service_manual_link TEXT,
    repair_youtube_links JSON,
    unlock_root_methods TEXT,
    battery_part_longevity TEXT,
    
    -- Links & Community
    manufacturer_website TEXT,
    support_website TEXT,
    community_resources JSON,
    sources JSON,
    images JSON,
    tags TEXT,
    
    -- API Integration Section
    api_usage JSON,
    
    -- Metadata
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    contributors TEXT,
    version INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS device_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER REFERENCES devices(id) ON DELETE CASCADE,
    imei TEXT UNIQUE,
    serial_number TEXT UNIQUE,
    blacklist_status TEXT,
    blacklist_last_checked TEXT,
    purchase_date TEXT,
    purchase_price REAL,
    condition TEXT,
    owner_notes TEXT,
    current_owner TEXT,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_devices_brand_model ON devices(brand, model_name);
CREATE INDEX IF NOT EXISTS idx_instances_imei ON device_instances(imei);
CREATE INDEX IF NOT EXISTS idx_instances_model ON device_instances(model_id);

-- Example trigger to update timestamp
CREATE TRIGGER IF NOT EXISTS update_devices_timestamp 
AFTER UPDATE ON devices
BEGIN
    UPDATE devices SET last_updated = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
