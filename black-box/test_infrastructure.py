
# Architecture:
# - TestCase: Individual test with input, expected behavior, and evaluation logic
# - TestScenario: Group of related tests targeting a specific threat
# - TestResult: Structured output from running a test
# - TestRunner: Orchestration layer that executes tests and aggregates results
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import time
from datetime import datetime


class ThreatCategory(Enum):
    """
    High-level categorization of security threats.
    
    These map to the three threat models we discussed:
    - Behavioral subversion (can attacker manipulate behavior?)
    - Capability failure (is the model reliable?)
    - Information disclosure (does the model leak sensitive info?)
    """
    BEHAVIORAL_SUBVERSION = "behavioral_subversion"
    CAPABILITY_FAILURE = "capability_failure"
    INFORMATION_DISCLOSURE = "information_disclosure"


class Severity(Enum):
    
    # Severity levels for test failures.
    # - CRITICAL: Immediate security risk (e.g., policy bypass)
    # - HIGH: Significant reliability issue (e.g., consistent misclassification)
    # - MEDIUM: Edge case that could cause problems
    # - LOW: Minor inconsistency
    # - INFO: Informational finding, not necessarily a vulnerability
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class TestCase:
    
    id: str
    name: str
    description: str
    category: ThreatCategory
    severity: Severity
    input_text: str
    expected_behavior: Dict[str, Any]
    evaluation_fn: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.evaluation_fn is None:
            # Default: check if predicted label matches expected label
            self.evaluation_fn = lambda pred, expected: pred['label'] == expected.get('label')


@dataclass
class TestResult:  
    test_id: str
    test_name: str
    passed: bool
    category: ThreatCategory
    severity: Severity
    
    # What we sent to the model
    input_text: str
    
    # What we expected vs what we got
    expected_behavior: Dict[str, Any]
    actual_output: Dict[str, Any]
    
    # Performance metrics
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Explanation of pass/fail
    failure_reason: Optional[str] = None
    
    # Additional context
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
       #Convert to dictionary for JSON serialization.
        return {
            'test_id': self.test_id,
            'test_name': self.test_name,
            'passed': self.passed,
            'category': self.category.value,
            'severity': self.severity.value,
            'input_text': self.input_text,
            'expected_behavior': self.expected_behavior,
            'actual_output': self.actual_output,
            'latency_ms': self.latency_ms,
            'timestamp': self.timestamp,
            'failure_reason': self.failure_reason,
            'metadata': self.metadata
        }


@dataclass
class TestScenario:
    
    id: str
    name: str
    description: str
    category: ThreatCategory
    test_cases: List[TestCase]
    
    # Pro version disclaimer
    pro_version_note: Optional[str] = None
    
    def __len__(self):
        return len(self.test_cases)
    
    def get_severity_counts(self) -> Dict[str, int]:
        counts = {severity.value: 0 for severity in Severity}
        for test in self.test_cases:
            counts[test.severity.value] += 1
        return counts


class TestRunner: 
    def __init__(self, model_interface):
        self.model = model_interface
        self.results: List[TestResult] = []
    
    def run_test_case(self, test_case: TestCase) -> TestResult:
        
        # Get prediction from model
        prediction = self.model.predict(test_case.input_text)
        
        # Evaluate pass/fail
        try:
            passed = test_case.evaluation_fn(prediction, test_case.expected_behavior)
            failure_reason = None if passed else self._generate_failure_reason(
                prediction, 
                test_case.expected_behavior
            )
        except Exception as e:
            # If evaluation fails, that's a test infrastructure problem, not a model problem
            passed = False
            failure_reason = f"Evaluation error: {str(e)}"
        
        # Create result object
        result = TestResult(
            test_id=test_case.id,
            test_name=test_case.name,
            passed=passed,
            category=test_case.category,
            severity=test_case.severity,
            input_text=test_case.input_text,
            expected_behavior=test_case.expected_behavior,
            actual_output=prediction,
            latency_ms=prediction.get('latency_ms', 0),
            failure_reason=failure_reason,
            metadata=test_case.metadata
        )
        
        self.results.append(result)
        return result
    
    def run_scenario(self, scenario: TestScenario, verbose: bool = True) -> List[TestResult]:
        scenario_results = []
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"Running Scenario: {scenario.name}")
            print(f"Description: {scenario.description}")
            print(f"Total Tests: {len(scenario.test_cases)}")
            print(f"{'='*70}\n")
        
        for i, test_case in enumerate(scenario.test_cases, 1):
            if verbose:
                print(f"[{i}/{len(scenario.test_cases)}] {test_case.name}...", end=' ')
            
            result = self.run_test_case(test_case)
            scenario_results.append(result)
            
            if verbose:
                status = "✓ PASS" if result.passed else "✗ FAIL"
                print(status)
                if not result.passed and result.failure_reason:
                    print(f"    Reason: {result.failure_reason}")
        
        if verbose and scenario.pro_version_note:
            print(f"\n{'─'*70}")
            print(f"ℹ️  Pro Version Note: {scenario.pro_version_note}")
            print(f"{'─'*70}\n")
        
        return scenario_results
    
    def run_multiple_scenarios(self, scenarios: List[TestScenario], verbose: bool = True) -> Dict[str, List[TestResult]]:
        all_results = {}
        
        for scenario in scenarios:
            results = self.run_scenario(scenario, verbose=verbose)
            all_results[scenario.id] = results
        
        return all_results
    
    def get_summary_stats(self) -> Dict[str, Any]:
        if not self.results:
            return {'error': 'No tests have been run yet'}
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        
        # Break down failures by severity
        failures_by_severity = {severity.value: 0 for severity in Severity}
        for result in self.results:
            if not result.passed:
                failures_by_severity[result.severity.value] += 1
        
        # Break down by category
        results_by_category = {}
        for category in ThreatCategory:
            cat_results = [r for r in self.results if r.category == category]
            if cat_results:
                results_by_category[category.value] = {
                    'total': len(cat_results),
                    'passed': sum(1 for r in cat_results if r.passed),
                    'failed': sum(1 for r in cat_results if not r.passed),
                    'pass_rate': sum(1 for r in cat_results if r.passed) / len(cat_results)
                }
        
        # Performance metrics
        latencies = [r.latency_ms for r in self.results]
        avg_latency = sum(latencies) / len(latencies)
        
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'pass_rate': passed_tests / total_tests,
            'failures_by_severity': failures_by_severity,
            'results_by_category': results_by_category,
            'performance': {
                'average_latency_ms': round(avg_latency, 2),
                'min_latency_ms': round(min(latencies), 2),
                'max_latency_ms': round(max(latencies), 2)
            },
            'model_stats': self.model.get_stats()
        }
    
    def _generate_failure_reason(self, prediction: Dict, expected: Dict) -> str:
        pred_label = prediction.get('label', 'UNKNOWN')
        expected_label = expected.get('label', 'UNKNOWN')
        confidence = prediction.get('confidence', 0)
        
        reason = f"Expected '{expected_label}' but got '{pred_label}'"
        
        if confidence < 0.6:
            reason += f" (low confidence: {confidence:.2%})"
        
        return reason