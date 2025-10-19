import argparse

parser = argparse.ArgumentParser(description='Simple Cli Example')
parser.add_argument("name", help="Your Name")
parser.add_argument("--formal", action="store_true")
parser.add_argument("--imformal", action="store_true")

args = parser.parse_args()

print(f"Hello, {args.name}! {'Formal mode.' if args.formal else ("Imformal Mode" if args.imformal else "")} ")