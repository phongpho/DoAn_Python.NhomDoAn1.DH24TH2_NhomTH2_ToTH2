from tkcalendar import DateEntry 
import mysql.connector

# ====== Kết nối MySQL ====== 
def connect_db(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="root",         
        password="qlsv",        
        database="quanlysinhvien" 
    )