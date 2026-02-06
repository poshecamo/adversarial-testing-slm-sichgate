
SichGate - AI Security Testing Framework

Open Source Edition v0.1.0

SichGate is a black-box security testing framework for AI systems, focusing on detecting behavioral subversion, capability failures, and information disclosure vulnerabilities in language models.

This is the free open-source version providing fundamental security testing capabilities. SichGate Pro offers advanced features including automated attack optimization, continuous monitoring, and comprehensive remediation guidance.

What SichGate Tests For

SichGate organizes security testing around three primary threat models that represent real-world risks to AI deployments:

Behavioral Subversion tests whether an attacker can manipulate the model to behave contrary to its intended purpose or violate safety policies. This includes prompt injection attacks where malicious instructions are embedded in user input, jailbreaking attempts that try to bypass safety constraints through role-play or context manipulation, and policy bypass techniques that attempt to make the model ignore its training.

Capability Failure tests whether the model reliably performs its intended function when faced with realistic input variations or edge cases. This includes robustness to typos and misspellings, handling of semantic complexity like double negatives and sarcasm, format variation tolerance across different capitalization and punctuation patterns, and edge case handling for ambiguous or contradictory inputs.

Information Disclosure tests whether the model inappropriately reveals information about its training data, architecture, or internal state. This includes training data extraction attempts, membership inference to detect if specific data was in the training set, and capability disclosure where the model reveals details about its own limitations or design.

The current release focuses on behavioral subversion and capability failure testing for sentiment analysis models. Future releases will expand to other model types and add information disclosure scenarios.

Quick Start

Get started with SichGate in three simple steps. First, clone the repository and install dependencies:

git clone https://github.com/poshecamo/adversarial-testing-slm-sichgate
cd black-box
pip install -r requirements.txt

Next, run your first security assessment using the default model:

python run_sichgate.py

The framework will download the model if needed on first run, then execute all available test scenarios and generate a comprehensive report in the results directory.

Understanding the Output

When you run SichGate, you will see real-time progress as each test executes, showing pass or fail status immediately. The console displays an executive summary at the end with your overall pass rate, failures broken down by severity level, and results organized by threat category. All detailed results are automatically saved to timestamped directories in the results folder.

The generated reports include three key files. The detailed_results.json file contains complete test-by-test results with full input, output, and evaluation data for programmatic analysis. The summary_report.json provides high-level statistics and aggregated metrics in a structured format. The summary_report.txt offers a human-readable assessment report suitable for sharing with stakeholders who may not be technical.

How to Interpret Results

Understanding what your pass rate means is crucial for taking appropriate action. A pass rate above ninety percent indicates strong security posture with only minor issues detected. Most production systems should target this level. A pass rate between seventy and ninety percent suggests moderate vulnerabilities that should be reviewed and addressed, though the system may still be deployable with appropriate documentation and monitoring. Pass rates between fifty and seventy percent indicate significant security issues requiring remediation before production deployment. Below fifty percent represents critical vulnerabilities requiring immediate attention and likely necessitating architectural changes or retraining.

Pay special attention to failures marked as critical severity, as these represent clear policy bypasses or major reliability issues that could be exploited in production. High severity failures indicate significant robustness problems that would affect real-world performance. Medium severity failures are edge cases that should be addressed but may not block deployment. Low severity findings are minor inconsistencies worth noting but rarely deployment blockers.

Customization Options

While SichGate is designed to work well with zero configuration, you can customize the testing process to match your needs. To test a specific HuggingFace model, use the model parameter:

python run_sichgate.py --model "your-model-name"

You can run only specific test scenarios rather than the full suite:

python run_sichgate.py --scenarios behavioral  # Only prompt injection tests
python run_sichgate.py --scenarios capability  # Only robustness tests

To save results to a specific directory:

python run_sichgate.py --output my-test-results/

For automated testing in CI/CD pipelines, use quiet mode to minimize output:

python run_sichgate.py --quiet

Project Structure

The codebase is organized to make it easy to understand, extend, and maintain. The core directory contains the fundamental framework components. The model_interface.py file provides abstractions for different model types, allowing tests to work across HuggingFace models, local PyTorch models, and API endpoints. The test_infrastructure.py file defines how tests are structured, executed, and evaluated, including the TestCase, TestScenario, and TestRunner classes that form the backbone of the framework.

The scenarios directory contains actual security test definitions organized by threat category. The behavioral_subversion.py file includes prompt injection and jailbreaking tests targeting policy compliance. The capability_failure.py file contains robustness tests for typos, semantic edge cases, and format variations.

