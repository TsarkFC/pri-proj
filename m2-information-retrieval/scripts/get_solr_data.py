import sys, json

if len(sys.argv) != 3:
    print("We need an input and output file!", sys.stderr)

output_file = open(sys.argv[2], "w")
with open(sys.argv[1], "r") as f:
    data = json.load(f)

output = []

for newspaper in data.keys():
    for urlkey in data[newspaper]:
        for version in data[newspaper][urlkey]:
            obj = data[newspaper][urlkey][version]
            obj["urlkey"] = urlkey # update urlkey - some versions have different urlkeys that have query parameters
            obj["newspaper"] = newspaper
            output.append(obj)

json.dump(output, output_file, indent=4)
