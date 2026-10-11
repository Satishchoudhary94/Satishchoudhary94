#!/usr/bin/env python3
"""Generate animated SVGs for the GitHub profile README."""
import sys, html, pathlib

OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
CYAN, PURPLE, GREEN, BG = "#00D9FF", "#7B2CFF", "#22C55E", "#050816"


# ───────────────────────── HEADER ─────────────────────────
def header():
    import random
    random.seed(7)
    stars = "".join(
        f'<circle cx="{random.randint(0,1200)}" cy="{random.randint(0,340)}" r="{random.choice([0.8,1,1.3,1.6])}" fill="#fff">'
        f'<animate attributeName="opacity" values="0.1;0.9;0.1" dur="{random.uniform(2,5):.1f}s" begin="{random.uniform(0,4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(70)
    )
    # floating hexagons (k8s vibe) on the right
    def hexagon(cx, cy, r, color, dur, delay):
        import math
        pts = " ".join(f"{cx + r*math.cos(math.radians(60*i-30)):.1f},{cy + r*math.sin(math.radians(60*i-30)):.1f}" for i in range(6))
        return (f'<g opacity="0.85"><polygon points="{pts}" fill="none" stroke="{color}" stroke-width="2">'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -14;0 0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
                f'<animate attributeName="stroke-opacity" values="0.3;1;0.3" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></polygon></g>')
    hexes = (hexagon(1030, 110, 46, CYAN, 4, 0) + hexagon(1110, 190, 30, PURPLE, 5, 1) +
             hexagon(960, 215, 24, CYAN, 3.5, 0.5) + hexagon(1120, 70, 18, PURPLE, 4.5, 1.5) +
             hexagon(80, 250, 22, PURPLE, 4, 0.8) + hexagon(140, 70, 16, CYAN, 5, 0.2))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG}"/><stop offset="0.6" stop-color="#0b1238"/><stop offset="1" stop-color="#111C44"/>
  </linearGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="#FFFFFF"/><stop offset="1" stop-color="{PURPLE}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{CYAN}" stroke-opacity="0.07"/>
  </pattern>
  <clipPath id="round"><rect width="1200" height="340" rx="18"/></clipPath>
</defs>
<g clip-path="url(#round)">
  <rect width="1200" height="340" fill="url(#bg)"/>
  <rect x="-40" y="-40" width="1280" height="420" fill="url(#grid)">
    <animateTransform attributeName="transform" type="translate" values="0 0;40 40" dur="6s" repeatCount="indefinite"/>
  </rect>
  {stars}
  {hexes}
  <!-- scan line -->
  <rect x="0" y="0" width="1200" height="2" fill="{CYAN}" opacity="0.35">
    <animate attributeName="y" values="0;340" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>
<text x="600" y="78" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{CYAN}" opacity="0">
  &lt;/&gt; hello, world — i build and run cloud platforms
  <animate attributeName="opacity" from="0" to="0.9" begin="0.2s" dur="1s" fill="freeze"/>
</text>
<text x="600" y="170" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="76" letter-spacing="6"
      fill="url(#name)" stroke="{CYAN}" stroke-width="1.2" stroke-dasharray="900" stroke-dashoffset="900" fill-opacity="0" filter="url(#glow)">SATISH CHOUDHARY
  <animate attributeName="stroke-dashoffset" from="900" to="0" dur="2.2s" fill="freeze"/>
  <animate attributeName="fill-opacity" from="0" to="1" begin="1.6s" dur="1s" fill="freeze"/>
</text>
<text x="600" y="222" text-anchor="middle" font-family="{MONO}" font-size="22" fill="#E6EDF3" opacity="0">
  DevOps <tspan fill="{CYAN}">•</tspan> Cloud <tspan fill="{CYAN}">•</tspan> Platform Engineering <tspan fill="{CYAN}">•</tspan> SRE
  <animate attributeName="opacity" from="0" to="1" begin="2.2s" dur="1s" fill="freeze"/>
</text>
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" begin="2.8s" dur="0.8s" fill="freeze"/>
  <rect x="395" y="252" width="410" height="40" rx="20" fill="{GREEN}" fill-opacity="0.12" stroke="{GREEN}" stroke-opacity="0.6"/>
  <circle cx="422" cy="272" r="6" fill="{GREEN}">
    <animate attributeName="r" values="5;8;5" dur="1.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>
  </circle>
  <text x="440" y="278" font-family="{MONO}" font-size="15" fill="{GREEN}">Open to DevOps / Platform / SRE roles</text>
