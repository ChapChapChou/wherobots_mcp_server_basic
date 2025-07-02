import logging
import os
import sys
from dotenv import load_dotenv

from wherobots.db import connect
from wherobots.db.region import Region
from wherobots.db.runtime import Runtime

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)20s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def connect_to_wherobots():
    """
    Connect to Wherobots and return connection.
    """
    load_dotenv()
    api_key = os.getenv("WHEROBOTS_API_KEY")
    if not api_key:
        raise ValueError("Please set the WHEROBOTS_API_KEY environment variable.")
    
    return connect(
        host="api.cloud.wherobots.com",
        api_key=api_key,
        runtime=Runtime.TINY,
        region=Region.AWS_US_WEST_2
    )

def show_catalogs():
    """Show all available catalogs in Wherobots."""
    try:
        with connect_to_wherobots() as conn:
            curr = conn.cursor()
            curr.execute("SHOW CATALOGS")
            results = curr.fetchall()
            catalog_names = results['catalog'].tolist()
            # currently we can`t return the catalogs directly with SQL cmd
            # due to issue in spark - iceberg connector, will be fixed in future
            # return {"catalogs": catalog_names}
            return {"catalogs: wherobots_open_data"}
    except Exception as e:
        return {"error": f"Failed to fetch catalogs: {str(e)}"}


def show_databases(catalog_name: str = "wherobots_open_data"):
    """
    Show all databases in a specific catalog.
    
    Args:
        catalog_name: Name of the catalog to list databases from (default: wherobots_open_data)
    """
    try:
        with connect_to_wherobots() as conn:
            curr = conn.cursor()
            sql = f"SHOW DATABASES FROM {catalog_name}"
            curr.execute(sql)
            results = curr.fetchall()
            database_names = results['namespace'].tolist()
            return {"catalog": catalog_name, "databases": database_names}
    except Exception as e:
        # Try alternative approach
        try:
            sql = "SHOW DATABASES"
            curr.execute(sql)
            results = curr.fetchall()
            database_names = results['namespace'].tolist()
            return {"catalog": catalog_name, "databases": database_names}
        except Exception as e2:
            return {"error": f"Failed to fetch databases from {catalog_name}: {str(e)}. Alternative approach also failed: {str(e2)}"}


def show_tables(catalog_name: str, database_name: str = "default"):
    """
    Show all tables in a specific catalog and database.
    
    Args:
        catalog_name: Name of the catalog to list tables from
        database_name: Name of the database to list tables from (default: default)
    """
    try:
        with connect_to_wherobots() as conn:
            curr = conn.cursor()
            
            # Try different approaches to show tables
            approaches = [
                f"SHOW TABLES FROM {catalog_name}.{database_name}",
                f"SHOW TABLES IN {catalog_name}.{database_name}",
                "SHOW TABLES",
                f"USE {catalog_name}.{database_name}; SHOW TABLES"
            ]
            
            for sql in approaches:
                try:
                    curr.execute(sql)
                    results = curr.fetchall()
                    # Check what columns are available
                    columns = results.columns.tolist()
                    
                    # Try different possible column names
                    table_column = None
                    for possible_col in ['tableName', 'table_name', 'name', 'Table']:
                        if possible_col in columns:
                            table_column = possible_col
                            break
                    
                    if table_column:
                        table_names = results[table_column].tolist()
                        return {"catalog": catalog_name, "database": database_name, "tables": table_names, "sql_used": sql}
                    else:
                        return {"catalog": catalog_name, "database": database_name, "columns_found": columns, "sql_used": sql, "raw_results": results.to_dict()}
                        
                except Exception as approach_error:
                    continue
                    
            return {"error": f"All approaches failed to fetch tables from {catalog_name}.{database_name}"}
    except Exception as e:
        return {"error": f"Failed to fetch tables from {catalog_name}.{database_name}: {str(e)}"}


def register_tools(mcp_instance):
    """Register all tools with the MCP instance."""
    mcp_instance.tool()(show_catalogs)
    mcp_instance.tool()(show_databases)
    mcp_instance.tool()(show_tables)
