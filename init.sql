-- Initial database setup for Hersel.it Portfolio
-- This file is automatically executed when MySQL container starts

USE hersel_portfolio;

-- Enable UTF8MB4 charset for emoji and international characters
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role ENUM('admin', 'user') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    content LONGTEXT,
    image_url VARCHAR(500),
    github_url VARCHAR(500),
    demo_url VARCHAR(500),
    technologies JSON,
    category_id INT,
    is_featured BOOLEAN DEFAULT FALSE,
    is_published BOOLEAN DEFAULT TRUE,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create posts table (for future blog functionality)
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    excerpt TEXT,
    content LONGTEXT,
    featured_image VARCHAR(500),
    category_id INT,
    author_id INT,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create settings table
CREATE TABLE IF NOT EXISTS settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value LONGTEXT,
    description TEXT,
    type ENUM('text', 'textarea', 'boolean', 'json') DEFAULT 'text',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Insert default categories
INSERT INTO categories (name, slug, description, color) VALUES
('Web Development', 'web-development', 'Progetti di sviluppo web', '#007bff'),
('Mobile Apps', 'mobile-apps', 'Applicazioni mobile', '#28a745'),
('Desktop Apps', 'desktop-apps', 'Applicazioni desktop', '#ffc107'),
('APIs', 'apis', 'API e servizi web', '#dc3545'),
('Tools & Utilities', 'tools-utilities', 'Strumenti e utility', '#6f42c1'),
('Open Source', 'open-source', 'Progetti open source', '#20c997')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Insert default settings
INSERT INTO settings (setting_key, setting_value, description, type) VALUES
('site_name', 'Hersel.it', 'Nome del sito', 'text'),
('site_description', 'Portfolio personale di Hersel Giannella - Developer', 'Descrizione del sito', 'textarea'),
('admin_email', 'admin@hersel.it', 'Email amministratore', 'text'),
('site_logo', '/static/img/logo.png', 'URL del logo', 'text'),
('social_github', 'https://github.com/BluLupo', 'GitHub URL', 'text'),
('social_linkedin', '', 'LinkedIn URL', 'text'),
('social_twitter', '', 'Twitter URL', 'text'),
('site_maintenance', 'false', 'Modalità manutenzione', 'boolean'),
('analytics_code', '', 'Codice Analytics', 'textarea'),
('projects_per_page', '12', 'Progetti per pagina', 'text'),
('featured_projects_limit', '6', 'Limite progetti in evidenza', 'text')
ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value);

-- Create admin user (password: AdminPass123!)
-- This creates a default admin user for initial access
-- Password hash for 'AdminPass123!' generated with bcrypt
INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES
('admin', 'admin@hersel.it', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqyaqr06eoAGNz9CpahtY1q', 'Admin', 'User', 'admin')
ON DUPLICATE KEY UPDATE role=VALUES(role);

-- Insert sample projects (optional)
INSERT INTO projects (title, slug, description, content, github_url, technologies, is_featured, is_published, created_by) VALUES
('Hersel.it Portfolio', 'hersel-it-portfolio', 'Portfolio dinamico sviluppato con Quart e MySQL', 
 '<h2>Portfolio Dinamico</h2><p>Questo portfolio è stato sviluppato utilizzando le seguenti tecnologie:</p><ul><li>Python con Quart framework</li><li>MySQL per il database</li><li>Bootstrap 5 per il frontend</li><li>Docker per il deployment</li></ul>', 
 'https://github.com/BluLupo/hersel.it', 
 '["Python", "Quart", "MySQL", "Bootstrap", "Docker"]', 
 TRUE, TRUE, 1),

('API REST con Quart', 'api-rest-quart', 'API RESTful asincrona per gestione dati', 
 '<h2>API REST</h2><p>API asincrona sviluppata con Quart per gestire operazioni CRUD su database MySQL.</p>', 
 '', 
 '["Python", "Quart", "MySQL", "REST API", "Async"]', 
 FALSE, TRUE, 1)
ON DUPLICATE KEY UPDATE title=VALUES(title);

-- Create indexes for better performance
CREATE INDEX idx_projects_published ON projects(is_published);
CREATE INDEX idx_projects_featured ON projects(is_featured);
CREATE INDEX idx_projects_category ON projects(category_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_posts_published ON posts(is_published);

-- Show confirmation message
SELECT 'Database initialized successfully!' as Status;
SELECT COUNT(*) as 'Total Categories' FROM categories;
SELECT COUNT(*) as 'Total Settings' FROM settings;
SELECT COUNT(*) as 'Admin Users' FROM users WHERE role='admin';
SELECT COUNT(*) as 'Sample Projects' FROM projects;