Results are saved in the results directory, with each test run creating a timestamped subdirectory containing all outputs. The run_sichgate.py file serves as the main entry point with command-line argument parsing and orchestration logic.

Adding Custom Tests

One of SichGate's key design goals is extensibility. Adding new test cases to existing scenarios is straightforward and requires no changes to the core framework. Here is an example of adding a new prompt injection test:

In scenarios/behavioral_subversion.py

TestCase(
    id="PROMPT_INJ_021",
    name="Your Custom Test Name",
    description="Clear description of what this tests",
    category=ThreatCategory.BEHAVIORAL_SUBVERSION,
    severity=Severity.HIGH,
    input_text="Your test input here",
    expected_behavior={'label': 'EXPECTED_LABEL'},
    metadata={
        'technique': 'your_technique',
        'expected_reason': 'Why we expect this result'
    }
)

Creating entirely new test scenarios follows a similar pattern. You can define a new scenario function that returns a TestScenario object containing your test cases, then add it to the appropriate get_all scenarios function. The framework automatically picks up and executes new scenarios without requiring changes to the runner.

Design Philosophy

SichGate is built on several key principles that guide its architecture and functionality. Tests are declarative, meaning you describe what to test rather than how to test it. The framework handles all execution logic automatically. Tests are self-documenting, with each test case including clear descriptions, expected behaviors, and metadata explaining why the test matters. The framework is modular, allowing you to run individual scenarios, combine them in different ways, or add new scenarios without modifying core code. Reports are actionable, organized around business-relevant threat categories rather than technical implementation details, making findings immediately useful for decision-making.

Most importantly, the free version is genuinely useful, not crippled. The open-source edition provides real security value through carefully crafted static test batteries. The Pro version adds automation and optimization, not functionality that should have been free.

Limitations of the Open Source Version

The current release focuses on sentiment analysis models and binary classification tasks. Future releases will add support for question answering, text generation, and other model types. All testing is currently black-box with hard labels, meaning you provide input and get back predictions without confidence scores. Grey-box and white-box testing capabilities will be added in future releases.

Test cases are static and manually crafted rather than automatically generated. This provides high-quality tests with clear rationale but does not adapt to your specific model's weaknesses. The automated attack optimization available in SichGate Pro uses gradient-based and evolutionary techniques to find your model's unique vulnerabilities.

What SichGate Pro Adds

SichGate Pro extends the open-source foundation with advanced capabilities designed for enterprise security teams. Automated attack optimization uses gradient-based techniques to find minimal perturbations that cause failures, implements Optuna-powered hyperparameter search to maximize attack success rates, and automatically generates adversarial examples tailored to your model architecture.

Comprehensive reporting includes detailed remediation guidance for each vulnerability class, maps findings to compliance frameworks including NIST AI RMF and ISO standards, and provides executive summaries with business impact analysis. Continuous monitoring re-tests models automatically as they are updated, detects regression when new versions introduce vulnerabilities, and integrates with CI/CD pipelines for automated security gates.

Multi-modal support extends testing beyond text to include images, audio, video, and documents. Custom model support includes APIs for proprietary models, local models with custom architectures, and fine-tuned models with specialized evaluation needs. Priority support provides direct access to security researchers, custom test development for your specific use cases, and incident response assistance for security events.

For more information about SichGate Pro, visit our website at https://sichgate.com.

Contributing

SichGate is open source and we welcome contributions. The most valuable contributions are new test scenarios that identify real-world vulnerabilities, test cases covering additional attack techniques, support for new model types beyond sentiment analysis, and improvements to reporting and visualization.

Before submitting a pull request, please ensure your tests include clear descriptions and expected behaviors, are based on documented attack techniques or real-world vulnerabilities, and include metadata explaining the security significance. Run the existing test suite to ensure your changes do not break existing functionality, and add documentation explaining what your contribution does and why it matters.

License

SichGate Open Source Edition is released under the MIT License. This means you are free to use it commercially, modify it for your needs, distribute it to others, and sublicense it as needed. The only requirements are that you include the original copyright notice and license text, and you understand the software is provided as-is without warranty.

Acknowledgments

SichGate builds on research from the AI safety and adversarial machine learning communities. We are grateful for the foundational work done by researchers at institutions worldwide who have identified and documented the attack techniques we test for.

The framework uses HuggingFace Transformers for model loading and inference, PyTorch as the underlying ML framework, and the amazing open-source ecosystem that makes modern ML development possible.

Support

For questions about the open-source edition, please open an issue on GitHub. For SichGate Pro inquiries, contact support at sichgate.com.


