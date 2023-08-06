# Sneakers AIO Quick Task Generator

A simple API for generating [Sneakers AIO Quick Task URLs.](https://sneakersaio.com/docs-api)

## Installation

-----

Using pip:

```bash
$ pip install sneakers-quick-task
```

In Python:

```javascript
from sneakersaio import QuickTask
```

## Usage

------

```python
# Create keywords task: sneakersaio://quick-task?sites=https%3A%2F%2Fkith.com,https%3A%2F%2Fwww.deadstock.ca&keywords=yeezy,350,-kid,-infant&color_keywords=&size=any%20size&mode=queue
quickTaskUrl = QuickTask.createKeywordsTask(["https://kith.com", "https://www.deadstock.ca"], ["yeezy", "350", "-kid", "-infant"], [], "any size", "queue");

# Create product url task: sneakersaio://quick-task?sites=https%3A%2F%2Fkith.com&color_keywords=white,red&product_url=https%3A%2F%2Fkith.com%2Fcollections%2Fkith-monday-program%2Fproducts%2Fkh2636-101&size=Medium&mode=safe
quickTaskUrl = QuickTask.createProductUrlTask("https://kith.com", "https://kith.com/collections/kith-monday-program/products/kh2636-101", ["white", "red"], "Medium");

# Create variant task: sneakersaio://quick-task?sites=https%3A%2F%2Fkith.com&variant=39246354940032&mode=safe
quickTaskUrl = QuickTask.createVariantTask("https://kith.com", "39246354940032");

# Create size id task: sneakersaio://quick-task?sites=https%3A%2F%2Fwww.footlocker.ca&size_id=22661425&mode=safe
quickTaskUrl = QuickTask.createSizeIDTask("https://www.footlocker.ca", "22661425");

# Create product number task: sneakersaio://quick-task?sites=https%3A%2F%2Fwww.footlocker.ca&color_keywords=white,red,-yellow&product_number=41047318&size=User%20Shoe&mode=safe
quickTaskUrl = QuickTask.createProductNumberTask("https://www.footlocker.ca", "41047318", ["white", "red", "-yellow"], "User Shoe")
```

## Documentation

-----

### Static methods

`createKeywordsTask(sites: list, keywords: list, colorKeywords: list = [], size: str = 'User Shoe', mode: str = 'safe') -> str`
:   Creates a Sneakers AIO Quick Task URL using the keywords search type.

**Returns**: `str` - Sneakers AIO Quick Task URL

| Param         | Type    | Default     | Description                                                                                                                                                                        |
| ------------- | ------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sites         | `[str]` |             | Array of website URLs to create tasks for. These should be for the base url of the site (no path or query). All sites must be of the same type (ie. all Shopify or all Footsites). |
| keywords      | `[str]` |             | Array of keywords to search for. Negative keywords begin with -                                                                                                                    |
| colorKeywords | `[str]` |             | Array of color keywords to search for. Negative keywords begin with -                                                                                                              |
| size          | `str`   | `User Shoe` | The size of the product. Special size types include: `"Any Size"`,` "One Size"`, `"User Shoe"` & `"User Clothing"`.                                                                |
| mode          | `str`   | `safe`      | The bot mode. Shopify modes include `"Safe"`, `"Quick"`, `"Queue"`, & `"Input"`. Footsites modes include `"Safe"` & `"Release"`. There may be more modes.                          |

`createProductUrlTask(site: str, productUrl: str, colorKeywords: list = [], size: str = 'User Shoe', mode: str = 'safe') -> str`
:   Creates a Sneakers AIO Quick Task URL using the product URL search type.

**Returns**: `str` - Sneakers AIO Quick Task URL

| Param         | Type    | Default     | Description                                                                                                                                               |
| ------------- | ------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| site          | `str`   |             | Website URL to create the task for. This should be for the base url of the site (no path or query).                                                       |
| productUrl    | `str`   |             | Full url of the product to purchase (w/ path).                                                                                                            |
| colorKeywords | `[str]` |             | Vector of color keywords to search for. Negative keywords begin with -                                                                                    |
| size          | `str`   | `User Shoe` | The size of the product. Special size types include: `"Any Size"`,` "One Size"`, `"User Shoe"` & `"User Clothing"`.                                       |
| mode          | `str`   | `safe`      | The bot mode. Shopify modes include `"Safe"`, `"Quick"`, `"Queue"`, & `"Input"`. Footsites modes include `"Safe"` & `"Release"`. There may be more modes. |

`createProductNumberTask(site: str, productNumber: str, colorKeywords: list = [], size: str = 'User Shoe', mode: str = 'safe') -> str`
:   Creates a Sneakers AIO Quick Task URL using the product URL search type.

**Returns**: `str` - Sneakers AIO Quick Task URL

| Param         | Type     | Default     | Description                                                                                                                                                                                                                                                  |
| ------------- | -------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| site          | `str`    |             | Website URL (Footsites only) to create the task for. This should be for the base url of the site (no path or query).                                                                                                                                         |
| productNumber | `str`    |             | Product Number of product to find. Can be found in the product url. Ie. the product number for [https://www.footlocker.ca/en/product/jordan-retro-3-mens/48818677.html](https://www.footlocker.ca/en/product/jordan-retro-3-mens/48818677.html) is 48818677. |
| colorKeywords | `[str]`  |             | Vector of color keywords to search for. Negative keywords begin with -                                                                                                                                                                                       |
| size          | `str`    | `User Shoe` | The size of the product. Special size types include: `"Any Size"`,` "One Size"`, `"User Shoe"` & `"User Clothing"`.                                                                                                                                          |
| mode          | `String` | `safe`      | The bot mode. Footsites modes include `"Safe"` & `"Release"`. There may be more modes.                                                                                                                                                                       |

`createSizeIDTask(site: str, sizeID: str, mode: str = 'safe') -> str`
:   Creates a Sneakers AIO Quick Task URL using the product URL search type.

**Returns**: `str` - Sneakers AIO Quick Task URL

| Param  | Type  | Default | Description                                                                                                          |
| ------ | ----- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| site   | `str` |         | Website URL (Footsites only) to create the task for. This should be for the base url of the site (no path or query). |
| sizeID | `str` |         | Size ID of the product to purchase (ID used for carting the product).                                                |
| mode   | `str` | `safe`  | The bot mode. Footsites modes include `"Safe"` & `"Release"`. There may be more modes.                               |

`createVariantTask(site: str, variant: str, mode: str = 'safe') -> str`
:   Creates a Sneakers AIO Quick Task URL using the product URL search type.

**Returns**: `str` - Sneakers AIO Quick Task URL

| Param   | Type  | Default | Description                                                                                                        |
| ------- | ----- | ------- | ------------------------------------------------------------------------------------------------------------------ |
| site    | `str` |         | Website URL (Shopify only) to create the task for. This should be for the base url of the site (no path or query). |
| variant | `str` |         | Variant of the product to purchase.                                                                                |
| mode    | `str` | `safe`  | The bot mode. Shopify modes include `"Safe"`, `"Quick"`, `"Queue"`, & `"Input"`. There may be more modes.          |
