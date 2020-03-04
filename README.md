[![licence](http://img.shields.io/badge/licence-MIT-blue.svg?style=flat)](https://github.com/1997alireza/Persian-Telegram-WordCloud/blob/master/LICENSE)

# Persian Telegram WordCloud

You can make the word cloud of the messages of your chat with your friend or a group of which you are a member. Or you can see which words a channel uses most.

Use Python 3.6+.

## Example

The word cloud of the channel `@mamlekate`

<p align="center">
<img src="https://raw.githubusercontent.com/1997alireza/Persian-Telegram-WordCloud/master/mamlekate.png" alt="" width="75%"/>
</p>


## Installation


First install the packages

    sh setup.sh

Then you need to get your own Telegram API ID and hash:

1. [Login to your Telegram account](https://my.telegram.org/) with the phone number of the developer account to use.
2. Click under API Development tools.
3. A Create new application window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
4. Click on Create application at the end.


## Usage

Edit and configure `config.json`. ([How?](#Configuration))

Run the main file to get your word cloud:

    python3 main.py


## Configuration

First the configuration file is as follows:
```json5
{
	"api_id": 12345,
	"api_hash": "<api_hash>",
	"phone_number": "<phone_number>",

	"dialogs_name": ["<dialog name>"],
	"target_identifier": "<phone_number> | @<username> | me | ",

	"crawl_all_of_dialog": false,
	"max_dialog_count": 20,
	"ignore_english_characters": true,

	"color_map": "PuBu",
	"background_color": "black"
}
```
<br>

- Fill in "api_id", "api_hash" and "phone_number" using your Telegram account details.

```json5
"api_id": 12345,
"api_hash": "################################",
"phone_number": "+980000000000",
```
<br>

- If you want to crawl several selected channels, groups or private chats, write their names (not their IDs) in the "dialogs_name" array. 
<br>If you leave the array empty the program crawls your first "max_dialog_count" groups and private chats.

```json5
"dialogs_name": ["Pavel Durov", "BBCPersian"],
```
or
```json5
"dialogs_name": [],
```
<br>

- If you want to crawl the messages from only one account, fill in "target_identifier" with the account's phone number or ID. If the target is yourself, you can just write "me" instead of your identifier.
<br>If you leave it empty, the messages from all senders will be crawled.

```json5
"target_identifier": "+980000000000",
```
or
```json5
"target_identifier": "@username",
```
or
```json5
"target_identifier": "me",
```
or
```json5
"target_identifier": "",
```

### More Options
- Only a limited number of messages per each dialog are crawled. Set "crawl_all_of_dialog" to true to crawl all of the messages in each dialog. It takes more time.
- "max_dialog_count" is the number of dialogs that are crawled when the "dialogs_name" array is empty.
- Set "ignore_english_characters" to false to not ignore the English characters in the messages.
- To change the color of texts and background of the word cloud use "color_map" and "background_color" parameters.
