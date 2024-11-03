import sqlite3

DB_PATH = "./todo.db"  # Update this path accordingly
INPROGRESS = "In Progress"
COMPLETED = "Completed"
FAILED = "Failed"


def add_to_item(items):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO items(item, status) values (?, ?)", (items, INPROGRESS))
        conn.commit()
        return {"item": items, "status": INPROGRESS}
    except Exception as e:
        print(e)
        return None


def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items")
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
