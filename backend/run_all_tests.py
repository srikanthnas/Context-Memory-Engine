import subprocess
import sys

TESTS = [

    # Core pipeline
    "test_core_memory_integration.py",
    "test_final_system_integration.py",

    # Image memory
    "test_image_memory_full_integration.py",

    # User profile
    "test_user_profile_extractor.py",
    "test_user_profile_upsert.py",
    "test_user_profile_integration.py",
    "test_user_profile_regression.py",

    # Explicit memory control
    "test_memory_command_parser.py",
    "test_memory_control_storage.py",
    "test_memory_control_integration.py",
]

print("=" * 70)
print("CONTEXT MEMORY ENGINE - FULL REGRESSION SUITE")
print("=" * 70)

passed = 0
failed = 0

for test in TESTS:

    print("\n" + "=" * 70)
    print("RUNNING:", test)
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, test]
    )

    if result.returncode == 0:
        passed += 1
    else:
        failed += 1

print("\n" + "=" * 70)
print("REGRESSION SUMMARY")
print("=" * 70)

print("Passed :", passed)
print("Failed :", failed)

if failed == 0:
    print("\nALL TESTS PASSED")
else:
    print("\nSOME TESTS FAILED")