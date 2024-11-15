import boto3, time
transcribe_client = boto3.client('transcribe')

def start_transcription(job_name, audio_uri, bucket_salida):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_uri},
        MediaFormat='mp3',
        LanguageCode='es-US',
        OutputBucketName=bucket_salida
    )

def check_transcription_status(job_name):
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            return status['TranscriptionJob']['TranscriptionJobStatus']
        time.sleep(5)
