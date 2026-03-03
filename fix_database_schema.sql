-- SQL script to add missing columns to finance_cash_submissions table
-- This should be run if the Django migration fails

-- For SQLite
ALTER TABLE finance_cash_submissions ADD COLUMN amount_cash DECIMAL(15,2) DEFAULT 0;
ALTER TABLE finance_cash_submissions ADD COLUMN amount_card DECIMAL(15,2) DEFAULT 0;
ALTER TABLE finance_cash_submissions ADD COLUMN amount_terminal DECIMAL(15,2) DEFAULT 0;
ALTER TABLE finance_cash_submissions ADD COLUMN amount_other DECIMAL(15,2) DEFAULT 0;

-- For PostgreSQL (if needed)
-- ALTER TABLE finance_cash_submissions ADD COLUMN amount_cash NUMERIC(15,2) DEFAULT 0;
-- ALTER TABLE finance_cash_submissions ADD COLUMN amount_card NUMERIC(15,2) DEFAULT 0;
-- ALTER TABLE finance_cash_submissions ADD COLUMN amount_terminal NUMERIC(15,2) DEFAULT 0;
-- ALTER TABLE finance_cash_submissions ADD COLUMN amount_other NUMERIC(15,2) DEFAULT 0;