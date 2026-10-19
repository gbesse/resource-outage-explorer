const texts = {
  fr: {
    eyebrow: 'RESSOURCES PARTAGÉES · EXERCICE SYNTHÉTIQUE',
    title: 'Plus de capacité.\nToujours le même point faible.',
    lede: 'Un renfort peut disparaître dans la même panne que les moyens existants. Explorez toutes les pertes du catalogue, voyez ce qui manque et comparez trois investissements déclarés.',
    stress: 'Définir l’épreuve',
    outageBudget: 'Budget de pannes simultanées',
    investmentBudget: 'Budget de renfort · points',
    analyze: 'Explorer les combinaisons →',
    units:
      'Les unités sont des créneaux de capacité d’exercice interchangeables, sans conversion physique implicite.',
    exercise: 'Outil d’exercice. Aucune ressource réelle vérifiée, réservée ou envoyée.',
    worst: 'Le pire cas du catalogue',
    certified: 'FLUX / COUPE VÉRIFIÉS',
    shortfall: 'unités non couvertes',
    scenarios: 'scénarios examinés',
    cut: 'capacité de la coupe',
    certificate: 'Pourquoi on ne peut pas allouer davantage',
    upgrades: 'Trois renforts, trois expositions',
    download: 'Exporter les preuves JSON',
    limits:
      'Modèle biparti à capacités entières, scénarios et expositions fournis. Pas de simulation opérationnelle de crise, délais, compétences implicites ou disponibilités réelles. L’exhaustivité est bornée au catalogue et au budget ; aucune probabilité de panne n’est estimée.',
    delivered: 'alloué',
    need: 'besoin',
    proof:
      'Allocation faisable = capacité de la coupe ; le flux maximal est démontré dans ce modèle.',
    best: 'meilleur renfort unique du catalogue',
    none: 'Aucun renfort éligible ou améliorant le pire cas.',
    busy: 'Calcul des allocations et coupes…',
    done: 'Toutes les combinaisons autorisées sont vérifiées.',
    error: 'Entrée non valide ou serveur indisponible.',
    events: 'Pannes',
    baseline: 'aucune',
    larger: 'Augmenter le moyen principal',
    shared: 'Renfort dans le même dépôt',
    independent: 'Renfort indépendant',
    worstShortfall: 'manque maximal',
    cost: 'coût déclaré',
    noProbability: 'Fréquence des cas ≠ probabilité de panne',
  },
  en: {
    eyebrow: 'SHARED RESOURCES · SYNTHETIC EXERCISE',
    title: 'More capacity.\nThe same single weakness.',
    lede: 'Backup capacity may disappear in the same outage as existing resources. Explore the failure catalog, see what remains unmet, and compare three declared investments.',
    stress: 'Define the stress test',
    outageBudget: 'Simultaneous outage budget',
    investmentBudget: 'Reinforcement budget · points',
    analyze: 'Explore combinations →',
    units:
      'Units are interchangeable exercise capacity slots, without implicit physical conversions.',
    exercise: 'Exercise tool. No real resource verified, reserved or dispatched.',
    worst: 'The catalog’s worst case',
    certified: 'FLOW / CUT CHECKED',
    shortfall: 'uncovered units',
    scenarios: 'scenarios checked',
    cut: 'cut capacity',
    certificate: 'Why no more units can be allocated',
    upgrades: 'Three reinforcements, three exposures',
    download: 'Export JSON evidence',
    limits:
      'Integer bipartite capacity model with supplied scenarios and exposures. No operational crisis simulation, delays, implicit skills or real availability. Exhaustiveness is limited to the catalog and budget; no outage probability is estimated.',
    delivered: 'allocated',
    need: 'need',
    proof: 'Feasible allocation = cut capacity; maximum flow is proven within this model.',
    best: 'best single catalog reinforcement',
    none: 'No eligible reinforcement improves the worst case.',
    busy: 'Computing allocations and cuts…',
    done: 'Every permitted combination was checked.',
    error: 'Invalid input or server unavailable.',
    events: 'Outages',
    baseline: 'none',
    larger: 'Larger main device',
    shared: 'Backup in the same depot',
    independent: 'Independent backup',
    worstShortfall: 'worst shortfall',
    cost: 'declared cost',
    noProbability: 'Scenario frequency ≠ outage probability',
  },
  es: {
    eyebrow: 'RECURSOS COMPARTIDOS · EJERCICIO SINTÉTICO',
    title: 'Más capacidad.\nEl mismo punto débil.',
    lede: 'Un refuerzo puede desaparecer con los recursos existentes en el mismo fallo. Explora el catálogo de pérdidas, observa necesidades pendientes y compara tres inversiones declaradas.',
    stress: 'Definir la prueba',
    outageBudget: 'Presupuesto de fallos simultáneos',
    investmentBudget: 'Presupuesto de refuerzo · puntos',
    analyze: 'Explorar combinaciones →',
    units:
      'Unidades intercambiables de capacidad de ejercicio, sin conversiones físicas implícitas.',
    exercise: 'Herramienta de ejercicio. Sin recursos reales verificados, reservados ni enviados.',
    worst: 'El peor caso del catálogo',
    certified: 'FLUJO / CORTE VERIFICADOS',
    shortfall: 'unidades sin cubrir',
    scenarios: 'escenarios examinados',
    cut: 'capacidad del corte',
    certificate: 'Por qué no se puede asignar más',
    upgrades: 'Tres refuerzos, tres exposiciones',
    download: 'Exportar pruebas JSON',
    limits:
      'Modelo bipartito de capacidad entera con escenarios y exposiciones proporcionados. Sin simulación operativa de crisis, demoras, capacidades implícitas ni disponibilidad real. Exhaustividad limitada al catálogo y presupuesto; no estima probabilidades de fallo.',
    delivered: 'asignado',
    need: 'necesidad',
    proof: 'Asignación factible = capacidad del corte; flujo máximo demostrado dentro del modelo.',
    best: 'mejor refuerzo único del catálogo',
    none: 'Ningún refuerzo elegible mejora el peor caso.',
    busy: 'Calculando asignaciones y cortes…',
    done: 'Todas las combinaciones permitidas verificadas.',
    error: 'Entrada no válida o servidor no disponible.',
    events: 'Fallos',
    baseline: 'ninguno',
    larger: 'Aumentar recurso principal',
    shared: 'Refuerzo en el mismo depósito',
    independent: 'Refuerzo independiente',
    worstShortfall: 'máxima carencia',
    cost: 'coste declarado',
    noProbability: 'Frecuencia de casos ≠ probabilidad de fallo',
  },
};
const lang = new URLSearchParams(location.search).get('lang') || 'en',
  m = texts[lang] || texts.en;
