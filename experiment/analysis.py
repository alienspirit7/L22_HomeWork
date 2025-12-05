"""Analysis and visualization for MCP token consumption experiment."""
from __future__ import annotations
import json
from typing import Optional
from token_counter import TokenAccumulator

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def compare_paradigms(traditional: TokenAccumulator, code_execution: TokenAccumulator) -> dict:
    """Compare token consumption between paradigms."""
    trad, code = traditional.summary(), code_execution.summary()
    total_diff = trad["grand_total"] - code["grand_total"]
    total_pct = (total_diff / trad["grand_total"]) * 100 if trad["grand_total"] > 0 else 0
    context_diff = trad["total_context_tokens"] - code["total_context_tokens"]
    context_pct = (context_diff / trad["total_context_tokens"]) * 100 if trad["total_context_tokens"] > 0 else 0
    
    return {
        "traditional": trad, "code_execution": code,
        "comparison": {
            "total_token_savings": total_diff, "total_savings_percentage": round(total_pct, 2),
            "context_token_savings": context_diff, "context_savings_percentage": round(context_pct, 2),
            "tokens_per_op_traditional": trad["tokens_per_operation"],
            "tokens_per_op_code_execution": code["tokens_per_operation"],
            "efficiency_multiplier": round(trad["grand_total"] / code["grand_total"], 2) if code["grand_total"] > 0 else 0
        },
        "theory_validation": {
            "pattern_traditional": "O(N×M)", "pattern_code_execution": "O(N+M)",
            "expected_savings": "60-70%", "actual_savings": f"{round(total_pct, 1)}%",
            "hypothesis_supported": total_pct >= 50
        }
    }

def print_comparison_table(comparison: dict) -> None:
    """Print formatted comparison table."""
    trad, code, comp = comparison["traditional"], comparison["code_execution"], comparison["comparison"]
    theory = comparison["theory_validation"]
    
    try:
        from tabulate import tabulate
        data = [
            ["Initial Context", trad["initial_context_tokens"], code["initial_context_tokens"]],
            ["Total Context", trad["total_context_tokens"], code["total_context_tokens"]],
            ["Reasoning", trad["total_reasoning_tokens"], code["total_reasoning_tokens"]],
            ["Tool Calls", trad["total_tool_call_tokens"], code["total_tool_call_tokens"]],
            ["Responses", trad["total_response_tokens"], code["total_response_tokens"]],
            ["─" * 20, "─" * 10, "─" * 10],
            ["GRAND TOTAL", trad["grand_total"], code["grand_total"]],
            ["Tokens/Operation", trad["tokens_per_operation"], code["tokens_per_operation"]],
        ]
        print("\n" + "=" * 70)
        print("TOKEN CONSUMPTION ANALYSIS: Traditional MCP vs Code Execution")
        print("=" * 70)
        print(tabulate(data, headers=["Metric", "Traditional", "Code Execution"], tablefmt="rounded_grid"))
    except ImportError:
        print(f"\nTraditional: {trad['grand_total']:,} tokens | Code Execution: {code['grand_total']:,} tokens")
    
    print(f"\n{'─' * 70}\nSAVINGS: {comp['total_token_savings']:,} tokens ({comp['total_savings_percentage']}%)")
    print(f"Context Savings: {comp['context_token_savings']:,} tokens ({comp['context_savings_percentage']}%)")
    print(f"Efficiency: {comp['efficiency_multiplier']}x | Hypothesis: {'✓ YES' if theory['hypothesis_supported'] else '✗ NO'}")
    print("=" * 70)

def generate_chart(comparison: dict, output_path: Optional[str] = None) -> None:
    """Generate comparison bar chart."""
    if not HAS_MATPLOTLIB:
        print("[Install matplotlib for charts: pip install matplotlib]")
        return
    
    trad, code = comparison["traditional"], comparison["code_execution"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('MCP Token Consumption: Traditional vs Code Execution', fontweight='bold')
    
    # Breakdown chart
    cats = ['Context', 'Reasoning', 'Tool Calls', 'Responses']
    trad_vals = [trad["total_context_tokens"], trad["total_reasoning_tokens"], 
                 trad["total_tool_call_tokens"], trad["total_response_tokens"]]
    code_vals = [code["total_context_tokens"], code["total_reasoning_tokens"],
                 code["total_tool_call_tokens"], code["total_response_tokens"]]
    x = range(len(cats))
    ax1.bar([i - 0.2 for i in x], trad_vals, 0.4, label='Traditional', color='#e74c3c')
    ax1.bar([i + 0.2 for i in x], code_vals, 0.4, label='Code Execution', color='#27ae60')
    ax1.set_xticks(x); ax1.set_xticklabels(cats, rotation=15)
    ax1.set_ylabel('Tokens'); ax1.legend(); ax1.grid(axis='y', alpha=0.3)
    ax1.set_title('Token Breakdown')
    
    # Total comparison
    bars = ax2.bar(['Traditional\n(O(N×M))', 'Code Execution\n(O(N+M))'], 
                   [trad["grand_total"], code["grand_total"]], color=['#e74c3c', '#27ae60'])
    for bar in bars:
        ax2.annotate(f'{int(bar.get_height()):,}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    ha='center', va='bottom', fontweight='bold')
    ax2.set_ylabel('Total Tokens'); ax2.set_title('Total Consumption'); ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"[Chart saved: {output_path}]")
    plt.show()

def save_results(comparison: dict, output_path: str) -> None:
    """Save comparison results to JSON."""
    with open(output_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    print(f"[Results saved: {output_path}]")
