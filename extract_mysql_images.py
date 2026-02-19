import os
import pymysql
import json
import datetime
from dotenv import load_dotenv

# Load old env variables
load_dotenv('.env')

def extract_mysql_images():
    print("--- Extracting original image references from MySQL ---")
    
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='agropastoral_db',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        data = {
            "projects": [],
            "gallery": [],
            "news": [],
            "impact": []
        }
        
        with connection.cursor() as cursor:
            # Programs
            try:
                cursor.execute("SELECT * FROM programs_program")
                data["programs"] = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching programs: {e}")

            # Projects
            try:
                cursor.execute("SELECT * FROM projects_project")
                data["projects"] = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching projects: {e}")
                
            # Gallery
            try:
                cursor.execute("SELECT * FROM gallery_gallery")
                data["gallery"] = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching gallery: {e}")
                
            # News
            try:
                cursor.execute("SELECT * FROM blog_news")
                data["news"] = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching news: {e}")
                
            # Impact
            try:
                cursor.execute("SELECT * FROM impact_impactstory")
                data["impact"] = cursor.fetchall()
            except Exception as e:
                print(f"Error fetching impact: {e}")
                
        connection.close()
        
        # Custom encoder for datetime
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime.date, datetime.datetime)):
                    return obj.isoformat()
                return super(DateTimeEncoder, self).default(obj)

        with open('original_data.json', 'w') as f:
            json.dump(data, f, indent=4, cls=DateTimeEncoder)
            
        print("[+] Success! Original data saved to original_data.json")
        
    except Exception as e:
        print(f"[-] Failed to connect to MySQL: {e}")
        print("Note: Ensure MySQL is running on port 3306 and uses the credentials in .env")

if __name__ == "__main__":
    extract_mysql_images()
