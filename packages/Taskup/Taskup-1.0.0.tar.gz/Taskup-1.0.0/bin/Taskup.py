import sys
from lib.parser import (parse_config)
from src.setup_config import setup_config
from src.run_task import run_task
from src.default_app import default_app
from src.choose_run import choose_run
from src.get_version import get_version

def main():
    config = open("Tasks.json").read()

    tasklist = parse_config(config)

    args = sys.argv.copy()
    # Removing default file name argument
    args.remove("main.py")

    # Default message of the app
    if len(args) == 0:
        default_app()

    # Function to the run a task
    run_task(tasklist, args, config)
    
    # The choose window of the app
    choose_run(args, config, tasklist)

    # Setup task function
    setup_config(args)

    # Get version
    get_version(args)


main()