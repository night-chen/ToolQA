import mysql
import mysql.connector as msql

def execute(sql_cmd):
    conn = msql.connect(host="<YOUR_MYSQL_HOST>", user='root',  
                        password="<YOUR_MYSQL_PASSWORD>")#give ur username, password
    cursor = conn.cursor()
    cursor.execute(sql_cmd)

    column_names = [i[0] for i in cursor.description]
    rows = cursor.fetchall()
    # return rows
    rows_string = []
    for row in rows:
        current_row = [column_names[i]+": "+str(row[i]) for i in range(len(row))]
        current_row = ', '.join(current_row)
        rows_string.append(current_row)
    rows_string = '\n'.join(rows_string)
    return rows_string

if __name__ == "__main__":
    sql_cmd = "SELECT latitude, longitude FROM yelp.yelp_data WHERE address='6830 Rising Sun Ave'"
    rows = execute(sql_cmd)
    print(rows)
