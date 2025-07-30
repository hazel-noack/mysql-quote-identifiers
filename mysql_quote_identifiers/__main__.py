import argparse
import logging


def cli():
    parser = argparse.ArgumentParser(
        description="The python mysql connector has no way to safely quote identifiers like table names or database names. This library implements basic functions to do that.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Sets the logging level to debug."
    )

    args = parser.parse_args()

    # Configure logging based on the debug flag
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.debug("Debug logging enabled")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )


if __name__ == "__main__":
    cli()
