from argparse import ArgumentParser
from main import run


def create_parser():
    parser = ArgumentParser()

    parser.add_argument('lat1', type=float, help='Latitude of the southwest point')
    parser.add_argument('lon1', type=float, help='Longitude of the southwest point')
    parser.add_argument('lat2', type=float, help='Latitude of the northeast point')
    parser.add_argument('lon2', type=float, help='Longitude of the northeast point')
    parser.add_argument('output', type=str, help='Path to the output file')

    return parser

def get_args():
    parser = create_parser()
    return parser.parse_args()

def main():
    args = get_args()
    latlon1 = (args.lat1, args.lon1)
    latlon2 = (args.lat2, args.lon2)
    output_path = args.output

    run(latlon1, latlon2, output_path)


if __name__ == '__main__':
    main()
