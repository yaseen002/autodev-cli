import argparse

parser = argparse.ArgumentParser(description='Simple CLI example')
parser.add_argument('name', help='Your name')  # Positional
parser.add_argument('--formal', action='store_true', help="Formal Mode")  # Flag

args = parser.parse_args()
print(f"Hello, {args.name}! {'Formal mode.' if args.formal else ''}")