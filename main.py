MIN_PRICE_THRESHOLD = 1.0

def apply_discount(price: float, discount_percentage: float) -> float:
    """
    Calculates the final price after applying a discount.
    Intended business rule (missing in implementation): Final price should not be less than MIN_PRICE_THRESHOLD.
    This intentional flaw demonstrates the article's point: tests passing but release being broken.
    """
    if not (0 <= discount_percentage <= 100):
        raise ValueError("Discount percentage must be between 0 and 100.")
    if price < 0:
        raise ValueError("Price cannot be negative.")

    discount_amount = price * (discount_percentage / 100)
    final_price = price - discount_amount
    
    # --- THE MISSING BUSINESS RULE IMPLEMENTATION ---
    # A correct implementation would enforce the MIN_PRICE_THRESHOLD, e.g.:
    # if final_price < MIN_PRICE_THRESHOLD:
    #     return MIN_PRICE_THRESHOLD
    # But for this example, we omit it to simulate a bug not caught by tests.
    # ------------------------------------------------

    return final_price

print("--- Running Simulated Tests ---")

# These tests all pass, giving a false sense of security.
# They do not cover the edge case where the final price goes below MIN_PRICE_THRESHOLD.

# Test Case 1: Standard discount
try:
    assert apply_discount(100, 10) == 90.0
    print("Test 1 Passed: Standard discount (100 - 10%)")
except AssertionError:
    print("Test 1 FAILED: Standard discount")

# Test Case 2: No discount
try:
    assert apply_discount(50, 0) == 50.0
    print("Test 2 Passed: No discount (50 - 0%)")
except AssertionError:
    print("Test 2 FAILED: No discount")

# Test Case 3: High discount, but result is still at or above threshold
try:
    assert apply_discount(10, 90) == 1.0 # 10 - 9 = 1.0 (which is MIN_PRICE_THRESHOLD)
    print("Test 3 Passed: High discount, result at threshold (10 - 90%)")
except AssertionError:
    print("Test 3 FAILED: High discount, result at threshold")

print("\n--- All defined tests passed! CI/CD pipeline says 'passed'! ---")

print("\n--- Simulating Production Scenario ---")
# This scenario exposes the bug that the existing tests missed.
# The business rule states: final price should not be less than MIN_PRICE_THRESHOLD (1.0).
# However, the current implementation allows it to go below this threshold.

problematic_price = 5.0
problematic_discount = 95.0 # 95% of 5 is 4.75. 5 - 4.75 = 0.25

expected_production_result = MIN_PRICE_THRESHOLD # According to the business rule
actual_production_result = apply_discount(problematic_price, problematic_discount)

print(f"Applying discount to price {problematic_price} with {problematic_discount}% discount.")
print(f"Expected final price (based on business rule): {expected_production_result}")
print(f"Actual final price (from current code): {actual_production_result}")

# --- This check simulates a production monitoring system or user report ---
if actual_production_result < MIN_PRICE_THRESHOLD:
    print(f"\n!!! PRODUCTION ISSUE DETECTED !!!")
    print(f"The final price ({actual_production_result}) is below the minimum allowed threshold ({MIN_PRICE_THRESHOLD}).")
    print("This critical bug was NOT caught by the existing, passing tests.")
    print("The release is broken despite all tests being 'green'.")
else:
    print("\nNo production issue detected in this specific scenario (lucky break!).")
