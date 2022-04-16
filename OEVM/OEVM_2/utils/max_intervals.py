def get_max_intervals(values):
    values = [f'{v:04b}' if type(v) is int else v for v in values]

    links = [0] * len(values)
    max_int = []
    desc = []

    n = len(values)

    for i in range(n):
        for j in range(i, n):
            diffpos = -1
            for k in range(len(values[i])):
                if values[i][k] != values[j][k]:
                    if diffpos != -1:
                        diffpos = -1
                        break
                    diffpos = k
            if diffpos >= 0:
                links[i] += 1
                links[j] += 1
                mask = list(values[i])
                mask[diffpos] = '-'
                max_int.append(''.join(mask))
                desc.append(values[i] + ', ' + values[j])
        if links[i] == 0:
            max_int.append(values[i])
            desc.append(None)
    return zip(max_int, desc)
