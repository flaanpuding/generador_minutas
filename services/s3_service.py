import boto3
s3_client = boto3.client('s3')
import json


def get_audio_file(bucket, key):
    s3_client.head_object(Bucket=bucket, Key=key)

def save_pdf_to_s3(pdf, job_name, bucket):
    s3_client.put_object(
        Bucket=bucket,
        Key=f"{job_name}_minuta.pdf",
        Body=pdf,
        ContentType='application/pdf'
    )

def get_transcription_text(job_name, bucket_salida):
    # Descarga el archivo de transcripción
    response = s3_client.get_object(
        Bucket=bucket_salida,
        Key=f"{job_name}.json"
    )
    
    # Lee y decodifica el contenido JSON
    transcription_data = json.loads(response['Body'].read())
    
    # Extrae el texto transcrito del JSON
    transcription_text = transcription_data['results']['transcripts'][0]['transcript']
    
    return transcription_text