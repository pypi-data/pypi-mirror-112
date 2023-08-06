API_BASE_URL = 'https://api.waifu.pics'

TYPES = {'sfw', 'nsfw'}

SFW_CATEGORIES = {
    'awoo',
    'bite',
    'blush',
    'bonk',
    'bully',
    'cringe',
    'cry',
    'cuddle',
    'dance',
    'glomp',
    'handhold',
    'happy',
    'highfive',
    'hug',
    'kill',
    'kiss',
    'lick',
    'megumin',
    'neko',
    'nom',
    'pat',
    'poke',
    'shinobu',
    'slap',
    'smile',
    'smug',
    'waifu',
    'wave',
    'wink',
    'yeet'
}

NSFW_CATEGORIES = {'blowjob', 'neko', 'trap', 'waifu'}

CATEGORY = {
    'sfw': SFW_CATEGORIES,
    'nsfw': NSFW_CATEGORIES,
}

HELP_TEXT = f"""
waifu help                  shows this message
waifu                       open a random sfw image on your browser
waifu [type] [category]     open an image from a particular type and category

Valid types:
    sfw, nsfw

Valid sfw categories:
    {', '.join(SFW_CATEGORIES)}

Valid nsfw categories:
    {', '.join(NSFW_CATEGORIES)}
"""

HELP_MSG = 'Run "waifu help" to get usage information.'
