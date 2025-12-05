"""Traditional MCP Architecture simulation - O(N×M) token pattern."""
from __future__ import annotations
import json
from token_counter import count_tokens, TokenMetrics, TokenAccumulator
from mock_mcp_server import TRAVEL_MCP_TOOLS, get_all_tools_json, get_mock_response

SYSTEM_PROMPT = """You are a travel assistant with MCP tools.
1. Analyze which tools are needed
2. Call each tool sequentially
3. Process results and respond
Use JSON-RPC 2.0 format for tool calls."""

def build_tools_context() -> str:
    """Build full tool definitions context."""
    return f"## MCP Tools\n```json\n{get_all_tools_json()}\n```"

def simulate_tool_discovery() -> int:
    """Simulate tools/list discovery call, return token count."""
    request = json.dumps({"jsonrpc": "2.0", "method": "tools/list", "params": {}}, indent=2)
    response = json.dumps({"result": {"tools": [t.to_schema() for t in TRAVEL_MCP_TOOLS]}}, indent=2)
    return count_tokens(request + response)

def simulate_tool_call(tool_name: str, args: dict) -> TokenMetrics:
    """Simulate a single tool call, return token metrics."""
    reasoning = f"Using '{tool_name}' tool with params:\n{json.dumps(args, indent=2)}"
    request = json.dumps({"method": "tools/call", "params": {"name": tool_name, "arguments": args}}, indent=2)
    response = json.dumps({"result": {"content": [{"text": get_mock_response(tool_name)}]}}, indent=2)
    processing = f"Received {tool_name} response, extracting relevant information..."
    return TokenMetrics(
        reasoning_tokens=count_tokens(reasoning) + count_tokens(processing),
        tool_call_tokens=count_tokens(request),
        response_tokens=count_tokens(response)
    )

def run_traditional_simulation(operations: list[dict]) -> TokenAccumulator:
    """Run full Traditional MCP simulation."""
    acc = TokenAccumulator("Traditional MCP")
    acc.initial_context_tokens = count_tokens(SYSTEM_PROMPT + build_tools_context()) + simulate_tool_discovery()
    
    context_reload = count_tokens(build_tools_context()) // 2  # Partial context reload per op
    for op in operations:
        metrics = simulate_tool_call(op["tool"], op["args"])
        metrics.context_tokens = context_reload
        acc.add_operation(metrics)
    return acc

# Test operations for travel planning scenario
TRAVEL_OPERATIONS = [
    {"tool": "search_flights", "args": {"origin": "JFK", "destination": "CDG", 
        "departure_date": "2024-03-15", "return_date": "2024-03-22", "passengers": 2}},
    {"tool": "check_weather", "args": {"location": "Paris, France", "units": "metric", "include_forecast": True}},
    {"tool": "search_hotels", "args": {"destination": "Paris", "check_in": "2024-03-15", 
        "check_out": "2024-03-22", "guests": 2, "min_stars": 3}},
    {"tool": "check_calendar", "args": {"start_date": "2024-03-15", "end_date": "2024-03-22", "timezone": "America/New_York"}},
    {"tool": "create_booking", "args": {"booking_type": "package", "item_id": "PKG-12345",
        "passengers": [{"first_name": "John", "last_name": "Doe"}, {"first_name": "Jane", "last_name": "Doe"}],
        "contact_email": "john.doe@email.com", "payment_method": "credit_card"}}
]

if __name__ == "__main__":
    results = run_traditional_simulation(TRAVEL_OPERATIONS)
    print(f"Traditional MCP: {results.grand_total:,} tokens ({results.tokens_per_operation:.0f}/op)")
