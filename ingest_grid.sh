curl --location --request POST 'http://localhost:5000/sun-spot-analyser-api/grid' \
--header 'Content-Type: application/json' \
--data-raw '{"size": 3, "values": "4, 2, 3, 2, 2, 1, 3, 2, 1"}'
