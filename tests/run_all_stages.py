"""
Master Verification Suite for SwarmForge Dark Factory (Stages 1 through 4).
Runs all stage test suites and verifies complete zero-dependency compliance.
"""
import sys
import unittest
import os
import time

def run_all_stages():
    start_time = time.time()
    print("=" * 70)
    print("[+] SWARMFORGE DARK FACTORY -- COMPREHENSIVE STAGES 1-4 VERIFICATION")
    print("=" * 70)
    
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Load Stage 1
    s1_path = os.path.join(repo_root, "stage-1")
    if s1_path not in sys.path:
        sys.path.insert(0, s1_path)
    import test_stage1
    suite.addTests(loader.loadTestsFromModule(test_stage1))

    # Load Stage 2
    s2_path = os.path.join(repo_root, "stage-2")
    if s2_path not in sys.path:
        sys.path.insert(0, s2_path)
    import test_stage2
    suite.addTests(loader.loadTestsFromModule(test_stage2))

    # Load Stage 3
    s3_path = os.path.join(repo_root, "stage-3")
    if s3_path not in sys.path:
        sys.path.insert(0, s3_path)
    import test_stage3
    suite.addTests(loader.loadTestsFromModule(test_stage3))

    # Load Stage 4
    s4_path = os.path.join(repo_root, "stage-4")
    if s4_path not in sys.path:
        sys.path.insert(0, s4_path)
    import test_stage4
    suite.addTests(loader.loadTestsFromModule(test_stage4))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("-" * 70)
    print(f"[*] Summary: Ran {result.testsRun} tests in {elapsed:.3f}s")
    print(f"[OK] Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"[!] Failures: {len(result.failures)} | Errors: {len(result.errors)}")
    print("-" * 70)

    if result.wasSuccessful():
        print("[SUCCESS] 100% VERIFIED: ALL 4 DARK FACTORY STAGES ARE PRODUCTION READY!")
        print("=" * 70)
        return 0
    else:
        print("[FAILED] Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_stages())
