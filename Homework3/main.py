from centers import find_centers

def main():
    latlon1 = (41.835095, -87.628891)
    latlon2 = (41.836216, -87.627802)

    centers = find_centers(latlon1, latlon2)

    print(centers)

if __name__ == '__main__':
    main()
