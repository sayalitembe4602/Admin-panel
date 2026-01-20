from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import pymysql

app = FastAPI()
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Sayalitembe@230712",
        database="enterprise_usage_system",
        cursorclass=pymysql.cursors.DictCursor
    )
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def login_page():
    return FileResponse("static/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

@app.post("/login")
async def login(request: Request):
    data = await request.json()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s AND role='admin'",
        (data["email"], data["password"])
    )

    user = cur.fetchone()
    db.close()

    return {"success": True} if user else {"success": False}

@app.get("/users")
def get_users():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    db.close()
    return users


@app.post("/users")
async def add_user(request: Request):
    data = await request.json()

    print("RECEIVED:", data)  

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
        (
            data["name"],
            data["email"],
            data["password"],
            data["role"]
        )
    )

    db.commit()
    db.close()

    return {"message": "User added successfully"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    db.close()
    return {"message": "Deleted"}

@app.get("/usage")
def usage():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM usage_logs")
    data = cur.fetchall()
    db.close()
    return data
