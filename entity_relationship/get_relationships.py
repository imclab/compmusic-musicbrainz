import codecs, json
import config

def get_items(header):
    items = {}
    artists, instruments = [], []
    for i in range(len(header)):
        if header[i] in ("album_title", "musical_form", "mizan", "tab", "album_mbid", "recording_mbid"):
            items[header[i]] = i
        elif header[i].startswith("instrument"):
            instruments.append(i)
        elif header[i].startswith("artist"):
            artists.append(i)
    items["artists_instruments"] = zip(artists, instruments)
    return items

def get_instrument_relationship_editor(entity_mbid0, entity_mbid1, instrument_id, index=0):
    rel_editor = {}
    index = str(index)
    rel_editor['rel-editor.rels.'+index+'.action'] = "add"
    rel_editor['rel-editor.rels.'+index+'.attrs.instrument.0'] = instrument_id
    rel_editor['rel-editor.rels.'+index+'.entity.0.gid'] = entity_mbid0
    rel_editor['rel-editor.rels.'+index+'.entity.0.type'] = "artist"
    rel_editor['rel-editor.rels.'+index+'.entity.1.gid'] = entity_mbid1
    rel_editor['rel-editor.rels.'+index+'.entity.1.type'] = "recording"
    rel_editor['rel-editor.rels.'+index+'.link_type'] = 148
    rel_editor['rel-editor.rels.'+index+'.period.ended'] = 0
    return rel_editor

def get_vocals_relationship_editor(entity_mbid0, entity_mbid1, vocals_id=4, index=0):
    rel_editor = {}
    index = str(index)
    rel_editor['rel-editor.rels.'+index+'.action'] = "add"
    rel_editor['rel-editor.rels.'+index+'.attrs.additional'] = 0
    rel_editor['rel-editor.rels.'+index+'.attrs.guest'] = 0
    rel_editor['rel-editor.rels.'+index+'.attrs.solo'] = 0
    rel_editor['rel-editor.rels.'+index+'.attrs.vocal.0'] = vocals_id
    rel_editor['rel-editor.rels.'+index+'.entity.0.gid'] = entity_mbid0
    rel_editor['rel-editor.rels.'+index+'.entity.0.type'] = "artist"
    rel_editor['rel-editor.rels.'+index+'.entity.1.gid'] = entity_mbid1
    rel_editor['rel-editor.rels.'+index+'.entity.1.type'] = "recording"
    rel_editor['rel-editor.rels.'+index+'.link_type'] = 149
    rel_editor['rel-editor.rels.'+index+'.period.ended'] = 0
    return rel_editor
    
if __name__ == '__main__':
    # Load instruments
    f = codecs.open("andalusian_music_catalog__instruments.csv", "r", "utf-8")
    instruments = {}
    first_line = True
    for line in f:
        if first_line: first_line = False
        else:
            instrument, _, mbid = line.strip().split(",")
            if len(mbid) > 0:
                instruments[instrument] = int(mbid)
                
    f.close()

    
    # Load artists
    f = codecs.open("andalusian_music_catalog__artists.csv", "r", "utf-8")
    artists = {}
    for line in f:
        mbid, artist = line.strip().split(",")
        if len(mbid) > 0:
            artists[artist] = mbid
    f.close()
    
    f = codecs.open("andalusian_music_catalog.csv", "r", "utf-8")
    items = {}
    first_line = True
    i = -1
    j = 0
    relationships = {"rel-editor.as_auto_editor": 0, "rel-editor.edit_note": "Adding artist-recording relationships to the recordings of the Tetouan Orchestra", "relations": []}
    cur_album_id = ""
    for line in f:
        data = line.strip().split(",")
        if first_line:
            header = data
            items = get_items(header)
            first_line = False
        elif len(data[items["recording_mbid"]]) > 0:
            if cur_album_id != data[items["album_mbid"]]:
                cur_album_id = data[items["album_mbid"]]
                i += 1
            for id_art, id_instr in items["artists_instruments"]:
                artist = data[id_art]
                instrument = data[id_instr]
                if artists.has_key(artist) and instruments.has_key(instrument):
                    print data[items["recording_mbid"]], data[items["mizan"]], data[items["tab"]], artist, instrument
                    if instruments[instrument] == 4:
                        rel_editor = get_vocals_relationship_editor(artists[artist], data[items["recording_mbid"]], instruments[instrument], j)
                    else:
                        rel_editor = get_instrument_relationship_editor(artists[artist], data[items["recording_mbid"]], instruments[instrument], j)
                    relationships["relations"].append(rel_editor)
                    j += 1
    f.close()
    
    json.dump(relationships, codecs.open("andalusian_music_catalog__relationships.json", "w", "utf-8"))