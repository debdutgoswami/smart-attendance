def get_list(attendance: list):
    present, absent = list(), list() # storing only absent list
    for index in range(len(attendance)-1):
        if str(attendance[index+1]).lower().isalpha():
            absent.append(attendance[index])
            if index==len(attendance)-2:
                break
        else:
            try:
                n = int(str(attendance[index]).lower())
                present.append(n)
            except ValueError:
                pass
    present.append(attendance.pop())
    prevContext = None
    if len(present)==0 or str(present[len(present)-1]).isalpha():
        prevContext = absent[len(absent)-1]
    elif len(absent)==0 or str(absent[len(absent)-1]).isalpha():
        prevContext = present[len(present)-1]
    elif present[len(present)-1]>absent[len(absent)-1]:
        prevContext = present[len(present)-1]
    else:
        prevContext = absent[len(absent)-1]

    return {"present": present, "absent": absent, "prevContext": prevContext}