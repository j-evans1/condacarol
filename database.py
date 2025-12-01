"""
Database module for CondaCarol
Handles PostgreSQL persistence with fallback to in-memory storage
"""

import os
import json
from typing import Dict, List, Set, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

# Database connection pool
db_pool = None

def init_database():
    """Initialize database connection and create tables"""
    global db_pool

    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        print("⚠️ No DATABASE_URL found - using in-memory storage (local development mode)")
        return None

    try:
        # Railway/Render provide DATABASE_URL in postgres:// format
        # psycopg2 needs postgresql:// format
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)

        # Create connection pool
        db_pool = SimpleConnectionPool(1, 10, database_url)

        # Create tables
        conn = db_pool.getconn()
        try:
            cur = conn.cursor()

            # Cities table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    city_name VARCHAR(255) PRIMARY KEY,
                    phase VARCHAR(50) DEFAULT 'setup',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Questions table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id SERIAL PRIMARY KEY,
                    city_name VARCHAR(255) REFERENCES cities(city_name) ON DELETE CASCADE,
                    question_text TEXT NOT NULL,
                    question_order INTEGER NOT NULL,
                    UNIQUE(city_name, question_order)
                )
            """)

            # Participants table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS participants (
                    id SERIAL PRIMARY KEY,
                    city_name VARCHAR(255) REFERENCES cities(city_name) ON DELETE CASCADE,
                    participant_name VARCHAR(255) NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(city_name, participant_name)
                )
            """)

            # Answers table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS answers (
                    id SERIAL PRIMARY KEY,
                    city_name VARCHAR(255) REFERENCES cities(city_name) ON DELETE CASCADE,
                    participant_name VARCHAR(255) NOT NULL,
                    question_order INTEGER NOT NULL,
                    answer_text TEXT NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(city_name, participant_name, question_order)
                )
            """)

            # Guesses table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS guesses (
                    id SERIAL PRIMARY KEY,
                    city_name VARCHAR(255) REFERENCES cities(city_name) ON DELETE CASCADE,
                    guesser_name VARCHAR(255) NOT NULL,
                    question_order INTEGER NOT NULL,
                    answer_id VARCHAR(255) NOT NULL,
                    guessed_name VARCHAR(255) NOT NULL,
                    correct_name VARCHAR(255) NOT NULL,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(city_name, guesser_name, question_order, answer_id)
                )
            """)

            conn.commit()
            print("✅ Database initialized successfully")

        finally:
            db_pool.putconn(conn)

        return db_pool

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("⚠️ Falling back to in-memory storage")
        return None


def get_connection():
    """Get database connection from pool"""
    if db_pool:
        return db_pool.getconn()
    return None


def release_connection(conn):
    """Release connection back to pool"""
    if db_pool and conn:
        db_pool.putconn(conn)


# Database operations
def create_city(city_name: str) -> bool:
    """Create a new city"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cities (city_name, phase) VALUES (%s, 'setup') ON CONFLICT (city_name) DO NOTHING",
            (city_name,)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating city: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def get_all_cities() -> List[str]:
    """Get list of all cities"""
    conn = get_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT city_name FROM cities ORDER BY created_at")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error getting cities: {e}")
        return []
    finally:
        release_connection(conn)


def get_city_phase(city_name: str) -> Optional[str]:
    """Get phase for a city"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("SELECT phase FROM cities WHERE city_name = %s", (city_name,))
        row = cur.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"Error getting city phase: {e}")
        return None
    finally:
        release_connection(conn)


def set_city_phase(city_name: str, phase: str) -> bool:
    """Set phase for a city"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("UPDATE cities SET phase = %s WHERE city_name = %s", (phase, city_name))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error setting city phase: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def add_question(city_name: str, question_text: str, order: int) -> bool:
    """Add a question to a city"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO questions (city_name, question_text, question_order) VALUES (%s, %s, %s)",
            (city_name, question_text, order)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding question: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def get_questions(city_name: str) -> List[str]:
    """Get all questions for a city"""
    conn = get_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT question_text FROM questions WHERE city_name = %s ORDER BY question_order",
            (city_name,)
        )
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error getting questions: {e}")
        return []
    finally:
        release_connection(conn)


