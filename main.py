import uuid
import time

import boto3

import s3


def text_to_speech(text: str) -> str:
    polly = boto3.client("polly")
    print("generating audio file")
    resp = polly.synthesize_speech(
        VoiceId="Joanna", OutputFormat="mp3", Text=text
    )
    audio_name = f"audio/{uuid.uuid4()}.mp3"
    file = open(audio_name, "wb")
    file.write(resp["AudioStream"].read())
    file.close()
    return audio_name


def speech_to_text(job_name: str, s3_object_url: str, bucket_name: str) -> None:
    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_object_url},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=bucket_name
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


if __name__ == "__main__":
    bucket_name = ''

    # filename = text_to_speech('This is a test of the polly service, this application is written on python')
    # upload_resp = s3.upload_file(file_path=filename, bucket=bucket_name)

    # speech_to_text(job_name='', s3_object_url="", bucket_name=bucket_name)
