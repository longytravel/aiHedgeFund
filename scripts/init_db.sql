-- AIHedgeFund Database Initialization
-- PostgreSQL 18.1
-- This script runs automatically when the Docker container is first created

-- Enable PostgreSQL 18.1 features
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation (uuidv7 support)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- Trigram indexing for text search
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- GIN indexes for performance

-- Set timezone to UK
SET timezone = 'Europe/London';

-- Create application schema
CREATE SCHEMA IF NOT EXISTS aihedgefund;

-- Grant permissions to application user
GRANT ALL PRIVILEGES ON SCHEMA aihedgefund TO aihedgefund;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA aihedgefund TO aihedgefund;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA aihedgefund TO aihedgefund;

-- Success message
DO $$
BEGIN
  RAISE NOTICE '✅ AIHedgeFund database initialized successfully';
  RAISE NOTICE '   PostgreSQL version: %', version();
  RAISE NOTICE '   Schema: aihedgefund';
  RAISE NOTICE '   Timezone: Europe/London';
END $$;
