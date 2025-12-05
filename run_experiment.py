#!/usr/bin/env python3
"""
Main experiment runner for MCP Token Consumption Research.

This experiment compares token consumption between:
1. Traditional MCP Architecture (Sequential Orchestration) - O(N×M)
2. Code Execution Paradigm (High-Level Composition) - O(N+M)

Run with: python experiment/run_experiment.py
"""

import os
import sys

# Add experiment directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from traditional_mcp import run_traditional_simulation, TRAVEL_OPERATIONS
from code_execution import run_code_execution_simulation
from analysis import compare_paradigms, print_comparison_table, generate_chart, save_results


def print_header():
    """Print experiment header."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║       MCP TOKEN CONSUMPTION RESEARCH EXPERIMENT                      ║
║                                                                      ║
║  Comparing: Traditional MCP vs Code Execution Paradigm               ║
║  Scenario:  Travel Planning with 5 Tools × 5 Operations              ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def print_scenario():
    """Print the test scenario."""
    print("TEST SCENARIO: Travel Planning Assistant")
    print("─" * 50)
    print("Operations to execute:")
    for i, op in enumerate(TRAVEL_OPERATIONS, 1):
        print(f"  {i}. {op['tool']}")
    print()


def run_experiment(generate_charts: bool = True, save_json: bool = True) -> dict:
    """
    Run the complete experiment.
    
    Args:
        generate_charts: Whether to generate matplotlib charts
        save_json: Whether to save results to JSON file
        
    Returns:
        Comparison results dictionary
    """
    print_header()
    print_scenario()
    
    # Run Traditional MCP simulation
    print("Running Traditional MCP Architecture simulation...")
    traditional_results = run_traditional_simulation(TRAVEL_OPERATIONS)
    print(f"  ✓ Completed: {traditional_results.grand_total:,} total tokens\n")
    
    # Run Code Execution simulation
    print("Running Code Execution Paradigm simulation...")
    code_execution_results = run_code_execution_simulation(TRAVEL_OPERATIONS)
    print(f"  ✓ Completed: {code_execution_results.grand_total:,} total tokens\n")
    
    # Compare results
    comparison = compare_paradigms(traditional_results, code_execution_results)
    
    # Print comparison table
    print_comparison_table(comparison)
    
    # Save results
    if save_json:
        output_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(output_dir, "results.json")
        save_results(comparison, json_path)
    
    # Generate charts
    if generate_charts:
        output_dir = os.path.dirname(os.path.abspath(__file__))
        chart_path = os.path.join(output_dir, "token_comparison_chart.png")
        try:
            generate_chart(comparison, chart_path)
        except Exception as e:
            print(f"\n[Chart generation failed: {e}]")
    
    # Print conclusion
    print_conclusion(comparison)
    
    return comparison


def print_conclusion(comparison: dict):
    """Print final conclusion."""
    theory = comparison["theory_validation"]
    comp = comparison["comparison"]
    
    print("\n" + "═" * 70)
    print("CONCLUSION")
    print("═" * 70)
    
    if theory["hypothesis_supported"]:
        print(f"""
✓ HYPOTHESIS CONFIRMED

The experiment demonstrates that the Code Execution Paradigm achieves
{comp['total_savings_percentage']}% token savings compared to Traditional MCP Architecture.

Key Findings:
  • Traditional MCP follows O(N×M) pattern - tokens grow with N tools × M operations
  • Code Execution follows O(N+M) pattern - one-time discovery + lean operations
  • Context overhead is reduced by {comp['context_savings_percentage']}%
  • Efficiency multiplier: {comp['efficiency_multiplier']}x

This validates the theoretical analysis from the MCP Servers Specialist skill
that the Code Execution paradigm fundamentally transforms LLM's role from
sequential orchestrator to high-level code composer, resulting in significant
token efficiency gains.
""")
    else:
        print(f"""
✗ HYPOTHESIS NOT FULLY SUPPORTED

The experiment shows {comp['total_savings_percentage']}% token savings, which is below
the expected 50%+ threshold for strong support of the hypothesis.

Further investigation may be needed to understand the discrepancy.
""")
    
    print("═" * 70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run MCP Token Consumption Experiment")
    parser.add_argument("--no-charts", action="store_true", help="Skip chart generation")
    parser.add_argument("--no-save", action="store_true", help="Skip saving results to JSON")
    
    args = parser.parse_args()
    
    run_experiment(
        generate_charts=not args.no_charts,
        save_json=not args.no_save
    )
