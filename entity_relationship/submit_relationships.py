import requests
import json
import codecs
from time import sleep
import config

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def get_musicbrainz_cookies():
    payload = {
        'action': 'login',
        'username': config.musicbrainz["auth"]["username"],
        'password': config.musicbrainz["auth"]["password"]
    }
    c = requests.session()
    c.post('http://musicbrainz.org/login?uri=%2F', data=payload)
    request = c.get('http://musicbrainz.org/')
    return request.cookies

def init_musicbrainz_relationships(relationships):
    relationships_mb = {}
    relationships_mb["rel-editor.edit_note"] = relationships["rel-editor.edit_note"]
    relationships_mb["rel-editor.as_auto_editor"] = relationships["rel-editor.as_auto_editor"]
    return relationships_mb

def submit_relationships(relationships_mb, cookies):
    url = "http://www.musicbrainz.org/relationship-editor"
    r = requests.post(url, relationships_mb, cookies=COOKIE)
    print r.content
    with open("requests_results.html", "w") as f:
        f.write(r.content)

if __name__ == '__main__':
    
    cookies = get_musicbrainz_cookies()
    relationships = json.load(codecs.open("andalusian_music_catalog__relationships.json", "r", "utf-8"))
    
    for chunk in chunks(relationships["relations"], 20):
        relationships_mb = init_musicbrainz_relationships(relationships)
        for relation in chunk:
            for k,v in relation.items():
                relationships_mb[k]=v
        print len(relationships_mb)
        submit_relationships(relationships_mb, cookies)
        sleep(2.0) #be nice