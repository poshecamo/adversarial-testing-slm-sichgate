"""
SichGate Usage Example

This script demonstrates how to use SichGate programmatically rather than
through the command-line interface. This is useful when you want to:

- Integrate SichGate into your own testing pipeline
- Customize test execution logic
- Build custom reporting
- Run tests as part of automated workflows

The examples progress from simple to advanced usage patterns.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.model_interface import HuggingFaceSentimentModel
from core.test_infrastructure import TestRunner, TestCase, TestScenario, ThreatCategory, Severity
from scenarios.behavioral_subversion import create_prompt_injection_scenario
from scenarios.capability_failure import (
    create_typo_robustness_scenario,
    create_semantic_edge_cases_scenario
)


def example_1_basic_usage():
    """
    Example 1: Basic usage - load model and run a single scenario
    
    This is the simplest way to use SichGate. You load a model, load a
    test scenario, and execute it. Perfect for getting started.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage")
    print("="*70 + "\n")
    
    # Load the model you want to test
    print("Loading model...")
    model = HuggingFaceSentimentModel()
    
    # Create a test runner
    runner = TestRunner(model)
    
    # Load a test scenario
    scenario = create_prompt_injection_scenario()
    
    # Run the tests
    print(f"\nRunning {len(scenario)} tests...\n")
    results = runner.run_scenario(scenario, verbose=True)
    
    # Get summary statistics
    summary = runner.get_summary_stats()
    print(f"\nPass rate: {summary['pass_rate']:.1%}")
    print(f"Critical failures: {summary['failures_by_severity']['critical']}")


def example_2_multiple_scenarios():
    """
    Example 2: Running multiple test scenarios
    
    Often you want to run several related test scenarios together to get
    a comprehensive assessment. This example shows how to do that and
    how to analyze results by scenario.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple Scenarios")
    print("="*70 + "\n")
    
    # Load model
    model = HuggingFaceSentimentModel()
    runner = TestRunner(model)
    
    # Load multiple scenarios
    scenarios = [
        create_prompt_injection_scenario(),
        create_typo_robustness_scenario(),
        create_semantic_edge_cases_scenario()
    ]
    
    # Run all scenarios
    all_results = runner.run_multiple_scenarios(scenarios, verbose=False)
    
    # Analyze results by scenario
    print("\nResults by Scenario:")
    print("-" * 70)
    
    for scenario in scenarios:
        scenario_results = all_results[scenario.id]
        passed = sum(1 for r in scenario_results if r.passed)
        total = len(scenario_results)
        
        print(f"\n{scenario.name}:")
        print(f"  Pass Rate: {passed/total:.1%} ({passed}/{total})")
        
        # Show critical failures for this scenario
        critical_fails = [r for r in scenario_results 
                         if not r.passed and r.severity == Severity.CRITICAL]
        
        if critical_fails:
            print(f"  Critical Failures: {len(critical_fails)}")
            for fail in critical_fails[:3]:  # Show first 3
                print(f"    - {fail.test_name}")


def example_3_custom_test_case():
    """
    Example 3: Creating and running custom test cases
    
    Sometimes you want to test specific inputs relevant to your use case.
    This example shows how to create custom test cases on the fly and
    run them alongside the standard test battery.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Test Cases")
    print("="*70 + "\n")
    
    # Load model
    model = HuggingFaceSentimentModel()
    runner = TestRunner(model)
    
    # Create custom test cases specific to your domain
    # For example, if you're deploying this for product reviews,
    # you might want to test specific product-related inputs
    
    custom_tests = [
        TestCase(
            id="CUSTOM_001",
            name="Product Return Scenario",
            description="Tests sentiment on return-related text",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="I had to return this product, but the refund process was smooth and helpful.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={'domain': 'product_reviews', 'aspect': 'returns'}
        ),
        
        TestCase(
            id="CUSTOM_002",
            name="Mixed Feature Review",
            description="Tests handling of mixed feature satisfaction",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="Camera is excellent but battery life is disappointing.",
            expected_behavior={'label': 'NEGATIVE'},  # Negative aspect mentioned last
            metadata={'domain': 'product_reviews', 'aspect': 'features'}
        ),
        
        TestCase(
            id="CUSTOM_003",
            name="Delayed Shipment Positive Outcome",
            description="Tests sentiment when complaint is resolved",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="Shipping was delayed, but customer service made it right with a discount.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={'domain': 'product_reviews', 'aspect': 'service_recovery'}
        )
    ]
    
    # Create a custom scenario from your tests
    custom_scenario = TestScenario(
        id="custom_product_review_tests",
        name="Domain-Specific Product Review Tests",
        description="Tests specific to our product review use case",
        category=ThreatCategory.CAPABILITY_FAILURE,
        test_cases=custom_tests
    )
    
    # Run your custom tests
    results = runner.run_scenario(custom_scenario, verbose=True)
    
    # Analyze custom test results
    passed = sum(1 for r in results if r.passed)
    print(f"\nCustom tests pass rate: {passed/len(results):.1%}")


