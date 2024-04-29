from gcp_setup import get_all_records_from_table

from flask import Flask

app = Flask(__name__)

def initialize():
    # This function will be called when the app starts
    print("Initializing the application...")

# Call the initialize function when the script is executed
initialize()

@app.route('/')
def index():
    # Call the get_all_records_from_table function with the table name
    records = get_all_records_from_table('server.user_logins')
    # Print the result
    for record in records:
        print(record)
    # Return a message to indicate the records have been printed (optional)
    return 'Records printed in the server console.'
if __name__ == '__main__':
    app.run(debug=True)
