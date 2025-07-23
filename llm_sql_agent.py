import sqlite3
import matplotlib.pyplot as plt

# Connect to your DB
conn = sqlite3.connect("ecommerce.db")

# Mock LLM logic to convert questions to SQL
def get_sql(question):
    question = question.lower()
    
    if "total sales" in question:
        return "SELECT SUM(total_sales) AS total_sales FROM total_sales;"
    
    elif "roas" in question:
        return "SELECT SUM(ad_sales) / SUM(ad_spend) AS roas FROM ad_sales;"
    
    elif "highest ad spend" in question.lower():
        return "SELECT item_id, SUM(ad_spend) AS total_spend FROM ad_sales GROUP BY item_id ORDER BY total_spend DESC LIMIT 5;"
    
    else:
        return "Sorry, I don't understand that question."

def run_agent(question):
    sql = get_sql(question)
    if not sql:
        print("Sorry, I don't understand that question.")
        return

    print("\nSQL Query:\n", sql)
    try:
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        print("\nAnswer:")
        for row in rows:
            print(dict(zip(columns, row)))

        # Graph for total sales
        if "total sales" in question.lower():
            cursor = conn.execute("SELECT date, total_sales FROM total_sales ORDER BY date;")
            data = cursor.fetchall()
            dates = [row[0] for row in data]
            sales = [row[1] for row in data]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, sales, marker='o', color='green')
            plt.xticks(rotation=45)
            plt.xlabel("Date")
            plt.ylabel("Total Sales")
            plt.title("Total Sales Over Time")
            plt.tight_layout()
            plt.show()

        # Graph for highest ad spend
        elif "highest ad spend" in question.lower():
            cursor = conn.execute("SELECT item_id, SUM(ad_spend) AS total_spend FROM ad_sales GROUP BY item_id ORDER BY total_spend DESC LIMIT 5;")
            data = cursor.fetchall()
            items = [str(row[0]) for row in data]
            spends = [row[1] for row in data]


            plt.figure(figsize=(8, 5))
            plt.bar(items, spends, color='orange')
            plt.xlabel("Item ID")
            plt.ylabel("Ad Spend")
            plt.title("Top 5 Items by Ad Spend")
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print("SQL Execution Error:", e)

# Start the agent
question = input("\nAsk your e-commerce question: ")
run_agent(question)
