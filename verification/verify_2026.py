"""Independent 2026 headline recomputation using Python stdlib only.
Input: public Stack Overflow 2026 CSV. No project imports.
"""
import argparse,csv,hashlib,json,sys
from pathlib import Path
from collections import Counter,defaultdict
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--csv',type=Path,required=True)
parser.add_argument('--tables',type=Path,default=Path(__file__).resolve().parents[1]/'outputs/sentiment_2026')
parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'raw-verification-results.json')
args=parser.parse_args()
p=args.csv
expected='ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c'
sha=hashlib.sha256(p.read_bytes()).hexdigest()
assert sha==expected,(sha,'checksum mismatch')
tools={'AI coding assistants or coding agents','General-purpose AI chat tools','AI agents or automated workflows','Internal AI tools built by my company'}
nonuser='I don’t use AI tools'
stances={'Very favorable','Somewhat favorable','Neutral','Somewhat unfavorable','Very unfavorable','Not sure'}
frequencies={'Daily','Weekly','Monthly or Infrequent'}
freqcols=[f'AIFreq_{i}' for i in range(1,5)]
seen_ids=set();counts=Counter();by_stance=defaultdict(Counter);policy=defaultdict(Counter);trust=Counter();stance_all=Counter();trust_selfidentified=Counter();stance_selfidentified=Counter();frequency_unselected=Counter()
def valid(s):return s not in ('','NA','N/A')
with p.open(newline='',encoding='utf-8-sig') as f:
 for r in csv.DictReader(f):
  counts['rows']+=1
  if r['ResponseId'] in seen_ids:counts['duplicate_response_ids']+=1
  seen_ids.add(r['ResponseId'])
  sel=set(r['AISelect'].split(';')) if valid(r['AISelect']) else set()
  has_tool=bool(sel & tools);says_no=nonuser in sel
  if valid(r['AISelect']):counts['answered_AISelect']+=1
  if has_tool and says_no:counts['contradictory_selection']+=1
  if says_no and not has_tool:counts['nonusers']+=1
  current=has_tool and not says_no
  if current:
   counts['current_users']+=1
   if valid(r['AITrust']):trust_selfidentified[r['AITrust']]+=1
   if r['AISentiment'] in stances:stance_selfidentified[r['AISentiment']]+=1
  else:continue
  fs=[r[c] for c in freqcols if r[c] in frequencies]
  if not fs:counts['current_users_no_valid_frequency']+=1;continue
  counts['current_users_with_frequency']+=1
  if valid(r['AITrust']):trust[r['AITrust']]+=1
  if r['AISentiment'] in stances:stance_all[r['AISentiment']]+=1
  daily='Daily' in fs
  ordered_tools=['AI coding assistants or coding agents','General-purpose AI chat tools','AI agents or automated workflows','Internal AI tools built by my company']
  selected_daily=any(r[c]=='Daily' and t in sel for c,t in zip(freqcols,ordered_tools))
  if daily!=selected_daily:counts['daily_classification_diff_using_selected_tools_only']+=1
  if daily:counts['daily_among_current_with_frequency']+=1
  if r['AISentiment'] not in stances or not valid(r['AITrust']):continue
  counts['primary_current_users']+=1
  counts['primary_daily']+=int(daily)
  s=r['AISentiment'];by_stance[s]['n']+=1;by_stance[s]['daily_n']+=int(daily)
  if valid(r['AIUse']):
   for group in (s,'All current users'):
    policy[(group,r['AIUse'])]['n']+=1;policy[(group,r['AIUse'])]['daily_n']+=int(daily)

