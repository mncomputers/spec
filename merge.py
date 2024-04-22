sections = ["Data types", "CPU"]

output = ""

with open("Header.md") as f:
    output = f.read()
    output += "\n\n"

output += "\n[comment]: # (This is automatically generated, please do not edit this file. Instead, edit specific files like `CPU.md`, then run `merge.py` to merge it.)\n\n|Sections:|\n|-|\n"
for x in sections:
    output += f"[{x}](#{x.lower().replace(' ', '-')})\n"
output += "\n"

for x in sections:
    with open(x + ".md", "r") as f:
        output += f"# {x}\n\n"
        for line in f.readlines():
            line = line.removesuffix('\n').removesuffix('\r').removesuffix('\n')
            if line.startswith("#"):
                hashtagAmount = 0
                for x in line:
                    if x == "#":
                        hashtagAmount += 1
                    elif x == " ":
                        break
                    else:
                        hashtagAmount = 0
                        break
                if hashtagAmount != 0:
                    line = "#" + line
            output += line + "\n"
        output += "\n"

gen_start_location = output.find("<!--?generate\n")
gen_end_location = -1

while gen_start_location != -1:
    gen_end_location = output.find("-->", gen_start_location)
    if gen_end_location == -1:
        print("unclosed '<!--?autogenerate' tag detected")
        exit()
    gen_end_location += 3
    code = output[gen_start_location + 14:gen_end_location - 4]
    new_output_1 = ""
    
    def set_output(_output: str) -> None:
        global new_output_1
        new_output_1 = _output

    exec(code, {"set_output": set_output}, {})

    before_output = output[:gen_start_location]
    after_output = output[gen_end_location:]

    new_output = ""
    
    for x in new_output_1.split("\n"):
        if x.startswith("#"):
            x = "#" + x
        new_output += x
        new_output += "\n"

    output = before_output + new_output + after_output

    gen_start_location = output.find("<!--?generate\n")
    break

with open("Full documentation.md", "w") as f:
    f.write(output)