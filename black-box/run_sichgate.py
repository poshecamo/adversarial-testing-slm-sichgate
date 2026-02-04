#!/usr/bin/env python3

# Usage:
#     python run_sichgate.py                    # Run all tests with default model
#     python run_sichgate.py --scenarios all    # Explicit: run everything
#     python run_sichgate.py --scenarios behavioral  # Run only behavioral tests
#     python run_sichgate.py --model {name    # Test specific model
#     python run_sichgate.py --output results/  # Specify output directory


import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from model_interface import HuggingFaceSentimentModel
from test_infrastructure import TestRunner, ThreatCategory
from behavioral_subversion import get_all_behavioral_scenarios
from capability_failure import get_all_capability_scenarios


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███████╗██╗ ██████╗██╗  ██╗ ██████╗  █████╗ ████████╗███████╗
║   ██╔════╝██║██╔════╝██║  ██║██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
║   ███████╗██║██║sich/███████║██║  ███╗███████║   ██║   █████╗  
║   ╚════██║██║██║gate ██╔══██║██║   ██║██╔══██║   ██║   ██╔══╝  
║   ███████║██║╚██████╗██║  ██║╚██████╔╝██║  ██║   ██║   ███████╗
║   ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
║                                                               ║
║            AI/ML Security Testing Framework - v0.1.0          ║
║                  Open Source Edition                          ║
╚═══════════════════════════════════════════════════════════════╝

Testing AI/ML systems for behavioral subversion, capability failures,
and information disclosure vulnerabilities.

This is the free open-source version. SichGate Pro includes:
  • Automated attack optimization using gradient-based techniques
  • Comprehensive vulnerability reports with remediation guidance  
  • Continuous monitoring and regression testing
  • Support for custom models and multi-modal inputs
  
Learn more: https://sichgate.com
Contact: support@sichgate.com

"""
    print(banner)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='SichGate AI Security Testing Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    Run all tests with default model
  %(prog)s --scenarios behavioral            Run only behavioral subversion tests
  %(prog)s --scenarios capability            Run only capability failure tests
  %(prog)s --model "model-name"              Test specific HuggingFace model
  %(prog)s --output results/my-test/         Save results to specific directory
  %(prog)s --quiet                           Minimal output, only summary

Scenarios:
  all          - All available test scenarios (default)
  behavioral   - Behavioral subversion tests (prompt injection, jailbreaking)
  capability   - Capability failure tests (robustness, edge cases)
        """
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='distilbert-base-uncased-finetuned-sst-2-english',
        help='HuggingFace model name to test (default: distilbert sentiment model)'
    )
    
    parser.add_argument(
        '--scenarios',
        type=str,
        default='all',
        choices=['all', 'behavioral', 'capability'],
        help='Which test scenarios to run (default: all)'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('results'),
        help='Directory to save results (default: ./results/)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output, only show summary'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip the banner display'
    )
    
    return parser.parse_args()


def load_scenarios(scenario_choice: str):
    """Load the requested test scenarios"""
    scenarios = []
    
    if scenario_choice in ['all', 'behavioral']:
        scenarios.extend(get_all_behavioral_scenarios())
    
    if scenario_choice in ['all', 'capability']:
        scenarios.extend(get_all_capability_scenarios())
    
    return scenarios


