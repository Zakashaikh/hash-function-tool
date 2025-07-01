# database.py - Simple Database Operations
# This file handles saving and retrieving data from our SQLite database

import sqlite3  # Python's built-in database library
from datetime import datetime

# Database filename
DATABASE_NAME = 'hash_results.db'

def init_db():
    """
    Initialize our database - create the table if it doesn't exist
    Think of this as creating a spreadsheet with specific columns
    """
    # Connect to the database (creates file if it doesn't exist)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create our table with columns
    # This is like creating a spreadsheet with these column headers:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hash_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            input_type TEXT NOT NULL,
            input_value TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            hash_result TEXT NOT NULL
        )
    ''')
    
    # Save changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_hash_result(input_type, input_value, algorithm, hash_result):
    """
    Save a hash result to our database
    This is like adding a new row to our spreadsheet
    
    Parameters:
    - input_type: 'text' or 'file'
    - input_value: the text or filename that was hashed
    - algorithm: 'MD5', 'SHA-1', etc.
    - hash_result: the actual hash value
    """
    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Insert new record (like adding a new row)
    cursor.execute('''
        INSERT INTO hash_results (timestamp, input_type, input_value, algorithm, hash_result)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, input_type, input_value, algorithm, hash_result))
    
    # Save and close
    conn.commit()
    conn.close()

def get_hash_history(limit=50):
    """
    Get the most recent hash operations from our database
    This is like reading rows from our spreadsheet
    
    Parameters:
    - limit: how many records to return (default 50)
    
    Returns:
    - List of dictionaries containing hash data
    """
    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Get recent records, ordered by most recent first
    cursor.execute('''
        SELECT timestamp, input_type, input_value, algorithm, hash_result
        FROM hash_results
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    # Fetch all results
    rows = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries (easier to work with in Python)
    history = []
    for row in rows:
        history.append({
            'timestamp': row[0],
            'input_type': row[1],
            'input_value': row[2],
            'algorithm': row[3],
            'hash_result': row[4]
        })
    
    return history

def get_database_stats():
    """
    Get some statistics about our database
    Useful for showing how much data we have
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Count total records
    cursor.execute('SELECT COUNT(*) FROM hash_results')
    total_records = cursor.fetchone()[0]
    
    # Count by algorithm
    cursor.execute('''
        SELECT algorithm, COUNT(*) 
        FROM hash_results 
        GROUP BY algorithm
    ''')
    algorithm_counts = cursor.fetchall()
    
    # Count by input type
    cursor.execute('''
        SELECT input_type, COUNT(*) 
        FROM hash_results 
        GROUP BY input_type
    ''')
    input_type_counts = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_records': total_records,
        'algorithm_counts': dict(algorithm_counts),
        'input_type_counts': dict(input_type_counts)
    }

# Test function to make sure everything works
if __name__ == '__main__':
    """
    This runs only if we run this file directly (for testing)
    """
    print("Testing database operations...")
    
    # Initialize database
    init_db()
    
    # Test saving a hash result
    save_hash_result('text', 'Hello World', 'SHA-256', 'test_hash_value')
    
    # Test getting history
    history = get_hash_history(5)
    print(f"Found {len(history)} records")
    
    # Test getting stats
    stats = get_database_stats()
    print(f"Database stats: {stats}")
    
    print("Database tests completed!")
