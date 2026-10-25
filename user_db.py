"""
IVTV User Accounts & Storage Database Manager
Local SQLite3 database engine with PBKDF2 password hashing,
session tokens, and cloud-synced user favorites & watch history.
"""

import sqlite3
import hashlib
import secrets
import os
import time
import re

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ivtv_users.db')

def get_connection():
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for high concurrency in multi-threaded HTTP server
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                display_name TEXT,
                avatar TEXT DEFAULT 'neon-star',
                created_at REAL NOT NULL,
                last_login REAL
            );
        """)
        
        # 2. Sessions table (tokens)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        
        # 3. User Favorites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_favorites (
                user_id INTEGER NOT NULL,
                channel_id TEXT NOT NULL,
                added_at REAL NOT NULL,
                PRIMARY KEY (user_id, channel_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        
        # 4. User Recent Channels
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_recent (
                user_id INTEGER NOT NULL,
                channel_id TEXT NOT NULL,
                watched_at REAL NOT NULL,
                PRIMARY KEY (user_id, channel_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 5. User Channel Watch Stats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER NOT NULL,
                channel_id TEXT NOT NULL,
                clicks INTEGER DEFAULT 0,
                seconds INTEGER DEFAULT 0,
                last_watched REAL DEFAULT 0,
                PRIMARY KEY (user_id, channel_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # Indexes for fast querying
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fav_user ON user_favorites(user_id, added_at DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_recent_user ON user_recent(user_id, watched_at DESC);")
        conn.commit()

# Initialize on import
init_db()

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return key.hex(), salt

def verify_password(stored_hash, stored_salt, password):
    key, _ = hash_password(password, stored_salt)
    return secrets.compare_digest(key, stored_hash)

def create_session(user_id, duration_days=30):
    token = secrets.token_hex(32)
    now = time.time()
    expires_at = now + (duration_days * 86400)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token, user_id, now, expires_at)
        )
        conn.commit()
    return token

def get_user_by_token(token):
    if not token:
        return None
    now = time.time()
    with get_connection() as conn:
        row = conn.execute("""
            SELECT u.id, u.username, u.display_name, u.avatar, u.created_at, u.last_login
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ? AND s.expires_at > ?
        """, (token, now)).fetchone()
        if row:
            return {
                "id": row["id"],
                "username": row["username"],
                "displayName": row["display_name"] or row["username"],
                "avatar": row["avatar"] or "neon-star",
                "createdAt": row["created_at"],
                "lastLogin": row["last_login"]
            }
    return None

def register_user(username, password, display_name=None, avatar='neon-star', initial_favorites=None):
    username = (username or '').strip()
    if not username or len(username) < 3 or len(username) > 30:
        raise ValueError("Username must be between 3 and 30 characters.")
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
    if not password or len(password) < 4:
        raise ValueError("Password must be at least 4 characters long.")

    display_name = (display_name or '').strip() or username
    avatar = (avatar or '').strip() or 'neon-star'
    p_hash, salt = hash_password(password)
    now = time.time()

    with get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt, display_name, avatar, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, p_hash, salt, display_name, avatar, now, now))
            user_id = cursor.lastrowid

            # Import initial local favorites if provided
            if initial_favorites and isinstance(initial_favorites, list):
                for ch_id in initial_favorites:
                    if isinstance(ch_id, str) and ch_id.strip():
                        cursor.execute("""
                            INSERT OR IGNORE INTO user_favorites (user_id, channel_id, added_at)
                            VALUES (?, ?, ?)
                        """, (user_id, ch_id.strip(), now))

            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Username '{username}' is already taken. Please choose another.")

    token = create_session(user_id)
    user = {
        "id": user_id,
        "username": username,
        "displayName": display_name,
        "avatar": avatar,
        "createdAt": now,
        "lastLogin": now
    }
    favorites = get_favorites(user_id)
    return user, token, favorites

def login_user(username, password):
    username = (username or '').strip()
    password = password or ''
    if not username or not password:
        raise ValueError("Username and password are required.")

    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, username, password_hash, salt, display_name, avatar, created_at
            FROM users WHERE username = ? COLLATE NOCASE
        """, (username,)).fetchone()

        if not row or not verify_password(row["password_hash"], row["salt"], password):
            raise ValueError("Invalid username or password.")

        user_id = row["id"]
        now = time.time()
        conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user_id))
        conn.commit()

        user = {
            "id": user_id,
            "username": row["username"],
            "displayName": row["display_name"] or row["username"],
            "avatar": row["avatar"] or "neon-star",
            "createdAt": row["created_at"],
            "lastLogin": now
        }

    token = create_session(user_id)
    favorites = get_favorites(user_id)
    recent = get_recent(user_id)
    return user, token, favorites, recent

