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
            data[newspaper][urlkey][version]["urlkey"] = urlkey # update urlkey - some versions have different urlkeys that have query parameters
            data[newspaper][urlkey][version]["newspaper"] = newspaper
            output.append(data[newspaper][urlkey][version])

json.dump(output, output_file, indent=4)
