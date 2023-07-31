def make_comparisons(scrapy_urls, scrutiny_urls):
    urls_missing_in_scrapy_urls = scrutiny_urls - scrapy_urls

    # Find the urls that are in group 2 but missing in group 1
    urls_missing_in_scrutiny_urls = scrapy_urls - scrutiny_urls

    # Find the urls that are in both groups
    urls_in_common = scrutiny_urls & scrapy_urls

    return (urls_missing_in_scrapy_urls, urls_missing_in_scrutiny_urls, urls_in_common)
    
    '''
    # Print the number of urls in each group
    with open("results.txt", "w") as file:
        print('___________________________________________\n' + text_gaps[i] + ' results:')
        print('Number of urls in scrutiny:' + str(len(scrutiny_urls)))
        print('Number of urls in scrapy:' + str(len(scrapy_urls)))
        print('Urls in common:' + str(len(urls_in_common)))

        # print the urls that are in group 1 but missing in group 2
        print('Urls missing in scrutiny:' + str(len(urls_missing_in_scrutiny_urls)))
        print('Urls missing in scrapy:' + str(len(urls_missing_in_scrapy_urls)))
        for url in urls_missing_in_scrutiny_urls:
            print(url)

        # Print the urls that are in group 2 but missing in group 1
        print('Urls missing in scrapy_urls:')
        #print (len(urls_missing_in_scrapy_urls))
        for url in urls_missing_in_scrapy_urls:
            print(url)

        # Print the urls that are in both groups
        print('Urls in common:')
        #print (len(urls_in_common))
        for url in urls_in_common:
            print(url)
            '''
    file.close()