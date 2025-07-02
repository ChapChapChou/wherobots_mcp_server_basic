# Wherobots MCP Server

A Model Context Protocol (MCP) server that provides access to Wherobots spatial data through standardized tools. This server enables you to explore and query spatial datasets from the Wherobots cloud platform.

## Features

- 🗂️ **Catalog Management**: Browse available data catalogs
- 🏛️ **Database Exploration**: List databases within catalogs
- 📊 **Table Discovery**: View tables and their schemas
- 🔍 **Schema Inspection**: Get detailed table structure information
- 🌐 **Spatial Data Access**: Connect to Wherobots' spatial datasets including:
  - Overture Maps Foundation data
  - Foursquare location data
  - Buildings, transportation, places, and more

## Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- 
- Wherobots API key
- VS Code with GitHub Copilot extension

## Installation

### Step 1: Set up the MCP Server

1. **Install uv package manager:**
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip
   pip install uv
   ```

2. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wherobots_mcp_server_basic
   ```

3. **Install dependencies using uv:**
   ```bash
   uv sync
   ```
   
   This will automatically create a virtual environment and install all dependencies defined in `pyproject.toml`.

### Step 2: Configure VS Code Client

1. **Install required VS Code extensions:**
   - Make sure you have **GitHub Copilot** extension installed
   - Ensure **MCP server functionality** is enabled in Copilot settings

2. **Add MCP server configuration to VS Code settings:**
   
   Open your VS Code `settings.json` file and add the following MCP configuration:
   
   ```json
   "mcp": {
       "inputs": [],
       "servers": {
           "basic_mcp_for_wherobots": {
               "command": "uv",
               "args": [
                   "run",
                   "python",
                   "/WHERE_YOU_DOWNLOAD_REPO/wherobots_mcp_server_basic/src/server.py"
               ],
               "cwd": "/WHERE_YOU_DOWNLOAD_REPO",
               "env": {
                   "WHEROBOTS_API_KEY": "YOUR_WHEROBOTS_API_KEY",
                   "WHEROBOTS_REGION": "us-west-2"
               }
           }
       }
   }
   ```

   **Important:** Replace the following placeholders:
   - `/WHERE_YOU_DOWNLOAD_REPO` with the actual path where you cloned the repository
   - `YOUR_WHEROBOTS_API_KEY` with your actual Wherobots API key
   
   **Note:** `cwd` (Current Working Directory) tells VS Code where to run the server command from. This should be the parent directory of your cloned repository.

3. **Refresh VS Code:**
   - Reload the VS Code window (Command Palette → "Developer: Reload Window")
   - This will load the MCP server configuration

4. **Start using the server:**
   - Open the chat interface in VS Code
   - You can now interact with Wherobots spatial data directly in the chat!

## Configuration

### Environment Variables

The MCP server supports the following environment variables:

- `WHEROBOTS_API_KEY`: Your Wherobots API key (required)
- `WHEROBOTS_REGION`: The region to connect to (default: us-west-2)

You can get your API key from the [Wherobots Cloud Console](https://console.wherobots.com/).

### Alternative Configuration with .env file

If you prefer using a `.env` file instead of environment variables in settings.json:

1. Create a `.env` file in the project root:
   ```bash
   WHEROBOTS_API_KEY=your_api_key_here
   WHEROBOTS_REGION=us-west-2
   ```

2. Update your VS Code settings.json to remove the `env` section:
   ```json
   "mcp": {
       "inputs": [],
       "servers": {
           "basic_mcp_for_wherobots": {
               "command": "uv",
               "args": [
                   "run",
                   "python",
                   "/WHERE_YOU_DOWNLOAD_REPO/wherobots_mcp_server_basic/src/server.py"
               ],
               "cwd": "/WHERE_YOU_DOWNLOAD_REPO"
           }
       }
   }
   ```

## Usage

Once configured, you can interact with Wherobots spatial data directly through natural language in VS Code's chat interface.

### Available Tools

The MCP server provides the following tools:

#### 1. Show Catalogs
Lists all available data catalogs in Wherobots.

#### 2. Show Databases  
Lists all databases within a specified catalog.

#### 3. Show Tables
Lists all tables within a specified database.

#### 4. Describe Table
Returns detailed schema information for a specific table.

### Example Usage

You can use natural language queries in the VS Code chat:

```
"Show me all the catalogs available in Wherobots"

"What databases are in the wherobots_open_data catalog?"

"List all tables in the overture_maps_foundation database"

"Describe the schema of the base_water table"

"How many tables are in overture_maps_foundation?"

"What does the buildings_building table look like?"
```

## Available Datasets

### Wherobots Open Data Catalog

The server provides access to the `wherobots_open_data` catalog, which includes:

#### Overture Maps Foundation
- **Buildings**: `buildings_building`, `buildings_building_part`
- **Transportation**: `transportation_segment`, `transportation_connector`
- **Places**: `places_place`
- **Administrative**: `divisions_division`, `divisions_division_area`, `divisions_division_boundary`
- **Base Features**: `base_land`, `base_water`, `base_land_cover`, `base_land_use`, `base_infrastructure`, `base_bathymetry`
- **Addresses**: `addresses_address`
- **Geocoding**: `geocodes`

#### Foursquare
- **Places**: `places` - Location-based places and points of interest data
- **Categories**: `categories` - Category classification system for places

## Development

### Project Structure

```
wherobots_mcp_server_basic/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── tools.py           # Tool implementations
│   └── prompt.py          # Server prompts
├── examples/
│   └── example_wb_spatial_api.py
├── pyproject.toml         # Project configuration
├── uv.lock               # Lock file
└── README.md
```

### Development Dependencies

Install development dependencies using uv:

```bash
uv sync --group dev
```

This includes:
- `pytest` for testing
- `black` for code formatting  
- `isort` for import sorting

## Configuration Details

The server connects to Wherobots Cloud with the following default settings:
- **Host**: `api.cloud.wherobots.com`
- **Runtime**: `TINY` (configurable)
- **Region**: `AWS_US_WEST_2` (configurable)

You can modify these settings in `src/tools.py` if needed.

## Error Handling

The server includes comprehensive error handling for:
- Missing API keys
- Connection failures
- Invalid queries
- Schema access issues

All errors are returned in a structured format with descriptive messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the [Wherobots Documentation](https://docs.wherobots.com/)
- Review the [Model Context Protocol specification](https://modelcontextprotocol.io/)
- Open an issue in this repository

## Related Links

- [Wherobots Cloud Platform](https://www.wherobots.com/)
- [Overture Maps Foundation](https://overturemaps.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)