from database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE Flight
        ADD COLUMN BaseFare DECIMAL(10,2) NOT NULL DEFAULT 0.00
    """)

    cursor.execute("""
        UPDATE Flight
        SET BaseFare =
            CASE FlightNumber
                WHEN 'ST101' THEN 320.00
                WHEN 'ST202' THEN 450.00
                WHEN 'ST303' THEN 520.00
                WHEN 'ST404' THEN 275.00
                WHEN 'ST505' THEN 350.00
                ELSE BaseFare
            END
    """)

    conn.commit()
    print("BaseFare column and fares added successfully.")

except Exception as e:
    print("Error:", e)

finally:
    cursor.close()
    conn.close()