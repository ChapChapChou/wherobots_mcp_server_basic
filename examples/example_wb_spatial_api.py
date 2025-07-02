import logging
import sys
import os
from dotenv import load_dotenv

from wherobots.db import connect
from wherobots.db.region import Region
from wherobots.db.runtime import Runtime

# Optionally, setup logging to get information about the driver's
# activity.
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)20s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Get your API key, or securely read it from a local file.
load_dotenv()  # Load environment variables from a .env file
api_key = os.getenv("WHEROBOTS_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")
print(f"API Key length: {len(api_key) if api_key else 0}")
if not api_key:
    raise ValueError("Please set the WHEROBOTS_API_KEY environment variable.")

def show_catalogs():
    curr.execute(sql3)
    results = curr.fetchall()
    print("Full results table:")
    print(results)
    print("\nAll catalogs:")
    # Extract catalog names from the results
    catalog_names = results['catalog'].tolist()
    for catalog in catalog_names:
        print(f"  - {catalog}")





def show_sql2():
    curr.execute(sql2)
    results = curr.fetchall()
    #results.show()
    print("All tables in overture_maps_foundation:")
    # Extract just the table names
    table_names = results['tableName'].tolist()
    for table in table_names:
        print(table)


with connect(
    host="api.cloud.wherobots.com",
    api_key=api_key,
    # runtime parameter specifies the compute resources allocated for the runtime environment.
    # Replace 'Runtime.TINY' with the desired runtime size, for example:
    # - For a small runtime: runtime=Runtime.SMALL
    # - For a medium runtime: runtime=Runtime.MEDIUM
    runtime=Runtime.TINY,
    # region parameter establishes a connection to a specified AWS cloud provider region.
    # Replace 'Region.AWS_US_WEST_2' with the desired AWS region, for example:
    # - For AWS US East (N. Virginia): region=Region.AWS_US_EAST_1
    region=Region.AWS_US_WEST_2) as conn:
        curr = conn.cursor()
        sql1 = """
            SELECT
                id,
                names['primary'],
                geometry,
                population
            FROM
                wherobots_open_data.overture_maps_foundation.admins_locality
            WHERE localityType = 'country'
            SORT BY population DESC
            LIMIT 10
        """
        sql2 = "SHOW TABLES FROM wherobots_open_data.overture_maps_foundation"
        sql3 = "SHOW CATALOGS LIKE 'wherobots*'"
        
        show_catalogs()  # Show all catalogs
        show_sql2()

    
        # Show databases in spark_catalog (separate commands)
        # print("=== Showing databases in spark_catalog ===")
        
        # try:
        #     curr.execute("USE CATALOG spark_catalog")
        #     curr.execute("SHOW DATABASES")
        #     results = curr.fetchall()
        #     print("Full results table:")
        #     print(results)
        #     print("\nAll databases in spark_catalog:")
        #     # Extract database names from the results
        #     database_names = results['namespace'].tolist()  # Changed from 'databaseName' to 'namespace'
        #     for database in database_names:
        #         print(f"  - {database}")
        # except Exception as e:
        #     print(f"Error showing databases: {e}")
        #     # Try alternative approach
        #     try:
        #         curr.execute("SHOW DATABASES FROM spark_catalog")
        #         results = curr.fetchall()
        #         print("Alternative approach - Full results table:")
        #         print(results)
        #         database_names = results['namespace'].tolist()
        #         for database in database_names:
        #             print(f"  - {database}")
        #     except Exception as e2:
        #         print(f"Alternative approach also failed: {e2}")
    