def clear_questions(city_name: str) -> bool:
    """Clear all questions for a city"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM questions WHERE city_name = %s", (city_name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing questions: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def add_participant(city_name: str, participant_name: str) -> bool:
    """Add a participant to a city"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO participants (city_name, participant_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (city_name, participant_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding participant: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def get_participants(city_name: str) -> Set[str]:
    """Get all participants for a city"""
    conn = get_connection()
    if not conn:
        return set()

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT participant_name FROM participants WHERE city_name = %s",
            (city_name,)
        )
        return set(row[0] for row in cur.fetchall())
    except Exception as e:
        print(f"Error getting participants: {e}")
        return set()
    finally:
        release_connection(conn)


def save_answer(city_name: str, participant_name: str, question_order: int, answer_text: str) -> bool:
    """Save an answer"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO answers (city_name, participant_name, question_order, answer_text)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (city_name, participant_name, question_order)
               DO UPDATE SET answer_text = EXCLUDED.answer_text""",
            (city_name, participant_name, question_order, answer_text)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving answer: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def get_answers(city_name: str) -> Dict[str, Dict[int, str]]:
    """Get all answers for a city"""
    conn = get_connection()
    if not conn:
        return {}

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT participant_name, question_order, answer_text FROM answers WHERE city_name = %s",
            (city_name,)
        )

        result = {}
        for participant_name, question_order, answer_text in cur.fetchall():
            if participant_name not in result:
                result[participant_name] = {}
            result[participant_name][question_order] = answer_text

        return result
    except Exception as e:
        print(f"Error getting answers: {e}")
        return {}
    finally:
        release_connection(conn)


def has_submitted_answers(city_name: str, participant_name: str) -> bool:
    """Check if participant has submitted answers"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM answers WHERE city_name = %s AND participant_name = %s",
            (city_name, participant_name)
        )
        count = cur.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error checking answers: {e}")
        return False
    finally:
        release_connection(conn)


def save_guess(city_name: str, guesser_name: str, question_order: int, answer_id: str,
               guessed_name: str, correct_name: str) -> bool:
    """Save a guess"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO guesses (city_name, guesser_name, question_order, answer_id, guessed_name, correct_name)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (city_name, guesser_name, question_order, answer_id)
               DO UPDATE SET guessed_name = EXCLUDED.guessed_name, correct_name = EXCLUDED.correct_name""",
            (city_name, guesser_name, question_order, answer_id, guessed_name, correct_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving guess: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)


def get_guesses(city_name: str) -> Dict[str, Dict[str, Dict]]:
    """Get all guesses for a city"""
    conn = get_connection()
    if not conn:
        return {}

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT guesser_name, question_order, answer_id, guessed_name, correct_name FROM guesses WHERE city_name = %s",
            (city_name,)
        )

        result = {}
        for guesser_name, question_order, answer_id, guessed_name, correct_name in cur.fetchall():
            if guesser_name not in result:
                result[guesser_name] = {}

            key = f"q{question_order}_a{answer_id}"
            result[guesser_name][key] = {
                'guessed': guessed_name,
                'correct': correct_name
            }

        return result
    except Exception as e:
        print(f"Error getting guesses: {e}")
        return {}
    finally:
        release_connection(conn)


def clear_city_data(city_name: str) -> bool:
    """Clear all data for a city (for admin reset)"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        # Foreign keys will cascade delete
        cur.execute("DELETE FROM cities WHERE city_name = %s", (city_name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing city data: {e}")
        conn.rollback()
        return False
    finally:
        release_connection(conn)
