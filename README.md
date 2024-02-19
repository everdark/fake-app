# What is it

This is a repository to demonstrate `opentelemetry` observability using a manually instrumented Python library,
[fake-evaluator](https://github.com/everdark/fake-evaluator).

```bash
# install dependencies
pip install -r requirements.txt

# run the app, the telemetry will go to console, instrumentation is down at package level
python app.py
```

## The sdk-backend pattern

Also known as the [no-collector pattern](https://opentelemetry.io/docs/collector/deployment/no-collector/).

Here we use [Jaeger](https://www.jaegertracing.io/) as the backend.
Be aware that it only supports direct export of traces but not metrics,
so it will fail to export metrics.

```bash
# run jaeger all-in-one backend
# for details: https://www.jaegertracing.io/docs/1.54/getting-started/
docker run --rm --name jaeger -d \
  -p 16686:16686 \
  -p 4317:4317 \
  jaegertracing/all-in-one:1.54
```

Then run the app to export the traces.
Visit `http://localhost:16686` for the UI.


```bash
# run prometheus
docker run --rm --name prom -d \
    -p 9090:9090 \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus:v2.45.3
```

## The sdk-collector-backend pattern

Also known as the [agent pattern](https://opentelemetry.io/docs/collector/deployment/agent/).

```bash
# spin up collector, and trace/metric backend
docker compose up -d

# now create some telemetry
python app.py
```

- Jaeger UI for traces: `http://localhost:16686`
- Prometheus UI for metrics: `http://localhost:9090`
