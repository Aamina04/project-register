CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    project_title VARCHAR(150) NOT NULL,
    dataset_type VARCHAR(50),
    status ENUM('pending', 'in-progress', 'completed') DEFAULT 'pending',
    deadline DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO projects (client_name, project_title, dataset_type, status, deadline, notes) VALUES
('Dr. Ayesha Malik', 'Household Survey — Nutrition Study', 'Survey Data (CSV)', 'in-progress', '2026-09-15', 'Cleaning phase started, 3 of 8 districts done.'),
('Faisal Rasheed', 'Retail Sales Trend Report', 'Excel Workbook', 'pending', '2026-09-05', 'Waiting on Q3 sales export from client.'),
('RADS Research Cell', 'Public Health Access Mapping', 'GIS + Survey', 'completed', '2026-08-01', 'Final dashboard delivered and approved.');