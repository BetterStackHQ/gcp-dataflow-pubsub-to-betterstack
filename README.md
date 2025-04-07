# Google Cloud Pub/Sub to Better Stack

A Dataflow Flex template that reads messages from Pub/Sub and sends them to Better Stack Telemetry.

## Running the template using Web UI

1. Go to Google Cloud Console -> Dataflow -> [Create job from template](https://console.cloud.google.com/dataflow/createjob)
2. Choose the name and region for the Dataflow job
3. Select **Custom Template**
4. As Template path, use `betterstack/pubsub-to-betterstack.json`
5. Set parameters based on your Google Cloud Pub/Sub Subscription and [Better Stack Telemetry source](https://telemetry.betterstack.com/team/260195/sources)
6. Click **Run job**

## Running the template using CLI

1. Set parameters based on your Google Cloud Pub/Sub Subscription and [Better Stack Telemetry source](https://telemetry.betterstack.com/team/260195/sources)
```bash
INPUT_SUBSCRIPTION=projects/$(gcloud config get-value project)/subscriptions/<your-pubsub-subscription-name>
SOURCE_TOKEN=<your-better-stack-source-token>
INGESTING_HOST=<your-better-stack-ingesting-host>
```

2. Create a Dataflow job using the template
```bash
gcloud dataflow flex-template run "pubsub-to-betterstack-$(date +%Y%m%d-%H%M%S)" \
    --template-file-gcs-location=gs://betterstack/pubsub-to-betterstack.json \
    --parameters input_subscription=$INPUT_SUBSCRIPTION \
    --parameters better_stack_source_token=$SOURCE_TOKEN \
    --parameters better_stack_ingesting_host=$INGESTING_HOST \
    --region=$(gcloud config get-value compute/region)
```

## Optional parameters

The template supports the following optional parameters:

- `batch_size`: Number of messages to batch before sending to Better Stack. Default: 100
- `window_size`: Window size in seconds for batching messages. Default: 10
- `max_retries`: Maximum number of retry attempts for failed requests. Uses exponential backoff between retries. Default: 3
- `initial_retry_delay`: Initial delay in seconds between retries. The delay doubles with each retry attempt. Default: 1

You can include these parameters in your Dataflow job in Optional Parameters section during creation in UI, or by adding them to the `gcloud dataflow flex-template run` command - e.g. `--parameters window_size=5`.

## Releasing new version

After making changes, rebuild the Docker image and the Dataflow template:

```bash
docker build --tag betterstack/gcp-dataflow-pubsub-to-betterstack .
docker push betterstack/gcp-dataflow-pubsub-to-betterstack
gcloud dataflow flex-template build gs://betterstack/pubsub-to-betterstack.json \
    --image "docker.io/betterstack/gcp-dataflow-pubsub-to-betterstack" \
    --sdk-language "PYTHON" \
    --metadata-file "metadata.json"
```

Requires access to `betterstack` Docker Hub repository, and `betterstack` Google Cloud Bucket.

## License

ISC License. See [LICENSE.md](LICENSE.md) for details.
