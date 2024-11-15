import boto3
comprehend_client = boto3.client('comprehend')

def analizar_transcripcion(transcripcion):
    # Extraer el resumen
    response_summary = comprehend_client.detect_syntax(
        Text=transcripcion,
        LanguageCode='es'
    )

    # Extraer entidades como nombres de personas (participantes)
    response_entities = comprehend_client.detect_entities(
        Text=transcripcion,
        LanguageCode='es'
    )

    participantes = [entity['Text'] for entity in response_entities['Entities'] if entity['Type'] == 'PERSON']

    # Extraer frases clave para detectar objetivos y compromisos
    response_key_phrases = comprehend_client.detect_key_phrases(
        Text=transcripcion,
        LanguageCode='es'
    )

    objetivos = []
    compromisos = []
    for phrase in response_key_phrases['KeyPhrases']:
        if 'objetivo' in phrase['Text'].lower() or 'meta' in phrase['Text'].lower():
            objetivos.append(phrase['Text'])
        elif 'compromiso' in phrase['Text'].lower() or 'acuerdo' in phrase['Text'].lower():
            compromisos.append(phrase['Text'])

    # Generar un resumen básico a partir de las frases clave
    resumen = ' '.join([phrase['Text'] for phrase in response_key_phrases['KeyPhrases'][:3]])

    return resumen, objetivos, compromisos, participantes