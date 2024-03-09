import re

name = "Hubert Müller"
end = "):"

bsp_str= "Hubert Müller Außenminister: blablabla heute ist gutes wetter Ulla Jelpe (DIE LINKE):"

start = f"{name}.*:"

regex_match = re.compile(start)
match = re.findall((regex_match), bsp_str)
newstart = "".join(match)  # re.findall Ergebnis -> Liste, diese in string umwandeln
print(newstart)

start_index = bsp_str.find(start, bsp_str.find(start))
start_index += len(newstart)



end_position = result.find(ende, start_index)
if ende != -1:
    rede = result[start_index:end_position].strip()
    print(rede)

#test