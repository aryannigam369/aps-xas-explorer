"""Parse SPEC blocks without executing the beamline's macros."""
from pathlib import Path
import json, re, hashlib, math, argparse
from datetime import datetime, timezone

def parse(root):
    inventory, spectra, catalog, files = [], [], [], []
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.name.startswith('.'): continue
        rel = str(path.relative_to(root)); text = path.read_text(errors='replace')
        files.append({'file':rel, 'bytes':path.stat().st_size, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        current = None; header = ''; blocks=[]
        for line in text.splitlines():
            if line.startswith('#F '): header=line[3:]
            elif line.startswith('#S '):
                bits=line[3:].split(maxsplit=1)
                current={'number':bits[0], 'command':bits[1] if len(bits)>1 else '', 'headerFile':header,'columns':[], 'data':[], 'edge':None,'date':'','comments':[]}
                blocks.append(current)
            elif current is not None:
                if line.startswith('#L '): current['columns']=line[3:].split()
                elif line.startswith('#N '): current['declared']=int(line[3:])
                elif line.startswith('#D '): current['date']=line[3:]
                elif line.startswith('#C exafs_edge_energy '): current['edge']=float(line.split()[-1])*1000
                elif line.startswith('#C '): current['comments'].append(line[3:])
                elif line.strip() and not line.startswith('#'):
                    try: values=[float(x) for x in line.split()]
                    except ValueError: continue
                    if not current['columns']: raise ValueError(f'{rel}: data before columns')
                    if len(values)!=len(current['columns']): raise ValueError(f'{rel}: malformed row')
                    if not all(math.isfinite(v) for v in values): raise ValueError(f'{rel}: nonfinite row')
                    current['data'].append(values)
        for bi,b in enumerate(blocks):
            cols=b['columns']; rows=b['data'];
            if 'declared' in b and b['declared']!=len(cols): raise ValueError(f'{rel}: #N/#L disagreement')
            main=path.parent.name in ['J14','T1','T20'] and b['command'].strip()=='exafsscan'
            match=re.match(r'(J14|T1|T20)_([A-Za-z]+)\s*(.*?)\s*\.(\d+)$',path.name)
            sample,element,label= (match[1],match[2],match[3].strip()) if match else ('Setup','—','—')
            sid=f'{path.parent.name}-{path.name}-{bi+1}'.replace(' ','_')
            row={'id':sid,'file':rel,'sample':sample,'element':element,'label':label,'scanNumber':b['number'],'command':b['command'],'headerFile':b['headerFile'],'date':b['date'],'points':len(rows),'channels':len(cols),'edgeEv':b['edge'],'scope':'Main spectroscopy' if main else 'Supplementary / setup','notes':'; '.join(b['comments'])}
            inventory.append(row)
            if not main: continue
            if cols[0]!='Energy': raise ValueError('Main scan has no Energy')
            E=[r[0]*1000 for r in rows]
            flags=[]
            if not b['headerFile'].startswith(sample): flags.append('Folder/header sample conflict')
            if sample=='J14' and element=='Ni' and label=='b': flags.append('Repeated filename label b')
            if len(blocks)>1: flags.append('Additional alignment block in source file')
            if any(y<=x for x,y in zip(E,E[1:])): flags.append('Non-increasing energy')
            z=dict(row,energyMin=min(E),energyMax=max(E),flags='; '.join(flags) or 'No structural flags',sha256=files[-1]['sha256'])
            catalog.append(z)
            for i,raw in enumerate(rows):
                d=dict(zip(cols,raw)); i0=d['i0']
                spectra.append({'scanId':sid,'sample':sample,'element':element,'point':i+1,'energyEv':round(E[i],6),'relativeEv':round(E[i]-b['edge'],6),'mu01':d['mu01'],'mu12':d['mu12'],'mu23':d['mu23'],'fluoA':d['flatot']/i0 if i0>0 else None,'fluoB':d['flbtot']/i0 if i0>0 else None,'i0':i0,'flatot':d['flatot'],'flbtot':d['flbtot'],'seconds':d['Seconds']})
    return catalog,spectra,inventory,files

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('output'); args=ap.parse_args()
    root=Path(args.input); cat,spec,inv,files=parse(root)
    source={'label':'Supplied SPEC beamline files · GUP38672_2014-2_12-BM','files':[f['file'] for f in files],'dateRange':'July 28, 2014 (SPEC #D headers; timezone unspecified)','freshness':'Historical acquisition, not live data','caveats':['Sample identities follow folder and filename; three J14 Cu headers say T20_Cu.','Filename labels a/b/c are preserved; their experimental meaning is not documented.','No spatial coordinate grid or sample descriptions supplied.','Raw channels and simple fluorescence/I0 ratios are not edge-step normalized, calibrated, or fitted.','Acquisition date uses #D; #E timestamp is inconsistent and is not used.'],'evidenceFlow':[{'title':'Read original files','detail':'Parse each #S block independently; split #L column labels and require every numeric row to match. Do not execute macros.'},{'title':'Select main spectra','detail':'Select exafsscan blocks in J14, T1 and T20 folders. Keep all other blocks in inventory.'},{'title':'Convert units','detail':'Energy and exafs_edge_energy are supplied on a keV scale; multiply by 1000 for eV.'},{'title':'Derive view channels','detail':'fluoA = flatot/i0 and fluoB = flbtot/i0 when i0>0. mu01, mu12 and mu23 are retained as recorded. No smoothing or fitting.'}], 'metricDefinitions':[{'label':'Fluorescence A / I0','definition':'Recorded flatot divided by recorded i0; uncorrected ratio, not concentration or edge-step normalization.','formula':'flatot / i0'},{'label':'Energy relative to nominal edge','definition':'Energy in eV minus the scan header exafs_edge_energy converted to eV. The edge is nominal, not fitted.','formula':'energyEv - edgeEv'}]}
    obj={'surface':'dashboard','title':'X-ray absorption explorer','generatedAt':datetime.now(timezone.utc).isoformat(),'status':'reviewed','buildStatus':'creating','filters':[], 'queries':{'catalog':{'rows':cat,'source':source},'spectra':{'rows':spec,'source':source},'inventory':{'rows':inv,'source':source},'files':{'rows':files,'source':source}}}
    target=Path(args.output)
    if target.exists():
        previous=json.loads(target.read_text())
        for key in ['id','filters','legacyPresentationTitle']:
            if key in previous: obj[key]=previous[key]
    target.write_text(json.dumps(obj,separators=(',',':'),allow_nan=False))
    print(json.dumps({'files':len(files),'mainScans':len(cat),'mainPoints':len(spec),'allBlocks':len(inv),'allRows':sum(x['points'] for x in inv),'elements':sorted(set(x['element'] for x in cat)),'flags':[{k:r[k] for k in ['file','flags']} for r in cat if r['flags']!='No structural flags']},indent=2))
