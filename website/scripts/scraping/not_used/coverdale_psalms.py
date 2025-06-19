from webpage_psalms import scrape_webpage, write_to_file


def main():
    psalm_content = scrape_webpage("http://justus.anglican.org/resources/bcp/1928/Psalms1.htm")

    print(psalm_content)

    # Writing content to a txt file
    write_to_file(psalm_content, "../../Psalms Raw/txt/coverdale.txt")


if __name__ == "__main__":
    main()