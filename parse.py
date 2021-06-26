import json

LOCAL_FILE = "./backend/local.json"
GLOBAL_FILE = "./backend/global.json"


def command_parse(text, wakeWord):
    if text[0] != wakeWord:
        return ("NULL")
    text = text[1:]
    arr = text.split(" ")
    if len(arr) > 1:
        return (arr[0], " ".join(arr[1:]))
    else:
        return (arr[0], "")


def static_commands(meetingId, command):
    with open(LOCAL_FILE, "r") as l, open(GLOBAL_FILE, "r") as g:
        local_data = json.load(l)
        global_data = json.load(g)
        try:
            output = local_data[meetingId]["settings"][command]
        except KeyError:
            output = global_data["settings"][command]
    return output


def get_custom_commands(text):
    output = []
    for command in text:
        output.append(command["command"])
    return output


def get_custom_command(text, com):
    for command in text:
        if command["command"] == com:
            return command["description"]


def return_command_output(meetingId, command, argument):
    if command in ["announcements", "faqs"]:
        return static_commands(meetingId, command)

    ## TO BE FINISHED!
    with open(LOCAL_FILE, "r") as l, open(GLOBAL_FILE, "r") as g:
        local_data = json.load(l)
        global_data = json.load(g)
        if command in get_custom_commands(
                local_data[meetingId]["settings"]["queueCommands"]):
            pass
        elif command in get_custom_commands(
                global_data["settings"]["queueCommands"]):
            pass
        elif command in get_custom_commands(
                local_data[meetingId]["settings"]["textCommands"]):
            return get_custom_command(
                local_data[meetingId]["settings"]["textCommands"], command)
        elif command in global_data["settings"]["textCommands"].keys():
            return global_data["settings"]["textCommands"][command]

    return None


if __name__ == "__main__":
    print(command_parse("!q What does the moon work", "!"))
    print(command_parse("*help", "*"))
    print(command_parse("/q What does the moon work", "/"))
    print(command_parse("SIR HOW THIS WORK PLS HELP", "/"))
    print(return_command_output("242323", "faqs", ""))
    print(return_command_output("242323", "hi", ""))
    # print(return_command_output("242323", "hi", ""))