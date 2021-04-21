import re


def traitResolution(resolution):
    # transforme "a x b" en deux variable
    resolution = re.sub("(\s*@.+\s*Hz)+", "", resolution)
    resolution = re.sub("\s*\(.*\)\s*", "", resolution)
    splits = re.split("[xX\x0b]", resolution)
    result = []
    if splits is None:
        return [0, 0]
    elif len(splits) == 0:
        return [0, 0]
    else:
        for split in splits:
            r = re.search("\d+", split)
            if r:
                if r.group(0):
                    result.append(r.group(0))
                else:
                    result.append("0")
            else:
                result.append("0")
        if len(result) == 1:
            result.append('0')
    return result


def traitrementGpu(gputext):
    tmp = re.sub('GeForce\s+', '', gputext)
    tmp = re.sub('GeForce®\s+', '', tmp)
    tmp = re.sub("®", "", tmp)
    result = re.sub('™', '', tmp)
    print(gputext)
    return result


def traitfreq(freqtext):
    freqtext = re.sub("[W]", "", freqtext)
    freqtext = re.sub("[w]", "", freqtext)
    r = re.search("\d+", freqtext)
    coef = 1
    rTaille = re.search("GB(/s)?", freqtext)
    if rTaille:
        if rTaille.group(0):
            coef = 1024

    if r:
        if r.group(0):
            return int(r.group(0))*coef
        else:
            return freqtext
    else:
        return ''


def traitSize(sizetext):
    size = []
    sizels = re.split("[ \*]", sizetext)
    for sizel in sizels:
        si = re.search(r"\d+", sizel)
        if si:
            size.append(int(si.group(0)))

    l = len(size)
    if l < 3:
        for i in range(l, 4):
            size.append("")
    return size


def traitsorties(sortie):
    sortie = re.sub("(\s*\(.*\)\s*)", "", sortie)
    sortie = re.sub("<sup>TM</sup>", "", sortie)
    sortie = re.sub("™", "", sortie)
    sortie = re.sub("\s*\(.*\)\s*", "", sortie)
    sortie = re.sub("\s*\(.*<br>\s*", "<br>", sortie)
    sortie = re.sub(r"[\n]+", "", sortie)
    sortie = re.sub(r"(<br>)*\n*<style>.*</style>", "", sortie)
    sortie = re.sub(r"\s*/\s*", ",", sortie)
    sortie = re.sub(r"Display Port\s*\**.*1\.4", "Display Port 1.4", sortie)
    sortie = re.sub(r"\s*<p>\s*", ",", sortie)
    sortie = re.sub(r"\s*[\x0b\u000b]\s*", ",", sortie)

    sorties = re.split("\n*<br>\s*\\n*\n*", sortie)
    result = []
    for sort in sorties:
        ss = re.split(",\s*", sort)
        for s in ss:
            if s != '':
                s2 = re.split("\s*\*\s*", s)
                final = {"type": s2[0], "qte": int(s2[1])}
                result.append(final)
    return result


def traitdivers(divers):
    divers = re.sub("^\d+\.\s*", "", divers)
    divers = re.sub("\n", "", divers)
    divers = re.sub("</*ol>\s*", "", divers)
    divers = re.sub(r"<style>.*<\\*/style>", "", divers)
    divsplits = re.split("<br>\\n*\d+\.\s*", divers)
    tmp = []
    result = []
    for dv in divsplits:
        dmp = re.split("<li>", dv)
        for d in dmp:
            if d != "":
                result.append(d)
    return result


def traittex(tex):
    tex = re.sub("[®]", "", tex)
    tex = re.sub("[™]", "", tex)
    return tex


def traitpin(pintexta):
    resultat = []
    pintexta = pintexta.lower()
    pintexta = re.sub("x", "*", pintexta)
    pintexta = re.sub("X", "*", pintexta)
    pintexta = re.sub("\+", ",", pintexta)
    pintexta = re.sub("[-]", " ", pintexta)
    pintexta = re.sub("and\s*", ", ", pintexta)
    pintexta = re.sub("One", "1 * ", pintexta)
    pintexta = re.sub("one", "1 * ", pintexta)
    pintexta = re.sub("Two", "2 * ", pintexta)
    pintexta = re.sub("Two", "2 * ", pintexta)
    pintexta = re.sub("\s{2,}", " ", pintexta)
    if re.search("n/a", pintexta):
        return ['']
    pintextB = re.split(",\s*", pintexta)
    for pintext in pintextB:
        res = pintext
        pin = None
        n = None
        r = re.search('\d+\s*pin', pintext)
        if r:
            pin = r.group(0)
            r2 = re.search("\d+pin", pin)
            if r2:
                r3 = re.search("\d+", r2.group(0))
                if r3:
                    pin = r3.group(0)+" "+"pin"
            pin = pin + "s"
            pintext = re.sub('\d+\s*pin(s)?', '', pintext)
        r = re.search('\*\s*\d+', pintext)
        if r:
            n = re.search("\d+", r.group(0)).group(0)
        if pin:
            if n:
                res = n + " x " + pin
            else:
                res = "1 x " + pin
        resultat.append(res)
        if resultat is None:
            resultat = ['']
    return resultat