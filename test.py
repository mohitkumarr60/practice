import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from IPython.display import Markdown, display
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SQLDatabase
from sqlalchemy import text
from llama_index.core.query_engine import NLSQLTableQueryEngine

load_dotenv()

llm = Gemini(api_key=os.getenv('GEMINI_API_KEY'), model_name="models/gemini-pro")

Settings.embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm

engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# create city SQL table
table_name = "city_stats"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("country", String(16), nullable=False),
)
metadata_obj.create_all(engine)

sql_database = SQLDatabase(engine, include_tables=["city_stats"])

sql_database = SQLDatabase(engine, include_tables=["city_stats"])
from sqlalchemy import insert

rows = [
    {"city_name": "Toronto", "population": 2930000, "country": "Canada"},
    {"city_name": "Tokyo", "population": 13960000, "country": "Japan"},
    {
        "city_name": "Chicago",
        "population": 2679000,
        "country": "United States",
    },
    {"city_name": "Seoul", "population": 9776000, "country": "South Korea"},
]
for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.begin() as connection:
        cursor = connection.execute(stmt)

# view current tables
stmt = select(
    city_stats_table.c.city_name,
    city_stats_table.c.population,
    city_stats_table.c.country,
).select_from(city_stats_table)

with engine.connect() as connection:
    results = connection.execute(stmt).fetchall()
    print(results)

with engine.connect() as con:
    rows = con.execute(text("SELECT city_name from city_stats"))
    for row in rows:
        print(row)

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["city_stats"], llm=llm
)
query_str = "Which city has the highest population?"
response = query_engine.query(query_str)
display(Markdown(f"<b>{response}</b>"))
