import yaml

# Read
stream = open("datablend.yaml", 'r')
parsed = yaml.load(stream)

# Show
for f in parsed['features']:
    print(f)
