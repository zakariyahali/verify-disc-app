To use the app:
1. run uvicorn main:app --reload
2. Use endpoint @post("/convert") 
    and deliver payload: {
                        "file_path": "assets/financellc.pdf"
                        }
3. Change the file path accordingly to test out different dummy PDF's

To run tests:
 - run script app/tests.py 
 - alternatively: python -m unittest discover -s app
