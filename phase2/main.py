import logging
from phase2.cli import CommandLineInterface


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_preferences():
    
    cli = CommandLineInterface()
    return cli.run()

if __name__ == "__main__":
    get_user_preferences()
