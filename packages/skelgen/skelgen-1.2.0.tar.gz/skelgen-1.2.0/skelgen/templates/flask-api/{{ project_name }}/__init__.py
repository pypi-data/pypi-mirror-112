from {{ project_name }}.server import app

def main():
    app.run(port=5000)
