import json
import numpy as np
import sys
import rich


# remover duplicados (remove todos sem deixar nenhum)
def sort_remove_duplicates(file):
    file.sort(key=lambda k: k["student_name"])
    removal = []
    for i in range(len(file) - 1):
        if file[i]["student_name"] == file[i + 1]["student_name"]:
            if i not in removal:
                removal.append(i)
            removal.append(i + 1)
    rich.print(
        f"\n>>> Foram encontrados {len(removal)} nomes repetidos. Eles já foram removidos :smiley:!"  # noqa
    )
    for item in sorted(removal, reverse=True):
        try:
            del file[item]
        except IndexError:
            pass
    rich.print(f">>> Total final {len(file)} nomes!")


# apenas duplicados
def sort_only_duplicates(file):
    file.sort(key=lambda k: k["student_name"])
    final = []

    for i in range(len(file) - 1):
        if (
            file[i]["student_name"] == file[i + 1]["student_name"]
            and file[i] not in final
        ):
            final.append(file[i + 1])
    rich.print(
        f"\n>>> Foram encontrados {len(final)} nomes repetidos. Eles já foram mergeados :smiley:!"  # noqa
    )
    file.clear()
    file.extend(final)


if len(sys.argv) < 3:
    raise ValueError("Número de argumentos menor que 3")
    exit()

try:
    with open(sys.argv[1], "r", encoding="utf-8") as file:
        file = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo JSON --> {sys.argv[1]} base inválido!")
    exit()

nomes = sys.argv[2:]
num_parts = len(nomes)

# #######################################################################
# Estas duas linhas abaixo devem ser descomentadas conforme
# seja necessário remover duplicados ou manter apenas os duplicados noqa
# #######################################################################

# sort_remove_duplicates(file)
# sort_only_duplicates(file)
split_list = np.array_split(file, num_parts)

for index in range(num_parts):
    with open(f"{nomes[index]}.json", "w", encoding="utf-8") as file_out:
        json.dump(
            split_list[index].tolist(), file_out, indent=2, ensure_ascii=False
        )

rich.print(
    f"\n:tada: Arquivo './{sys.argv[1]}' dividido em {num_parts} partes:\n"
)
for nome in nomes:
    rich.print(f">>> [bold]./{nome}.json[/bold]")
