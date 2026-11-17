import zipfile,xml.etree.ElementTree as E,json,pathlib,collections
out=pathlib.Path('C:/Users/Administrator/.agents/skills/danbaosi/references/sources')
z=zipfile.ZipFile(out/'original.docx'); ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W='{'+ns['w']+'}'
rels={e.attrib['Id']:e.attrib.get('Target') for e in E.fromstring(z.read('word/_rels/document.xml.rels'))}
root=E.fromstring(z.read('word/document.xml')); records=[]
for i,p in enumerate(root.iter(W+'p'),1):
 text=''.join(e.text or '' for e in p.iter() if e.tag in [W+'t',W+'delText'])
 style=p.find('w:pPr/w:pStyle',ns)
 imgs=[rels.get(e.attrib.get('{'+ns['r']+'}embed','')) for e in p.findall('.//a:blip',ns)]
 records.append({'id':f'P{i:04d}','style':style.attrib.get(W+'val') if style is not None else '', 'text':text,'images':imgs})
(out/'paragraphs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
(out/'fulltext.md').write_text('\n\n'.join('['+p['id']+'] '+p['text']+(' [MEDIA: '+','.join(str(x) for x in p['images'])+']' if p['images'] else '') for p in records),encoding='utf8')
media=out/'media';media.mkdir(exist_ok=True)
for n in z.namelist():
 if n.startswith('word/media/'): (media/pathlib.Path(n).name).write_bytes(z.read(n))
report={'entries':z.namelist(),'paragraphs':len(records),'text_characters':sum(len(p['text']) for p in records),'styles':dict(collections.Counter(p['style'] for p in records)),'tables':len(root.findall('.//w:tbl',ns)),'textboxes':len(root.findall('.//w:txbxContent',ns)),'tracked_insertions':len(root.findall('.//w:ins',ns)),'tracked_deletions':len(root.findall('.//w:del',ns)),'hyperlinks':len(root.findall('.//w:hyperlink',ns))}
(out/'package-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2)); print('\n'.join(f"{p['id']} style={p['style']} {p['text'][:150]}" for p in records[:45]))
