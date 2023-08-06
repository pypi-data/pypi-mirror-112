import urllib.parse

class QuickTask:

    @staticmethod
    def __dictToSneakersURL(raw: dict) -> str:
        '''Convert json to quick task url'''
        res = "sneakersaio://quick-task?"
        paramArr = []
        # Iterate keys in arr
        for key in raw:
            if (raw[key] != None):
                keyValue = key + "="
                if type(raw[key]) == list:
                    # List case, encode all elements in list
                    arr = ([urllib.parse.quote(el, safe="") for el in raw[key]])
                    keyValue += ",".join(arr)
                else:
                    # Normal case, encode current element
                    keyValue += urllib.parse.quote(raw[key], safe="")
                paramArr.append(keyValue)
        # Append & seperated paramArr to res & return
        return res + "&".join(paramArr)

    @staticmethod
    def __getSneakersURL(sites: list, keywords: list, colorKeywords: list,
                    productUrl: str, variant: str, sizeID: str,
                    productNumber: str, size: str, mode: str) -> str:
        '''Return quick task url given parameters'''
        dict = {
            "sites": sites,
            "keywords": keywords,
            "color_keywords": colorKeywords,
            "product_url": productUrl,
            "variant": variant,
            "size_id": sizeID,
            "product_number": productNumber,
            "size": size,
            "mode": mode
        }
        return QuickTask.__dictToSneakersURL(dict)

    @staticmethod
    def createKeywordsTask(sites: list, keywords: list, colorKeywords: list = [],
                        size: str = "User Shoe", mode: str = "safe"):
        '''
        Creates a Sneakers AIO Quick Task URL using the keywords search type.

        @param sites: Array of website URLs to create tasks for. These should be
        for the base url of the site (no path or query). All sites must be of the same type
        (ie. all Shopify or all Footsites).

        @param keywords: Array of keywords to search for. Negative keywords
        begin with -

        @param colorKeywords: Array of color keywords to search for. Negative keywords
        begin with -

        @param size: The size of the product. Special size types include: "Any Size", 
        "One Size", "User Shoe" & "User Clothing". Default: "User Shoe"

        @param mode: The bot mode. Shopify modes include "Safe", "Quick", "Queue", & "Input".
        Footsites modes include "Safe" & "Release".
        There may be more modes.
        Default: "Safe"

        @return: Sneakers AIO Quick Task URL
        '''
        return QuickTask.__getSneakersURL(sites, keywords, colorKeywords, None, None,
                            None, None, size, mode)

    @staticmethod
    def createProductUrlTask(site: str, productUrl: str, colorKeywords: list = [],
                            size: str = "User Shoe", mode: str = "safe"):
        '''
        Creates a Sneakers AIO Quick Task URL using the product URL search type.

        @param site: Website URL to create the task for. This should be
        for the base url of the site (no path or query).

        @param productUrl: Full url of the product to purchase (w/ path).

        @param colorKeywords: Vector of color keywords to search for. Negative keywords
        begin with -

        @param size: The size of the product. Special size types include: "Any Size", 
        "One Size", "User Shoe" & "User Clothing". Default: "User Shoe"

        @param mode: The bot mode. Shopify modes include "Safe", "Quick", "Queue", & "Input".
        Footsites modes include "Safe" & "Release".
        There may be more modes.
        Default: "Safe"

        @return: Sneakers AIO Quick Task URL
        '''
        return QuickTask.__getSneakersURL([site], None, colorKeywords, productUrl, None,
                            None, None, size, mode)

    @staticmethod
    def createVariantTask(site: str, variant: str, mode: str = "safe"):
        '''
        Creates a Sneakers AIO Quick Task URL using the product URL search type.

        @param site: Website URL (Shopify only) to create the task for. This should be
        for the base url of the site (no path or query).

        @param variant: Variant of the product to purchase.

        @param mode: The bot mode. Shopify modes include "Safe", "Quick", "Queue", & "Input".
        There may be more modes.
        Default: "Safe"

        @return: Sneakers AIO Quick Task URL
        '''
        return QuickTask.__getSneakersURL([site], None, None, None, variant,
                            None, None, None, mode)

    @staticmethod
    def createSizeIDTask(site: str, sizeID: str, mode: str = "safe"):
        '''
        Creates a Sneakers AIO Quick Task URL using the product URL search type.

        @param site: Website URL (Footsites only) to create the task for. This should be
        for the base url of the site (no path or query).

        @param sizeID: Size ID of the product to purchase (ID used for carting the product).

        @param mode: The bot mode. Footsites modes include "Safe" & "Release".
        There may be more modes.
        Default: "Safe"

        @return: Sneakers AIO Quick Task URL
        '''
        return QuickTask.__getSneakersURL([site], None, None, None, None,
                            sizeID, None, None, mode)

    @staticmethod
    def createProductNumberTask(site: str, productNumber: str, colorKeywords: list = [],
                                size: str = "User Shoe", mode: str = "safe"):
        '''
        Creates a Sneakers AIO Quick Task URL using the product URL search type.

        @param site: Website URL (Footsites only) to create the task for. This should be
        for the base url of the site (no path or query).

        @param productNumber: Product Number of product to find. Can be found in the
        product url. Ie. the product number for
        https://www.footlocker.ca/en/product/jordan-retro-3-mens/48818677.html
        is 48818677.

        @param colorKeywords: Vector of color keywords to search for. Negative keywords
        begin with -

        @param size: The size of the product. Special size types include: "Any Size", 
        "One Size", "User Shoe" & "User Clothing". Default: "User Shoe"

        @param mode: The bot mode. Shopify modes include "Safe", "Quick", "Queue", & "Input".
        Footsites modes include "Safe" & "Release".
        There may be more modes.
        Default: "Safe"

        @return: Sneakers AIO Quick Task URL
        '''
        return QuickTask.__getSneakersURL(site, None, colorKeywords, None, None,
                            None, productNumber, size, mode)
