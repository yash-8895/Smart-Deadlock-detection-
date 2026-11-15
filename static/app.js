const defaults = {
 max:[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]],
 allocation:[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]],
 available:[3,3,2]
};
function makeGrid(targetId, matrix, prefix, editable=true) {
 const target=document.getElementById(targetId); target.innerHTML='';
 const table=document.createElement('table');
 const head=document.createElement('tr'); head.innerHTML='<th></th>'+matrix[0].map((_,j)=>`<th>R${j+1}</th>`).join(''); table.appendChild(head);
 matrix.forEach((row,i)=>{const tr=document.createElement('tr');tr.innerHTML=`<th>P${i+1}</th>`+row.map((v,j)=>`<td>${editable?`<input type="number" min="0" step="1" id="${prefix}-${i}-${j}" value="${v}" aria-label="${prefix} process ${i+1} resource ${j+1}">`: `<span>${v}</span>`}</td>`).join('');table.appendChild(tr);});
 target.appendChild(table);
}
function renderAvailable(values){document.getElementById('available').innerHTML=values.map((v,j)=>`<label>R${j+1}<input type="number" min="0" step="1" id="av-${j}" value="${v}"></label>`).join('');}
function resetDemo(){makeGrid('max-grid',defaults.max,'max');makeGrid('alloc-grid',defaults.allocation,'alloc');renderAvailable(defaults.available);document.getElementById('error').textContent='';document.getElementById('result').className='empty';document.getElementById('result').textContent='Run the algorithm to see the result.';document.getElementById('need-grid').innerHTML='';}
function readMatrix(prefix){return defaults.max.map((row,i)=>row.map((_,j)=>{const el=document.getElementById(`${prefix}-${i}-${j}`);const n=Number(el.value);if(el.value.trim()===''||!Number.isInteger(n)||n<0)throw new Error('Enter non-negative whole numbers in every resource field.');return n;}));}
function readData(){const max=readMatrix('max'), allocation=readMatrix('alloc'), available=defaults.available.map((_,j)=>{const el=document.getElementById(`av-${j}`),n=Number(el.value);if(el.value.trim()===''||!Number.isInteger(n)||n<0)throw new Error('Available resources must be non-negative whole numbers.');return n;});return {max,allocation,available};}
function renderNeed(need){makeGrid('need-grid',need,'need',false);}
async function analyze(){const err=document.getElementById('error'),result=document.getElementById('result');err.textContent='';result.className='empty';result.textContent='Analyzing…';try{const data=readData();const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const payload=await response.json();if(!response.ok)throw new Error(payload.error||'Request failed');renderNeed(payload.need);result.className=payload.safe?'result-card safe':'result-card unsafe';result.innerHTML=`<div class="result-icon">${payload.safe?'✓':'!'}</div><div><h3>${payload.safe?'SAFE STATE':'UNSAFE STATE'}</h3><p>${payload.message}</p><p><strong>Safe sequence:</strong> ${payload.safe?payload.sequence_labels.join(' → '):'No complete safe sequence found'}</p></div>`;await loadLogs();}catch(e){result.className='empty';result.textContent='Unable to analyze.';err.textContent=e.message;}}
async function loadLogs(){const el=document.getElementById('logs');try{const r=await fetch('/api/logs');const rows=await r.json();el.innerHTML=rows.length?rows.map(x=>`<article class="log"><div><strong>#${x.id} · ${x.safe_state?'Safe':'Unsafe'}</strong><small>${x.created_at}</small></div><p>${x.message}</p><small>Sequence: ${JSON.parse(x.safe_sequence).join(' → ')||'None'}</small></article>`).join(''):'No analyses stored yet.';}catch(e){el.textContent='Could not load database logs.';}}
async function checkHealth(){try{const r=await fetch('/api/health');const d=await r.json();document.getElementById('status').textContent='● Backend connected';document.getElementById('status').classList.add('online');}catch(e){document.getElementById('status').textContent='● Backend unavailable';}}
document.getElementById('analyze').addEventListener('click',analyze);document.getElementById('reset').addEventListener('click',resetDemo);document.getElementById('load-logs').addEventListener('click',loadLogs);
resetDemo();checkHealth();loadLogs();