# Backend

## How to launch server using Docker
1. Install docker 
2. Build docker image `docker build -t app .`
3. Run docker `docker run -p 8000:8000 app`
4. Expect output like 
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Execute it directly
1. Make sure python 3.11 is installed `python --version`
2. Create env `python -m venv uxmate-be` and activate `source uxmate-be/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Launch server `uvicorn main:app --reload`


## Execute the test 
To execute the test use command like this:
    `pytest main_test.py::<test name> -s`
For example:
    `pytest main_test.py::test_end_2_end_happy_path -s`
