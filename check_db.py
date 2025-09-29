import sqlite3

conn = sqlite3.connect('aura_memory.db')
cursor = conn.cursor()

print('=== Database Tables ===')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(f'Table: {table[0]}')

print('\n=== Goals Table ===')
try:
    cursor.execute('SELECT * FROM goals LIMIT 5')
    goals = cursor.fetchall()
    if goals:
        for goal in goals:
            print(goal)
    else:
        print('No goals found')
except Exception as e:
    print(f'Error: {e}')

print('\n=== Moods Table ===')
try:
    cursor.execute('SELECT * FROM moods LIMIT 5')
    moods = cursor.fetchall()
    if moods:
        for mood in moods:
            print(mood)
    else:
        print('No moods found')
except Exception as e:
    print(f'Error: {e}')

print('\n=== Progress Table ===')
try:
    cursor.execute('SELECT * FROM progress LIMIT 5')
    progress = cursor.fetchall()
    if progress:
        for prog in progress:
            print(prog)
    else:
        print('No progress found')
except Exception as e:
    print(f'Error: {e}')

conn.close()
