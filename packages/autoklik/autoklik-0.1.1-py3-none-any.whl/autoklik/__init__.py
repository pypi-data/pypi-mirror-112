"""Auto clicker built around xdotool.

If window-name and window-id isn't given
you will be asked to select the window to send clicks to using your mouse.
"""

import argparse
import logging
import subprocess
import time


CLICK_NAMES = {"1": "left click", "2": "middle click", "3": "right click"}


def setup_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-t",
        "--type",
        choices=["1", "2", "3"],
        default="1",
        help="""The type of click to send. 1 is left click,
                2 is middle click and 3 is right click.""",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=1000,
        help="The interval between clicks in ms.",
    )
    parser.add_argument(
        "-w",
        "--window-name",
        help="""The name of the window to send clicks to. A search will be made using
                the provided text and a selection screen shown if there are
                multiple choices.""",
    )
    parser.add_argument(
        "-W", "--window-id", help="The id of the window to send clicks to."
    )
    parser.add_argument(
        "-f",
        "--ignore-when-focused",
        action="store_true",
        help="Don't send clicks to the select window when that window is focused.",
    )
    return parser


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.WARNING)
    parser = setup_arguments()
    args = parser.parse_args()

    logging.debug(args)

    if args.window_id:
        window = {
            "window_id": args.window_id,
            "window_name": get_window_name_from_id(args.window_id),
        }
    elif args.window_name:
        window_id = get_window_id_from_name(args.window_name)
        window = {
            "window_id": window_id,
            "window_name": get_window_name_from_id(window_id),
        }
    else:
        window = select_window()

    click = {"click_id": args.type, "click_name": CLICK_NAMES[args.type]}

    do_click(window, click, args.interval, args.ignore_when_focused)


def select_window():
    print("Please select a window")
    window_id = (
        subprocess.run(["xdotool", "selectwindow"], capture_output=True)
        .stdout.strip()
        .decode("UTF-8")
    )

    window_name = get_window_name_from_id(window_id)

    print(f"You have selected: {window_name}")

    while True:
        answer = input("Is this the correct window (yes/no):")
        if answer == "yes" or answer == "no":
            break
        else:
            print("Please provide a yes or no answer.")

    if answer == "yes":
        return {"window_id": window_id, "window_name": window_name}
    else:
        select_window()


def get_window_id_from_name(window_name):
    """Get the window id from the name of a window.

    If the name matches multiple windows, the user will be presented with the names
    of all the matched window to pick the one they want.
    """
    output = (
        subprocess.run(
            ["xdotool", "search", "--name", window_name], capture_output=True
        )
        .stdout.strip()
        .decode("UTF-8")
        .split("\n")
    )
    if len(output) == 1:
        return output[0]

    print("Multiple windows match the name:\n")
    i = 0
    for window in output:
        print(f"    {i}. {get_window_name_from_id(window)}")
        i += 1
    selected_window = int(input("\nPlease pick the desired window: "))

    return output[selected_window]


def get_window_name_from_id(window_id):
    """
    Gets the name of of a window using the window id.
    """
    return (
        subprocess.run(["xdotool", "getwindowname", window_id], capture_output=True)
        .stdout.strip()
        .decode("UTF-8")
    )


def do_click(window, click, interval, ignore_when_focused):
    print(
        f"Sending {click['click_name']}s every {interval}ms to {window['window_name']}"
    )

    interval = interval / 1000
    next_time = time.time() + interval

    while True:
        time.sleep(max(0, next_time - time.time()))

        if ignore_when_focused:
            active_window = (
                subprocess.run(["xdotool", "getactivewindow"], capture_output=True)
                .stdout.strip()
                .decode("UTF-8")
            )

            logging.debug(f"active window id: {active_window}")
            logging.debug(f"sending clicks to window id: {window['window_id']}")

            if active_window == window["window_id"]:
                next_time += (time.time() - next_time) // interval * interval + interval
                logging.info("click skipped")
                continue

        send_click(window, click)
        next_time += (time.time() - next_time) // interval * interval + interval


def send_click(window, click):
    # Send mouse down and up separately to prevent wrong mouse inputs from being
    # sent when those inputs are press on the actual mouse at the same time a click
    # event is sent
    subprocess.run(
        ["xdotool", "mousedown", "--window", window["window_id"], click["click_id"]]
    )
    subprocess.run(
        ["xdotool", "mouseup", "--window", window["window_id"], click["click_id"]]
    )
    logging.info(f"{click['click_name']} sent")


if __name__ == "__main__":
    main()
