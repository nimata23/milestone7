from website import create_app, create_test_app

#app = create_app()
app = create_test_app()

if __name__ == '__main__':
    app.run(debug=True)