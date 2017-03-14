from setup import (ProbePoint, LinkPoint)
from matching import belongs_to


def get_matched_probes(link):
    tolerance = 10
    (min_x, min_y) = (link.minX, link.minY)
    (max_x, max_y) = (link.maxX, link.maxY)

    # using raw query here because it's considerably faster
    query_text = '''
    SELECT * FROM probepoint
    WHERE x > ? - {tolerance} AND
          y > ? - {tolerance} AND
          x < ? + {tolerance} AND
          y < ? + {tolerance}
    '''.format(tolerance=tolerance)

    candidate_points = ProbePoint.raw(query_text, min_x, min_y, max_x, max_y)

    belongs_to_link = belongs_to(link)

    matched_probe_points = [p
                            for p in candidate_points.execute()
                            if belongs_to_link(p)]

    return matched_probe_points

def main():
    for link in LinkPoint.select().limit(2):
        print(link.shapeInfo)
        matched_probes = get_matched_probes(link)
        print('matched', len(matched_probes), 'probes')

if __name__ == '__main__':
    main()