</g>
</svg>'''


# ───────────────────────── TERMINAL ─────────────────────────
def terminal():
    # (kind, segments) — kind: cmd (typed) | out (appears)
    P = f'<tspan fill="{GREEN}">satish@platform</tspan><tspan fill="#8B949E">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="#8B949E">$ </tspan>'
    lines = [
        ("cmd", "whoami"),
        ("out", [("Satish Choudhary", "#FFFFFF"), (" — DevOps / Platform Engineer, India", "#8B949E")]),
        ("cmd", "cat stack.yaml"),
        ("out", [("cloud:   ", PURPLE), ("[AWS, EKS, Lambda, VPC, IAM, CloudWatch]", "#E6EDF3")]),
        ("out", [("iac:     ", PURPLE), ("[Terraform, Helm]", "#E6EDF3")]),
        ("out", [("cicd:    ", PURPLE), ("[GitHub Actions, Jenkins, Argo CD]", "#E6EDF3")]),
        ("out", [("observe: ", PURPLE), ("[Datadog, Prometheus, Grafana]", "#E6EDF3")]),
        ("cmd", "kubectl get pods -n production"),
        ("out", [("NAME                     READY   STATUS    RESTARTS", "#8B949E")]),
        ("out", [("api-7d9f8c6b5-x2kqp      1/1     ", "#E6EDF3"), ("Running", GREEN), ("   0", "#E6EDF3")]),
        ("out", [("worker-5c8b7d4f9-m7tzl   1/1     ", "#E6EDF3"), ("Running", GREEN), ("   0", "#E6EDF3")]),
        ("cmd", "terraform apply -auto-approve"),
        ("out", [("Apply complete! ", GREEN), ("Resources: 42 added, 0 changed, 0 destroyed.", "#E6EDF3")]),
        ("cmd", "echo $MOTTO"),
        ("out", [("Automate the repeatable. Monitor the critical. Improve continuously.", CYAN)]),
    ]
    W, LH, X0, Y0, FS = 900, 24, 24, 82, 15
    CW = FS * 0.602  # monospace char width
    prompt_w = len("satish@platform:~$ ") * CW
    H = Y0 + LH * len(lines) + 40
    TOTAL = 22.0  # seconds per loop

    # schedule
    t, sched = 0.6, []
    for kind, content in lines:
        if kind == "cmd":
            dur = 0.07 * len(content) + 0.2
            sched.append((t, dur)); t += dur + 0.35
        else:
            sched.append((t, 0)); t += 0.12
    end = t + 0.2
    hold_end = TOTAL - 0.6

    def kt(x):  # time → keyTime
        return f"{min(max(x / TOTAL, 0), 1):.4f}"

    body, clips = [], []
    for i, ((kind, content), (start, dur)) in enumerate(zip(lines, sched)):
        y = Y0 + i * LH
        vis = (f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(start)};{kt(start+0.01)};{kt(hold_end)};{kt(hold_end+0.01)};1" '
               f'dur="{TOTAL}s" repeatCount="indefinite"/>')
        if kind == "cmd":
            tw = len(content) * CW + 4
            clips.append(
                f'<clipPath id="c{i}"><rect x="{X0+prompt_w-2:.1f}" y="{y-LH+6}" height="{LH}" width="0">'
                f'<animate attributeName="width" values="0;0;{tw:.1f};{tw:.1f};0;0" keyTimes="0;{kt(start)};{kt(start+dur)};{kt(hold_end)};{kt(hold_end+0.01)};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
                f'</rect></clipPath>')
            body.append(f'<g opacity="0">{vis}<text x="{X0}" y="{y}">{P}</text>'
                        f'<text x="{X0+prompt_w:.1f}" y="{y}" fill="#FFFFFF" clip-path="url(#c{i})">{html.escape(content)}</text></g>')
        else:
            spans = "".join(f'<tspan fill="{c}">{html.escape(s)}</tspan>' for s, c in content)
            body.append(f'<g opacity="0">{vis}<text x="{X0}" y="{y}" xml:space="preserve">{spans}</text></g>')

    # blinking cursor at final prompt
    cy = Y0 + len(lines) * LH
    cursor = (f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{kt(end)};{kt(end+0.01)};{kt(hold_end)};{kt(hold_end+0.01)};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
              f'<text x="{X0}" y="{cy}">{P}</text>'
              f'<rect x="{X0+prompt_w:.1f}" y="{cy-14}" width="9" height="18" fill="{CYAN}">'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="tb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  {''.join(clips)}
</defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0D1117" stroke="url(#tb)" stroke-width="2"/>
<rect x="1" y="1" width="{W-2}" height="42" rx="14" fill="#161B22"/>
<rect x="1" y="30" width="{W-2}" height="13" fill="#161B22"/>
<circle cx="26" cy="22" r="7" fill="#FF5F56"/><circle cx="50" cy="22" r="7" fill="#FFBD2E"/><circle cx="74" cy="22" r="7" fill="#27C93F"/>
<text x="{W/2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8B949E">satish@platform: ~ — zsh</text>
<g font-family="{MONO}" font-size="{FS}" xml:space="preserve">
{chr(10).join(body)}
{cursor}
</g>
</svg>'''


