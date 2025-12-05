"""Code Execution Paradigm simulation - O(N+M) token pattern."""
from __future__ import annotations
import json
from token_counter import count_tokens, TokenMetrics, TokenAccumulator

SYSTEM_PROMPT = """You are a travel assistant using code execution paradigm.
Express intentions at high level. Infrastructure handles:
- Tool discovery and selection
- Parameter construction
- Batch execution
Focus on WHAT you need, not HOW to get it."""

CAPABILITY_MANIFEST = """## Capabilities
- travel.search: Search flights, hotels, transport
- travel.book: Create reservations
- info.weather: Weather forecasts
- calendar.availability: Check schedule
Priority hints: speed (0-1), quality (0-1), cost (0-1)"""

def simulate_batch_execution() -> TokenMetrics:
    """Simulate batch execution of search operations."""
    batch_request = {"intent": "travel_planning", "requirements": [
        {"type": "flights", "from": "JFK", "to": "CDG", "dates": "2024-03-15 to 2024-03-22"},
        {"type": "weather", "location": "Paris"},
        {"type": "hotels", "location": "Paris", "dates": "same"},
        {"type": "calendar", "check": "conflicts"}
    ], "priorities": {"speed": 0.6, "quality": 0.8, "cost": 0.7}}
    
    aggregated_response = {"status": "complete", "results": {
        "flight_options": 2, "best_flight": {"price": 385, "airline": "United"},
        "weather_summary": "Mild, 15-20°C, some rain expected",
        "hotel_options": 2, "recommended_hotel": {"name": "Boutique Montmartre", "price": 150},
        "calendar_status": "Available with 2 minor conflicts", "total_estimated_cost": 1785
    }, "recommendations": ["Book United flight", "Boutique Montmartre highly rated"]}
    
    reasoning = "Requesting aggregated travel analysis. System handles tool execution."
    return TokenMetrics(
        reasoning_tokens=count_tokens(reasoning),
        tool_call_tokens=count_tokens(json.dumps(batch_request, indent=2)),
        response_tokens=count_tokens(json.dumps(aggregated_response, indent=2))
    )

def simulate_booking_intent() -> TokenMetrics:
    """Simulate booking step as separate intent."""
    intent = {"action": "book", "selections": {"flight": "FL-UA456", "hotel": "HTL-002"}, "passengers": 2}
    response = {"status": "confirmed", "booking_ref": "BK-2024-12345", "total": 835.00}
    return TokenMetrics(
        reasoning_tokens=count_tokens("Proceeding with booking."),
        tool_call_tokens=count_tokens(json.dumps(intent, indent=2)),
        response_tokens=count_tokens(json.dumps(response, indent=2))
    )

def run_code_execution_simulation(operations: list[dict]) -> TokenAccumulator:
    """Run full Code Execution paradigm simulation."""
    acc = TokenAccumulator("Code Execution")
    acc.initial_context_tokens = count_tokens(SYSTEM_PROMPT + "\n\n" + CAPABILITY_MANIFEST)
    
    # Batch all search operations into single intent
    acc.add_operation(simulate_batch_execution())
    # Booking as separate action
    acc.add_operation(simulate_booking_intent())
    return acc

if __name__ == "__main__":
    from traditional_mcp import TRAVEL_OPERATIONS
    results = run_code_execution_simulation(TRAVEL_OPERATIONS)
    print(f"Code Execution: {results.grand_total:,} tokens ({results.tokens_per_operation:.0f}/op)")
