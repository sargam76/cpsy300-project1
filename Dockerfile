FROM python:3.9-slim

WORKDIR /app

COPY All_Diets.csv .
COPY data_analysis.py .

RUN pip install pandas matplotlib seaborn

CMD ["python3", "data_analysis.py"]
