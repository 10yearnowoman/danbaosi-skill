import pathlib,json,re
out=pathlib.Path(__file__).parent
p=json.loads((out/'paragraphs.json').read_text(encoding='utf8')); articles=[]
for r in p:
 if (r['style']=='shimo heading 1' and re.match(r'^\d+',r['text'])) or not articles: articles.append({'id':f'A{len(articles)+1:02d}','title':r['text'],'paragraphs':[]})
 articles[-1]['paragraphs'].append(r)
d=out/'articles';d.mkdir(exist_ok=True)
for a in articles:
 (d/(a['id']+'.md')).write_text('# '+a['id']+' '+a['title']+'\n\n'+'\n\n'.join('['+r['id']+'] '+r['text']+(' [MEDIA '+str(r['images'])+']' if r['images'] else '') for r in a['paragraphs']),encoding='utf8')
index=[{'id':a['id'],'title':a['title'],'start':a['paragraphs'][0]['id'],'end':a['paragraphs'][-1]['id'],'characters':sum(len(r['text']) for r in a['paragraphs'])} for a in articles]
(out/'article-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(index,ensure_ascii=False,indent=2))

