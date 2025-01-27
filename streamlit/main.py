import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection
@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="skripsi",
            user="dwiandharavalkyrie",
            password="Ra867293",
            cursor_factory=RealDictCursor
        )
        st.write("Database connection successful!")
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def create_table():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="skripsi",
            user="dwiandharavalkyrie",
            password="Ra867293",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
       # cur.execute('''CREATE TABLE IF NOT EXISTS user (
                        #    id SERIAL PRIMARY KEY,
                       #     email VARCHAR(255) UNIQUE NOT NULL,
                       #     password VARCHAR(255) NOT NULL
                        #)''')
        conn.commit()
    except Exception as e:
        st.error(f"Error creating table: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def register_user(email, password):
    conn = get_connection()
    if conn is None:
        st.error("Database connection is not available.")
        return False

    try:
        cur = conn.cursor()
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        cur.close()
        return True
    except psycopg2.IntegrityError as e:
        conn.rollback()
        st.error(f"IntegrityError: {e}")
        return False
    except Exception as e:
        st.error(f"Unexpected error during registration: {e}")
        return False


def login_user(email, password):
    conn = get_connection()
    if conn is None:
        st.error("Database connection is not available.")
        return False

    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user['password'], password):
        return True
    return False


# Streamlit UI
st.title("Create Account")

# Tab for Register and Login
auth_mode = st.sidebar.radio("Choose an option:", ["Register", "Login"])

if auth_mode == "Register":
    st.header("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(email, password):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Email already exists. Please use a different email.")

elif auth_mode == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(email, password):
            st.success("Login successful! Welcome.")
        else:
            st.error("Invalid email or password.")

# Create table on first run
create_table()