# ───────────────────────── PIPELINE ─────────────────────────
def pipeline():
    stages = [("git push", "Code", "#F05032"), ("Actions", "Build + Test", "#2088FF"),
              ("Trivy", "Scan", "#1904DA"), ("ECR", "Registry", "#FF9900"),
              ("Argo CD", "GitOps Sync", "#EF7B4D"), ("EKS", "Deploy", "#326CE5"),
              ("Grafana", "Observe", "#F46800")]
    W, H, NW, NH, Y = 1200, 230, 140, 84, 80
    gap = (W - 40 - NW * len(stages)) / (len(stages) - 1)
    xs = [20 + i * (NW + gap) for i in range(len(stages))]
    cyc = 7.0
    nodes, links = [], []
    for i, (name, sub, col) in enumerate(stages):
        x = xs[i]
        b = i * cyc / len(stages)
        nodes.append(f'''<g>
  <rect x="{x:.1f}" y="{Y}" width="{NW}" height="{NH}" rx="14" fill="#0D1117" stroke="{col}" stroke-width="2">
    <animate attributeName="stroke-width" values="2;4;2" dur="{cyc}s" begin="{b:.2f}s" keyTimes="0;0.08;0.2" calcMode="linear" repeatCount="indefinite"/>
  </rect>
  <rect x="{x:.1f}" y="{Y}" width="{NW}" height="{NH}" rx="14" fill="{col}" opacity="0.08">
    <animate attributeName="opacity" values="0.08;0.35;0.08;0.08" keyTimes="0;0.06;0.18;1" dur="{cyc}s" begin="{b:.2f}s" repeatCount="indefinite"/>
  </rect>
  <circle cx="{x+NW-14:.1f}" cy="{Y+14}" r="4" fill="{GREEN}">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="1.6s" begin="{i*0.2:.1f}s" repeatCount="indefinite"/>
  </circle>
  <text x="{x+NW/2:.1f}" y="{Y+38}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="18" fill="#FFFFFF">{name}</text>
  <text x="{x+NW/2:.1f}" y="{Y+62}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#8B949E">{sub}</text>
</g>''')
        if i < len(stages) - 1:
            x1, x2, ym = x + NW, xs[i + 1], Y + NH / 2
            links.append(f'''<line x1="{x1:.1f}" y1="{ym}" x2="{x2:.1f}" y2="{ym}" stroke="#30363D" stroke-width="2" stroke-dasharray="4 4">
  <animate attributeName="stroke-dashoffset" from="8" to="0" dur="0.5s" repeatCount="indefinite"/></line>
<circle r="4" fill="{CYAN}"><animateMotion path="M{x1:.1f},{ym} L{x2:.1f},{ym}" dur="{cyc/len(stages):.2f}s" begin="{b:.2f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" dur="{cyc/len(stages):.2f}s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{BG}" stroke="#30363D"/>
<text x="24" y="42" font-family="{MONO}" font-size="15" fill="{CYAN}">$ ./ship.sh --env production</text>
<text x="{W-24}" y="42" text-anchor="end" font-family="{MONO}" font-size="13" fill="{GREEN}">● all checks passing</text>
{''.join(links)}
{''.join(nodes)}
<text x="{W/2}" y="{H-22}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8B949E">commit → container → cluster, fully automated with GitOps</text>
</svg>'''


for name, fn in [("header.svg", header), ("terminal.svg", terminal), ("pipeline.svg", pipeline)]:
    (OUT / name).write_text(fn())
    print("wrote", OUT / name)
