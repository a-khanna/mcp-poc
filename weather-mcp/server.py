from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx
import asyncio


app = Server("weather-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_weather":
        city = arguments["city"]
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"http://localhost:8000/weather/{city}")
                response.raise_for_status()
                data = response.json()
                return [TextContent(
                    type="text",
                    text=f"Weather for {data['city']}:\n- Temperature: {data['temperature']}°C\n- Condition: {data['condition']}\n- Humidity: {data['humidity']}%"
                )]
            except httpx.HTTPError as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    return []


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
