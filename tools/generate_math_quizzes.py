#!/usr/bin/env python3
"""Generate 8 more 6e math quizzes (3-10)"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent / "Mathematiques/6e"
BASE_DIR.mkdir(parents=True, exist_ok=True)

def create_html_quiz(filename, title, subtitle, quiz_id, questions, answers):
    """Create a quiz HTML file"""
    options_html = ""
    for i, q in enumerate(questions, 1):
        q_options = ""
        for opt in q['options']:
            q_options += f'        <div class="option"><input type="radio" name="q{i}" value="{opt[0]}" id="q{i}{opt[0]}"/><label for="q{i}{opt[0]}">{opt[1]}</label></div>\n'

        options_html += f'''    <div class="question-block">
      <div class="question-num">Question {i}</div>
      <div class="question-text">{q['text']}</div>
      <div class="options">
{q_options}      </div>
    </div>

'''

    answers_dict = ",".join([f"q{i}:'{answers[i-1]}'" for i in range(1, len(answers)+1)])

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{
      --navy:#e8dcc8; --navy-dark:#d4c9b3; --navy-card:#f0e8d8;
      --navy-border:#ddd2bf; --navy-hover:#ede5d6;
      --gold:#c9a84c; --gold-light:#e2c46e; --gold-dim:#a68842;
      --green:#2ecc8a; --red:#e05555;
      --text:#3d3220; --text-bright:#2b2416; --text-muted:#8b7d69; --text-soft:#9d8f7a;
      --mono:'IBM Plex Mono',monospace;
      --sans:'IBM Plex Sans',sans-serif;
      --serif:'Playfair Display',Georgia,serif;
    }}
    html{{scroll-behavior:smooth;}}
    body{{font-family:var(--sans);background:var(--navy);color:var(--text);min-height:100vh;}}
    nav{{display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:56px;border-bottom:1px solid var(--navy-border);background:var(--navy-dark);position:sticky;top:0;z-index:100;}}
    .nav-logo{{font-family:var(--serif);font-size:20px;font-weight:700;color:var(--gold);text-decoration:none;letter-spacing:.06em;}}
    .nav-right{{display:flex;align-items:center;gap:24px;}}
    .nav-link{{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-soft);text-decoration:none;transition:color .2s;}}
    .nav-link:hover{{color:var(--gold);}}
    .container{{max-width:900px;margin:0 auto;padding:40px 20px;}}
    .header{{text-align:center;margin-bottom:48px;padding-bottom:24px;border-bottom:2px solid var(--navy-border);}}
    .header h1{{font-family:var(--serif);font-size:36px;font-weight:900;color:var(--text-bright);margin-bottom:8px;}}
    .header p{{font-family:var(--mono);font-size:12px;color:var(--text-muted);letter-spacing:.06em;text-transform:uppercase;}}
    .question-block{{margin-bottom:40px;padding:24px;background:var(--navy-card);border:1px solid var(--navy-border);border-radius:4px;}}
    .question-num{{font-family:var(--mono);font-size:11px;color:var(--gold);text-transform:uppercase;margin-bottom:8px;letter-spacing:.1em;}}
    .question-text{{font-family:var(--serif);font-size:18px;font-weight:700;color:var(--text-bright);margin-bottom:16px;line-height:1.4;}}
    .options{{display:flex;flex-direction:column;gap:10px;}}
    .option{{display:flex;align-items:center;padding:12px 16px;border:1px solid var(--navy-border);border-radius:3px;cursor:pointer;transition:all .2s;background:#fff;position:relative;}}
    .option:hover{{background:var(--navy-hover);border-color:var(--gold);}}
    .option input[type="radio"]{{margin-right:12px;cursor:pointer;}}
    .option label{{cursor:pointer;flex:1;font-size:15px;}}
    .option input[type="radio"]:checked ~ label{{font-weight:600;color:var(--gold);}}
    .submit-btn{{display:block;width:100%;padding:16px;margin-top:48px;background:var(--gold);color:var(--text-bright);border:none;border-radius:3px;font-family:var(--sans);font-size:14px;font-weight:600;cursor:pointer;transition:all .2s;letter-spacing:.08em;text-transform:uppercase;}}
    .submit-btn:hover{{background:var(--gold-dim);transform:translateY(-2px);}}
    .result{{margin-top:48px;padding:24px;background:var(--navy-card);border:2px solid var(--navy-border);border-radius:4px;text-align:center;}}
    .result h2{{font-family:var(--serif);font-size:24px;color:var(--text-bright);margin-bottom:12px;}}
    .score-display{{font-family:var(--mono);font-size:48px;font-weight:bold;color:var(--gold);margin:16px 0;}}
    .result p{{font-size:14px;color:var(--text-muted);margin-bottom:8px;}}
    .download-btn{{display:inline-block;margin-top:16px;padding:10px 20px;background:var(--gold);color:var(--text-bright);text-decoration:none;border-radius:3px;font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase;}}
    @media(max-width:600px){{.container{{padding:20px 16px;}} .header h1{{font-size:28px;}} .question-text{{font-size:16px;}} nav{{padding:0 20px;}}}}
  </style>
</head>
<body>

<nav>
  <a class="nav-logo" href="../../index.html">SELMA</a>
  <div class="nav-right">
    <a class="nav-link" href="../../index.html">Accueil</a>
    <a class="nav-link active" href="#">Quiz Maths</a>
  </div>
</nav>

<div class="container">
  <div class="header">
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>

  <form id="quiz-form">
{options_html}    <button type="submit" class="submit-btn">Soumettre le quiz</button>
  </form>

  <div id="result" style="display:none;">
    <div class="result">
      <h2>Quiz Terminé!</h2>
      <div class="score-display" id="score-num">0/15</div>
      <p id="score-percent">0%</p>
      <a href="javascript:location.reload()" class="download-btn">Recommencer</a>
    </div>
  </div>
</div>

<script>
  const QUIZ_ID = "{quiz_id}";
  const CORRECT_ANSWERS = {{{answers_dict}}};

  document.getElementById('quiz-form').addEventListener('submit', (e) => {{
    e.preventDefault();
    let score = 0;
    for (let i = 1; i <= 15; i++) {{
      const answer = document.querySelector(`input[name="q${{i}}"]:checked`);
      if (answer && answer.value === CORRECT_ANSWERS[`q${{i}}`]) score++;
    }}

    const percent = Math.round((score / 15) * 100);
    document.getElementById('score-num').textContent = `${{score}}/15`;
    document.getElementById('score-percent').textContent = `${{percent}}%`;
    document.getElementById('quiz-form').style.display = 'none';
    document.getElementById('result').style.display = 'block';

    const hist = JSON.parse(localStorage.getItem(`scores_${{QUIZ_ID}}`) || '[]');
    hist.unshift({{score, total: 15, date: new Date().toLocaleDateString('fr-FR')}});
    localStorage.setItem(`scores_${{QUIZ_ID}}`, JSON.stringify(hist));

    const txt = `Quiz: {title}\\nScore: ${{score}}/15 (${{percent}}%)\\nDate: ${{new Date().toLocaleDateString('fr-FR')}}\\n`;
    const blob = new Blob([txt], {{type: 'text/plain'}});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `score_{filename.replace('.html', '')}_${{Date.now()}}.txt`;
    a.click();
  }});
</script>
</body>
</html>
'''

    filepath = BASE_DIR / filename
    filepath.write_text(html, encoding='utf-8')
    print(f"✓ {filename}")

# QUIZ 3: Fractions & Mixed Numbers
q3_questions = [
    {'text': 'La fraction 5/3 est égale au nombre mixte :', 'options': [('a', '1 + 2/3'), ('b', '2 + 1/3'), ('c', '1 + 1/3'), ('d', '2 + 2/3')]},
    {'text': 'Convertis 7/4 en nombre mixte :', 'options': [('a', '2 + 3/4'), ('b', '1 + 3/4'), ('c', '1 + 2/4'), ('d', '3 + 1/4')]},
    {'text': '2 + 1/5 est égal à quelle fraction ?', 'options': [('a', '3/5'), ('b', '11/5'), ('c', '2/5'), ('d', '7/5')]},
    {'text': 'Le nombre 8/3 se lit :', 'options': [('a', '3 entiers et 2 tiers'), ('b', '2 entiers et 2 tiers'), ('c', '8 tiers'), ('d', '2 entiers et 1 tiers')]},
    {'text': 'Écris 1 + 3/7 sous forme de fraction :', 'options': [('a', '4/7'), ('b', '10/7'), ('c', '3/7'), ('d', '11/7')]},
    {'text': 'La fraction 13/4 est égale à :', 'options': [('a', '3 + 1/4'), ('b', '2 + 5/4'), ('c', '4 + 1/4'), ('d', '2 + 1/4')]},
    {'text': '3 + 2/5 est égal à :', 'options': [('a', '5/5'), ('b', '17/5'), ('c', '6/5'), ('d', '15/5')]},
    {'text': 'Convertis 11/6 en nombre mixte :', 'options': [('a', '1 + 5/6'), ('b', '2 + 5/6'), ('c', '1 + 4/6'), ('d', '2 + 1/6')]},
    {'text': '5 + 1/3 est égal à quelle fraction ?', 'options': [('a', '6/3'), ('b', '16/3'), ('c', '5/3'), ('d', '8/3')]},
    {'text': 'Le nombre mixte 2 + 3/8 est égal à :', 'options': [('a', '5/8'), ('b', '19/8'), ('c', '11/8'), ('d', '10/8')]},
    {'text': 'Écris 4 + 1/2 sous forme de fraction :', 'options': [('a', '5/2'), ('b', '9/2'), ('c', '8/2'), ('d', '4/2')]},
    {'text': 'La fraction 9/2 se lit :', 'options': [('a', '2 entiers et 1 demi'), ('b', '4 entiers et 1 demi'), ('c', '9 demis'), ('d', '3 entiers et 1 demi')]},
    {'text': '6 + 1/4 est égal à :', 'options': [('a', '7/4'), ('b', '25/4'), ('c', '24/4'), ('d', '13/4')]},
    {'text': 'Convertis 14/5 en nombre mixte :', 'options': [('a', '2 + 4/5'), ('b', '3 + 4/5'), ('c', '2 + 3/5'), ('d', '3 + 1/5')]},
    {'text': 'Le nombre mixte 3 + 2/7 est égal à :', 'options': [('a', '5/7'), ('b', '21/7'), ('c', '23/7'), ('d', '9/7')]},
]
q3_answers = ['a', 'b', 'b', 'b', 'b', 'a', 'b', 'a', 'b', 'b', 'b', 'c', 'b', 'a', 'c']
create_html_quiz('quiz_fractions_mixed_numbers.html', 'Fractions — Nombres Mixtes', 'Conversion entre fractions et nombres mixtes', 'Maths6e_Fractions_MixedNumbers', q3_questions, q3_answers)

# QUIZ 4: Comparing & Ordering Fractions
q4_questions = [
    {'text': 'Quelle fraction est la plus grande : 3/8 ou 5/8 ?', 'options': [('a', '3/8'), ('b', '5/8'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': 'Laquelle de ces fractions est équivalente à 2/3 ?', 'options': [('a', '4/6'), ('b', '3/4'), ('c', '5/9'), ('d', '2/4')]},
    {'text': 'Ordonne ces fractions du plus petit au plus grand : 1/4, 1/8, 1/2', 'options': [('a', '1/2, 1/4, 1/8'), ('b', '1/8, 1/4, 1/2'), ('c', '1/4, 1/8, 1/2'), ('d', '1/2, 1/8, 1/4')]},
    {'text': 'Quelle fraction est la plus petite : 7/10 ou 4/10 ?', 'options': [('a', '7/10'), ('b', '4/10'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': '3/5 est égale à quelle fraction ?', 'options': [('a', '6/10'), ('b', '5/10'), ('c', '3/10'), ('d', '9/15')]},
    {'text': 'Laquelle de ces fractions est plus grande : 2/5 ou 1/3 ?', 'options': [('a', '2/5'), ('b', '1/3'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': '2/4 est égale à :', 'options': [('a', '1/2'), ('b', '2/8'), ('c', '4/8'), ('d', '3/6')]},
    {'text': 'Ordonne du plus petit au plus grand : 2/3, 3/4, 5/12', 'options': [('a', '2/3, 3/4, 5/12'), ('b', '5/12, 2/3, 3/4'), ('c', '3/4, 2/3, 5/12'), ('d', '5/12, 3/4, 2/3')]},
    {'text': 'Quelle fraction est plus grande : 7/8 ou 6/7 ?', 'options': [('a', '7/8'), ('b', '6/7'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': '5/6 est égale à :', 'options': [('a', '10/12'), ('b', '5/12'), ('c', '6/12'), ('d', '4/6')]},
    {'text': 'Laquelle de ces fractions est équivalente à 3/4 ?', 'options': [('a', '6/8'), ('b', '4/5'), ('c', '9/16'), ('d', '3/5')]},
    {'text': 'Compare 4/9 et 4/11. Quelle est la plus grande ?', 'options': [('a', '4/9'), ('b', '4/11'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': 'Ordonne du plus petit au plus grand : 1/6, 1/3, 1/2', 'options': [('a', '1/2, 1/3, 1/6'), ('b', '1/6, 1/3, 1/2'), ('c', '1/3, 1/2, 1/6'), ('d', '1/3, 1/6, 1/2')]},
    {'text': '7/10 est égale à :', 'options': [('a', '14/20'), ('b', '7/20'), ('c', '10/20'), ('d', '3/10')]},
    {'text': 'Quelle fraction est la plus grande : 5/7 ou 3/4 ?', 'options': [('a', '5/7'), ('b', '3/4'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
]
q4_answers = ['b', 'a', 'b', 'b', 'a', 'a', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'b']
create_html_quiz('quiz_comparing_fractions.html', 'Fractions — Comparaison & Ordre', 'Comparer et ordonner les fractions', 'Maths6e_Comparing_Fractions', q4_questions, q4_answers)

# QUIZ 5: Adding & Subtracting Fractions
q5_questions = [
    {'text': 'Calcule 1/4 + 2/4 :', 'options': [('a', '3/8'), ('b', '2/8'), ('c', '3/4'), ('d', '2/4')]},
    {'text': 'Quel est le résultat de 3/8 + 2/8 ?', 'options': [('a', '5/8'), ('b', '5/16'), ('c', '1/8'), ('d', '6/8')]},
    {'text': 'Calcule 7/10 - 3/10 :', 'options': [('a', '2/10'), ('b', '4/10'), ('c', '10/10'), ('d', '4/20')]},
    {'text': 'Quel est le résultat de 5/6 - 1/6 ?', 'options': [('a', '6/6'), ('b', '5/12'), ('c', '4/6'), ('d', '1/6')]},
    {'text': 'Additionne 1/3 + 1/3 :', 'options': [('a', '2/3'), ('b', '2/6'), ('c', '1/6'), ('d', '1/3')]},
    {'text': 'Calcule 9/12 - 3/12 :', 'options': [('a', '6/12'), ('b', '6/24'), ('c', '3/12'), ('d', '12/12')]},
    {'text': 'Quel est 2/5 + 2/5 ?', 'options': [('a', '4/5'), ('b', '4/10'), ('c', '2/10'), ('d', '1/5')]},
    {'text': 'Calcule 8/10 - 5/10 :', 'options': [('a', '3/20'), ('b', '3/10'), ('c', '13/10'), ('d', '2/10')]},
    {'text': 'Additionne 3/4 + 1/4 :', 'options': [('a', '4/8'), ('b', '3/8'), ('c', '4/4'), ('d', '2/4')]},
    {'text': 'Quel est 5/9 - 2/9 ?', 'options': [('a', '3/18'), ('b', '7/9'), ('c', '3/9'), ('d', '2/9')]},
    {'text': 'Calcule 1/2 + 1/4 (dénominateurs liés) :', 'options': [('a', '2/4'), ('b', '3/4'), ('c', '2/6'), ('d', '1/4')]},
    {'text': 'Quel est 3/4 - 1/2 ?', 'options': [('a', '1/4'), ('b', '1/2'), ('c', '2/4'), ('d', '3/8')]},
    {'text': 'Additionne 1/3 + 1/6 :', 'options': [('a', '2/6'), ('b', '1/2'), ('c', '2/9'), ('d', '1/9')]},
    {'text': 'Calcule 5/6 - 1/3 :', 'options': [('a', '4/6'), ('b', '3/6'), ('c', '2/6'), ('d', '4/3')]},
    {'text': 'Quel est 2/3 + 1/6 ?', 'options': [('a', '3/9'), ('b', '5/6'), ('c', '1/3'), ('d', '3/6')]},
]
q5_answers = ['c', 'a', 'b', 'c', 'a', 'a', 'a', 'b', 'c', 'c', 'b', 'a', 'b', 'c', 'b']
create_html_quiz('quiz_adding_subtracting_fractions.html', 'Fractions — Addition & Soustraction', 'Additionner et soustraire des fractions', 'Maths6e_Adding_Fractions', q5_questions, q5_answers)

# QUIZ 6: Multiplying by Fractions
q6_questions = [
    {'text': 'Calcule 1/2 de 20 :', 'options': [('a', '10'), ('b', '20'), ('c', '5'), ('d', '40')]},
    {'text': 'Quel est 2/5 de 50 ?', 'options': [('a', '20'), ('b', '10'), ('c', '30'), ('d', '25')]},
    {'text': 'Calcule 3/4 de 24 :', 'options': [('a', '6'), ('b', '18'), ('c', '12'), ('d', '8')]},
    {'text': 'Quel est 1/3 de 30 ?', 'options': [('a', '10'), ('b', '15'), ('c', '20'), ('d', '30')]},
    {'text': 'Calcule 3/5 de 40 :', 'options': [('a', '24'), ('b', '20'), ('c', '8'), ('d', '32')]},
    {'text': 'Quel est 2/3 de 18 ?', 'options': [('a', '6'), ('b', '12'), ('c', '9'), ('d', '18')]},
    {'text': 'Calcule 1/4 de 100 :', 'options': [('a', '25'), ('b', '50'), ('c', '75'), ('d', '20')]},
    {'text': 'Quel est 5/6 de 36 ?', 'options': [('a', '6'), ('b', '18'), ('c', '30'), ('d', '24')]},
    {'text': 'Calcule 2/4 de 60 :', 'options': [('a', '20'), ('b', '30'), ('c', '40'), ('d', '10')]},
    {'text': 'Quel est 3/10 de 50 ?', 'options': [('a', '10'), ('b', '15'), ('c', '20'), ('d', '30')]},
    {'text': 'Calcule 4/5 de 25 :', 'options': [('a', '20'), ('b', '15'), ('c', '10'), ('d', '5')]},
    {'text': 'Quel est 1/6 de 42 ?', 'options': [('a', '7'), ('b', '14'), ('c', '21'), ('d', '28')]},
    {'text': 'Calcule 3/8 de 80 :', 'options': [('a', '30'), ('b', '40'), ('c', '20'), ('d', '50')]},
    {'text': 'Quel est 2/7 de 35 ?', 'options': [('a', '5'), ('b', '10'), ('c', '15'), ('d', '20')]},
    {'text': 'Calcule 7/10 de 60 :', 'options': [('a', '30'), ('b', '35'), ('c', '40'), ('d', '42')]},
]
q6_answers = ['a', 'a', 'b', 'a', 'a', 'b', 'a', 'c', 'b', 'b', 'a', 'a', 'a', 'b', 'd']
create_html_quiz('quiz_multiplying_fractions.html', 'Fractions — Multiplier par une Fraction', 'Calculer une fraction d\'un nombre', 'Maths6e_Multiplying_Fractions', q6_questions, q6_answers)

# QUIZ 7: Proportionality Basics
q7_questions = [
    {'text': 'Deux grandeurs sont proportionnelles si :', 'options': [('a', 'elles augmentent ensemble'), ('b', 'en multipliant l\'une par un nombre, l\'autre est multipliée par le même nombre'), ('c', 'elles sont toujours égales'), ('d', 'l\'une est plus grande que l\'autre')]},
    {'text': 'Si 3 livres coûtent 15€, combien coûte 1 livre ?', 'options': [('a', '3€'), ('b', '5€'), ('c', '10€'), ('d', '15€')]},
    {'text': 'Une voiture parcourt 120 km en 2 heures. Quelle distance en 4 heures ?', 'options': [('a', '60 km'), ('b', '240 km'), ('c', '180 km'), ('d', '360 km')]},
    {'text': 'Laquelle de ces situations est proportionnelle ?', 'options': [('a', 'L\'âge et la taille d\'une personne'), ('b', 'Le nombre d\'articles et le prix total'), ('c', 'L\'année et le nombre d\'habitants'), ('d', 'L\'heure et la température')]},
    {'text': 'Si 4 kg de pommes coûtent 12€, quel prix pour 2 kg ?', 'options': [('a', '3€'), ('b', '6€'), ('c', '8€'), ('d', '12€')]},
    {'text': 'Sur un tableau : si x=2 et y=10, et si y=25, alors x=', 'options': [('a', '4'), ('b', '5'), ('c', '10'), ('d', '20')]},
    {'text': 'Une recette : 200g de farine pour 4 personnes. Pour 8 personnes ?', 'options': [('a', '100g'), ('b', '200g'), ('c', '400g'), ('d', '600g')]},
    {'text': 'Si 5 stylos coûtent 10€, combien coûtent 8 stylos ?', 'options': [('a', '12€'), ('b', '14€'), ('c', '16€'), ('d', '18€')]},
    {'text': 'Sur une carte : 1 cm = 10 km. 5 cm représente ?', 'options': [('a', '5 km'), ('b', '15 km'), ('c', '30 km'), ('d', '50 km')]},
    {'text': 'Un train roule à 100 km/h. En 3 heures, il parcourt ?', 'options': [('a', '100 km'), ('b', '150 km'), ('c', '200 km'), ('d', '300 km')]},
    {'text': 'Si 6 oeufs coûtent 3€, quel prix pour 12 oeufs ?', 'options': [('a', '3€'), ('b', '6€'), ('c', '9€'), ('d', '12€')]},
    {'text': 'Une imprimante : 60 pages par minute. En 5 minutes ?', 'options': [('a', '100 pages'), ('b', '200 pages'), ('c', '300 pages'), ('d', '400 pages')]},
    {'text': 'La proportionnalité est un modèle qui :', 'options': [('a', 'ne fonctionne jamais'), ('b', 'fonctionne toujours'), ('c', 'fonctionne pour certaines situations'), ('d', 'est compliqué à utiliser')]},
    {'text': 'Si 2 mètres de tissu coûtent 20€, 5 mètres coûtent ?', 'options': [('a', '25€'), ('b', '40€'), ('c', '50€'), ('d', '100€')]},
    {'text': 'Procedure du retour à l\'unité : d\'abord :', 'options': [('a', 'multiplier par le coefficient'), ('b', 'trouver le prix d\'une unité'), ('c', 'additionner'), ('d', 'diviser par 2')]},
]
q7_answers = ['b', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'd', 'd', 'b', 'c', 'c', 'c', 'b']
create_html_quiz('quiz_proportionality_basics.html', 'Proportionnalité — Bases', 'Reconnaître et utiliser la proportionnalité', 'Maths6e_Proportionality_Basics', q7_questions, q7_answers)

# QUIZ 8: Proportionality Problems
q8_questions = [
    {'text': 'Une recette pour 4 personnes : 400g de farine, 2 oeufs, 200ml de lait. Pour 2 personnes ?', 'options': [('a', '200g farine, 1 oeuf, 100ml lait'), ('b', '800g farine, 4 oeufs, 400ml lait'), ('c', '300g farine, 1,5 oeuf, 150ml lait'), ('d', '600g farine, 3 oeufs, 300ml lait')]},
    {'text': 'Léa achète 3 kg de cerises à 9€. Quel prix pour 5 kg ?', 'options': [('a', '12€'), ('b', '15€'), ('c', '18€'), ('d', '21€')]},
    {'text': 'Une voiture consomme 7 litres pour 100 km. Consommation en 250 km ?', 'options': [('a', '14 litres'), ('b', '17,5 litres'), ('c', '21 litres'), ('d', '35 litres')]},
    {'text': 'Tableau : 2→6, 5→?, 10→30. Quelle valeur pour 5 ?', 'options': [('a', '12'), ('b', '15'), ('c', '18'), ('d', '24')]},
    {'text': 'Proportionnalité additive : 3€ + 3€ + 3€ = 9€. Si 7 objets, coût ?', 'options': [('a', '18€'), ('b', '21€'), ('c', '24€'), ('d', '27€')]},
    {'text': 'Léon gagne 180€ en 5 jours. Combien en 8 jours ?', 'options': [('a', '216€'), ('b', '260€'), ('c', '288€'), ('d', '360€')]},
    {'text': 'Une recette : 300g de sucre pour 6 gâteaux. Pour 9 gâteaux ?', 'options': [('a', '400g'), ('b', '450g'), ('c', '500g'), ('d', '550g')]},
    {'text': 'Proportion : 4 stylos→12€, 7 stylos→?', 'options': [('a', '18€'), ('b', '19€'), ('c', '20€'), ('d', '21€')]},
    {'text': 'Un cycliste fait 15 km en 1 heure. Distance en 3,5 heures ?', 'options': [('a', '45 km'), ('b', '50 km'), ('c', '52,5 km'), ('d', '60 km')]},
    {'text': 'Coefficient de proportionnalité : 2→8. Coefficient=?', 'options': [('a', '2'), ('b', '3'), ('c', '4'), ('d', '5')]},
    {'text': 'Utilise la linéarité : si 10 coûte 25€, combien 6+4=10 ?', 'options': [('a', '12€ + 10€'), ('b', '15€ + 10€'), ('c', '20€ + 5€'), ('d', '18€ + 7€')]},
    {'text': 'La méthode du retour à l\'unité : si 4→20, une unité→?', 'options': [('a', '4'), ('b', '5'), ('c', '10'), ('d', '20')]},
    {'text': 'Problème : 3 livres pèsent 900g. Poids de 5 livres ?', 'options': [('a', '1200g'), ('b', '1350g'), ('c', '1500g'), ('d', '1650g')]},
    {'text': 'Tableau proportionnel : 3→12, 7→?', 'options': [('a', '28'), ('b', '30'), ('c', '32'), ('d', '35')]},
    {'text': 'Linéarité multiplicative : si 5€ pour 2 articles, 25€ pour ?', 'options': [('a', '8 articles'), ('b', '10 articles'), ('c', '12 articles'), ('d', '15 articles')]},
]
q8_answers = ['a', 'b', 'b', 'b', 'b', 'c', 'b', 'd', 'c', 'c', 'c', 'b', 'c', 'a', 'b']
create_html_quiz('quiz_proportionality_problems.html', 'Proportionnalité — Problèmes', 'Résoudre des problèmes de proportionnalité', 'Maths6e_Proportionality_Problems', q8_questions, q8_answers)

# QUIZ 9: Percentages
q9_questions = [
    {'text': '25% est égal à la fraction :', 'options': [('a', '1/2'), ('b', '1/4'), ('c', '1/3'), ('d', '3/4')]},
    {'text': 'Quel pourcentage représente 1/2 ?', 'options': [('a', '25%'), ('b', '33%'), ('c', '50%'), ('d', '75%')]},
    {'text': 'Calcule 10% de 200 :', 'options': [('a', '10'), ('b', '20'), ('c', '30'), ('d', '40')]},
    {'text': 'Quel pourcentage représente 1/4 ?', 'options': [('a', '20%'), ('b', '25%'), ('c', '33%'), ('d', '50%')]},
    {'text': 'Calcule 50% de 80 :', 'options': [('a', '20'), ('b', '30'), ('c', '40'), ('d', '50')]},
    {'text': '20% est égal à :', 'options': [('a', '1/3'), ('b', '1/5'), ('c', '2/3'), ('d', '1/2')]},
    {'text': 'Quel pourcentage est 75% égal à ?', 'options': [('a', '1/4'), ('b', '1/2'), ('c', '3/4'), ('d', '1/3')]},
    {'text': 'Calcule 25% de 40 :', 'options': [('a', '10'), ('b', '15'), ('c', '20'), ('d', '30')]},
    {'text': 'Une classe de 20 élèves : 10 font du foot. Pourcentage ?', 'options': [('a', '25%'), ('b', '50%'), ('c', '75%'), ('d', '100%')]},
    {'text': 'Calcule 33% de 300 :', 'options': [('a', '50'), ('b', '75'), ('c', '100'), ('d', '150')]},
    {'text': 'Un aliment contient 40% de glucides en 100g. Combien dans 50g ?', 'options': [('a', '10g'), ('b', '20g'), ('c', '40g'), ('d', '50g')]},
    {'text': 'Sur 100 élèves, 30 font du tennis. Quel pourcentage ?', 'options': [('a', '10%'), ('b', '20%'), ('c', '30%'), ('d', '40%')]},
    {'text': 'Calcule 5% de 200 :', 'options': [('a', '5'), ('b', '10'), ('c', '15'), ('d', '20')]},
    {'text': 'Un objet coûte 100€. Réduction de 20%. Nouveau prix ?', 'options': [('a', '70€'), ('b', '75€'), ('c', '80€'), ('d', '90€')]},
    {'text': 'Quel pourcentage de 200 égale 50 ?', 'options': [('a', '20%'), ('b', '25%'), ('c', '30%'), ('d', '50%')]},
]
q9_answers = ['b', 'c', 'b', 'b', 'c', 'b', 'c', 'a', 'b', 'c', 'b', 'c', 'b', 'c', 'b']
create_html_quiz('quiz_percentages.html', 'Pourcentages', 'Calculer et utiliser les pourcentages', 'Maths6e_Percentages', q9_questions, q9_answers)

# QUIZ 10: Challenge Quiz (Mixed)
q10_questions = [
    {'text': 'Convertis la fraction 7/3 en nombre mixte :', 'options': [('a', '1 + 4/3'), ('b', '2 + 1/3'), ('c', '3 + 1/3'), ('d', '2 + 2/3')]},
    {'text': '3/4 + 1/8 = ?', 'options': [('a', '4/12'), ('b', '7/8'), ('c', '2/8'), ('d', '5/8')]},
    {'text': 'Calcule 40% de 250 :', 'options': [('a', '80'), ('b', '100'), ('c', '120'), ('d', '150')]},
    {'text': 'Une recette pour 6 personnes nécessite 180g de beurre. Pour 9 personnes ?', 'options': [('a', '200g'), ('b', '240g'), ('c', '270g'), ('d', '300g')]},
    {'text': '2/3 de 90 = ?', 'options': [('a', '45'), ('b', '50'), ('c', '60'), ('d', '75')]},
    {'text': 'Quelle fraction est équivalente à 6/9 ?', 'options': [('a', '2/3'), ('b', '1/2'), ('c', '3/4'), ('d', '4/6')]},
    {'text': 'Un magasin réduit tous les prix de 30%. Un article à 50€ coûte maintenant ?', 'options': [('a', '30€'), ('b', '35€'), ('c', '40€'), ('d', '45€')]},
    {'text': 'Quelle est la plus grande : 5/8 ou 7/12 ?', 'options': [('a', '5/8'), ('b', '7/12'), ('c', 'Elles sont égales'), ('d', 'Impossible à dire')]},
    {'text': 'Une voiture parcourt 150 km en 2 heures. En 5 heures ?', 'options': [('a', '300 km'), ('b', '375 km'), ('c', '450 km'), ('d', '500 km')]},
    {'text': 'Calcule 3/5 × 1/2 = ?', 'options': [('a', '3/7'), ('b', '3/10'), ('c', '4/10'), ('d', '5/10')]},
    {'text': '50% + 25% = ?', 'options': [('a', '0,5'), ('b', '0,75'), ('c', '0,25'), ('d', '1')]},
    {'text': 'Si 4 kg coûtent 12€, 7 kg coûtent ?', 'options': [('a', '18€'), ('b', '20€'), ('c', '21€'), ('d', '24€')]},
    {'text': 'Quelle est 1/6 de 72 ?', 'options': [('a', '10'), ('b', '12'), ('c', '14'), ('d', '18')]},
    {'text': 'Une recette : pour 8 crêpes, 200ml de lait. Pour 4 crêpes ?', 'options': [('a', '100ml'), ('b', '150ml'), ('c', '200ml'), ('d', '250ml')]},
    {'text': 'Ordonne ces nombres du plus petit au plus grand : 0,5 ; 3/5 ; 40%', 'options': [('a', '0,5, 3/5, 40%'), ('b', '40%, 0,5, 3/5'), ('c', '40%, 3/5, 0,5'), ('d', '3/5, 0,5, 40%')]},
]
q10_answers = ['b', 'b', 'b', 'c', 'c', 'a', 'b', 'a', 'b', 'b', 'b', 'c', 'b', 'a', 'b']
create_html_quiz('quiz_challenge_mixed.html', 'Quiz Défi — Mélangé', 'Proportionnalité, fractions, pourcentages', 'Maths6e_Challenge_Mixed', q10_questions, q10_answers)

print("\n✓ All 8 quizzes created successfully!")
