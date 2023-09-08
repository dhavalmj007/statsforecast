# Statsforcasting [link](https://nixtla.github.io/statsforecast/docs/getting-started/getting_started_complete.html)

## To run in Local
1. Open this project in IDE of your choice PyCharm(Recommended) or VSCode
   1. Follow [this](https://www.youtube.com/watch?v=GTtpypvLoeY) video to set up PyCharm
2. Create virtual environment either through Conda or Venv (Follow the video)
3. Activate the Venv
4. Run `pip install -r requirement.txt`
5. To run the code `python script.py`

## To run in Docker

1. Install docker by following the guide from [here](https://docs.docker.com/engine/install/)
2. Build docker image `docker build -t statsforecast:0.1 .`
3. Run the image `docker run -it statsforecast:0.1`
