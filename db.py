import sqlite3
import uuid

DB_NAME = "hotel.db"


def get_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            room_type TEXT,
            available_rooms INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            hotel_name TEXT,
            room_type TEXT,
            check_in TEXT,
            check_out TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def seed_hotels():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM hotels")
    if cur.fetchone()[0] == 0:
        hotels = [
            ("Hotel A", "New York", "Deluxe", 5),
            ("Hotel A", "New York", "Standard", 10),
            ("Hotel B", "New York", "Deluxe", 3),
            ("Hotel D", "Los Angeles", "Standard", 8),
        ]
        cur.executemany(
            "INSERT INTO hotels (name, location, room_type, available_rooms) VALUES (?, ?, ?, ?)",
            hotels
        )

    conn.commit()
    conn.close()


# ------------------------
# DB Operations
# ------------------------

def get_hotels_by_location(location: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT name, room_type, available_rooms FROM hotels WHERE location = ?",
        (location,)
    )
    rows = cur.fetchall()
    conn.close()

    return rows


def book_room_db(hotel_name, room_type, check_in, check_out):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT available_rooms FROM hotels
        WHERE name = ? AND room_type = ?
    """, (hotel_name, room_type))

    row = cur.fetchone()
    if not row or row[0] <= 0:
        conn.close()
        return None

    cur.execute("""
        UPDATE hotels
        SET available_rooms = available_rooms - 1
        WHERE name = ? AND room_type = ?
    """, (hotel_name, room_type))

    booking_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO bookings
        (booking_id, hotel_name, room_type, check_in, check_out, status)
        VALUES (?, ?, ?, ?, ?, 'BOOKED')
    """, (booking_id, hotel_name, room_type, check_in, check_out))

    conn.commit()
    conn.close()

    return booking_id


def cancel_booking_db(booking_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT hotel_name, room_type, status
        FROM bookings WHERE booking_id = ?
    """, (booking_id,))

    row = cur.fetchone()
    if not row:
        conn.close()
        return "NOT_FOUND"

    if row[2] == "CANCELLED":
        conn.close()
        return "ALREADY_CANCELLED"

    hotel_name, room_type, _ = row

    cur.execute("""
        UPDATE bookings
        SET status = 'CANCELLED'
        WHERE booking_id = ?
    """, (booking_id,))

    cur.execute("""
        UPDATE hotels
        SET available_rooms = available_rooms + 1
        WHERE name = ? AND room_type = ?
    """, (hotel_name, room_type))

    conn.commit()
    conn.close()

    return "CANCELLED"