def rate(d):return {**dict(d),'daily_pct':100*d['daily_n']/d['n']}
report={'source':str(p),'sha256':sha,'counts':dict(counts),'stance_primary':{s:rate(d) for s,d in by_stance.items()},'trust_selfidentified_users_including_missing_frequency_denominator':sum(trust_selfidentified.values()),'stance_selfidentified_users_including_missing_frequency_denominator':sum(stance_selfidentified.values()),'current_user_distribution_definition':'Selected >=1 recognized tool, did not also select non-use, and answered at least1 recognized frequency item.','trust_current_user_denominator':sum(trust.values()),'trust_current_user_distribution':{s:{'n':n,'pct':100*n/sum(trust.values())}for s,n in trust.items()},'stance_current_user_denominator':sum(stance_all.values()),'stance_current_user_distribution':{s:{'n':n,'pct':100*n/sum(stance_all.values())}for s,n in stance_all.items()},'policy':[{'stance':s,'policy':pol,**rate(d)}for(s,pol),d in policy.items() if s in ('Very unfavorable','All current users')]}
output=args.output;output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
# Compare every primary stance row and every policy cell with supplied tables.
package=args.tables
label={'Very unfavorable':'Very unfavorable','Unfavorable':'Somewhat unfavorable','Unsure':'Not sure','Indifferent':'Neutral','Favorable':'Somewhat favorable','Very favorable':'Very favorable'}
checks=[]
with (package/'current_user_daily_use_by_stance.csv').open() as f:
 for row in csv.DictReader(f):
  computed=by_stance[label[row['favorable_stance']]]
  assert computed['n']==int(row['n'])
  assert computed['daily_n']==int(row['daily_n'])
  assert abs(computed['daily_n']/computed['n']-float(row['daily_rate']))<1e-12
  checks.append('stance '+row['favorable_stance'])
polmap={'Optional, individual choice':'AI use is mostly optional and left up to individuals','Encouraged, varies by team':'Some teams actively encourage AI use, but practices vary across the organization','Approved tools and guidance':'My organization provides approved AI tools and guidance for how to use them','Expected for some work':'My organization expects some employees to use AI tools for certain types of work','Measured in performance':'My organization measures or evaluates AI use as part of employee or team performance','Org does not use AI':'My organization does not currently use AI tools or agents for work','Not sure':'Not sure'}
with (package/'current_user_daily_by_stance_and_org_policy.csv').open() as f:
 for row in csv.DictReader(f):
  lab=row['favorable_stance'];s=label.get(lab,lab);computed=policy[(s,polmap[row['org_ai_policy']])]
  assert computed['n']==int(row['n'])
  assert abs(computed['daily_n']/computed['n']-float(row['daily_rate']))<1e-12
  checks.append('policy '+lab+' / '+row['org_ai_policy'])
report['source_table_cells_verified']=len(checks)
report['source_table_check_list']=checks
output.write_text(json.dumps(report,indent=2)+'\n')
print('ALL SOURCE TABLE CHECKS PASSED',len(checks))

with (package/'four_year_context.csv').open() as f:
 row=next(r for r in csv.DictReader(f) if r['year']=='2026')
assert int(row['current_users'])==counts['current_users_with_frequency']
assert int(row['answered_ai_use_item'])==counts['current_users_with_frequency']+counts['nonusers']
assert int(row['trust_current_user_denominator'])==sum(trust.values())
assert int(row['stance_current_user_denominator'])==sum(stance_all.values())
trust_cols={'I do not trust it for most work tasks':'trust2026_Not for most tasks','I trust it for low-risk work tasks only':'trust2026_Low-risk tasks only','I trust it when I can easily verify the output':'trust2026_When I can verify','I trust it for many tasks, but not important work decisions':'trust2026_Many tasks, not key decisions','I trust it for many tasks, including important work decisions':'trust2026_Incl. key decisions','Not sure / I do not use AI tools':'trust2026_Not sure'}
for label,col in trust_cols.items():
 assert abs(float(row[col])-100*trust[label]/sum(trust.values()))<1e-12
report['trust_distribution_cells_verified']=6
report['four_year_context_2026_denominators_verified']=True
output.write_text(json.dumps(report,indent=2)+'\n')
print('ALL TRUST CELLS AND2026CONTEXT DENOMINATORS VERIFIED')
