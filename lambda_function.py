from config import BUCKET_ENTRADA, BUCKET_SALIDA
from services.s3_service import get_audio_file, save_pdf_to_s3, get_transcription_text
from services.transcribe_service import start_transcription, check_transcription_status
from services.comprehend_service import analizar_transcripcion
from services.pdf_generator import crear_pdf_minuta
from utils.logging_util import log_event
from datetime import datetime
import json

def lambda_handler(event, context):
    log_event("Evento recibido:", event)
    
    archivo_audio = event['Records'][0]['s3']['object']['key']
    job_name = f"transcription_job_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    audio_uri = f"s3://{BUCKET_ENTRADA}/{archivo_audio}"

    try:
        get_audio_file(BUCKET_ENTRADA, archivo_audio)
        log_event("Inicia transcripcion de audio",{})
        start_transcription(job_name, audio_uri, BUCKET_SALIDA)
        transcription_status = check_transcription_status(job_name)

        if transcription_status == 'COMPLETED':
            log_event("Se completa transcripcion",{})
            transcription_text = get_transcription_text(job_name, BUCKET_SALIDA)
            log_event("Se inicia analisis con Amazon Comprehend",{})
            # Analizar la transcripción con Amazon Comprehend
            resumen, objetivos, compromisos, participantes = analizar_transcripcion(transcription_text)
            log_event("Se completa analisis con Amazon Comprehend",{})
            # Generar y guardar la minuta en PDF
            nombre_pdf = f"{job_name}_minuta.pdf"
            log_event("Se inicia creacion pdf",{})
            pdf_minuta = crear_pdf_minuta(nombre_pdf, resumen, objetivos, compromisos, participantes, transcription_text)
            log_event("Se crea pdf",{})
            #pdf_minuta = generar_minuta_pdf(transcription_text)
            save_pdf_to_s3(pdf_minuta, job_name, BUCKET_SALIDA)
            return {'statusCode': 200, 'body': json.dumps("Minuta guardada.")}
        else:
            return {'statusCode': 500, 'body': json.dumps("Error en la transcripción.")}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f"Error inesperado: {str(e)}")}