document.documentElement.lang = texts[lang] ? lang : 'en';
document.querySelectorAll('[data-i18n]').forEach((x) => (x.textContent = m[x.dataset.i18n]));
document.querySelectorAll('nav a').forEach((a) => {
  if (a.textContent.toLowerCase() === document.documentElement.lang)
    a.setAttribute('aria-current', 'page');
});
const $ = (id) => document.getElementById(id),
  el = (tag, text, cls) => {
    const x = document.createElement(tag);
    if (text !== undefined) x.textContent = text;
    if (cls) x.className = cls;
    return x;
  };
let initial, report;
const names = {
  'larger-main-device': 'larger',
  'backup-in-same-depot': 'shared',
  'independent-backup': 'independent',
};
function svg(tag, attrs, text) {
  const x = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) x.setAttribute(k, v);
  if (text !== undefined) x.textContent = text;
  $('network').append(x);
  return x;
}
function render(data) {
  report = data;
  const worst = data.baseline.worst,
    flow = worst.flow;
  $('shortfall').textContent = worst.shortfall;
  $('scenarios').textContent = data.baseline.scenarios_checked;
  $('cut').textContent = flow.cut_capacity;
  $('events').textContent = m.events + ': ' + (worst.events.join(' + ') || m.baseline);
  $('digest').textContent = flow.case_sha256;
  $('network').replaceChildren();
  const rs = data.source_case.resources,
    ds = data.source_case.demands;
  for (const a of flow.allocations) {
    const y1 = 55 + rs.findIndex((r) => r.id === a.resource) * 80,
      y2 = 55 + ds.findIndex((d) => d.id === a.demand) * 80;
    svg('line', { x1: 140, y1, x2: 500, y2, stroke: '#7eadd1', 'stroke-width': 2 + a.units });
    svg('text', { x: 320, y: (y1 + y2) / 2 - 7, fill: '#c7dce9', 'font-size': 12 }, a.units);
  }
  for (const [r, i] of rs.map((x, i) => [x, i])) {
    const disabled = flow.disabled.includes(r.id),
      y = 55 + i * 80;
    svg('rect', {
      x: 8,
      y: y - 25,
      width: 132,
      height: 50,
      rx: 6,
      fill: disabled ? '#4c2927' : '#152e3c',
      stroke: disabled ? '#9f6254' : '#49748c',
    });
    svg('text', { x: 18, y: y - 3, fill: '#e0e8ed', 'font-size': 10 }, r.id);
    svg(
      'text',
      { x: 18, y: y + 14, fill: disabled ? '#d6a79c' : '#8bb5cf', 'font-size': 10 },
      disabled ? '×' : String(r.capacity),
    );
  }
  for (const [d, i] of ds.map((x, i) => [x, i])) {
    const y = 55 + i * 80;
    svg('rect', {
      x: 500,
      y: y - 25,
      width: 142,
      height: 50,
      rx: 6,
      fill: '#17272f',
      stroke: '#506b7b',
    });
    svg('text', { x: 512, y: y - 3, fill: '#dde9ed', 'font-size': 11 }, d.id);
    svg(
      'text',
      { x: 512, y: y + 14, fill: '#a6c5d8', 'font-size': 10 },
      `${d.need - flow.unmet[d.id]} / ${d.need} ${m.delivered}`,
    );
  }
  $('certificate').replaceChildren();
  $('certificate').append(
    el('p', `${flow.delivered_units} = ${flow.cut_capacity} · ${m.proof}`, 'proof'),
  );
  for (const edge of flow.cut_edges)
    $('certificate').append(el('code', `${edge.from} → ${edge.to}: ${edge.capacity}`, 'cut-edge'));
  $('upgrades').replaceChildren();
  for (const u of data.upgrade_comparisons) {
    const box = el(
      'div',
      undefined,
      'upgrade' + (u.upgrade === data.best_single_catalog_upgrade ? ' best' : ''),
    );
    box.append(
      el('strong', m[names[u.upgrade]] || u.upgrade),
      el('span', `${m.cost}: ${u.cost} · ${m.worstShortfall}: ${u.worst_shortfall}`),
    );
    if (u.upgrade === data.best_single_catalog_upgrade) box.append(el('small', m.best));
    $('upgrades').append(box);
  }
  if (!data.best_single_catalog_upgrade) $('upgrades').append(el('p', m.none, 'hint'));
  $('status').textContent = m.done;
}
async function run() {
  $('analyze').disabled = true;
  $('status').textContent = m.busy;
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case: initial,
        outage_budget: Number($('outage-budget').value),
        investment_budget: Number($('investment-budget').value),
      }),
    });
    if (!response.ok) throw Error();
    render(await response.json());
  } catch {
    $('status').textContent = m.error;
  } finally {
    $('analyze').disabled = false;
  }
}
$('analyze').addEventListener('click', run);
$('download').addEventListener('click', () => {
  if (!report) return;
  const url = URL.createObjectURL(
      new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }),
    ),
    a = el('a');
  a.href = url;
  a.download = 'resource-outage-evidence.json';
  a.click();
  URL.revokeObjectURL(url);
});
try {
  const response = await fetch('/api/example');
  if (!response.ok) throw Error();
  initial = await response.json();
  await run();
} catch {
  $('status').textContent = m.error;
}
