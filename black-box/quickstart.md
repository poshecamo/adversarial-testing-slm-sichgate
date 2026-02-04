# SichGate Quick Start Guide

Get up and running with SichGate in under 5 minutes.

## Installation

Open your terminal and run these commands:

```bash
# Clone the repository
git clone https://github.com/poshecamo/adversarial-testing-slm-sichgate
cd black-box

# Install dependencies
pip install -r requirements.txt
```

That's it! SichGate is now installed.

## Your First Test

Run your first security assessment with a single command:

```bash
python run_sichgate.py
```

This will automatically download a sentiment analysis model (on first run only) and execute all available security tests against it. The entire process takes about two to three minutes, depending on your internet speed for the initial model download and your hardware for test execution.

## Understanding the Results

When the tests complete, you will see a summary that looks like this:

```
TEST SUMMARY
======================================================================

Overall Pass Rate: 73.5%
Total Tests: 35
Passed: 26
Failed: 9

Failures by Severity:
  CRITICAL: 3
  HIGH: 4
  MEDIUM: 2

Results by Category:
  Behavioral Subversion: 65.0% (13/20)
  Capability Failure: 86.7% (13/15)

Average Latency: 45.23ms
```

The pass rate tells you what percentage of security tests your model passed. A score above ninety percent is excellent, between seventy and ninety percent indicates some issues worth investigating, between fifty and seventy percent suggests significant problems, and below fifty percent represents critical vulnerabilities.

The failures by severity section shows how serious the detected issues are. Critical failures represent clear security vulnerabilities like successful prompt injection attacks. High severity indicates significant robustness problems. Medium suggests edge cases that should be addressed. Low represents minor inconsistencies.

Results by category breaks down performance across different threat types. Behavioral subversion tests check if the model can be manipulated to ignore its intended purpose. Capability failure tests verify that the model handles realistic input variations correctly.

## Detailed Results

All results are automatically saved to timestamped directories in the results folder. Navigate to the most recent directory and you will find three files.

The summary_report.txt file provides a human-readable assessment suitable for sharing with your team or stakeholders. This is the file you want to start with.

The summary_report.json file contains the same information in structured format, useful for programmatic analysis or integration with other tools.

The detailed_results.json file includes every individual test result with complete input, output, and evaluation data. This is valuable when you need to understand exactly why specific tests failed.

## What to Do With Failures

When you encounter test failures, the first step is to review the detailed results to understand what went wrong. Each failed test includes an explanation of why it failed and what the expected behavior should have been.

For critical failures, these represent serious vulnerabilities that should be addressed before production deployment. Common critical failures include successful prompt injection attacks where the model follows injected instructions instead of analyzing actual sentiment, or complete failure to handle basic input variations.

For high severity failures, investigate whether these represent systematic issues or isolated edge cases. If multiple similar tests fail, that suggests a pattern worth fixing. Consider whether retraining, adding specific examples to your training data, or implementing input validation could address these issues.

For medium and low severity failures, prioritize based on your specific deployment context. Some edge cases may be acceptable risks depending on your use case, while others might be critical for your particular application.

## Testing Your Own Model

To test your own HuggingFace model instead of the default, simply specify the model name:

```bash
python run_sichgate.py --model "your-username/your-model-name"
```

The model must be a binary sentiment classifier for the current test battery to work properly. Future versions of SichGate will support additional model types.

## Next Steps

Now that you have run your first security assessment, you might want to explore some more advanced capabilities.

To run only specific test categories:

```bash
python run_sichgate.py --scenarios behavioral  # Only prompt injection tests
python run_sichgate.py --scenarios capability  # Only robustness tests
```

To use SichGate programmatically in your own code:

```bash
python examples/usage_examples.py
```

This demonstrates how to integrate SichGate into your own testing workflows, create custom test cases, and analyze results in detail.

To learn about the framework architecture and how to extend it:

Read the full README.md for comprehensive documentation about the project structure, design philosophy, and how to contribute your own test scenarios.

## Getting Help

If tests are not running, first check that you have installed all requirements by running pip install -r requirements.txt again. Ensure you have internet connection for the initial model download. Verify that the model name is correct if you are testing a custom model.

If you are getting unexpected results, review the detailed results JSON to understand exactly what the model predicted versus what was expected. Consider whether the test assumptions match your model's actual training and intended use case. Remember that some test failures are expected, especially for models not specifically hardened against adversarial attacks.

For questions about how to interpret results or what actions to take, consult the main README.md which includes detailed guidance on understanding and responding to different types of failures.

## What's Next

This open-source version provides fundamental security testing with carefully crafted static test cases. SichGate Pro adds automated attack optimization, continuous monitoring, and comprehensive remediation guidance.

If you find SichGate valuable and want more sophisticated testing capabilities, visit https://sichgate.com to learn about the Pro version or contact support@sichgate.com to discuss your security testing needs.

Happy testing! Remember, finding vulnerabilities before attackers do is the first step toward building trustworthy AI systems.