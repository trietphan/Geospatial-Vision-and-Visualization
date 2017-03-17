from setup import (ProbePoint, LinkPoint, MatchedPoint)
from matching import belongs_to
from attributes import (find_directions, create_matched_point, get_updated_link_shape)
from snap import match_probes
from utils import in_chunks


def get_candidate_probes(link):
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

    candidate_probes = ProbePoint.raw(query_text, min_x, min_y, max_x, max_y)

    return candidate_probes.execute()

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
    for link in LinkPoint.select().limit(2):
        candidate_probes = get_candidate_probes(link)
        matched_probes = match_probes(candidate_probes)

        belongs_to_link = belongs_to(link)
        nearby_matched_probes = [p
                                 for p in matched_probes
                                 if belongs_to_link(p)]

        sample_id_to_direction = find_directions(link, matched_probes)
        get_direction = lambda probe: sample_id_to_direction.get(probe.sampleID)
        matched_points = (create_matched_point(link, probe, get_direction)
                          for probe in matched_probes)

        # insert matched points
        insert_at_once = 500
        for chunk in in_chunks(matched_points, insert_at_once):
            MatchedPoint.insert_many(chunk).execute()

        # update slopes
        updated_link_shape = get_updated_link_shape(link, matched_probes)
        link.shapeInfo = updated_link_shape
        link.save()


if __name__ == '__main__':
    main()
