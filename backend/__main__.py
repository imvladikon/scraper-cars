from backend import app, db

if __name__ == '__main__':
    db.model.bind(**app.config['PONY'])
    db.model.generate_mapping(create_tables=True)
    app.run(debug=True, threaded=True)