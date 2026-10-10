"""Render verified MC experiment results to a PDF with vector checkpoint charts."""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from mc_run_lifecycle import verify_completed
from mc_standard_report import build_report


def chart_data(payload):
    """Serializable chart source values; never infer missing observations as zero."""
    resolved = payload['resolved_configuration']
    metrics = list(payload.get('metric_registry', {}))
    if not metrics:
        metrics = list(next(iter(next(iter(payload['summary'].values())).values()))['metrics'])
    charts = []
    for metric in metrics:
        for wave in resolved['checkpoints']:
            values = []
            for scenario in resolved['scenarios']:
                entry = payload['summary'][scenario['name']][str(wave)]
                stats = entry['metrics'].get(metric)
                values.append({'scenario': scenario['name'], 'observed': entry['observed'],
                               'mean': stats['mean'] if stats else None,
                               'ci95_halfwidth': stats['ci95_halfwidth'] if stats else None})
            charts.append({'metric': metric, 'wave': wave,
                           'unit': payload.get('metric_registry', {}).get(metric, {}).get('unit', 'count'),
                           'values': values})
    return charts


def make_chart(chart):
    usable = [v for v in chart['values'] if v['mean'] is not None]
    width, height = 490, max(110, 34 * len(chart['values']) + 55)
    drawing = Drawing(width, height)
    if not usable:
        drawing.add(String(10, height / 2, 'No observations', fontSize=10))
        return drawing
    maximum = max((v['mean'] + (v['ci95_halfwidth'] or 0)) for v in usable)
    minimum = min(0, min(v['mean'] - (v['ci95_halfwidth'] or 0) for v in usable))
    span = maximum - minimum or 1
    left, right = 170, 465
    x = lambda value: left + (value - minimum) / span * (right - left)
    drawing.add(Line(x(0), 18, x(0), height - 18, strokeColor=colors.grey)) if minimum <= 0 <= maximum else None
    for i, value in enumerate(chart['values']):
        y = height - 40 - i * 34
        label = value['scenario']
        drawing.add(String(3, y + 3, label[:26] + ('…' if len(label) > 26 else ''), fontSize=8))
        if value['mean'] is None:
            drawing.add(String(left, y + 3, 'No observations', fontSize=8))
            continue
        start, end = sorted((x(0), x(value['mean'])))
        drawing.add(Rect(start, y, max(1, end - start), 12, fillColor=colors.HexColor('#567b9c'), strokeColor=None))
        ci = value['ci95_halfwidth'] or 0
        drawing.add(Line(x(value['mean'] - ci), y + 6, x(value['mean'] + ci), y + 6, strokeColor=colors.black))
        drawing.add(String(right - 2, y + 15, 'n=%s' % value['observed'], fontSize=7, textAnchor='end'))
    drawing.add(String(left, 5, 'Mean (95%% CI whisker); %s' % chart['unit'], fontSize=8))
    return drawing


def pdf_report(payload, manifest, output):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SmallReport', parent=styles['BodyText'], fontSize=8, leading=11, spaceAfter=5))
    styles.add(ParagraphStyle(name='ChartTitle', parent=styles['Heading3'], fontSize=10, spaceBefore=12))
    story = []
    markdown = build_report(payload, manifest)
    story.append(Paragraph('Tower Dominion — Experiment Report', styles['Title']))
    story.append(Paragraph('Verified simulation results and visual comparisons', styles['Italic']))
    story.append(Spacer(1, 12))
    for line in markdown.splitlines():
        if line.startswith('# '):
            continue
        if line.startswith('## '):
            story.append(Paragraph(escape(line[3:]), styles['Heading2']))
        elif line.startswith('### '):
            story.append(Paragraph(escape(line[4:]), styles['Heading3']))
        elif line.startswith('|'):
            # Preserve the exact numerical content of the Markdown report in a compact monospaced line.
            story.append(Paragraph(escape(line).replace(' ', '&nbsp;'), styles['SmallReport']))
        elif line.strip():
            story.append(Paragraph(escape(line).replace('**', '').replace('`', ''), styles['SmallReport']))
        else:
            story.append(Spacer(1, 4))
    story.append(PageBreak())
    story.append(Paragraph('Checkpoint charts', styles['Heading1']))
    for chart in chart_data(payload):
        story.append(KeepTogether([Paragraph('%s — Wave %s' % (escape(chart['metric']), chart['wave']), styles['ChartTitle']), make_chart(chart), Spacer(1, 10)]))
    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=38, leftMargin=38, topMargin=42, bottomMargin=42,
                            title='Tower Dominion Experiment Report')
    doc.build(story)


def render(directory):
    directory = Path(directory)
    manifest = verify_completed(directory)
    payload = json.loads((directory / 'results.json').read_text())
    pdf = directory / 'report.pdf'
    chart_file = directory / 'charts.json'
    if pdf.exists() or chart_file.exists():
        raise FileExistsError('report.pdf or charts.json already exists')
    # Chart data is the canonical source for every plotted mean and denominator.
    pdf_report(payload, manifest, pdf)
    with chart_file.open('x') as file:
        json.dump({'charts': chart_data(payload)}, file, indent=2)
    return pdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    print(render(parser.parse_args().output))
