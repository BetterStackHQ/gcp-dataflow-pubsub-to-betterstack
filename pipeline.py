import argparse
import json
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
from typing import Dict, Any

class PubSubToBetterStack(beam.DoFn):
    def __init__(self, source_token: str, ingesting_host: str):
        self.source_token = source_token
        self.ingesting_url = ingesting_host if '://' in ingesting_host else f'https://{ingesting_host}'
        self.headers = {
            'Authorization': f'Bearer {source_token}',
            'Content-Type': 'application/json'
        }

    def process(self, element: bytes) -> None:
        try:
            # Parse the Pub/Sub data
            data = json.loads(element.decode('utf-8'))

            # Rename timestamp key to dt to be understood by Better Stack
            if 'timestamp' in data:
                data['dt'] = data.pop('timestamp')

            # Send to Better Stack
            response = requests.post(
                self.ingesting_url,
                headers=self.headers,
                json=data
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
        help='The name of the Pub/Sub subscription to read from'
    )
    parser.add_argument(
        '--better_stack_source_token',
        required=True,
        help='The source token of your telemetry source in Better Stack'
    )
    parser.add_argument(
        '--better_stack_ingesting_host',
        required=True,
        help='The ingesting host of your telemetry source in Better Stack'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(
        pipeline_args,
        save_main_session=True
    )

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                subscription=known_args.input_subscription
            )
            | 'Send to Better Stack' >> beam.ParDo(
                PubSubToBetterStack(
                    known_args.better_stack_source_token,
                    known_args.better_stack_ingesting_host
                )
            )
        )

if __name__ == '__main__':
    run() 