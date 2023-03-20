
# Osu Profile Analyzer

Analyzes your osu profile and suggest you what map to farm, skill to improve, based on your latest and overall behavior.





## Run Backend Locally

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

cd to backend folder

```bash
  cd .\Backend\
```

Make sure that you created .env file inside Backend folder and added OSU_APP_SECRET=* 
and OSU_APP_ID=* from https://osu.ppy.sh/home/account/edit#new-oauth-application

Start the backend server

```bash
  #uvicorn main:app --reload
```

## Run Frontend Locally

Install node.js

```bash
  link: https://nodejs.org/en/download
```

cd to frontend folder in project in new terminal

```bash
  cd .\Frontend\
```

install node.js dependencies

```bash
  npm install axios
```

run frontend

```bash
  npm run dev
```

## Author

- [@Koshys](https://github.com/KoshysDev)

