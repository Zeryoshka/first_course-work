import os


def return_auctions_list():
    folder = 'app/auction_module/auctions'

    directory = os.fsencode(folder)
    auctions_list = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            auctions_list.append(folder+filename)

    return auctions_list