def example_4_analyzing_failures():
    """
    Example 4: Detailed failure analysis
    
    When tests fail, you need to understand why. This example shows how to
    drill into failure details to identify patterns and prioritize fixes.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Analyzing Failures")
    print("="*70 + "\n")
    
    # Load and run tests
    model = HuggingFaceSentimentModel()
    runner = TestRunner(model)
    
    scenario = create_prompt_injection_scenario()
    results = runner.run_scenario(scenario, verbose=False)
    
    # Get all failures
    failures = [r for r in results if not r.passed]
    
    print(f"Total failures: {len(failures)}\n")
    
    # Analyze failures by attack technique
    print("Failures by Attack Technique:")
    print("-" * 70)
    
    technique_failures = {}
    for fail in failures:
        technique = fail.metadata.get('technique', 'unknown')
        if technique not in technique_failures:
            technique_failures[technique] = []
        technique_failures[technique].append(fail)
    
    for technique, fails in technique_failures.items():
        print(f"\n{technique.replace('_', ' ').title()}: {len(fails)} failure(s)")
        
        # Show example
        if fails:
            example = fails[0]
            print(f"  Example: {example.test_name}")
            print(f"  Input: {example.input_text[:80]}...")
            print(f"  Expected: {example.expected_behavior['label']}")
            print(f"  Got: {example.actual_output['label']}")
            print(f"  Reason: {example.failure_reason}")


def example_5_performance_analysis():
    """
    Example 5: Performance and latency analysis
    
    Security testing also reveals performance characteristics. This example
    shows how to analyze the latency distribution of your tests.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Performance Analysis")
    print("="*70 + "\n")
    
    # Run tests
    model = HuggingFaceSentimentModel()
    runner = TestRunner(model)
    
    scenarios = [create_prompt_injection_scenario()]
    runner.run_multiple_scenarios(scenarios, verbose=False)
    
    # Analyze latency
    latencies = [r.latency_ms for r in runner.results]
    
    print("Latency Statistics:")
    print("-" * 70)
    print(f"Mean: {sum(latencies)/len(latencies):.2f}ms")
    print(f"Min: {min(latencies):.2f}ms")
    print(f"Max: {max(latencies):.2f}ms")
    
    # Check if any tests are unusually slow
    mean_latency = sum(latencies) / len(latencies)
    slow_tests = [r for r in runner.results if r.latency_ms > mean_latency * 2]
    
    if slow_tests:
        print(f"\nSlow tests (>2x mean latency): {len(slow_tests)}")
        for test in slow_tests[:5]:  # Show first 5
            print(f"  - {test.test_name}: {test.latency_ms:.2f}ms")


def example_6_batch_testing():
    """
    Example 6: Efficient batch testing
    
    When testing many inputs, batch processing can be significantly faster
    than individual predictions. This example shows how to leverage batching.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Batch Testing (Advanced)")
    print("="*70 + "\n")
    
    model = HuggingFaceSentimentModel()
    
    # Collect all test inputs
    scenario = create_prompt_injection_scenario()
    test_inputs = [tc.input_text for tc in scenario.test_cases]
    
    print(f"Testing {len(test_inputs)} inputs in batch mode...\n")
    
    # Use batch prediction for efficiency
    import time
    start = time.time()
    batch_results = model.predict_batch(test_inputs)
    batch_time = time.time() - start
    
    print(f"Batch processing completed in {batch_time:.2f}s")
    print(f"Average time per input: {batch_time/len(test_inputs)*1000:.2f}ms")
    
    # Compare to individual predictions
    print("\nNote: Batch processing is typically 2-5x faster than individual")
    print("predictions, depending on batch size and hardware.")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("SICHGATE USAGE EXAMPLES")
    print("="*70)
    print("\nThese examples demonstrate different ways to use SichGate")
    print("programmatically in your own testing workflows.\n")
    
    # Run each example
    # Uncomment the examples you want to run
    
    example_1_basic_usage()
    # example_2_multiple_scenarios()
    # example_3_custom_test_case()
    # example_4_analyzing_failures()
    # example_5_performance_analysis()
    # example_6_batch_testing()
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("\nTo run other examples, edit this file and uncomment them in main()")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()