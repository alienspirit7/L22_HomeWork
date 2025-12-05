"""Mock MCP Server with travel planning tools following MCP spec."""
from __future__ import annotations
import json
from dataclasses import dataclass

@dataclass
class MCPTool:
    """MCP Tool definition."""
    name: str
    description: str
    input_schema: dict
    
    def to_schema(self) -> dict:
        return {"name": self.name, "description": self.description, "inputSchema": self.input_schema}

# Compact tool definitions - essential fields only
TRAVEL_MCP_TOOLS = [
    MCPTool("search_flights", "Search for available flights between airports on specified dates.",
        {"type": "object", "required": ["origin", "destination", "departure_date"],
         "properties": {"origin": {"type": "string"}, "destination": {"type": "string"},
                       "departure_date": {"type": "string", "format": "date"},
                       "return_date": {"type": "string"}, "passengers": {"type": "integer", "default": 1},
                       "cabin_class": {"type": "string", "enum": ["economy", "business", "first"]},
                       "max_stops": {"type": "integer"}, "sort_by": {"type": "string"}}}),
    MCPTool("check_weather", "Get current weather and forecast for a location.",
        {"type": "object", "required": ["location"],
         "properties": {"location": {"type": "string"}, "units": {"type": "string", "enum": ["metric", "imperial"]},
                       "include_forecast": {"type": "boolean"}, "include_hourly": {"type": "boolean"}}}),
    MCPTool("search_hotels", "Search for available hotels in a destination.",
        {"type": "object", "required": ["destination", "check_in", "check_out"],
         "properties": {"destination": {"type": "string"}, "check_in": {"type": "string"},
                       "check_out": {"type": "string"}, "guests": {"type": "integer"},
                       "min_stars": {"type": "integer"}, "max_price": {"type": "number"},
                       "amenities": {"type": "array", "items": {"type": "string"}}}}),
    MCPTool("check_calendar", "Check calendar availability for date ranges.",
        {"type": "object", "required": ["start_date", "end_date"],
         "properties": {"start_date": {"type": "string"}, "end_date": {"type": "string"},
                       "calendars": {"type": "array"}, "timezone": {"type": "string"},
                       "min_duration_minutes": {"type": "integer"}}}),
    MCPTool("create_booking", "Create a booking for flight, hotel, or travel package.",
        {"type": "object", "required": ["booking_type", "item_id", "passengers", "contact_email", "payment_method"],
         "properties": {"booking_type": {"type": "string", "enum": ["flight", "hotel", "package"]},
                       "item_id": {"type": "string"},
                       "passengers": {"type": "array", "items": {"type": "object"}},
                       "contact_email": {"type": "string"}, "payment_method": {"type": "string"},
                       "special_requests": {"type": "string"}, "add_to_calendar": {"type": "boolean"}}})
]

# Mock responses for each tool
MOCK_RESPONSES = {
    "search_flights": {"flights": [
        {"id": "FL-AA123", "airline": "American Airlines", "price": 450.00, "stops": 0, "duration_minutes": 210},
        {"id": "FL-UA456", "airline": "United Airlines", "price": 385.00, "stops": 1, "duration_minutes": 270}
    ], "total_results": 2},
    "check_weather": {"location": "Paris, France",
        "current": {"temperature": 18, "humidity": 65, "conditions": "Partly Cloudy"},
        "forecast": [{"date": "2024-03-15", "high": 20, "low": 12, "conditions": "Sunny"}]},
    "search_hotels": {"hotels": [
        {"id": "HTL-001", "name": "Grand Hotel Paris", "stars": 4, "rating": 8.7, "price_per_night": 220.00},
        {"id": "HTL-002", "name": "Boutique Montmartre", "stars": 3, "rating": 9.1, "price_per_night": 150.00}
    ], "total_results": 2},
    "check_calendar": {
        "busy_slots": [{"start": "2024-03-15T09:00:00Z", "end": "2024-03-15T10:00:00Z", "event": "Team Meeting"}],
        "free_slots": [{"start": "2024-03-15T10:00:00Z", "end": "2024-03-15T17:00:00Z"}]},
    "create_booking": {"booking_id": "BK-2024-12345", "status": "confirmed", "total_amount": 835.00}
}

def get_all_tools_json() -> str:
    """Get JSON string of all tool definitions for token counting."""
    return json.dumps([t.to_schema() for t in TRAVEL_MCP_TOOLS], indent=2)

def get_tool_by_name(name: str) -> MCPTool | None:
    """Get a specific tool by name."""
    return next((t for t in TRAVEL_MCP_TOOLS if t.name == name), None)

def get_mock_response(tool_name: str) -> str:
    """Get mock response JSON for a tool."""
    return json.dumps(MOCK_RESPONSES.get(tool_name, {"status": "success"}), indent=2)

if __name__ == "__main__":
    print(f"Tools: {len(TRAVEL_MCP_TOOLS)}")
    print(f"Total schema tokens (approx): {len(get_all_tools_json())} chars")
