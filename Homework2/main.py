from setup import (ProbePoint, LinkPoint)
from matching import belongs_to


def get_matched_probes(link):
    '''
    Given a link returns a list of nearby probes.
    :param link: a road link object
    :type link: setup.LinkPoint
    :return: a list of probes that are close to the given link
    :rtype: list[setup.ProbePoint]
    '''
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

def format_map_points(link, probes):
    '''
    For debugging purposes, output can be pasted directly into
    https://www.mapcustomizer.com/ bulk entry
    '''
    probes = '\n'.join(['{},{} <green>'.format(p.latitude, p.longitude)
                        for p in probes])

    link_points = '\n'.join(['{},{} <red>'.format(*link_point.split('/'))
                             for link_point in link.shapeInfo.split('|')])

    return '\n'.join([link_points, probes])


def main():
    for link in LinkPoint.select().limit(5):
        matched_probes = get_matched_probes(link)
        print('Matched {} probes'.format(len(matched_probes)))
        print('START'.center(40, '-'))
        print(format_map_points(link, matched_probes))
        print('END'.center(40, '-'))


if __name__ == '__main__':
    main()