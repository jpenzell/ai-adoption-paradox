from pathlib import Path
import argparse, csv, json, math

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--expected',type=Path,required=True)
parser.add_argument('--actual',type=Path,required=True)
parser.add_argument('--output',type=Path,default=ROOT/'model-comparison-report.json')
args=parser.parse_args()
EXPECTED=args.expected
ACTUAL=args.actual
ABS_TOL=1e-9
REL_TOL=1e-7

def num(value):
    if isinstance(value,bool):return None
    if isinstance(value,(int,float)):return float(value)
    if isinstance(value,str):
        try:return float(value)
        except ValueError:return None
    return None

def compare(left,right,path,stats):
    if isinstance(left,dict) and isinstance(right,dict):
        if set(left)!=set(right):stats['issues'].append({'path':path,'kind':'keys','expected':sorted(left),'actual':sorted(right)})
        for k in left.keys() & right.keys():compare(left[k],right[k],path+'/'+str(k),stats)
        return
    if isinstance(left,list) and isinstance(right,list):
        if len(left)!=len(right):stats['issues'].append({'path':path,'kind':'length','expected':len(left),'actual':len(right)})
        for i,(a,b) in enumerate(zip(left,right)):compare(a,b,path+f'/{i}',stats)
        return
    a,b=num(left),num(right)
    if a is not None and b is not None:
        stats['numeric_cells']+=1
        if math.isnan(a) and math.isnan(b):return
        if a==b:return
        delta=abs(a-b)
        stats['max_abs_delta']=max(stats['max_abs_delta'],delta)
        if not math.isclose(a,b,rel_tol=REL_TOL,abs_tol=ABS_TOL):stats['issues'].append({'path':path,'kind':'number','expected':a,'actual':b,'abs_delta':delta})
    elif left!=right:
        stats['issues'].append({'path':path,'kind':'value','expected':left,'actual':right})

results=[]
for source in sorted(EXPECTED.iterdir()):
    if source.suffix not in ['.csv','.json']:continue
    actual=ACTUAL/source.name
    if not actual.exists():
        results.append({'file':source.name,'status':'skipped_historical_context' if source.name=='four_year_context.csv' else 'missing','issues':[]})
        continue
    if source.suffix=='.csv':
        with source.open() as f:reader=csv.DictReader(f);left=list(reader);headers_left=reader.fieldnames
        with actual.open() as f:reader=csv.DictReader(f);right=list(reader);headers_right=reader.fieldnames
    else:left=json.loads(source.read_text());right=json.loads(actual.read_text());headers_left=headers_right=None
    stats={'file':source.name,'status':'pass','numeric_cells':0,'max_abs_delta':0.0,'issues':[]}
    if headers_left!=headers_right:stats['issues'].append({'kind':'headers','expected':headers_left,'actual':headers_right})
    compare(left,right,'',stats)
    if stats['issues']:stats['status']='difference'
    results.append(stats)
summary={'absolute_tolerance':ABS_TOL,'relative_tolerance':REL_TOL,'files':results,
 'pass_count':sum(x['status']=='pass' for x in results),
 'difference_count':sum(x['status']=='difference' for x in results),
 'skipped_count':sum(x['status']=='skipped_historical_context' for x in results),
 'missing_count':sum(x['status']=='missing' for x in results)}
args.output.write_text(json.dumps(summary,indent=2,allow_nan=True))
print(json.dumps({k:v for k,v in summary.items() if k!='files'},indent=2))
for entry in results:
 print(entry['status'],entry['file'],'max_delta',entry.get('max_abs_delta',0),'issues',len(entry['issues']))
 for issue in entry['issues'][:4]:print(' ',issue)
