
# Osu Profile Analyzer

Analyzes your osu profile and suggest you what map to farm, skill to improve, based on your latest and overall behavior.





## Run Locally

Clone the project

```bash
  git clone https://github.com/KoshysDev/FastAPI-Osu-Profile-Analyzer.git
```

Go to the project directory

```bash
  cd FastAPI-Osu-Profile-Analyzer
```

Install dependencies

```bash
  pip install dependency.txt
```

Make sure that you created .env file inside Backend folder and added JWT_SECRET=*replaceme* line inside

Create database

```bash
  cd .\Backend\
  python
  import services
  services.create_database()
```

Start the server

```bash
  #uvicorn main:app --reload
```


## Author

- [@Koshys](https://github.com/KoshysDev)

