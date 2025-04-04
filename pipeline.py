import argparse
import json
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
from typing import Dict, Any

class PubSubToBetterStack(beam.DoFn):
    def __init__(self, source_token: str, ingest_host: str):
        self.source_token = source_token
        self.ingest_host = ingest_host
        self.headers = {
            'Authorization': f'Bearer {source_token}',
            'Content-Type': 'application/json'
        }

    def process(self, element: bytes) -> None:
        try:
            # Parse the PubSub message
            message = json.loads(element.decode('utf-8'))
            
            # Send to Better Stack
            response = requests.post(
                self.ingest_host,
                headers=self.headers,
                json=message
            )
            
            if response.status_code != 202:
                raise Exception(f"Failed to send to Better Stack: {response.text}")
                
        except Exception as e:
            # Log the error but don't fail the pipeline
            print(f"Error processing message: {str(e)}")

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_subscription',
        required=True,
        help='Input PubSub subscription to read from'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Get Better Stack credentials from environment variables
    source_token = os.environ.get('BETTER_STACK_SOURCE_TOKEN')
    ingest_host = os.environ.get('BETTER_STACK_INGESTING_HOST')

    if not source_token or not ingest_host:
        raise ValueError(
            "Environment variables BETTER_STACK_SOURCE_TOKEN and BETTER_STACK_INGESTING_HOST must be set"
        )

    pipeline_options = PipelineOptions(
        pipeline_args,
        save_main_session=True
    )

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'Read from PubSub' >> beam.io.ReadFromPubSub(
                subscription=known_args.input_subscription
            )
            | 'Send to Better Stack' >> beam.ParDo(
                PubSubToBetterStack(source_token, ingest_host)
            )
        )

if __name__ == '__main__':
    run() 