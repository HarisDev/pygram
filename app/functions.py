def returnName(first_name, last_name, username):

    display_name = ""

    if first_name == "":
        display_name = username
    else:
        display_name = first_name + " " + last_name

    return display_name