def logout_user(token):
    if not token:
        return
    with get_connection() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()

def update_profile(user_id, display_name=None, avatar=None, new_password=None):
    with get_connection() as conn:
        if display_name is not None:
            display_name = display_name.strip()
            conn.execute("UPDATE users SET display_name = ? WHERE id = ?", (display_name, user_id))
        if avatar is not None:
            conn.execute("UPDATE users SET avatar = ? WHERE id = ?", (avatar.strip(), user_id))
        if new_password:
            if len(new_password) < 4:
                raise ValueError("New password must be at least 4 characters long.")
            p_hash, salt = hash_password(new_password)
            conn.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (p_hash, salt, user_id))
        conn.commit()

def get_favorites(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT channel_id FROM user_favorites
            WHERE user_id = ? ORDER BY added_at DESC
        """, (user_id,)).fetchall()
        return [r["channel_id"] for r in rows]

def set_favorites(user_id, channel_ids):
    now = time.time()
    with get_connection() as conn:
        conn.execute("DELETE FROM user_favorites WHERE user_id = ?", (user_id,))
        for idx, ch_id in enumerate(channel_ids):
            if isinstance(ch_id, str) and ch_id.strip():
                # Stagger added_at so ordering is preserved
                conn.execute("""
                    INSERT INTO user_favorites (user_id, channel_id, added_at)
                    VALUES (?, ?, ?)
                """, (user_id, ch_id.strip(), now - idx))
        conn.commit()
    return get_favorites(user_id)

def toggle_favorite(user_id, channel_id):
    channel_id = (channel_id or '').strip()
    if not channel_id:
        return False, get_favorites(user_id)

    now = time.time()
    with get_connection() as conn:
        existing = conn.execute("""
            SELECT 1 FROM user_favorites WHERE user_id = ? AND channel_id = ?
        """, (user_id, channel_id)).fetchone()

        if existing:
            conn.execute("DELETE FROM user_favorites WHERE user_id = ? AND channel_id = ?", (user_id, channel_id))
            added = False
        else:
            conn.execute("""
                INSERT INTO user_favorites (user_id, channel_id, added_at)
                VALUES (?, ?, ?)
            """, (user_id, channel_id, now))
            added = True
        conn.commit()

    return added, get_favorites(user_id)

def sync_favorites(user_id, local_favorites):
    """Merges incoming local favorites into user's DB favorites and returns merged list."""
    now = time.time()
    with get_connection() as conn:
        if isinstance(local_favorites, list):
            for ch_id in local_favorites:
                if isinstance(ch_id, str) and ch_id.strip():
                    conn.execute("""
                        INSERT OR IGNORE INTO user_favorites (user_id, channel_id, added_at)
                        VALUES (?, ?, ?)
                    """, (user_id, ch_id.strip(), now))
        conn.commit()
    return get_favorites(user_id)

def get_recent(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT channel_id FROM user_recent
            WHERE user_id = ? ORDER BY watched_at DESC LIMIT 12
        """, (user_id,)).fetchall()
        return [r["channel_id"] for r in rows]

def add_recent(user_id, channel_id):
    channel_id = (channel_id or '').strip()
    if not channel_id:
        return get_recent(user_id)

    now = time.time()
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO user_recent (user_id, channel_id, watched_at)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, channel_id) DO UPDATE SET watched_at = ?
        """, (user_id, channel_id, now, now))
        # Keep only top 12
        conn.execute("""
            DELETE FROM user_recent WHERE user_id = ? AND channel_id NOT IN (
                SELECT channel_id FROM user_recent WHERE user_id = ? ORDER BY watched_at DESC LIMIT 12
            )
        """, (user_id, user_id))
        conn.commit()
    return get_recent(user_id)

def get_stats(user_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT channel_id, clicks, seconds, last_watched
            FROM user_stats WHERE user_id = ?
        """, (user_id,)).fetchall()
        result = {}
        for r in rows:
            result[r["channel_id"]] = {
                "clicks": r["clicks"],
                "seconds": r["seconds"],
                "lastWatched": r["last_watched"]
            }
        return result

def track_stat(user_id, channel_id, clicks=0, seconds=0):
    channel_id = (channel_id or '').strip()
    if not channel_id:
        return
    now = time.time()
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO user_stats (user_id, channel_id, clicks, seconds, last_watched)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, channel_id) DO UPDATE SET
                clicks = clicks + ?,
                seconds = seconds + ?,
                last_watched = ?
        """, (user_id, channel_id, clicks, seconds, now, clicks, seconds, now))
        conn.commit()
