import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Gitlab projects info')

    parser.add_argument('--output', type=str, required=False,
                        help='Output format')
    parser.add_argument('--activity', type=bool, required=False,
                        default=False, help='Show last activity dates')
    parser.add_argument('--since', type=int, required=False,
                        default=30, help='Show projects with activity since N days ago')

    return parser.parse_args()
