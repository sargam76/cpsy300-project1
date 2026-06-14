from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

def process_nutritional_data_from_azurite():
    connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqCnrIMWesygtHFnaOGmkqGgzNaI2WqiidxFrMoioSZ9TnZlrF5HHAa6+bpj30ypfzA==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = 'datasets'
    blob_name = 'All_Diets.csv'

    try:
        blob_service_client.create_container(container_name)
        print("Container created!")
    except:
        print("Container already exists!")

    with open('/home/sargam/project1/All_Diets.csv', 'rb') as f:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(f, overwrite=True)
        print("All_Diets.csv uploaded to Azurite!")

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))
    print("CSV read from Azurite successfully!")

    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

    os.makedirs('simulated_nosql', exist_ok=True)
    result = avg_macros.reset_index().to_dict(orient='records')
    with open('simulated_nosql/results.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("Results saved to simulated_nosql/results.json!")

    return "Data processed and stored successfully."

print(process_nutritional_data_from_azurite())
