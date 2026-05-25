-- Fix script for trip aQs9dF data inconsistencies
-- Run this script to clean up duplicate expenses and fix data issues

USE travelSchema_v2;

-- 1. Delete the duplicate/orphaned trek cost expense (expenseId 198)
-- This expense has no balance records and is causing the total calculation to be wrong
DELETE FROM expenses WHERE expenseId = 198;

-- 2. Update the medical certificate expense description (fix typo)
UPDATE expenses 
SET expenseDesc = 'Medical certificate'
WHERE expenseId = 203;

-- 3. Verify the fixes
-- Check remaining expenses for trip aQs9dF
SELECT expenseId, expenseAmount, expenseDesc, expenseSelf, expenseSplitBw 
FROM expenses 
WHERE tripId = 'aQs9dF' 
ORDER BY expenseId;

-- Check total amount (should now be 18048)
SELECT SUM(expenseAmount) as total_amount 
FROM expenses 
WHERE tripId = 'aQs9dF';

-- Check balance records (should be empty for self expenses)
SELECT * 
FROM Balance 
WHERE tripId = 'aQs9dF';