# Test the logic for showing dev_otp
EMAIL_ENABLED = True
OTP_DEBUG = True
email = "test@example.com"

# Original logic
original_result = OTP_DEBUG or not (EMAIL_ENABLED if email else False)
print(f"Original logic result: {original_result}")

# Fixed logic
fixed_result = not (EMAIL_ENABLED if email else False)
print(f"Fixed logic result: {fixed_result}")

# Expected behavior:
# When EMAIL_ENABLED=True and email is provided, dev_otp should NOT be shown
# When EMAIL_ENABLED=False and email is provided, dev_otp should be shown
# When email is not provided, dev_otp should be shown (for phone OTP)

print("\nTesting different scenarios:")
print("1. EMAIL_ENABLED=True, email provided:", not (EMAIL_ENABLED if email else False))
print("2. EMAIL_ENABLED=False, email provided:", not (False if email else False))
print("3. EMAIL_ENABLED=True, email not provided:", not (EMAIL_ENABLED if None else False))
print("4. EMAIL_ENABLED=False, email not provided:", not (False if None else False))