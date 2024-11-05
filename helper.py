import sqlite3

DB_PATH = "./todo.db"  # Update this path accordingly
INPROGRESS = "In Progress"
COMPLETED = "Completed"
FAILED = "Failed"

def check_login(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, password))
        user_data = c.fetchone()
        return user_data[0] if user_data else None
    except Exception as e:
        print(e)
        return None

def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM accounts WHERE username=?", (username,))
        if c.fetchone() is not None:
            return False

        c.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False

def add_to_item(items, user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO items(item, status, posted_by) values (?, ?, ?)", (items, INPROGRESS, user_id))
        conn.commit()
        return {"item": items, "status": INPROGRESS}
    except Exception as e:
        print(e)
        return None


def get_all_items(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where posted_by='%s'" % user_id)
        rows = c.fetchall()
        return {"count": len(rows), "items": rows}
    except Exception as e:
        print("Error: ", e)
        return None


def get_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where item='%s'" % item)
        status = c.fetchone()[0]
        return status
    except Exception as e:
        print(e)
        return None


def update_status(item, status):
    if status.lower().strip() == "in progress":
        status = INPROGRESS
    elif status.lower().strip() == "completed":
        status = COMPLETED
    else:
        print("Invalid Status: " + status)
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("update items set status=? where id=?", (status, item))
        conn.commit()
        return {item: status}
    except Exception as e:
        print("Error: ", e)
        return None


def delete_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("delete from items where id=?", (item,))
        conn.commit()
        return {"item": item}
    except Exception as e:
        print("Error: ", e)
        return None
