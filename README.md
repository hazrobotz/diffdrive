
## Building standalone diffdrive test

### 1 Local venv/conda build
-- create an environment, and activate --

git clone https://github.com/hazrobotz/diffdrive.git

cd diffdrive

pip install -r requirements.txt

cd code

python webservice.py

### 2 Local docker build

git clone https://github.com/hazrobotz/diffdrive.git

cd diffdrive

docker build -t testdiffdrive .

docker run --rm --net=host -p 8000:8000 -v /tmp:/app/saved -e PORT=8000 -e NUM_PLANTS=2 -e SAMPLE_PERIOD=0.02 testdiffdrive
