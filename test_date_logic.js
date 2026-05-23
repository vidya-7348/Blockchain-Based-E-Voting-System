// Test script to check date logic in JavaScript

console.log("=== Testing Date Logic ===");

// Simulate the dates from your voting_dates table
const resultDateStr = "2026-01-01T00:00:00"; // From your database
const resultDate = new Date(resultDateStr);
const currentDate = new Date();

console.log("Result date:", resultDate);
console.log("Current date:", currentDate);
console.log("Has result date passed?", currentDate >= resultDate);

// Test with a past date
const pastDate = new Date("2025-01-01T00:00:00");
console.log("\nTesting with past date:");
console.log("Past date:", pastDate);
console.log("Current date:", currentDate);
console.log("Has past date passed?", currentDate >= pastDate);

// Test with a future date
const futureDate = new Date("2027-01-01T00:00:00");
console.log("\nTesting with future date:");
console.log("Future date:", futureDate);
console.log("Current date:", currentDate);
console.log("Has future date passed?", currentDate >= futureDate);