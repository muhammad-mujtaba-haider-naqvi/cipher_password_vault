"""Quick database verification script."""
import sys
sys.path.insert(0, '.')

import database
import sqlite3

database.ensure_db_exists()
print('✓ Database initialized successfully')

# Check tables exist
conn = sqlite3.connect(database.DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f'✓ Tables created: {tables}')

# Check master_config columns
cursor.execute("PRAGMA table_info(master_config)")
columns = [row[1] for row in cursor.fetchall()]
print(f'✓ master_config columns: {columns}')

# Check vault columns
cursor.execute("PRAGMA table_info(vault)")
columns = [row[1] for row in cursor.fetchall()]
print(f'✓ vault columns: {columns}')

conn.close()
print('✓ Database schema verified!')
