import os
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
import pandas as pd
class Database:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
        # Setup
        self.table_name = 'flights_data'
        self.csv_path = 'data/flights_cleaned.csv'

        # Read CSV
        self.flights_raw_data = pd.read_csv(self.csv_path, delimiter=',', encoding='utf-8')

        # Create SQLAlchemy engine
        self.engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

    def _table_has_rows(self):
        """Return True if the target table exists and has at least one row."""
        insp = inspect(self.engine)
        if not insp.has_table(self.table_name):
            return False
        with self.engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM {self.table_name} LIMIT 1"))
            return result.first() is not None

    def load_data_db(self):
        """Load the CSV into the database only if data isn't already there."""
        if self._table_has_rows():
            print("📦 Data already present — skipping import.")
            return
        self.flights_raw_data["Date_of_Journey"] = pd.to_datetime(self.flights_raw_data["Date_of_Journey"]).dt.date
        self.flights_raw_data["Price"] = pd.to_numeric(self.flights_raw_data["Price"], errors="coerce")

        # Define correct PostgreSQL column types
        dtype_map = {
            "Airline": sqlalchemy.String(),
            "Date_of_Journey": sqlalchemy.Date(),
            "Source": sqlalchemy.String(),
            "Destination": sqlalchemy.String(),
            "Route": sqlalchemy.String(),
            "Dep_Time": sqlalchemy.String(),
            "Duration": sqlalchemy.String(),
            "Total_Stops": sqlalchemy.String(),
            "Price": sqlalchemy.Integer(),
        }

        print("📥 Loading CSV data into flights_data ...")
        self.flights_raw_data.to_sql(
            self.table_name,
            con=self.engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000,
            dtype=dtype_map
        )
        print("✅ Data loaded into flights_data.")

    def close(self):
        """Close the database engine connection."""
        self.engine.dispose()
        print("🔌 Connection closed.")

    def fetch_city_names(self):
        query = """
        SELECT DISTINCT "Destination" FROM flights_data
        UNION
        SELECT DISTINCT "Source" FROM flights_data
        """
        with self.engine.connect() as connection:
            result = pd.read_sql_query(text(query), con=connection)
        return result

    def fetch_all_flights(self, source, destination):
        query = f"""
            SELECT "Airline", "Route", "Dep_Time","Duration", "Price" FROM flights_data
            WHERE "Source" = '{source}' AND "Destination" = '{destination}'
            """
        with self.engine.connect() as connection:
            result = pd.read_sql_query(text(query), con=connection)
        return result

    def fetch_airline_frequency(self):
        query = f"""
                select "Airline", count(*) as number_of_flights from flights_data
                group by "Airline"
                order by number_of_flights desc
                """
        with self.engine.connect() as connection:
            result = pd.read_sql_query(text(query), con=connection)
        return result

    def busy_airport(self):
        query = f"""
                select "Source", Count(*) as aircraft_movements from (select "Source" from flights_data
                                                      Union ALL
													  select "Destination" from flights_data) as t
                Group by t."Source"
                Order by aircraft_movements desc
                """
        with self.engine.connect() as connection:
            result = pd.read_sql_query(text(query), con=connection)
        return result

    def daily_frequency(self):
        query = f"""
                select "Date_of_Journey", count(*) as daily_number_of_flights from flights_data
                group by "Date_of_Journey"
                order by daily_number_of_flights desc
              """
        with self.engine.connect() as connection:
            result = pd.read_sql_query(text(query), con=connection)
        return result