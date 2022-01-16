"""
Run `python3 -m tests` from project root to run all test cases as a single TestSuite.
Add the test modules you want to run to the `test_modules` list below.
"""
import sys
import unittest

test_modules = [
    'tests.test_crypto',
    'tests.test_database',
    'tests.test_server'
]

suite = unittest.TestSuite()

for t in test_modules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

results = unittest.TextTestRunner().run(suite)
if results.errors or results.failures:
    sys.exit(1)

# `print(suite)` will output something like :
#
# <unittest.suite.TestSuite tests=[
#     <unittest.suite.TestSuite tests=[
#         <unittest.suite.TestSuite tests=[
#             <tests.test_crypto.TestCrypto testMethod=test_decryption_content>,
#             <tests.test_crypto.TestCrypto testMethod=test_decryption_key>,
#             <tests.test_crypto.TestCrypto testMethod=test_decryption_message>,
#             <tests.test_crypto.TestCrypto testMethod=test_encryption_content>,
#             <tests.test_crypto.TestCrypto testMethod=test_encryption_key>,
#             <tests.test_crypto.TestCrypto testMethod=test_encryption_message>,
#             <tests.test_crypto.TestCrypto testMethod=test_key_creation>,
#             <tests.test_crypto.TestCrypto testMethod=test_key_size>,
#             <tests.test_crypto.TestCrypto testMethod=test_key_unique>
#         ]>
#     ]>,
#     <unittest.suite.TestSuite tests=[
#         <unittest.suite.TestSuite tests=[
#             <tests.test_database.TestDatabase testMethod=test_is_ip_valid>,
#             <tests.test_database.TestDatabase testMethod=test_is_password_valid>,
#             <tests.test_database.TestDatabase testMethod=test_is_port_valid>,
#             <tests.test_database.TestDatabase testMethod=test_is_user_registered>,
#             <tests.test_database.TestDatabase testMethod=test_is_username_valid>,
#             <tests.test_database.TestDatabase testMethod=test_user_create>,
#             <tests.test_database.TestDatabase testMethod=test_user_login>
#         ]>
#     ]>
# ]>
