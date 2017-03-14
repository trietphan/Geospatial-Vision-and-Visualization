from setup import (ProbePoint, LinkPoint)
from matching import belongs_to


def match_probes_to_links():
    for link in LinkPoint.select().limit(200):
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

        matched_points = [p
                          for p in candidate_points.execute()
                          if belongs_to_link(p)]

        print('matched', len(matched_points), 'points')

def main():
    match_probes_to_links()

if __name__ == '__main__':
    main()