def save_results(runner: TestRunner, scenarios, output_dir: Path, model_name: str):
    """
    Save test results in multiple formats for different audiences.
    
    We generate:
    - detailed_results.json: Complete test-by-test results for analysis
    - summary_report.json: High-level summary statistics
    - summary_report.txt: Human-readable text summary
    """
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp for this test run
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    run_dir = output_dir / f"run_{timestamp}"
    run_dir.mkdir(exist_ok=True)
    
    # Save detailed results
    detailed_results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'sichgate_version': '0.1.0',
            'test_type': 'open_source_edition'
        },
        'scenarios': {
            scenario.id: {
                'name': scenario.name,
                'description': scenario.description,
                'category': scenario.category.value,
                'total_tests': len(scenario.test_cases),
                'results': [
                    r.to_dict() for r in runner.results 
                    if any(tc.id == r.test_id for tc in scenario.test_cases)
                ]
            }
            for scenario in scenarios
        }
    }
    
    with open(run_dir / 'detailed_results.json', 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    # Generate summary statistics
    summary = runner.get_summary_stats()
    summary['metadata'] = detailed_results['metadata']
    
    with open(run_dir / 'summary_report.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Generate human-readable text summary
    generate_text_report(summary, scenarios, run_dir / 'summary_report.txt')
    
    print(f"\n{'='*70}")
    print(f"Results saved to: {run_dir}")
    print(f"{'='*70}")
    
    return run_dir


def generate_text_report(summary: dict, scenarios, output_path: Path):
    """Generate a human-readable text report"""
    
    with open(output_path, 'w') as f:
        # Header
        f.write("="*70 + "\n")
        f.write("SICHGATE SECURITY ASSESSMENT REPORT\n")
        f.write("="*70 + "\n\n")
        
        # Metadata
        f.write(f"Test Date: {summary['metadata']['timestamp']}\n")
        f.write(f"Model Tested: {summary['metadata']['model']}\n")
        f.write(f"SichGate Version: {summary['metadata']['sichgate_version']}\n\n")
        
        # Executive Summary
        f.write("-"*70 + "\n")
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-"*70 + "\n\n")
        
        pass_rate = summary['pass_rate'] * 100
        f.write(f"Overall Pass Rate: {pass_rate:.1f}%\n")
        f.write(f"Total Tests Run: {summary['total_tests']}\n")
        f.write(f"Tests Passed: {summary['passed']}\n")
        f.write(f"Tests Failed: {summary['failed']}\n\n")
        
        # Security Risk Assessment
        f.write("Security Risk Level: ")
        if pass_rate >= 90:
            f.write("LOW - Model shows strong security posture\n")
        elif pass_rate >= 70:
            f.write("MEDIUM - Some vulnerabilities detected, review recommended\n")
        elif pass_rate >= 50:
            f.write("HIGH - Significant vulnerabilities found, remediation needed\n")
        else:
            f.write("CRITICAL - Severe vulnerabilities detected, immediate action required\n")
        f.write("\n")
        
        # Failures by Severity
        f.write("-"*70 + "\n")
        f.write("FAILURES BY SEVERITY\n")
        f.write("-"*70 + "\n\n")
        
        for severity, count in summary['failures_by_severity'].items():
            if count > 0:
                f.write(f"{severity.upper()}: {count} failure(s)\n")
        f.write("\n")
        
        # Results by Category
        f.write("-"*70 + "\n")
        f.write("RESULTS BY THREAT CATEGORY\n")
        f.write("-"*70 + "\n\n")
        
        for category, stats in summary['results_by_category'].items():
            cat_pass_rate = stats['pass_rate'] * 100
            f.write(f"{category.replace('_', ' ').title()}:\n")
            f.write(f"  Pass Rate: {cat_pass_rate:.1f}%\n")
            f.write(f"  Passed: {stats['passed']}/{stats['total']}\n")
            f.write(f"  Failed: {stats['failed']}/{stats['total']}\n\n")
        
        # Scenario Details
        f.write("-"*70 + "\n")
        f.write("SCENARIO DETAILS\n")
        f.write("-"*70 + "\n\n")
        
        for scenario in scenarios:
            f.write(f"Scenario: {scenario.name}\n")
            f.write(f"Description: {scenario.description}\n")
            
            # Calculate pass rate for this scenario
            scenario_results = [
                r for r in summary.get('results', [])
                if any(tc.id == r.get('test_id') for tc in scenario.test_cases)
            ]
            # ... (we'd calculate from the runner's results, but we don't have access here)
            
            if scenario.pro_version_note:
                f.write(f"\nPro Version: {scenario.pro_version_note}\n")
            
            f.write("\n")
        
        # Performance Metrics
        f.write("-"*70 + "\n")
        f.write("PERFORMANCE METRICS\n")
        f.write("-"*70 + "\n\n")
        
        perf = summary['performance']
        f.write(f"Average Latency: {perf['average_latency_ms']:.2f}ms\n")
        f.write(f"Min Latency: {perf['min_latency_ms']:.2f}ms\n")
        f.write(f"Max Latency: {perf['max_latency_ms']:.2f}ms\n\n")
        
        # Footer
        f.write("="*70 + "\n")
        f.write("This report was generated by SichGate Open Source Edition.\n")
        f.write("\nFor more sophisticated testing including automated attack\n")
        f.write("optimization, detailed remediation guidance, and continuous\n")
        f.write("monitoring, contact sales@sichgate.com for SichGate Pro.\n")
        f.write("="*70 + "\n")


def print_summary(summary: dict):
    """Print summary to console"""
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}\n")
    
    pass_rate = summary['pass_rate'] * 100
    print(f"Overall Pass Rate: {pass_rate:.1f}%")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}\n")
    
    print("Failures by Severity:")
    for severity, count in summary['failures_by_severity'].items():
        if count > 0:
            print(f"  {severity.upper()}: {count}")
    
    print("\nResults by Category:")
    for category, stats in summary['results_by_category'].items():
        cat_pass_rate = stats['pass_rate'] * 100
        print(f"  {category.replace('_', ' ').title()}: {cat_pass_rate:.1f}% ({stats['passed']}/{stats['total']})")
    
    print(f"\nAverage Latency: {summary['performance']['average_latency_ms']:.2f}ms")


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Display banner unless suppressed
    if not args.no_banner:
        print_banner()
    
    # Load the model
    print(f"Loading model: {args.model}")
    print("(This may take a moment on first run as weights are downloaded...)\n")
    
    try:
        model = HuggingFaceSentimentModel(args.model)
    except Exception as e:
        print(f"\nError loading model: {e}")
        print("\nPlease ensure:")
        print("  1. You have internet connection (for first-time download)")
        print("  2. The model name is correct")
        print("  3. You have installed required packages: pip install -r requirements.txt")
        sys.exit(1)
    
    # Load scenarios
    scenarios = load_scenarios(args.scenarios)
    
    if not scenarios:
        print(f"Error: No scenarios found for choice '{args.scenarios}'")
        sys.exit(1)
    
    print(f"Loaded {len(scenarios)} test scenario(s)\n")
    
    # Create test runner
    runner = TestRunner(model)
    
    # Execute tests
    verbose = not args.quiet
    runner.run_multiple_scenarios(scenarios, verbose=verbose)
    
    # Display summary
    summary = runner.get_summary_stats()
    print_summary(summary)
    
    # Save results
    output_dir = save_results(runner, scenarios, args.output, args.model)
    
    print("\nReview the detailed results in the output directory.")
    print("\nThank you for using SichGate Open Source Edition!")
    print("For advanced testing capabilities, visit https://sichgate.com\n")
    
    # Exit with appropriate code
    # Exit code 1 if any critical failures, 0 otherwise
    critical_failures = summary['failures_by_severity'].get('critical', 0)
    sys.exit(1 if critical_failures > 0 else 0)


if __name__ == '__main__':
    main()